# Headless Blender: keyframe a procedural run / jump / cling / sit on a UniRig skeleton (roles by bone position),
# export one GLB with the four actions. Fallback for when there are no Mixamo clips for the character.
# run: blender -b -P blend_gait.py -- models/dedric-rig.glb models/dedric-anim.glb [biped|quad]
import bpy, sys, math
from mathutils import Vector, Quaternion, Matrix

argv = sys.argv[sys.argv.index('--') + 1:]
IN, OUT = argv[0], argv[1]
KIND = argv[2] if len(argv) > 2 else 'biped'
FPS = 24

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
sc = bpy.context.scene; sc.render.fps = FPS
arm = [o for o in sc.objects if o.type == 'ARMATURE'][0]
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

# ---------- roles from bone positions (same idea as girlRoles()/dogRoles() in the world) ----------
B = arm.data.bones
def kids(b): return [c for c in b.children]
lo = Vector((min(b.head_local.x for b in B), min(b.head_local.y for b in B), min(b.head_local.z for b in B)))
hi = Vector((max(b.head_local.x for b in B), max(b.head_local.y for b in B), max(b.head_local.z for b in B)))
sz = hi - lo
def n(b): return Vector(((b.head_local.x - lo.x) / max(sz.x, 1e-6), (b.head_local.y - lo.y) / max(sz.y, 1e-6), (b.head_local.z - lo.z) / max(sz.z, 1e-6)))
chains = []
for b in B:
    if kids(b): continue
    ch = [b]; c = b
    while c.parent and len(kids(c.parent)) == 1:
        c = c.parent; ch.insert(0, c)
    chains.append(ch)
tip = lambda c: n(c[-1])
# forward axis: the side with the head/snout; for a biped use -Y (glTF forward) unless the rig says otherwise
if KIND == 'quad':
    legs = sorted(chains, key=lambda c: tip(c).z)[:4]
    rest = [c for c in chains if c not in legs]
    tail = sorted(rest, key=lambda c: tip(c).y)[-1] if rest else None          # rearmost (+Y is back for glTF)
    head = sorted([c for c in rest if c is not tail], key=lambda c: tip(c).y)[0] if len(rest) > 1 else None
    front = sorted(legs, key=lambda c: n(c[0]).y)[:2]; back = [c for c in legs if c not in front]
    front = sorted(front, key=lambda c: n(c[0]).x); back = sorted(back, key=lambda c: n(c[0]).x)
    ROLES = {'FL': front[0], 'FR': front[1], 'BL': back[0], 'BR': back[1], 'tail': tail, 'head': head}
else:
    legs = sorted(chains, key=lambda c: tip(c).z)[:2]
    rest = [c for c in chains if c not in legs]
    arms = sorted(rest, key=lambda c: -abs(tip(c).x - .5))[:2]
    head = sorted([c for c in rest if c not in arms], key=lambda c: -tip(c).z)[0]
    legs = sorted(legs, key=lambda c: n(c[0]).x); arms = sorted(arms, key=lambda c: n(c[0]).x)
    spine = []
    c = head[0]
    while c.parent:
        c = c.parent; spine.insert(0, c)
    ROLES = {'L': legs[0], 'R': legs[1], 'AL': arms[0], 'AR': arms[1], 'head': head, 'spine': spine}
print('roles:', {k: ([b.name for b in v] if v else None) for k, v in ROLES.items()})

P = arm.pose.bones
REST = {pb.name: pb.matrix.copy() for pb in P}      # armature-space rest pose
ROOT = P[[b.name for b in B if not b.parent][0]]

def rot_world(pb, axis, ang):
    """Rotate a pose bone about a world axis through its head, on top of the current pose (children follow)."""
    if not hasattr(pb, 'matrix_basis'): pb = P[pb.name]     # chains hold data bones; we pose the pose bones
    bpy.context.view_layer.update()
    m = pb.matrix.copy()
    head = m.to_translation()
    R = Matrix.Translation(head) @ Matrix.Rotation(ang, 4, axis) @ Matrix.Translation(-head)
    pb.matrix = R @ m

def reset():
    for pb in P:
        pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()

def key_all(f):
    for pb in P:
        pb.keyframe_insert('rotation_quaternion', frame=f)
        pb.keyframe_insert('location', frame=f)

def new_action(name):
    act = bpy.data.actions.new(name)
    if not arm.animation_data: arm.animation_data_create()
    arm.animation_data.action = act
    return act

X, Z = Vector((1, 0, 0)), Vector((0, 0, 1))
H = sz.z
d = lambda deg: math.radians(deg)

# ---------- biped clips ----------
if KIND == 'biped':
    L, R, AL, AR, HEAD, SPINE = ROLES['L'], ROLES['R'], ROLES['AL'], ROLES['AR'], ROLES['head'], ROLES['spine']
    def limb(chain, hip, knee, side_swing=0):
        rot_world(chain[0], X, hip)
        if len(chain) > 1: rot_world(chain[1], X, knee)
    # RUN: 16-frame loop
    new_action('Running')
    for i in range(17):
        t = i / 16; ph = t * 2 * math.pi
        reset()
        ROOT.location.z = REST[ROOT.name].to_translation().z * 0 + abs(math.sin(ph * 2)) * H * .035   # bob twice per cycle
        limb(L, d(38) * math.sin(ph), d(-55) * max(0, math.sin(ph + .6)))
        limb(R, d(38) * math.sin(ph + math.pi), d(-55) * max(0, math.sin(ph + math.pi + .6)))
        rot_world(AL[0], X, d(-30) * math.sin(ph)); rot_world(AL[min(1, len(AL) - 1)], X, d(-50))
        rot_world(AR[0], X, d(-30) * math.sin(ph + math.pi)); rot_world(AR[min(1, len(AR) - 1)], X, d(-50))
        if SPINE: rot_world(SPINE[min(1, len(SPINE) - 1)], X, d(-8))
        rot_world(HEAD[0], X, d(6))
        key_all(i + 1)
    # JUMP: crouch (0-6) -> launch (6-12) -> apex tuck (12-20) -> fall (20-28) -> land squash (28-36)
    new_action('Jump')
    def jump_pose(t):
        reset()
        if t < .17:   # crouch
            k = t / .17; ROOT.location.z = -H * .10 * k
            limb(L, d(-35) * k, d(60) * k); limb(R, d(-35) * k, d(60) * k)
            rot_world(AL[0], X, d(35) * k); rot_world(AR[0], X, d(35) * k)
            if SPINE: rot_world(SPINE[0], X, d(-18) * k)
        elif t < .56:  # in the air, arms up, knees tucked then extended
            k = (t - .17) / .39; up = math.sin(k * math.pi)
            ROOT.location.z = H * .55 * up
            limb(L, d(-25) * up, d(80) * up); limb(R, d(-15) * up, d(70) * up)
            rot_world(AL[0], X, d(-120) * min(1, k * 2)); rot_world(AR[0], X, d(-120) * min(1, k * 2))
            if SPINE: rot_world(SPINE[0], X, d(8) * up)
        elif t < .8:   # fall: legs reaching down
            k = (t - .56) / .24
            ROOT.location.z = H * .55 * (1 - k) ** 2 * .3
            limb(L, d(-10), d(20)); limb(R, d(-10), d(20))
            rot_world(AL[0], X, d(-120) * (1 - k) + d(20) * k); rot_world(AR[0], X, d(-120) * (1 - k) + d(20) * k)
        else:          # land squash and recover
            k = (t - .8) / .2; s = math.sin(k * math.pi)
            ROOT.location.z = -H * .08 * s
            limb(L, d(-30) * s, d(55) * s); limb(R, d(-30) * s, d(55) * s)
            rot_world(AL[0], X, d(25) * s); rot_world(AR[0], X, d(25) * s)
            if SPINE: rot_world(SPINE[0], X, d(-15) * s)
    for i in range(37):
        jump_pose(i / 36); key_all(i + 1)
    # HANGING IDLE (cling): arms up gripping, body hanging, legs dangling
    new_action('Hanging Idle')
    for i in range(17):
        ph = i / 16 * 2 * math.pi
        reset()
        rot_world(AL[0], X, d(-165)); rot_world(AR[0], X, d(-165))
        rot_world(AL[min(1, len(AL) - 1)], X, d(-10)); rot_world(AR[min(1, len(AR) - 1)], X, d(-10))
        limb(L, d(12) * math.sin(ph) - d(5), d(25)); limb(R, d(12) * math.sin(ph + 1.2) - d(5), d(25))
        if SPINE: rot_world(SPINE[0], X, d(10))
        rot_world(HEAD[0], X, d(-15))
        key_all(i + 1)
    # SITTING IDLE: on the ledge, breathing
    new_action('Sitting Idle')
    for i in range(25):
        ph = i / 24 * 2 * math.pi
        reset()
        ROOT.location.z = -H * .28
        limb(L, d(-88), d(85)); limb(R, d(-88), d(85))
        rot_world(AL[0], X, d(20)); rot_world(AR[0], X, d(20))
        rot_world(AL[min(1, len(AL) - 1)], X, d(-60)); rot_world(AR[min(1, len(AR) - 1)], X, d(-60))
        if SPINE: rot_world(SPINE[0], X, d(-6) + d(2) * math.sin(ph))
        rot_world(HEAD[0], X, d(4) * math.sin(ph))
        key_all(i + 1)
else:
    # ---------- quadruped clips: gallop / jump / cling (paws up on the ledge) / sit ----------
    FL, FR, BL, BR, TAIL, HEAD = ROLES['FL'], ROLES['FR'], ROLES['BL'], ROLES['BR'], ROLES['tail'], ROLES['head']
    def leg(chain, hip, knee):
        rot_world(chain[0], X, hip)
        if len(chain) > 1: rot_world(chain[1], X, knee)
    new_action('Running')
    for i in range(17):
        ph = i / 16 * 2 * math.pi
        reset()
        ROOT.location.z = abs(math.sin(ph)) * H * .12
        leg(FL, d(45) * math.sin(ph), d(-40) * max(0, math.sin(ph + .5))); leg(FR, d(45) * math.sin(ph + .6), d(-40) * max(0, math.sin(ph + 1.1)))
        leg(BL, d(45) * math.sin(ph + math.pi), d(-40) * max(0, math.sin(ph + math.pi + .5))); leg(BR, d(45) * math.sin(ph + math.pi + .6), d(-40) * max(0, math.sin(ph + math.pi + 1.1)))
        if TAIL: rot_world(TAIL[0], X, d(25) * math.sin(ph * 2))
        if HEAD: rot_world(HEAD[0], X, d(8) * math.sin(ph))
        key_all(i + 1)
    new_action('Jump')
    for i in range(37):
        t = i / 36; reset()
        if t < .2:
            k = t / .2; ROOT.location.z = -H * .15 * k; [leg(c, d(-35) * k, d(50) * k) for c in (BL, BR)]; [leg(c, d(-20) * k, d(30) * k) for c in (FL, FR)]
        elif t < .6:
            k = (t - .2) / .4; up = math.sin(k * math.pi); ROOT.location.z = H * .9 * up
            [leg(c, d(-40) * up, d(-20) * up) for c in (FL, FR)]; [leg(c, d(40) * up, d(-45) * up) for c in (BL, BR)]
            if TAIL: rot_world(TAIL[0], X, d(-30) * up)
        elif t < .8:
            k = (t - .6) / .2; ROOT.location.z = H * .9 * (1 - k) ** 2 * .3; [leg(c, d(-15), d(10)) for c in (FL, FR, BL, BR)]
        else:
            k = (t - .8) / .2; s = math.sin(k * math.pi); ROOT.location.z = -H * .12 * s; [leg(c, d(-30) * s, d(45) * s) for c in (FL, FR, BL, BR)]
        key_all(i + 1)
    new_action('Hanging Idle')
    for i in range(17):
        ph = i / 16 * 2 * math.pi; reset()
        [leg(c, d(-140), d(-30)) for c in (FL, FR)]; [leg(c, d(20) * math.sin(ph) - d(10), d(25)) for c in (BL, BR)]
        if HEAD: rot_world(HEAD[0], X, d(-20))
        if TAIL: rot_world(TAIL[0], X, d(15) * math.sin(ph))
        key_all(i + 1)
    new_action('Sitting Idle')
    for i in range(25):
        ph = i / 24 * 2 * math.pi; reset()
        ROOT.location.z = -H * .18
        [leg(c, d(-90), d(80)) for c in (BL, BR)]; [leg(c, d(10), d(0)) for c in (FL, FR)]
        if TAIL: rot_world(TAIL[0], Z, d(35) * math.sin(ph * 2))
        if HEAD: rot_world(HEAD[0], X, d(5) * math.sin(ph))
        key_all(i + 1)

# keep every action in the file (NLA strips) so the glTF exporter writes all four
bpy.ops.object.mode_set(mode='OBJECT')
ad = arm.animation_data
for act in bpy.data.actions:
    tr = ad.nla_tracks.new(); tr.name = act.name; tr.strips.new(act.name, int(act.frame_range[0]), act)
ad.action = None
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_animations=True, export_skins=True, export_apply=False, export_nla_strips=True, export_yup=True)
print('exported', OUT, 'actions', [a.name for a in bpy.data.actions])
