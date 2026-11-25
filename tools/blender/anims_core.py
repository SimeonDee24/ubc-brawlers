# Movement, ledge, defence, hurt and getup animations. exec() after poselib.py.
# Hand targets: (forward, up, outward) from the shoulder joint, in the body frame.
# Feet: ('w', forward, ankle height, outward) on the ground (follows pos), or ('b', forward, up, outward) from the hip joint.
# R = near the camera = the game's "front" limbs (F); L = far side = "back" limbs (B).
A = {}

def P(base, **kw):
    q = dict(base)
    face = kw.pop('face', None)
    if face: q.update(FACES[face]); q['face'] = face
    q.update(kw)
    return q

def SWAP(p):
    """mirror the limbs (left <-> right)"""
    q = dict(p)
    for a, b in (('handR', 'handL'), ('poleR', 'poleL'), ('hdirR', 'hdirL'), ('hbackR', 'hbackL'), ('curlR', 'curlL'),
                 ('thumbR', 'thumbL'), ('footR', 'footL'), ('kneeR', 'kneeL'), ('fpR', 'fpL'), ('toeR', 'toeL')):
        q[a], q[b] = p[b], p[a]
    return q

FIST = dict(curlR=0.95, curlL=0.95, thumbR=0.9, thumbL=0.9)
LOOSE = dict(curlR=0.55, curlL=0.55, thumbR=0.5, thumbL=0.5)
OPEN = dict(curlR=0.12, curlL=0.12, thumbR=0.1, thumbL=0.1)

# ---------------------------------------------------------------- stance
STANCE = make(
    pos=(0.0, -0.055), hips=(6, -26, 0), spine=(4, -6, 0), chest=(5, -8, 0), neck=(-4, 12, 0), head=(-5, 14, 0),
    handR=(0.3, -0.17, -0.1), poleR=(-0.2, -1.0, 0.7), hdirR=(0.6, 0.75, -0.1), hbackR=(0.1, -0.2, 1.0),
    handL=(0.2, -0.2, -0.17), poleL=(-0.2, -1.0, 0.6), hdirL=(0.55, 0.8, -0.2), hbackL=(0.2, -0.2, 1.0),
    footR=('w', 0.17, 0.095, 0.09), footL=('w', -0.16, 0.095, 0.14), kneeR=(1, 0, 0.3), kneeL=(1, 0, 0.35), fpL=0, toeL=0,
    face='smile', **FIST)
STAND = STANCE

A['idle'] = dict(loop=True, length=80, keys=[
    (0, STANCE),
    (40, P(STANCE, pos=(0.0, -0.068), chest=(7, -9, 0), head=(-3, 15, 0), handR=(0.3, -0.19, -0.1), handL=(0.2, -0.22, -0.17))),
])

# ---------------------------------------------------------------- walk (22-frame cycle, feet slide at the walk speed)
WALK = make(pos=(0, -0.02), hips=(3, 0, 0), spine=(3, 0, 0), chest=(2, 0, 0), neck=(-2, 0, 0), head=(-2, 4, 0),
            poleR=(-0.6, -0.5, 0.6), poleL=(-0.6, -0.5, 0.6), hdirR=(0.2, -1, 0.1), hdirL=(0.2, -1, 0.1), face='smile', **LOOSE)
W0 = P(WALK, pos=(0, -0.035), hips=(3, 8, 0), chest=(2, -14, 0),
       footR=('w', 0.36, 0.095, 0.1), footL=('w', -0.36, 0.12, 0.1), fpL=-28, toeL=28, fpR=10,
       handR=(-0.16, -0.48, 0.04), handL=(0.2, -0.45, 0.02), kneeR=(1, 0, 0.1), kneeL=(1, 0, 0.1))
W1 = P(WALK, pos=(0, 0.0), hips=(3, 0, 0), chest=(2, -4, 0),
       footR=('w', 0.0, 0.095, 0.1), footL=('w', 0.04, 0.22, 0.1), fpL=-10,
       handR=(0.0, -0.53, 0.06), handL=(0.04, -0.52, 0.05), kneeR=(1, 0, 0.1), kneeL=(1, 0, 0.1))
A['walk'] = dict(loop=True, length=22, keys=[(0, W0, 'lin'), (6, W1, 'lin'), (11, SWAP(P(W0, hips=(3, -8, 0), chest=(2, 6, 0))), 'lin'), (17, SWAP(W1), 'lin')])

# ---------------------------------------------------------------- run (20-frame cycle, leaning in, arms pumping)
RUN = make(pos=(0, -0.03), hips=(16, 0, 0), spine=(8, 0, 0), chest=(6, 0, 0), neck=(-10, 0, 0), head=(-12, 6, 0), face='focus', **FIST,
           poleR=(-1, -0.3, 0.3), poleL=(-1, -0.3, 0.3), hdirR=(0.6, 0.2, 0), hdirL=(0.6, 0.2, 0))
R0 = P(RUN, pos=(0, -0.07), hips=(16, 10, 0), chest=(6, -18, 0),
       footR=('w', 0.48, 0.1, 0.09), footL=('b', -0.42, -0.5, 0.09), fpL=-50, toeL=20, kneeL=(1, 0, 0.1),
       handR=(-0.22, -0.3, 0.0), handL=(0.32, -0.08, -0.06))
R1 = P(RUN, pos=(0, 0.02), hips=(16, 0, 0), chest=(6, -6, 0),
       footR=('w', -0.18, 0.13, 0.09), footL=('b', 0.32, -0.52, 0.09), fpR=-20, fpL=-25, kneeL=(1, 0, 0.1),
       handR=(0.02, -0.4, 0.04), handL=(0.06, -0.38, 0.02))
A['run'] = dict(loop=True, length=20, keys=[(0, R0, 'lin'), (5, R1, 'lin'), (10, SWAP(P(R0, hips=(16, -10, 0), chest=(6, 8, 0))), 'lin'), (15, SWAP(R1), 'lin')])

# brake / turnaround skid: heels dug in, leaning back
BR = make(pos=(-0.05, -0.12), hips=(-10, -20, 0), spine=(-6, 0, 0), chest=(-4, -6, 0), neck=(6, 8, 0), head=(4, 8, 0), face='focus',
          footR=('w', 0.32, 0.1, 0.1), footL=('w', -0.12, 0.095, 0.13), fpR=22, kneeR=(1, 0, 0.2), kneeL=(1, 0, 0.3),
          handR=(0.22, -0.3, 0.1), handL=(-0.2, -0.2, 0.15), poleR=(-0.5, -0.6, 0.6), poleL=(-0.2, -0.6, 0.8),
          hdirR=(0.5, -0.6, 0.3), hdirL=(-0.4, -0.6, 0.3), **LOOSE)
A['brake'] = dict(length=16, keys=[(0, P(R1, pos=(0, -0.04))), (4, BR, 'out'), (16, P(BR, pos=(-0.04, -0.1), hips=(-6, -20, 0)))])

# ---------------------------------------------------------------- crouch / crawl
CROUCH = make(pos=(0.0, -0.4), hips=(34, -24, 0), spine=(10, -4, 0), chest=(6, -6, 0), neck=(-22, 10, 0), head=(-18, 12, 0), face='focus',
              footR=('w', 0.18, 0.1, 0.16), footL=('w', -0.2, 0.11, 0.17), fpL=-22, toeL=24, kneeR=(1, 0.2, 0.4), kneeL=(1, -0.6, 0.5),
              handR=(0.3, -0.28, 0.0), handL=(0.24, -0.3, -0.08), poleR=(-0.3, -1, 0.5), poleL=(-0.3, -1, 0.5),
              hdirR=(0.7, 0.4, 0), hdirL=(0.7, 0.4, 0), **FIST)
A['crouch'] = dict(length=5, keys=[(0, STANCE), (2, P(CROUCH, pos=(0, -0.2), hips=(18, -24, 0)), 'in'), (5, CROUCH, 'out')])
CR0 = P(CROUCH, footR=('w', 0.32, 0.1, 0.16), footL=('w', -0.24, 0.11, 0.17), handR=(0.36, -0.3, 0.0), handL=(0.18, -0.3, -0.08))
CR1 = P(CROUCH, pos=(0, -0.38), footR=('w', 0.0, 0.16, 0.16), footL=('w', 0.04, 0.11, 0.17), handR=(0.22, -0.3, 0.0), handL=(0.32, -0.3, -0.08))
A['crawl'] = dict(loop=True, length=32, keys=[(0, CR0, 'lin'), (16, CR1, 'lin')])

# ---------------------------------------------------------------- jumps
SQUAT = P(STANCE, pos=(0, -0.2), hips=(20, -24, 0), chest=(8, -6, 0), head=(-10, 14, 0),
          handR=(0.1, -0.38, 0.05), handL=(-0.05, -0.38, 0.0), poleR=(-0.8, -0.3, 0.6), poleL=(-0.8, -0.3, 0.6), **LOOSE)
A['jumpsquat'] = dict(length=3, keys=[(0, STANCE), (3, SQUAT, 'out')])
AIR = make(pos=(0, 0.0), hips=(4, -18, 0), spine=(4, -4, 0), chest=(2, -6, 0), neck=(-2, 10, 0), head=(-4, 12, 0), face='smile',
           footR=('b', 0.16, -0.66, 0.11), footL=('b', -0.14, -0.74, 0.12), kneeR=(1, 0.4, 0.2), kneeL=(1, -0.2, 0.2), fpR=-25, fpL=-35,
           handR=(0.22, -0.2, 0.18), handL=(-0.2, -0.26, 0.22), poleR=(-0.4, -0.8, 0.6), poleL=(0.2, -0.8, 0.6),
           hdirR=(0.6, -0.4, 0.3), hdirL=(-0.3, -0.6, 0.4), **LOOSE)
JUMP_UP = P(AIR, hips=(-2, -18, 0), chest=(-4, -8, 0), head=(-10, 12, 0),
            footR=('b', 0.05, -0.8, 0.1), footL=('b', -0.08, -0.8, 0.12), fpR=-45, fpL=-50,
            handR=(0.18, 0.35, 0.12), handL=(-0.15, -0.35, 0.2), hdirR=(0.2, 1, 0), poleR=(0.4, -0.6, 0.7))
A['jump'] = dict(length=14, keys=[(0, SQUAT), (3, JUMP_UP, 'out'), (14, AIR)])
TUCK = P(AIR, hips=(30, -10, 0), spine=(14, 0, 0), chest=(10, 0, 0), head=(-12, 10, 0), face='focus',
         footR=('b', 0.34, -0.26, 0.1), footL=('b', 0.3, -0.32, 0.12), fpR=-30, fpL=-30, kneeR=(1, 1, 0.2), kneeL=(1, 1, 0.2),
         handR=(0.32, -0.42, 0.0), handL=(0.3, -0.42, 0.06), poleR=(-0.3, -0.5, 1), poleL=(-0.3, -0.5, 1), **FIST)
A['djump'] = dict(length=22, keys=[(0, P(AIR, hips=(10, -16, 0))), (3, P(TUCK, rot=60)), (8, P(TUCK, rot=200), 'lin'), (13, P(TUCK, rot=330), 'lin'),
                                   (17, P(AIR, rot=360, hips=(10, -16, 0)), 'out'), (22, P(AIR, rot=360))])
FALL = P(AIR, handR=(0.18, 0.02, 0.22), handL=(-0.12, -0.05, 0.26), hdirR=(0.4, 0.3, 0.6), hdirL=(-0.2, 0.3, 0.7),
         footR=('b', 0.12, -0.7, 0.12), footL=('b', -0.18, -0.68, 0.13), face='neutral')
A['fall'] = dict(loop=True, length=28, keys=[(0, FALL), (14, P(FALL, handR=(0.2, 0.08, 0.24), handL=(-0.14, 0.0, 0.28), footR=('b', 0.16, -0.68, 0.12)))])
LANDP = P(STANCE, pos=(0, -0.26), hips=(22, -24, 0), chest=(10, -6, 0), head=(-12, 14, 0), handR=(0.2, -0.4, 0.15), handL=(0.0, -0.4, 0.18),
          poleR=(-0.6, -0.4, 0.7), poleL=(-0.6, -0.4, 0.7), **LOOSE)
A['land'] = dict(length=8, keys=[(0, LANDP), (2, P(LANDP, pos=(0, -0.28)), 'out'), (8, STANCE)])

# ---------------------------------------------------------------- ledge (hands on the ledge 44px above the feet)
HANG = make(pos=(0.0, 0.0), hips=(4, -6, 0), spine=(2, 0, 0), chest=(0, -4, 0), neck=(-14, 8, 0), head=(-14, 10, 0), face='focus',
            handR=(0.2, 0.5, -0.04), handL=(0.2, 0.5, -0.12), poleR=(0.3, -0.2, 1), poleL=(0.3, -0.2, 1), hdirR=(0.6, 0.8, 0), hdirL=(0.6, 0.8, 0),
            hbackR=(0, 1, 0.2), hbackL=(0, 1, 0.2), footR=('b', 0.1, -0.8, 0.1), footL=('b', -0.06, -0.82, 0.12), fpR=-40, fpL=-40,
            curlR=0.7, curlL=0.7, thumbR=0.6, thumbL=0.6)
A['ledge'] = dict(loop=True, length=60, keys=[(0, HANG), (30, P(HANG, footR=('b', 0.14, -0.78, 0.1), footL=('b', -0.02, -0.8, 0.12), head=(-12, 12, 0)))])
CLIMB1 = P(HANG, pos=(0.05, 0.25), hips=(40, -10, 0), chest=(14, 0, 0), handR=(0.25, 0.25, -0.04), handL=(0.25, 0.25, -0.12),
           footR=('b', 0.4, -0.3, 0.1), footL=('b', 0.05, -0.6, 0.12), kneeR=(1, 1, 0.1))
CLIMB2 = P(STANCE, pos=(0.05, -0.3), hips=(30, -20, 0), chest=(10, -6, 0), handR=(0.3, -0.35, 0.05), handL=(0.2, -0.38, 0.0), **LOOSE)
A['ledgeGetup'] = dict(length=23, keys=[(0, HANG), (8, CLIMB1), (15, CLIMB2, 'out'), (23, STANCE)])
BALL = make(pos=(0, -0.5), hips=(60, -10, 0), spine=(20, 0, 0), chest=(16, 0, 0), neck=(-6, 0, 0), head=(-10, 0, 0), face='focus',
            footR=('b', 0.36, -0.22, 0.1), footL=('b', 0.3, -0.26, 0.12), kneeR=(1, 1, 0.1), kneeL=(1, 1, 0.1), fpR=-20, fpL=-20,
            handR=(0.32, -0.42, -0.04), handL=(0.28, -0.42, 0.0), poleR=(-0.3, -0.6, 1), poleL=(-0.3, -0.6, 1), **FIST)
A['ledgeRoll'] = dict(length=37, keys=[(0, HANG), (6, CLIMB1), (11, P(BALL, rot=60)), (18, P(BALL, rot=200), 'lin'), (25, P(BALL, rot=340), 'lin'),
                                       (31, P(CROUCH, rot=360)), (37, P(STANCE, rot=360))])
LKICK = P(CROUCH, pos=(0.05, -0.32), hips=(-10, -10, 0), chest=(-6, 0, 0), face='yell', footR=('b', 0.72, -0.25, 0.1), fpR=10, kneeR=(0, 1, 0.1),
          handR=(-0.2, -0.4, 0.2), handL=(-0.25, -0.45, 0.1))
A['ledgeAttack'] = dict(length=40, keys=[(0, HANG), (8, CLIMB1), (16, P(CROUCH, pos=(0.0, -0.35))), (19, P(LKICK, footR=('b', 0.3, -0.45, 0.1))),
                                         (22, LKICK, 'snap'), (26, LKICK), (34, P(CROUCH, pos=(0.0, -0.3))), (40, STANCE)])

# ---------------------------------------------------------------- shield and dodges
SHIELD = P(STANCE, pos=(0, -0.12), hips=(10, -20, 0), chest=(8, -6, 0), head=(-10, 12, 0), face='focus',
           handR=(0.2, 0.0, -0.18), handL=(0.18, -0.05, -0.08), poleR=(-0.2, -1, 0.6), poleL=(-0.2, -1, 0.5), hdirR=(0.2, 1, 0), hdirL=(0.2, 1, 0))
A['shield'] = dict(length=4, keys=[(0, STANCE), (4, SHIELD, 'out')])
A['roll'] = dict(length=31, keys=[(0, STANCE), (3, P(CROUCH, pos=(0, -0.3))), (7, P(BALL, pos=(0, -0.55), rot=0)), (13, P(BALL, pos=(0, -0.56))),
                                  (19, P(BALL, pos=(0, -0.55))), (25, P(CROUCH, pos=(0, -0.32))), (31, STANCE)])
SIDESTEP = P(STANCE, pos=(-0.08, -0.08), hips=(-16, -40, 0), chest=(-10, -10, 0), head=(-6, 20, 0), face='neutral',
             footR=('w', 0.12, 0.095, 0.12), footL=('w', -0.24, 0.12, 0.2), handR=(-0.05, -0.3, 0.2), handL=(-0.2, -0.3, 0.2),
             poleR=(-0.4, -0.6, 0.6), poleL=(-0.4, -0.6, 0.6), hdirR=(-0.1, -1, 0.2), hdirL=(-0.1, -1, 0.2), **LOOSE)
A['spotDodge'] = dict(length=27, keys=[(0, STANCE), (3, SIDESTEP, 'out'), (16, P(SIDESTEP, pos=(-0.1, -0.1))), (22, P(STANCE, pos=(0, -0.08))), (27, STANCE)])
A['airDodge'] = dict(length=42, keys=[(0, AIR), (3, P(TUCK, rot=10)), (27, P(TUCK, rot=16, hips=(34, -10, 0))), (37, AIR), (42, FALL)])

# ---------------------------------------------------------------- hurt, tumble, dizzy
HURT = make(pos=(-0.03, 0.0), hips=(-9, 10, 0), spine=(-8, 0, 0), chest=(-8, 8, 0), neck=(-4, 0, 0), head=(-14, 6, 4), face='hurt',
            handR=(0.42, 0.26, 0.2), handL=(-0.42, 0.3, 0.2), poleR=(-0.5, 0, 1), poleL=(-0.5, -0.5, 1),
            hdirR=(0.6, 0.8, 0.3), hdirL=(-0.6, 0.6, 0.4), footR=('b', 0.36, -0.68, 0.1), footL=('b', -0.06, -0.74, 0.12), fpR=-10, fpL=-30, **OPEN)
A['hurt'] = dict(loop=True, length=12, keys=[(0, HURT), (6, P(HURT, chest=(-12, 10, 0), head=(-18, 6, 6), handR=(0.4, 0.32, 0.22), handL=(-0.38, 0.36, 0.22)))])
TUMB = P(HURT, rot=-50, hips=(-10, 0, 0), handR=(-0.1, 0.35, 0.3), handL=(-0.2, 0.3, 0.3), footR=('b', 0.4, -0.5, 0.12), footL=('b', 0.1, -0.7, 0.12))
A['tumble'] = dict(loop=True, length=28, keys=[(0, P(TUMB, rot=-18)), (14, P(TUMB, rot=-42, handR=(0.1, 0.3, 0.32), handL=(-0.3, 0.2, 0.3), footR=('b', 0.5, -0.4, 0.12), footL=('b', 0.0, -0.75, 0.12)))])
DIZZY = P(STANCE, pos=(0, -0.08), hips=(-4, -20, 6), chest=(-6, -4, 6), head=(-10, 14, 14), face='hurt',
          handR=(0.05, -0.45, 0.12), handL=(-0.05, -0.47, 0.14), poleR=(-0.4, -0.3, 1), poleL=(-0.4, -0.3, 1), hdirR=(0, -1, 0.2), hdirL=(0, -1, 0.2), **OPEN)
A['dizzy'] = dict(loop=True, length=48, keys=[(0, DIZZY), (24, P(DIZZY, hips=(-4, -20, -6), chest=(-6, -4, -6), head=(-10, 14, -14)))])
HELP = P(FALL, face='hurt', handR=(0.1, 0.35, 0.25), handL=(-0.15, 0.3, 0.3), hdirR=(0.2, 1, 0.3), hdirL=(-0.2, 1, 0.3), **OPEN)
A['helpless'] = dict(loop=True, length=16, keys=[(0, HELP), (8, P(HELP, handR=(0.15, 0.25, 0.32), handL=(-0.05, 0.4, 0.25), footR=('b', 0.2, -0.6, 0.12)))])

# ---------------------------------------------------------------- knockdown and getups (lying on his back)
LIE = make(pos=(-0.25, -0.86), rot=-88, hips=(0, 0, 0), spine=(-2, 0, 0), chest=(-2, 0, 0), neck=(-6, 20, 0), head=(-10, 24, 0), face='hurt',
           handR=(0.12, -0.36, 0.12), handL=(0.12, -0.36, 0.18), poleR=(0, 0, 1), poleL=(0, 0, 1), hdirR=(0.3, -1, 0.1), hdirL=(0.3, -1, 0.1),
           footR=('b', 0.1, -0.8, 0.12), footL=('b', 0.05, -0.8, 0.16), fpR=60, fpL=55, kneeR=(1, 0, 0.3), kneeL=(1, 0, 0.3), **OPEN)
A['lie'] = dict(length=6, keys=[(0, P(LIE, pos=(-0.2, -0.75), rot=-70)), (6, LIE, 'out')])
SIT = P(CROUCH, pos=(-0.05, -0.45), hips=(40, -16, 0), chest=(10, -6, 0), handR=(0.1, -0.5, 0.1), handL=(-0.15, -0.5, 0.15), face='focus')
A['getupStand'] = dict(length=26, keys=[(0, LIE), (8, LIE), (16, P(LIE, rot=-30, pos=(-0.1, -0.55), hips=(30, 0, 0), footR=('b', 0.4, -0.4, 0.12), footL=('b', 0.35, -0.45, 0.15))),
                                        (21, SIT), (26, STANCE)])
A['getupRoll'] = dict(length=27, keys=[(0, LIE), (4, LIE), (9, P(SIT, pos=(-0.05, -0.5))), (13, P(BALL, pos=(0, -0.56))), (19, P(BALL, pos=(0, -0.57))), (24, P(CROUCH, pos=(0, -0.35))), (27, STANCE)])
GUA1 = P(CROUCH, pos=(0.0, -0.56), hips=(10, 0, 0), chest=(4, 0, 0), face='yell', footR=('b', 0.8, -0.32, 0.1), fpR=10, kneeR=(0, 1, 0.1),
         footL=('w', -0.1, 0.12, 0.18), handR=(-0.15, -0.45, 0.25), handL=(-0.05, -0.5, 0.2), hdirR=(0, -1, 0.2), hdirL=(0, -1, 0.2))
A['getupAttack'] = dict(length=40, keys=[(0, LIE), (10, LIE), (15, P(SIT, pos=(-0.05, -0.55))), (18, GUA1, 'snap'), (19, GUA1),
                                         (22, P(GUA1, yaw=-180), 'lin'), (24, P(GUA1, yaw=-180)), (28, P(GUA1, yaw=-360), 'lin'), (34, P(CROUCH, pos=(0, -0.3))), (40, STANCE)])
