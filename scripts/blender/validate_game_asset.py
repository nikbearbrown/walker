"""
validate_game_asset.py — static checks on the EXPORT collection of a .blend.
Never saves. Exit 0 = no errors. Prints one JSON report an agent can parse.

  blender --background asset.blend --python-exit-code 1 \
    --python scripts/blender/validate_game_asset.py -- --engine godot
"""
import argparse
import json
import re
import sys

import bpy

ENGINES = ["godot", "bevy", "babylon", "unreal", "unity"]
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--engine", choices=ENGINES, required=True)
ap.add_argument("--collection", default="EXPORT")
ap.add_argument("--max-tris", type=int, default=0, help="per-object budget; 0 disables")
ap.add_argument("--max-influences", type=int, default=4)
args = ap.parse_args(argv)

errors, warnings = [], []
EPS = 1e-4
AUTO_SUFFIX = re.compile(r"\.\d{3}$")
GODOT_HINTS = "col|convcol|colonly|convcolonly|noimp|rigid|navmesh|occ|occonly|vehicle|wheel"
NAME_RULE = re.compile(
    rf"^[A-Za-z0-9_]+(-({GODOT_HINTS}))?$" if args.engine == "godot" else r"^[A-Za-z0-9_]+$"
)
UE_COLLISION = re.compile(r"^(UCX|UBX|USP|UCP)_(.+)$")
LOD = re.compile(r"^(.+)_LOD(\d+)$")
SIDE = re.compile(r"^(.*?)([._\- ])([LlRr])$")


def is_collision(name):
    if args.engine == "unreal":
        return bool(UE_COLLISION.match(name))
    if args.engine == "godot":
        return bool(re.search(r"-(colonly|convcolonly)$", name))
    return False


def flip_side(name):
    m = SIDE.match(name)
    if not m:
        return None
    swap = {"L": "R", "R": "L", "l": "r", "r": "l"}[m.group(3)]
    return f"{m.group(1)}{m.group(2)}{swap}"


def deform_parent(bone):
    p = bone.parent
    while p is not None and not p.use_deform:
        p = p.parent
    return p


coll = bpy.data.collections.get(args.collection)
objs = list(coll.all_objects) if coll else []
if coll is None:
    errors.append(f"No '{args.collection}' collection: nothing is marked for export.")
elif not objs:
    errors.append(f"'{args.collection}' is empty.")
names = {o.name for o in objs}
render_names = {n for n in names if not is_collision(n)}
depsgraph = bpy.context.evaluated_depsgraph_get()
tri_total = 0
used_materials = set()

for o in objs:
    for label, n in (("object", o.name), ("data", getattr(o.data, "name", ""))):
        if n and AUTO_SUFFIX.search(n):
            errors.append(f"{label} '{n}': Blender duplicate suffix (.###) in exported data.")
    if not NAME_RULE.match(o.name):
        errors.append(f"'{o.name}': characters outside the {args.engine} naming rule.")
    if o.type == "MESH" and o.data.name != o.name:
        warnings.append(f"'{o.name}': mesh data is named '{o.data.name}'; keep them identical.")
    if o.type not in {"MESH", "ARMATURE"}:
        continue

    _, rot, scale = o.matrix_basis.decompose()
    if any(s < 0 for s in scale):
        errors.append(f"'{o.name}': negative scale (flips normals, breaks skinning).")
    elif any(abs(s - 1.0) > EPS for s in scale):
        errors.append(f"'{o.name}': unapplied scale {tuple(round(s, 4) for s in scale)}.")
    if rot.angle > EPS:
        warnings.append(f"'{o.name}': unapplied rotation.")

    if o.type == "MESH":
        me = o.data
        col = is_collision(o.name)
        arm = o.find_armature()

        ngons = sum(1 for p in me.polygons if len(p.vertices) > 4)
        if ngons:
            warnings.append(f"'{o.name}': {ngons} n-gons; triangulate deliberately before baking.")
        if not col:
            if len(me.materials) == 0 or any(m is None for m in me.materials):
                errors.append(f"'{o.name}': missing or empty material slot.")
            for m in me.materials:
                if m is not None:
                    used_materials.add(m)
            if not me.uv_layers:
                warnings.append(f"'{o.name}': no UV map.")

        if args.engine == "unreal":
            if col:
                rest = UE_COLLISION.match(o.name).group(2)
                if not any(rest == n or re.fullmatch(re.escape(n) + r"_\d+", rest) for n in render_names):
                    errors.append(f"Collision '{o.name}' matches no render mesh name.")
            else:
                want = "SK_" if arm else "SM_"
                if not o.name.startswith(want):
                    kind = "skinned" if arm else "static"
                    errors.append(f"'{o.name}': {kind} mesh must start with {want}.")

        if not col:
            ev = o.evaluated_get(depsgraph)
            tmp = ev.to_mesh()
            tris = sum(len(p.vertices) - 2 for p in tmp.polygons)
            ev.to_mesh_clear()
            tri_total += tris
            if args.max_tris and tris > args.max_tris:
                errors.append(f"'{o.name}': {tris} tris exceeds budget {args.max_tris}.")

        if arm is not None:
            deform = {b.name for b in arm.data.bones if b.use_deform}
            gname = {g.index: g.name for g in o.vertex_groups}
            stray = sorted(g.name for g in o.vertex_groups if g.name not in deform)
            if stray:
                warnings.append(f"'{o.name}': vertex groups with no deform bone: {stray[:8]}")
            over = unweighted = 0
            for v in me.vertices:
                k = sum(1 for g in v.groups if g.weight > EPS and gname.get(g.group) in deform)
                over += k > args.max_influences
                unweighted += k == 0
            if over:
                errors.append(f"'{o.name}': {over} verts exceed {args.max_influences} influences.")
            if unweighted:
                errors.append(f"'{o.name}': {unweighted} verts have no deform weight.")

    if o.type == "ARMATURE":
        bones = o.data.bones
        roots = [b.name for b in bones if b.use_deform and deform_parent(b) is None]
        if len(roots) != 1:
            errors.append(f"Armature '{o.name}': {len(roots)} deform roots {roots[:5]}; ship exactly one.")
        top = [b.name for b in bones if b.parent is None]
        if len(top) != 1:
            errors.append(f"Armature '{o.name}': {len(top)} top-level bones {top[:5]}; ship exactly one root.")
        if args.engine in {"godot", "bevy", "babylon"}:
            # Verified on Blender 5.1.2: deform-only glTF export drops a non-deform root
            # and substitutes a 'neutral_bone'. FBX keeps it; glTF does not.
            dead_top = [b.name for b in bones if b.parent is None and not b.use_deform]
            if dead_top:
                errors.append(f"Armature '{o.name}': root bone(s) {dead_top} have Deform off; glTF "
                              "deform-only export drops them. Enable Deform (zero weights is fine).")
        helpers = sum(1 for b in bones if not b.use_deform)
        if helpers:
            warnings.append(f"Armature '{o.name}': {helpers} non-deform bones; export deform-only "
                            "or ship a separate deform rig.")
        bone_names = {b.name for b in bones}
        unpaired = sorted(n for n in bone_names if (f := flip_side(n)) and f not in bone_names)
        if unpaired:
            warnings.append(f"Armature '{o.name}': side-suffixed bones with no mirror: {unpaired[:8]}")
        if any(AUTO_SUFFIX.search(n) for n in bone_names):
            errors.append(f"Armature '{o.name}': bone names carry a duplicate suffix (.###).")
        if args.engine == "unreal" and o.name == "Armature":
            warnings.append("Armature object still named 'Armature'; confirm your verified root "
                            "convention and check the Skeleton Tree after import.")

for m in used_materials:
    if AUTO_SUFFIX.search(m.name):
        errors.append(f"material '{m.name}': duplicate suffix; engines will create a second material.")

lods = {}
for n in names:
    m = LOD.match(n)
    if m:
        lods.setdefault(m.group(1), set()).add(int(m.group(2)))
for base, levels in sorted(lods.items()):
    if levels != set(range(len(levels))):
        errors.append(f"LOD set '{base}': levels {sorted(levels)} must start at 0 and be contiguous.")

for a in bpy.data.actions:
    if AUTO_SUFFIX.search(a.name):
        warnings.append(f"Action '{a.name}': duplicate suffix; leaks into 'all actions' exports.")
unit_scale = bpy.context.scene.unit_settings.scale_length
if args.engine != "unreal" and abs(unit_scale - 1.0) > 1e-6:
    warnings.append(f"Scene unit scale is {unit_scale}; {args.engine} expects 1.0.")

print(json.dumps({
    "engine": args.engine,
    "blender": bpy.app.version_string,
    "objects": len(objs),
    "triangles": tri_total,
    "unit_scale": unit_scale,
    "errors": errors,
    "warnings": warnings,
}, indent=2))
sys.exit(1 if errors else 0)
