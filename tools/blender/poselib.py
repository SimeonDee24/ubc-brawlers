# Simeon pose library (runs inside Blender). exec() this file, then use pose_apply / build_action.
# Character frame: f = forward (his facing, world -Y), u = up (world +Z), s = side (+ = his left, world +X).
import bpy, math
from mathutils import Vector, Matrix, Quaternion, Euler

RIG = bpy.data.objects['Rig']
ARM = RIG.data

def V(f, u, s=0.0):
    return Vector((s, -f, u))

def rad(d):
    return math.radians(d)

# ---------------------------------------------------------------- defaults
# arms: hand target relative to the shoulder joint, in the body frame (f, u, s_out)
#       s_out is outward from the body (positive = away from the midline on that side)
# legs: ankle target: ('w', f, u, s_out) world/ground relative to the root, or ('b', f, u, s_out) relative to the hip joint
DEFAULT = dict(
    pos=(0.0, 0.0), rot=0.0, yaw=0.0,           # body offset (f, u) and whole-body pitch (deg, + = forward roll), yaw (deg)
    hips=(0, 0, 0), spine=(4, 0, 0), chest=(2, 0, 0), neck=(-2, 0, 0), head=(-2, 0, 0),   # (lean fwd, twist, side bend)
    handR=(0.03, -0.5, 0.04), handL=(0.03, -0.5, 0.04),
    poleR=(-0.3, -0.2, 1.0), poleL=(-0.3, -0.2, 1.0),       # elbow direction (f, u, s_out)
    hdirR=(0.15, -1.0, 0.0), hdirL=(0.15, -1.0, 0.0),        # where the fingers point (f, u, s_out)
    hbackR=(0.0, 0.0, 1.0), hbackL=(0.0, 0.0, 1.0),          # back of the hand faces (f, u, s_out)
    curlR=0.25, curlL=0.25, thumbR=0.3, thumbL=0.3,         # 0 = flat open hand, 1 = tight fist
    footR=('w', 0.02, 0.095, 0.11), footL=('w', -0.02, 0.095, 0.11),
    kneeR=(1.0, 0.0, 0.08), kneeL=(1.0, 0.0, 0.08),
    fpR=0.0, fpL=0.0, toeR=0.0, toeL=0.0,                   # foot pitch (+ = toes up) and toe bend, deg
    mouth=0.0, browR=(0, 0), browL=(0, 0), squint=0.0,      # brow: (raise m*100, tilt deg: + = inner end down / angry)
    props=(),                                               # 'controller' 'bat' 'ball' 'chips' 'card'
    face='neutral',
)

REST = {b.name: b.matrix_local.copy() for b in ARM.bones}
def rest_head(n): return REST[n].to_translation()
LEN = {b.name: b.length for b in ARM.bones}
PROPS = ('controller', 'bat', 'ball', 'chips', 'card')

def body_matrix(P):
    piv = Vector((0, 0, 1.08))
    R = Matrix.Rotation(rad(P['yaw']), 4, 'Z') @ Matrix.Rotation(rad(P['rot']), 4, 'X')
    off = V(P['pos'][0], P['pos'][1])
    return Matrix.Translation(piv + off) @ R @ Matrix.Translation(-piv)

def set_world(pb, M):
    pb.matrix = M
    bpy.context.view_layer.update()

def aim_matrix(head, ydir, zhint):
    y = ydir.normalized()
    z = (zhint - y*zhint.dot(y))
    if z.length < 1e-6: z = y.orthogonal()
    z.normalize(); x = y.cross(z).normalized()
    M = Matrix((x, y, z)).transposed().to_4x4(); M.translation = head
    return M

def min_rot_matrix(name, head, ydir, parent_delta=None):
    rest = REST[name]
    ry = Vector(rest.col[1][:3]).normalized()
    base = rest.to_3x3()
    if parent_delta is not None:
        base = parent_delta @ base; ry = (parent_delta @ ry).normalized()
    q = ry.rotation_difference(ydir.normalized())
    M = (q.to_matrix() @ base).to_4x4(); M.translation = head
    return M

def two_bone(S, T, L1, L2, pole):
    d = T - S; dist = d.length
    dist = min(max(dist, abs(L1 - L2) + 1e-4), L1 + L2 - 1e-4)
    dn = d.normalized()
    a = (L1*L1 + dist*dist - L2*L2)/(2*L1*dist)
    a = max(-1, min(1, a))
    h = L1*math.sqrt(1 - a*a)
    p = pole - dn*pole.dot(dn)
    if p.length < 1e-6: p = dn.orthogonal()
    p.normalize()
    E = S + dn*(L1*a) + p*h
    return E, S + dn*dist

def side_vec(f, u, so, s):   # (f, u, outward) on side s (+1 left, -1 right) in body frame
    return V(f, u, so*s)

def pose_apply(P):
    pbs = RIG.pose.bones
    for pb in pbs:
        pb.rotation_mode = 'QUATERNION'
        pb.location = (0, 0, 0); pb.rotation_quaternion = (1, 0, 0, 0); pb.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    BM = body_matrix(P); BR = BM.to_3x3()
    set_world(pbs['body'], BM @ REST['body'])
    for n in ('hips', 'spine', 'chest', 'neck', 'head'):
        lean, tw, sb = P[n]
        pbs[n].rotation_quaternion = Euler((rad(lean), rad(tw), rad(-sb))).to_quaternion()
    bpy.context.view_layer.update()
    # arms
    for k, s in (('L', 1), ('R', -1)):
        ua, fa, hd = pbs['upper_arm.' + k], pbs['forearm.' + k], pbs['hand.' + k]
        S = ua.head.copy()
        T = S + BR @ side_vec(*P['hand' + k], s)
        pole = BR @ side_vec(*P['pole' + k], s)
        E, H = two_bone(S, T, LEN['upper_arm.' + k], LEN['forearm.' + k], pole)
        delta = (pbs['shoulder.' + k].matrix.to_3x3() @ REST['shoulder.' + k].to_3x3().inverted())
        set_world(ua, min_rot_matrix('upper_arm.' + k, S, E - S, delta))
        hdir = BR @ side_vec(*P['hdir' + k], s); hback = BR @ side_vec(*P['hback' + k], s)
        # forearm twists halfway toward the hand's roll
        fz = hback - (H - E).normalized()*hback.dot((H - E).normalized())
        set_world(fa, aim_matrix(E, H - E, fz if fz.length > 1e-4 else Vector((0, 0, 1))))
        set_world(hd, aim_matrix(H, hdir, hback))
        c, t = P['curl' + k], P['thumb' + k]
        for fn in ('index', 'middle', 'ring', 'pinky'):
            spread = {'index': 4, 'middle': 0, 'ring': -3, 'pinky': -7}[fn]*(1 - c)
            pbs[f'{fn}1.{k}'].rotation_quaternion = Euler((rad(-8 - 82*c), 0, rad(spread*s))).to_quaternion()
            pbs[f'{fn}2.{k}'].rotation_quaternion = Euler((rad(-10 - 95*c), 0, 0)).to_quaternion()
        pbs['thumb1.' + k].rotation_quaternion = Euler((rad(-10 - 25*t), 0, rad(s*(-5 - 30*t)))).to_quaternion()
        pbs['thumb2.' + k].rotation_quaternion = Euler((rad(-10 - 50*t), 0, 0)).to_quaternion()
        bpy.context.view_layer.update()
    # legs
    for k, s in (('L', 1), ('R', -1)):
        th, sh, ft, to = pbs['thigh.' + k], pbs['shin.' + k], pbs['foot.' + k], pbs['toe.' + k]
        S = th.head.copy()
        spec = P['foot' + k]
        if spec[0] == 'w':
            T = Vector((spec[3]*s, -spec[1], spec[2])) + V(P['pos'][0], 0)
        else:
            T = S + BR @ side_vec(spec[1], spec[2], spec[3], s)
        pole = BR @ side_vec(*P['knee' + k], s)
        E, A = two_bone(S, T, LEN['thigh.' + k], LEN['shin.' + k], pole)
        delta = pbs['hips'].matrix.to_3x3() @ REST['hips'].to_3x3().inverted()
        set_world(th, min_rot_matrix('thigh.' + k, S, E - S, delta))
        set_world(sh, aim_matrix(E, A - E, BR @ V(1, 0, 0)))
        # foot: rest direction rotated by pitch about the body's side axis (planted feet ignore body pitch)
        rest_dir = (Vector(REST['foot.' + k].col[1][:3])).normalized()
        R = (Matrix.Rotation(rad(-P['fp' + k]), 3, Vector((1, 0, 0))))
        fr = BR if spec[0] == 'b' else Matrix.Rotation(rad(P['yaw']), 3, 'Z')
        set_world(ft, aim_matrix(A, fr @ R @ rest_dir, fr @ R @ Vector((0, 0, 1))))
        to.rotation_quaternion = Euler((rad(P['toe' + k]), 0, 0)).to_quaternion()
        bpy.context.view_layer.update()
    # face
    m = max(0.0, P['mouth']); pbs['mouth'].scale = (m, m, m)
    for k in ('L', 'R'):
        up, tilt = P['brow' + k]
        b = pbs['brow.' + k]; b.location = (0, 0, up*0.01)
        b.rotation_quaternion = Euler((0, rad(tilt*(1 if k == 'L' else -1)), 0)).to_quaternion()
        e = pbs['eye.' + k]; sq = 1 - 0.7*P['squint']; e.scale = (1, 1, sq)
    for pn in PROPS:
        v = 1.0 if pn in P['props'] else 0.0
        pbs['prop_' + pn].scale = (v, v, v)
    bpy.context.view_layer.update()

# ---------------------------------------------------------------- faces
FACES = {
    'neutral': dict(mouth=0.0, browR=(0, 0), browL=(0, 0), squint=0.0),
    'smile': dict(mouth=0.0, browR=(0.15, -4), browL=(0.15, -4), squint=0.12),
    'yell': dict(mouth=1.0, browR=(-0.25, 16), browL=(-0.25, 16), squint=0.25),
    'hurt': dict(mouth=0.55, browR=(0.3, -18), browL=(0.3, -18), squint=0.7),
    'focus': dict(mouth=0.0, browR=(-0.2, 12), browL=(-0.2, 12), squint=0.2),
}

def make(**kw):
    P = dict(DEFAULT)
    face = kw.get('face')
    if face: P.update(FACES[face])
    P.update(kw)
    return P

# ---------------------------------------------------------------- interpolation
def ease(t, kind):
    if kind == 'lin': return t
    if kind == 'in': return t*t
    if kind == 'out': return 1 - (1 - t)*(1 - t)
    if kind == 'snap': return 1 - (1 - t)**3
    return t*t*(3 - 2*t)   # 'io'

def lerp(a, b, t):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return a + (b - a)*t
    if isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b):
        if a and isinstance(a[0], str):
            if a[0] != b[0]: return b if t >= 0.5 else a
            return (a[0],) + tuple(x + (y - x)*t for x, y in zip(a[1:], b[1:]))
        if all(isinstance(x, (int, float)) for x in a + b):
            return tuple(x + (y - x)*t for x, y in zip(a, b))
    return b if t >= 0.5 else a

def blend(A, B, t):
    return {k: lerp(A[k], B[k], t) for k in A}

def sample(keys, frame, loop=False, total=None):
    """keys: list of (frame, pose, ease_into_this_key)"""
    if loop:
        frame = frame % total
        keys = keys + [(total, keys[0][1], keys[0][2] if len(keys[0]) > 2 else 'io')]
    if frame <= keys[0][0]: return keys[0][1]
    for (f0, p0, *_), (f1, p1, *e) in zip(keys, keys[1:]):
        if f0 <= frame <= f1:
            t = (frame - f0)/(f1 - f0) if f1 > f0 else 1
            return blend(p0, p1, ease(t, e[0] if e else 'io'))
    return keys[-1][1]

def action_fcurves(act):
    fcs = []
    if hasattr(act, 'layers'):
        for layer in act.layers:
            for strip in layer.strips:
                for cb in getattr(strip, 'channelbags', []):
                    fcs += list(cb.fcurves)
    if not fcs and hasattr(act, 'fcurves'):
        fcs = list(act.fcurves)
    return fcs

def build_action(name, keys, length, loop=False):
    """Bake an action with a key on every frame 0..length (inclusive) for every bone."""
    act = bpy.data.actions.get(name)
    if act: bpy.data.actions.remove(act)
    act = bpy.data.actions.new(name); act.use_fake_user = True
    RIG.animation_data_create(); RIG.animation_data.action = act
    frames = []
    for fr in range(0, length + 1):
        P = sample(keys, fr, loop, length)
        pose_apply(P)
        for pb in RIG.pose.bones:
            pb.keyframe_insert('location', frame=fr, group=pb.name)
            pb.keyframe_insert('rotation_quaternion', frame=fr, group=pb.name)
            pb.keyframe_insert('scale', frame=fr, group=pb.name)
        frames.append(P)
    for fc in action_fcurves(act):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    act['loop'] = 1 if loop else 0
    act['length'] = length
    return act, frames
