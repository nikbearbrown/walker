"""
make_test_asset.py — build a tiny known-good scene to prove the pipeline end to end:
a 1 m crate (static) and a 3-bone skinned column (rigged), in an EXPORT collection.
Pass --bad to inject the classic mistakes (unapplied scale, .001 name, extra roots)
so you can watch the validator catch them.

  blender --background --python scripts/blender/make_test_asset.py -- --out build/test.blend [--bad]
"""
import argparse
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--bad", action="store_true")
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
export = bpy.data.collections.new("EXPORT")
work = bpy.data.collections.new("WORK")
scene.collection.children.link(export)
scene.collection.children.link(work)

mat = bpy.data.materials.new("MAT_Test")


def add_mesh(name, verts, faces, coll):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    me.uv_layers.new(name="UVMap")
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


# Crate: 1 m cube, origin at floor contact.
h = 0.5
cv = [(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0), (-h, -h, 1), (h, -h, 1), (h, h, 1), (-h, h, 1)]
cf = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
crate = add_mesh("Crate", cv, cf, export)

# Skinned column: 3 stacked quads-rings, 1.8 m tall, bones root -> spine -> head.
ring = [(-0.2, -0.2), (0.2, -0.2), (0.2, 0.2), (-0.2, 0.2)]
zs = [0.0, 0.6, 1.2, 1.8]
verts = [(x, y, z) for z in zs for x, y in ring]
faces = []
for i in range(3):
    for j in range(4):
        a, b = i * 4 + j, i * 4 + (j + 1) % 4
        faces.append((a, b, b + 4, a + 4))
column = add_mesh("Column", verts, faces, export)
column.location = (2.0, 0, 0)

arm_data = bpy.data.armatures.new("Rig")
rig = bpy.data.objects.new("Rig", arm_data)
export.objects.link(rig)
rig.location = (2.0, 0, 0)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
eb = arm_data.edit_bones
root = eb.new("root"); root.head, root.tail = (0, 0, 0), (0, 0, 0.3)
spine = eb.new("spine_01"); spine.head, spine.tail = (0, 0, 0.3), (0, 0, 1.2); spine.parent = root
head = eb.new("head"); head.head, head.tail = (0, 0, 1.2), (0, 0, 1.8); head.parent = spine
if args.bad:
    stray = eb.new("stray"); stray.head, stray.tail = (0.5, 0, 0), (0.5, 0, 0.3)  # second root
bpy.ops.object.mode_set(mode="OBJECT")
for b in arm_data.bones:
    b.use_deform = True

# Skin: rigid-ish weights by height band.
column.parent = rig
mod = column.modifiers.new("Armature", "ARMATURE")
mod.object = rig
groups = {n: column.vertex_groups.new(name=n) for n in ("root", "spine_01", "head")}
for v in column.data.vertices:
    z = v.co.z
    groups["root" if z < 0.1 else "spine_01" if z < 1.5 else "head"].add([v.index], 1.0, "REPLACE")

# One action so animation export has something to carry.
rig.animation_data_create()
act = bpy.data.actions.new("Idle")
rig.animation_data.action = act
rig.pose.bones["head"].rotation_mode = "XYZ"
for f, ang in ((1, 0.0), (24, 0.3), (48, 0.0)):
    rig.pose.bones["head"].rotation_euler = (ang, 0, 0)
    rig.pose.bones["head"].keyframe_insert("rotation_euler", frame=f)

if args.bad:
    crate.scale = (2, 2, 2)                       # unapplied scale
    crate.name = "Crate.001"                      # duplicate-suffix name
    column.data.vertices[0].select = True
    for g in column.data.vertices[0].groups:      # leave one vertex unweighted
        column.vertex_groups[g.group].remove([0])

bpy.ops.wm.save_as_mainfile(filepath=args.out)
print("wrote", args.out)
