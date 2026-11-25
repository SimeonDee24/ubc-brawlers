# Specials, grabs and throws. exec() after anims_attacks.py.
import math

# ---------------------------------------------------------------- Jump Shot (neutral special)
BALLP = dict(props=('ball',))
JS_G = P(STANCE, pos=(0, -0.12), hips=(10, -24, 0), chest=(6, -8, 0), face='focus', handR=(0.32, -0.18, -0.02), hdirR=(1, 0.1, 0), hbackR=(0, -1, 0),
         curlR=0.25, thumbR=0.2, handL=(0.3, -0.14, -0.2), hdirL=(0.6, 0, -0.8), hbackL=(0, 0, -1), curlL=0.2, **BALLP)
JS_SET = P(JS_G, pos=(0, -0.14), hips=(6, -26, 0), chest=(0, -10, 0), head=(-14, 16, 0), handR=(0.12, 0.42, -0.06), hdirR=(0.3, 1, 0), hbackR=(-1, 0, 0),
           handL=(0.14, 0.36, -0.2), hdirL=(0.2, 1, -0.4))
JS_RISE = P(JS_SET, pos=(0, 0.0), footR=('w', 0.17, 0.14, 0.09), footL=('w', -0.16, 0.15, 0.14), fpR=-30, fpL=-35, toeR=30, toeL=35)
JS_REL = P(JS_RISE, props=(), face='smile', handR=(0.18, 0.46, -0.08), hdirR=(1, -0.3, 0), hbackR=(0, 1, 0), curlR=0.3, handL=(0.2, 0.28, -0.1))
A['jumpShot'] = dict(length=38, keys=[(0, STANCE), (3, JS_G), (6, JS_SET), (11, JS_RISE), (13, P(JS_RISE, handR=(0.2, 0.46, -0.06))),
                                      (14, JS_REL, 'snap'), (22, JS_REL), (32, P(STANCE, pos=(0, -0.08))), (38, STANCE)])

# ---------------------------------------------------------------- Combo Breaker: a game controller swung by its cord
CTRL = dict(props=('controller',), curlR=1, thumbR=0.9)
def swing_pose(theta, lean, drop, face='yell'):
    f, u = d2(theta)
    return P(STANCE, pos=(0.04, -0.06 - drop*0.04), hips=(lean, -30, 0), chest=(lean*0.6, -12, 0), head=(-lean*0.5, 18, 0), face=face,
             handR=(f*0.5, u*0.5, -0.04), hdirR=(f, u, 0.0), hbackR=(0, 0, 1), poleR=(-u, f, 0.4), **CTRL)
SWINGS = {  # front-arm angle from, to; body lean; hip drop
    'combo1': (150, 40, 10, 0), 'combo2': (30, 140, -6, 0), 'combo2Up': (50, 165, -8, 0), 'combo2Down': (120, -10, 24, 4),
    'combo3': (160, 50, 12, 0), 'combo3Up': (0, 165, -16, 0), 'combo3Down': (110, -20, 26, 5),
    'combo4': (200, 70, 18, 1), 'combo4Up': (-10, 175, -20, 0), 'combo4Down': (100, 60, 30, 6),
}
for name, (a0, a1, lean, drop) in SWINGS.items():
    W = swing_pose(a0, -lean*0.5, drop, 'focus'); M = swing_pose((a0 + a1)/2, lean*0.4, drop); E = swing_pose(a1, lean, drop)
    if name == 'combo4Down':
        # three quick jabs at their feet, then a last one that launches
        J0 = swing_pose(100, lean, drop); J1 = swing_pose(60, lean, drop)
        keys = [(0, STANCE), (3, J0), (5, J1, 'snap'), (7, J0), (8, J1, 'snap'), (10, J0), (11, J1, 'snap'), (13, J0), (14, swing_pose(78, lean, drop), 'snap'),
                (24, swing_pose(70, lean, drop)), (32, P(STANCE, props=('controller',))), (40, STANCE)]
        A[name] = dict(length=40, keys=keys); continue
    L = 38 if name.startswith('combo4') else 30
    A[name] = dict(length=L, keys=[(0, P(STANCE, **CTRL)), (3, W), (4, M, 'lin'), (6, E, 'snap'), (14, P(E, pos=(0.04, -0.07))),
                                   (L - 6, P(STANCE, **CTRL)), (L, P(STANCE, **CTRL))])

# ---------------------------------------------------------------- Alley-Oop (up special): rising kicks, then a spinning side kick
AO_A = P(AIR, face='yell', hips=(-10, -20, 0), chest=(-8, -8, 0), head=(-10, 14, 0), footR=('b', 0.45, 0.05, 0.08), fpR=10, kneeR=(0, 1, 0.1),
         footL=('b', -0.06, -0.78, 0.12), handR=(-0.15, 0.3, 0.3), handL=(-0.2, -0.1, 0.32), **FIST)
AO_B = P(AO_A, footR=('b', 0.25, -0.45, 0.08), kneeR=(1, 1, 0.1), footL=('b', 0.3, -0.25, 0.12), kneeL=(1, 1, 0.1))
AO_F = P(AIR, face='yell', hips=(-24, -20, 0), chest=(-14, -10, 0), head=(0, 20, 0), footR=('b', 0.8, -0.1, 0.06), fpR=0, kneeR=(0, 1, 0.1),
         footL=('b', 0.1, -0.7, 0.12), handR=(-0.2, 0.1, 0.35), handL=(-0.3, 0.1, 0.3), **FIST)
ao_keys = [(0, STANCE), (4, P(CROUCH, pos=(0, -0.3)))]
for i in range(6): ao_keys.append((7 + i*3, AO_A if i % 2 == 0 else AO_B, 'snap'))
ao_keys += [(21, P(AO_F, yaw=-180), 'lin'), (23, P(AO_F, yaw=-360), 'out'), (26, P(AO_F, yaw=-360)), (34, P(AO_F, yaw=-360)), (42, P(HELP, yaw=-360)), (46, P(HELP, yaw=-360))]
A['alleyOop'] = dict(length=46, keys=ao_keys)

# ---------------------------------------------------------------- Bluff (down special): a playing card held up, daring them
CARD = dict(props=('card',), curlR=0.55, thumbR=0.9)
BL = P(STANCE, pos=(0, -0.04), hips=(0, -30, 0), chest=(-4, -14, 0), head=(-6, 22, 4), face='smile', handR=(0.26, 0.2, -0.16), hdirR=(0.3, 1, 0),
       hbackR=(1, 0, 0.2), poleR=(-0.3, -1, 0.7), handL=(-0.02, -0.32, 0.12), hdirL=(-0.2, -1, 0.3), hbackL=(0, 0, 1), curlL=0.6, **CARD)
A['bluff'] = dict(length=46, keys=[(0, STANCE), (4, P(BL, handR=(0.3, 0.0, -0.12))), (10, BL, 'out'), (34, P(BL, head=(-4, 22, 6))),
                                   (40, P(STANCE, props=('card',))), (46, STANCE)])
BH_W = P(BL, hips=(-6, -50, 0), chest=(-8, -20, 0), face='yell', handR=(-0.15, 0.25, 0.1), hdirR=(-0.6, 0.6, 0))
BH_H = P(BL, pos=(0.08, -0.06), hips=(10, 10, 0), chest=(8, 20, 0), face='yell', handR=(0.55, 0.0, -0.1), hdirR=(1, 0, 0), hbackR=(0, 1, 0))
A['bluffHit'] = dict(length=30, keys=[(0, BL), (2, BH_W), (4, BH_H, 'snap'), (8, P(BH_H, handR=(0.45, -0.2, -0.1))), (20, P(STANCE, props=('card',), face='smile')), (30, STANCE)])

# ---------------------------------------------------------------- grabs
GR_R = P(STANCE, pos=(0.06, -0.08), hips=(12, -10, 0), chest=(10, 0, 0), face='focus', handR=(0.5, -0.12, -0.12), handL=(0.52, -0.1, -0.24),
         hdirR=(1, 0, 0), hbackR=(0, 0.4, 1), hdirL=(1, 0, 0), hbackL=(0, 0.4, 1), **OPEN)
GR_C = P(GR_R, handR=(0.46, -0.14, -0.12), handL=(0.48, -0.12, -0.24), **dict(curlR=0.6, curlL=0.6))
A['grab'] = dict(length=34, keys=[(0, STANCE), (4, P(GR_R, handR=(0.3, -0.12, -0.05), handL=(0.32, -0.1, -0.15))), (6, GR_R, 'snap'), (9, GR_C), (24, P(STANCE, pos=(0, -0.07))), (34, STANCE)])
A['dashGrab'] = dict(length=42, keys=[(0, R0), (6, P(GR_R, pos=(0.1, -0.14), hips=(24, -10, 0), handR=(0.3, -0.12, -0.05), handL=(0.32, -0.1, -0.15))),
                                      (9, P(GR_R, pos=(0.14, -0.15), hips=(26, -10, 0)), 'snap'), (12, P(GR_C, pos=(0.14, -0.15))), (30, P(STANCE, pos=(0.1, -0.1))), (42, STANCE)])
A['pivotGrab'] = dict(length=38, keys=[(0, P(STANCE, yaw=180)), (6, P(STANCE, yaw=60)), (8, P(GR_R, handR=(0.3, -0.12, -0.05), handL=(0.32, -0.1, -0.15))),
                                       (10, GR_R, 'snap'), (13, GR_C), (28, P(STANCE, pos=(0, -0.07))), (38, STANCE)])
HOLD = P(GR_C, pos=(0.02, -0.09), handR=(0.44, -0.16, -0.12), handL=(0.46, -0.14, -0.22), curlR=0.8, curlL=0.8, face='smile')
A['holding'] = dict(loop=True, length=48, keys=[(0, HOLD), (24, P(HOLD, pos=(0.02, -0.1), chest=(12, 0, 0)))])
A['pummel'] = dict(length=13, keys=[(0, HOLD), (3, P(HOLD, footR=('b', 0.35, -0.4, 0.08), kneeR=(1, 1, 0.1))),
                                    (4, P(HOLD, face='yell', footR=('b', 0.4, -0.3, 0.08), kneeR=(1, 1, 0.1), fpR=-40), 'snap'), (13, HOLD)])
GRABBED = P(HURT, pos=(0, -0.02), rot=0, hips=(-12, 10, 0), handR=(0.15, 0.1, 0.25), handL=(-0.2, -0.05, 0.3), footR=('w', 0.08, 0.13, 0.1), footL=('w', -0.08, 0.15, 0.12))
A['grabbed'] = dict(loop=True, length=20, keys=[(0, GRABBED), (10, P(GRABBED, hips=(-16, 14, 0), handR=(0.2, 0.18, 0.28)))])

# ---------------------------------------------------------------- throws
FT_B = P(HOLD, pos=(-0.06, -0.1), hips=(-10, -20, 0), chest=(-8, -10, 0), handR=(0.3, -0.05, -0.12), handL=(0.32, -0.02, -0.22))
FT_H = P(GR_R, pos=(0.12, -0.08), hips=(24, 0, 0), chest=(16, 6, 0), face='yell', handR=(0.55, 0.05, -0.1), handL=(0.56, 0.08, -0.2),
         footL=('w', -0.12, 0.14, 0.14), fpL=-30, toeL=30)
A['fthrow'] = dict(length=32, keys=[(0, HOLD), (5, FT_B), (10, FT_H, 'snap'), (19, P(FT_H, face='smile')), (32, STANCE)])
# back throw: one and a half turns, staying smooth through the game's facing flips on frames 8, 16 and 24
SPIN = P(HOLD, pos=(0, -0.1), hips=(-8, 0, 0), chest=(-8, 0, 0), face='yell', handR=(0.5, 0.0, -0.1), handL=(0.5, 0.02, -0.2))
def bt_yaw(t):
    if t <= 8: return 90*(t/8)**1.5
    if t <= 16: return 90 - 180*(t - 8)/8
    if t <= 24: return -90 + 180*(t - 16)/8
    return 90 - 180*min(1, (t - 24)/8)
bt = [(0, P(SPIN, yaw=0))]
for t in range(2, 33, 2): bt.append((t, P(SPIN, yaw=bt_yaw(t)), 'lin'))
bt += [(34, P(GR_R, yaw=-90, face='yell', handR=(0.5, 0.15, -0.1), handL=(0.5, 0.2, -0.2))), (42, P(STANCE, yaw=-30)), (51, STANCE)]
A['bthrow'] = dict(length=51, keys=bt)
UT_L = P(SQUAT, pos=(0, -0.22), handR=(0.32, -0.2, -0.1), handL=(0.34, -0.18, -0.2), face='focus')
UT_T = P(JUMP_UP, pos=(0, 0.04), face='yell', handR=(0.08, 0.55, -0.1), handL=(0.1, 0.55, -0.2), hdirR=(0, 1, 0), hdirL=(0, 1, 0), **OPEN,
         footR=('w', 0.17, 0.15, 0.09), footL=('w', -0.16, 0.16, 0.14), fpR=-30, fpL=-30)
A['uthrow'] = dict(length=31, keys=[(0, HOLD), (5, UT_L), (11, UT_T, 'snap'), (20, UT_T), (31, STANCE)])
DT_U = P(UT_T, pos=(0, -0.02), handR=(0.15, 0.5, -0.1), handL=(0.17, 0.5, -0.2), **FIST)
DT_S = P(CROUCH, pos=(0.06, -0.42), hips=(40, -10, 0), chest=(14, 0, 0), face='yell', handR=(0.6, -0.3, -0.12), handL=(0.6, -0.28, -0.22),
         hdirR=(1, -0.6, 0), hdirL=(1, -0.6, 0), **FIST)
A['dthrow'] = dict(length=33, keys=[(0, HOLD), (6, DT_U), (11, DT_S, 'in'), (25, P(DT_S, pos=(0.06, -0.38))), (33, STANCE)])
