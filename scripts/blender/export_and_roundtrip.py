"""
export_and_roundtrip.py — export EXPORT with an engine preset, re-import into a
cleared in-memory scene, compare counts and size. Never saves the .blend.
Proves the file is complete and correctly scaled as Blender reads it back;
it does NOT prove the engine reads it the same way.

  blender --background asset.blend --python-exit-code 1 \
    --python scripts/blender/export_and_roundtrip.py -- --engine godot --out build/Crate.glb
"""
import argparse
import json
import os
import sys

import bpy
from mathutils import Vector

ENGINES = ["godot", "bevy", "babylon", "unreal", "unity"]
GLTF_ENGINES = {"godot", "bevy", "babylon"}
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--engine", choices=ENGINES, required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--collection", default="EXPORT")
args = ap.parse_args(argv)
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

FBX_COMMON = dict(
    use_selection=True,
    object_types={"MESH", "ARMATURE", "EMPTY"},
    apply_unit_scale=True,
    mesh_smooth_type="FACE",
    add_leaf_bones=False,
    use_armature_deform_only=True,
    bake_anim=True,
    path_mode="COPY",
    embed_textures=True,
)
FBX_PRESETS = {
    "unreal": dict(FBX_COMMON, apply_scale_options="FBX_SCALE_ALL"),
    "unity": dict(FBX_COMMON, apply_scale_options="FBX_SCALE_UNITS", axis_forward="-Z", axis_up="Y"),
}


def measure(objs, deform_only):
    dg = bpy.context.evaluated_depsgraph_get()
    tris = bones = meshes = 0
    lo, hi = Vector((1e18,) * 3), Vector((-1e18,) * 3)
    for o in objs:
        # The glTF importer adds display-only bone-shape meshes; they are not exported content.
        if any(c.name == "glTF_not_exported" for c in o.users_collection):
            continue
        if o.type == "ARMATURE":
            bones += sum(1 for b in o.data.bones if b.use_deform or not deform_only)
            continue
        if o.type != "MESH":
            continue
        meshes += 1
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        tris += sum(len(p.vertices) - 2 for p in me.polygons)
        ev.to_mesh_clear()
        for corner in ev.bound_box:
            w = ev.matrix_world @ Vector(corner)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    size = [round(x, 4) for x in (hi - lo)] if meshes else [0.0, 0.0, 0.0]
    return {"meshes": meshes, "tris": tris, "deform_bones": bones, "size_m": size}


coll = bpy.data.collections.get(args.collection)
if coll is None:
    sys.exit(f"No '{args.collection}' collection.")
export_objs = list(coll.all_objects)
before = measure(export_objs, deform_only=True)

# Select via the data API, not operators.
for o in bpy.context.view_layer.objects:
    o.select_set(o in export_objs)

if args.engine in GLTF_ENGINES:
    bpy.ops.export_scene.gltf(filepath=args.out, export_format="GLB", use_selection=True,
                              export_apply=True, export_def_bones=True)
else:
    bpy.ops.export_scene.fbx(filepath=args.out, **FBX_PRESETS[args.engine])

# Clear the in-memory scene; the .blend on disk is never written.
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

if args.engine in GLTF_ENGINES:
    bpy.ops.import_scene.gltf(filepath=args.out)
else:
    bpy.ops.import_scene.fbx(filepath=args.out)
after = measure(list(bpy.context.scene.objects), deform_only=False)

problems = [f"{k}: {before[k]} -> {after[k]}"
            for k in ("meshes", "tris", "deform_bones") if before[k] != after[k]]
if any(abs(a - b) > 1e-3 * max(1.0, abs(a)) for a, b in zip(before["size_m"], after["size_m"])):
    problems.append(f"size_m: {before['size_m']} -> {after['size_m']}")

print(json.dumps({"engine": args.engine, "file": args.out, "before": before,
                  "after": after, "problems": problems}, indent=2))
sys.exit(1 if problems else 0)
