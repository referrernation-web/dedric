# Headless Blender: render 8-frame side-view sprite strips (transparent) from an animated GLB.
# run: blender -b -P blend_sprites.py -- models/dedric-anim.glb out_dir H "run=Running" "jump=Jump" "cling=Hanging Idle" ["sit=Sitting Idle"]
#   clip names are matched case-insensitively as substrings of the GLB action names; "*" = the first action.
#   Output: out_dir/<key>_0.png .. _7.png (each H px tall, facing +X = right), then strip.py packs them.
import bpy, sys, os, math
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:]
GLB, OUT, H = argv[0], argv[1], int(argv[2])
CLIPS = [a.split('=', 1) for a in argv[3:]]
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene
arm = [o for o in sc.objects if o.type == 'ARMATURE']
arm = arm[0] if arm else None
meshes = [o for o in sc.objects if o.type == 'MESH']
acts = list(bpy.data.actions)
print('actions:', [a.name for a in acts])

# ---- bounds over the rest pose: frame the character so every clip fits (tallest jump gets headroom) ----
def bounds():
    lo = Vector((1e9, 1e9, 1e9)); hi = Vector((-1e9, -1e9, -1e9))
    dg = bpy.context.evaluated_depsgraph_get()
    for m in meshes:
        ev = m.evaluated_get(dg)
        for v in ev.data.vertices:
            w = ev.matrix_world @ v.co
            lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z))); hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
    return lo, hi

lo, hi = bounds()
size = hi - lo
cz = (lo.z + hi.z) / 2
print('rest bounds', [round(x, 2) for x in lo], [round(x, 2) for x in hi])

# ---- lights + ortho camera on +X looking -X (side view, character faces +X after the glTF import: -Y forward -> we spin it) ----
root = arm if arm else meshes[0]
root.rotation_euler = (root.rotation_euler.x, root.rotation_euler.y, root.rotation_euler.z + math.radians(90))   # -Y facing -> +X facing
bpy.context.view_layer.update()

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
cam.data.type = 'ORTHO'
sc.collection.objects.link(cam); sc.camera = cam
pad = 1.35                     # head/foot room for the jump apex and the crouch
ortho = max(size.z, max(size.x, size.y)) * pad
cam.data.ortho_scale = ortho
cam.location = (max(size.x, size.y) * 4, 0, cz + size.z * .12)
cam.rotation_euler = (math.radians(90), 0, math.radians(90))

def light(name, kind, loc, energy, col=(1, 1, 1)):
    l = bpy.data.lights.new(name, kind); l.energy = energy; l.color = col
    o = bpy.data.objects.new(name, l); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (Vector(loc) * -1).to_track_quat('-Z', 'Y').to_euler(); return o
light('key', 'SUN', (4, -3, 6), 3.5); light('fill', 'SUN', (4, 4, 3), 1.6, (.85, .8, 1)); light('rim', 'SUN', (-3, 2, 5), 2.2, (.75, 1, .6))
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
sc.world.node_tree.nodes['Background'].inputs[1].default_value = .6

# ---- render settings: EEVEE, transparent film, square-ish frame ----
sc.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'SceneEEVEE') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
sc.render.film_transparent = True
sc.render.resolution_y = H
sc.render.resolution_x = int(H * 1.0)
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'

def find_action(pat):
    if pat == '*':
        return acts[0] if acts else None
    for a in acts:
        if pat.lower() in a.name.lower():
            return a
    return None

for key, pat in CLIPS:
    act = find_action(pat)
    if not act:
        print('!! no action for', key, pat); continue
    if arm:
        if not arm.animation_data: arm.animation_data_create()
        arm.animation_data.action = act
    f0, f1 = act.frame_range
    # one cycle for loops (run/gallop); the whole clip for jump/cling
    frames = [f0 + (f1 - f0) * i / 8 for i in range(8)] if key in ('run', 'gallop') else [f0 + (f1 - f0) * i / 7 for i in range(8)]
    for i, f in enumerate(frames):
        sc.frame_set(int(round(f)))
        sc.render.filepath = os.path.join(OUT, f'{key}_{i}.png')
        bpy.ops.render.render(write_still=True)
    print('rendered', key, 'from', act.name, 'frames', [int(round(f)) for f in frames])
print('done')
