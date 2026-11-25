# Build every action in A, bake 2D joints for the game, export the GLB. exec() after poselib + anim files.
import bpy, json, math
from mathutils import Vector

OUTDIR = '/Users/sldee2006/Documents/Simeon-3d-Models/'
# The game camera: looks at his right side, turned 30 degrees toward his front, 6 degrees from above.
CAM_YAW, CAM_PITCH = 30.0, 6.0
def cam_axes():
    y, p = math.radians(CAM_YAW), math.radians(CAM_PITCH)
    # direction from the character toward the camera
    to_cam = Vector((-math.cos(y)*math.cos(p), -math.sin(y)*math.cos(p), math.sin(p)))
    right = Vector((0, 0, 1)).cross(to_cam).normalized()   # screen right
    up = to_cam.cross(right).normalized()
    return right, up, to_cam
RIGHT, UP, TOCAM = cam_axes()
# Gameplay joints use the same yaw but no downward tilt, so the floor stays the floor in 2D.
_p = CAM_PITCH; CAM_PITCH = 0.0; RIGHT, UP, _ = cam_axes(); CAM_PITCH = _p
PX_PER_M = 42.0/1.78   # the game draws Simeon 42px tall (70 inches)

def proj(p):
    return (p.dot(RIGHT)*PX_PER_M, -p.dot(UP)*PX_PER_M)   # game: x forward, y down, origin at the feet

def bake_frame(P):
    pb = RIG.pose.bones
    def W(n, tail=False): return RIG.matrix_world @ (pb[n].tail if tail else pb[n].head)
    j = {
        'hip': proj(W('hips')), 'neck': proj(W('neck')), 'headTop': proj(W('head', True)),
        'shF': proj(W('upper_arm.R')), 'elF': proj(W('forearm.R')), 'wrF': proj(W('hand.R')), 'knF': proj(W('hand.R', True)),
        'shB': proj(W('upper_arm.L')), 'elB': proj(W('forearm.L')), 'wrB': proj(W('hand.L')), 'knB': proj(W('hand.L', True)),
        'hipF': proj(W('thigh.R')), 'kneeF': proj(W('shin.R')), 'ankF': proj(W('foot.R')), 'toeF': proj(W('toe.R', True)),
        'hipB': proj(W('thigh.L')), 'kneeB': proj(W('shin.L')), 'ankB': proj(W('foot.L')), 'toeB': proj(W('toe.L', True)),
    }
    # weapon points straight from the 3D prop, so bat and controller hitboxes sit on the prop itself
    props = P.get('props', ())
    if 'bat' in props or 'controller' in props:
        b = pb['prop_bat' if 'bat' in props else 'prop_controller']
        M = RIG.matrix_world @ b.matrix
        h = M.to_translation(); X = -Vector(M.col[0][:3]).normalized(); Y = Vector(M.col[1][:3]).normalized()
        if 'bat' in props: j['wF'], j['wM'] = proj(h + X*0.64), proj(h + X*0.36)
        else: j['wF'], j['wM'] = proj(h + Y*0.56), proj(h + Y*0.3)
    j = {k: [round(v[0], 2), round(v[1], 2)] for k, v in j.items()}
    j['handF'] = 'fist' if P['curlR'] > 0.6 else 'open'
    j['handB'] = 'fist' if P['curlL'] > 0.6 else 'open'
    j['face'] = P.get('face', 'neutral')
    return j

def build_all(names=None):
    bpy.context.scene.render.fps = 60
    baked = {}
    for name, spec in A.items():
        if names and name not in names: continue
        act, frames = build_action(name, spec['keys'], spec['length'], spec.get('loop', False))
        out = []
        for fr, P in enumerate(frames):
            bpy.context.scene.frame_set(fr)
            pose_apply(P)
            out.append(bake_frame(P))
        baked[name] = {'loop': bool(spec.get('loop')), 'frames': out}
    with open(OUTDIR + 'baked2d.json', 'w') as f: json.dump(baked, f)
    return baked

def export_glb(path=OUTDIR + 'simeon.glb'):
    sc = bpy.context.scene
    bpy.ops.object.mode_set(mode='OBJECT') if bpy.context.object and bpy.context.object.mode != 'OBJECT' else None
    bpy.ops.object.select_all(action='DESELECT')
    RIG.select_set(True)
    for o in sc.objects:
        if o.type == 'MESH' and o.parent == RIG: o.select_set(True)
    bpy.context.view_layer.objects.active = RIG
    RIG.animation_data.action = None
    pose_apply(make())
    bpy.ops.export_scene.gltf(
        filepath=path, export_format='GLB', use_selection=True,
        export_animation_mode='ACTIONS', export_force_sampling=True, export_frame_step=1,
        export_skins=True, export_morph=False, export_yup=True, export_apply=False,
        export_texcoords=False, export_normals=True, export_materials='EXPORT',
        export_def_bones=False, export_optimize_animation_size=True, export_anim_single_armature=True)
    return path
