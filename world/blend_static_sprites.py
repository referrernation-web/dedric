# ponytail: stopgap sprite renderer for UNRIGGED meshes — whole-body jump/bob/tilt, no joints.
# run: blender -b -P blend_static_sprites.py -- in.glb out_dir H     (out_dir ABSOLUTE)
# Replace with blend_gait.py + blend_sprites.py once the UniRig GLB lands.
import bpy, sys, os, math
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
GLB, OUT, H = argv[0], argv[1], int(argv[2])
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == 'MESH']
roots = [o for o in sc.objects if o.parent is None]
root = bpy.data.objects.new('root', None); sc.collection.objects.link(root)
for o in roots: o.parent = root
bpy.context.view_layer.update()
lo = Vector((1e9,)*3); hi = Vector((-1e9,)*3)
dg = bpy.context.evaluated_depsgraph_get()
for m in meshes:
    ev = m.evaluated_get(dg)
    for v in ev.data.vertices:
        w = ev.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
size = hi - lo; cz = (lo.z + hi.z) / 2
# pivot at the feet so squash/tilt happen around the ground
for o in roots: o.location -= Vector((0, 0, lo.z))
root.rotation_euler = (0, 0, math.radians(125))   # 3/4 view, face toward +X camera & screen-right
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); cam.data.type = 'ORTHO'
sc.collection.objects.link(cam); sc.camera = cam
cam.data.ortho_scale = max(size.z, size.x, size.y) * 1.5
cam.location = (max(size.x, size.y) * 4, 0, size.z * .72)
cam.rotation_euler = (math.radians(90), 0, math.radians(90))
def light(name, loc, e, col=(1, 1, 1)):
    l = bpy.data.lights.new(name, 'SUN'); l.energy = e; l.color = col
    o = bpy.data.objects.new(name, l); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (Vector(loc) * -1).to_track_quat('-Z', 'Y').to_euler()
light('key', (4, -3, 6), 3.5); light('fill', (4, 4, 3), 1.6, (.85, .8, 1)); light('rim', (-3, 2, 5), 2.2, (.75, 1, .6))
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
sc.world.node_tree.nodes['Background'].inputs[1].default_value = .6
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = H
sc.render.image_settings.color_mode = 'RGBA'; sc.view_settings.view_transform = 'Standard'
def pose(key, t):   # t in [0,1) -> (z offset, tilt rad, (sx,sy,sz))
    z = size.z
    if key == 'run':  b = abs(math.sin(t * 2 * math.pi)); return z * .06 * b, math.radians(-10), (1, 1, 1 - .04 * b)
    if key == 'jump':
        a = math.sin(t * math.pi); crouch = max(0, 1 - t * 6) * .12 + max(0, (t - .85) * 6) * .1
        return z * .38 * a, math.radians(-6 * a), (1 + crouch * .6, 1 + crouch * .6, 1 - crouch)
    if key == 'cling': return z * .02 * math.sin(t * 2 * math.pi), math.radians(-25), (1, 1, 1)
    return 0, math.radians(15), (1, 1, .82)   # sit
for key in ('run', 'jump', 'cling', 'sit'):
    for i in range(8):
        t = i / 8 if key in ('run', 'cling') else i / 7
        dz, tilt, s = pose(key, t)
        root.location = (0, 0, dz); root.rotation_euler = (0, tilt, math.radians(125)); root.scale = s
        sc.render.filepath = os.path.join(OUT, f'{key}_{i}.png'); bpy.ops.render.render(write_still=True)
print('done')
