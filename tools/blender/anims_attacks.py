# Normals, aerials and smashes. exec() after anims_core.py.
import math

def d2(theta):
    """direction in the body's side plane from a 2D arm angle (0 = straight down, 90 = forward, 180 = up)"""
    t = math.radians(theta)
    return (math.sin(t), -math.cos(t))

def ARM(theta, reach=0.5, out=-0.05):
    f, u = d2(theta)
    return (f*reach, u*reach, out)

def hand_for(prop_dir, knuckle_dir):
    """hand orientation so a held prop points along prop_dir (grip X) with the knuckles along knuckle_dir"""
    b = Vector(prop_dir).normalized(); k = Vector(knuckle_dir).normalized()
    k = (k - b*k.dot(b)).normalized()
    back = b.cross(k)
    return tuple(k), tuple(back)

def GRIP(f, u, c, tw):
    """both hands together on one handle: point (f, u) in front, c = sideways (+ his left), tw = total chest twist (deg)"""
    s = math.sin(math.radians(tw)); co = math.cos(math.radians(tw))
    return dict(handR=(f - 0.2*s, u, -(c + 0.2*co)), handL=(f + 0.2*s, u + 0.05, c - 0.2*co))

# ---------------------------------------------------------------- jab combo
PUNCH_R = dict(hdirR=(1, 0.05, 0), hbackR=(0, 1, 0), curlR=1, thumbR=1)
PUNCH_L = dict(hdirL=(1, 0.05, 0), hbackL=(0, 1, 0), curlL=1, thumbL=1)
JAB1 = P(STANCE, pos=(0.08, -0.07), hips=(10, -18, 0), chest=(6, -4, 0), head=(-6, 12, 0), handR=(0.72, -0.04, -0.02), face='yell', **PUNCH_R)
A['jab1'] = dict(length=16, keys=[(0, STANCE), (1, P(STANCE, handR=(0.18, -0.14, -0.08))), (2, JAB1, 'snap'), (5, P(JAB1, handR=(0.66, -0.05, -0.03))),
                                  (10, P(STANCE, handR=(0.36, -0.12, -0.1)), 'io'), (16, STANCE)])
JAB2 = P(STANCE, pos=(0.1, -0.08), hips=(10, 4, 0), chest=(8, 14, 0), head=(-6, -4, 0), handL=(0.74, -0.03, -0.2),
         handR=(0.16, -0.12, -0.1), footL=('w', -0.12, 0.11, 0.14), fpL=-20, toeL=25, face='yell', **PUNCH_L)
A['jab2'] = dict(length=18, keys=[(0, P(JAB1, handR=(0.36, -0.1, -0.12))), (2, JAB2, 'snap'), (5, JAB2), (11, P(STANCE, handL=(0.32, -0.14, -0.18)), 'io'), (18, STANCE)])
CHAMBER = P(STANCE, pos=(0.0, -0.02), hips=(-6, -30, 0), chest=(-6, -10, 0), footR=('b', 0.3, -0.42, 0.08), fpR=-20, kneeR=(1, 1, 0.1),
            handR=(0.1, -0.2, 0.05), handL=(-0.05, -0.25, 0.1))
KICK = P(CHAMBER, pos=(0.02, 0.0), hips=(-14, -32, 0), chest=(-10, -10, 0), head=(4, 18, 0), footR=('b', 0.76, -0.2, 0.06), fpR=20, kneeR=(0, 1, 0.2),
         footL=('w', -0.14, 0.095, 0.12), fpL=-12, toeL=14, handR=(-0.1, -0.32, 0.12), handL=(-0.2, -0.3, 0.15), face='yell')
A['jab3'] = dict(length=26, keys=[(0, JAB2), (2, CHAMBER), (3, KICK, 'snap'), (6, KICK), (11, CHAMBER), (19, P(STANCE, pos=(0.0, -0.08))), (26, STANCE)])

# ---------------------------------------------------------------- forward tilt: boxer's one-two, stepping in
GUARD = P(STANCE, pos=(0.0, -0.08), handR=(0.24, -0.1, -0.12), handL=(0.18, -0.12, -0.18))
FT_JAB = P(JAB1, pos=(0.12, -0.08), handR=(0.74, -0.03, -0.02), handL=(0.16, -0.1, -0.18))
FT_COIL = P(GUARD, pos=(0.1, -0.1), hips=(6, -34, 0), chest=(6, -16, 0), handR=(0.28, -0.1, -0.12), handL=(0.12, -0.1, -0.16))
FT_CROSS = P(JAB2, pos=(0.22, -0.1), hips=(16, 12, 0), chest=(12, 18, 0), head=(-8, -6, 0), handL=(0.78, -0.02, -0.22),
             footR=('w', 0.32, 0.095, 0.1), footL=('w', -0.04, 0.14, 0.14), fpL=-35, toeL=35)
A['ftilt'] = dict(length=24, keys=[(0, STANCE), (2, GUARD), (4, FT_JAB, 'snap'), (7, P(FT_JAB, handR=(0.3, -0.08, -0.12))), (9, FT_COIL),
                                   (11, FT_CROSS, 'snap'), (16, P(FT_CROSS, handL=(0.7, -0.03, -0.22))), (21, P(GUARD, pos=(0.14, -0.08))), (24, P(STANCE, pos=(0.14, -0.055)))])

# ---------------------------------------------------------------- up tilt: rising uppercut
UT_LOAD = P(STANCE, pos=(0.0, -0.2), hips=(18, -30, 0), chest=(10, -14, 0), handR=(0.2, -0.42, -0.02), poleR=(-0.6, -0.4, 0.7),
            hdirR=(0.3, 0.9, 0), hbackR=(1, 0, 0), face='focus')
UT_1 = P(UT_LOAD, pos=(0.02, -0.08), hips=(6, -30, 0), chest=(0, -14, 0), handR=(0.4, 0.0, -0.12), face='yell')
UT_2 = P(UT_1, pos=(0.02, 0.02), hips=(-8, -26, 0), chest=(-10, -12, 0), head=(-16, 16, 0), handR=(0.2, 0.42, -0.12), hdirR=(0, 1, 0), hbackR=(0, 0, 1),
         footL=('w', -0.16, 0.13, 0.14), fpL=-30, toeL=30, fpR=-15)
UT_3 = P(UT_2, handR=(0.06, 0.53, -0.08))
A['utilt'] = dict(length=23, keys=[(0, STANCE), (4, UT_LOAD), (6, UT_1, 'snap'), (8, UT_2), (11, UT_3), (15, UT_3), (23, STANCE)])

# ---------------------------------------------------------------- down tilt: low floor sweep around him
DT_BASE = make(pos=(0.0, -0.4), hips=(38, -10, 0), spine=(10, 0, 0), chest=(6, 0, 0), neck=(-22, 8, 0), head=(-20, 10, 0), face='yell',
               footL=('w', -0.05, 0.12, 0.18), fpL=-40, toeL=40, kneeL=(0.6, -1, 0.4),
               handL=(0.2, -0.55, 0.12), poleL=(-0.4, 0, 1), hdirL=(0.3, -1, 0.1), hbackL=(0, 0, 1), curlL=0.15,
               handR=(0.25, -0.35, 0.1), poleR=(-0.4, -0.6, 0.7), curlR=0.9, thumbR=0.9, kneeR=(0.3, 1, 0.3))
A['dtilt'] = dict(length=17, keys=[(0, STANCE), (2, P(DT_BASE, footR=('b', -0.2, -0.45, 0.2))),
    (3, P(DT_BASE, footR=('b', -0.62, -0.38, 0.12), fpR=30)), (4, P(DT_BASE, footR=('b', -0.4, -0.42, 0.4)), 'lin'),
    (5, P(DT_BASE, footR=('b', 0.1, -0.44, 0.45)), 'lin'), (6, P(DT_BASE, footR=('b', 0.5, -0.4, 0.3)), 'lin'),
    (7, P(DT_BASE, footR=('b', 0.68, -0.38, 0.12), fpR=10), 'lin'), (12, P(DT_BASE, footR=('b', 0.66, -0.38, 0.12), fpR=10)),
    (17, P(CROUCH, pos=(0, -0.42)))])

# ---------------------------------------------------------------- dash attack: a hopping double kick
DA_HOP = P(R1, pos=(0.0, 0.05), hips=(4, -20, 0), chest=(0, -10, 0), footR=('b', 0.3, -0.5, 0.1), footL=('b', -0.2, -0.62, 0.12))
DA_K1 = P(AIR, pos=(0.22, 0.02), hips=(-28, -24, 0), chest=(-12, -10, 0), head=(4, 16, 0), face='yell',
          footR=('b', 1.0, -0.12, 0.08), fpR=15, kneeR=(0, 1, 0.1), footL=('b', -0.25, -0.6, 0.12), handR=(-0.2, -0.2, 0.3), handL=(-0.25, 0.05, 0.3), **FIST)
DA_SW = P(DA_K1, footR=('b', 0.1, -0.7, 0.1), footL=('b', 0.2, -0.4, 0.12), hips=(-10, -10, 0))
DA_K2 = P(DA_K1, pos=(0.3, 0.12), hips=(-36, 10, 0), chest=(-16, 6, 0), head=(8, 4, 0), footL=('b', 1.0, 0.06, 0.1), fpL=20, kneeL=(0, 1, 0.1),
          footR=('b', -0.15, -0.7, 0.1), handR=(-0.15, 0.05, 0.32), handL=(-0.3, -0.25, 0.2))
A['dashAttack'] = dict(length=40, keys=[(0, R0), (3, DA_HOP), (6, DA_K1, 'snap'), (9, DA_K1), (12, DA_SW), (15, DA_K2, 'snap'), (21, DA_K2),
                                        (28, P(LANDP, pos=(0.08, -0.24))), (40, P(STANCE, pos=(0.08, -0.055)))])

# ---------------------------------------------------------------- aerials
# neutral air: tuck, then a full spin with the near leg straight out (out on frame 6)
N_T = P(TUCK, hips=(20, -10, 0))
N_K = P(AIR, hips=(-6, -10, 0), chest=(-4, -4, 0), face='yell', footR=('b', 0.76, -0.18, 0.06), fpR=10, kneeR=(0, 1, 0.1),
        footL=('b', -0.1, -0.5, 0.12), kneeL=(1, 0.5, 0.1), handR=(-0.2, -0.05, 0.35), handL=(-0.2, 0.05, 0.35), **FIST)
A['nair'] = dict(length=30, keys=[(0, AIR), (3, N_T), (6, P(N_K, yaw=0), 'snap'), (9, P(N_K, yaw=-120), 'lin'), (12, P(N_K, yaw=-240), 'lin'),
                                  (15, P(N_K, yaw=-360), 'lin'), (20, P(N_T, yaw=-400)), (30, P(AIR, yaw=-360))])
# forward air: Banjo-style haymaker, fist cocked behind the head, then a huge overhead arc
FA_WIND = P(AIR, rot=-14, hips=(-10, -30, 0), chest=(-12, -24, 0), head=(-6, 24, 0), face='yell',
            handR=(-0.32, 0.3, 0.08), poleR=(-0.2, -1, 0.6), hdirR=(-0.5, 0.8, 0), hbackR=(0, 0, 1),
            handL=(0.45, 0.05, -0.05), hdirL=(1, 0.2, 0), footR=('b', 0.4, -0.35, 0.1), kneeR=(1, 1, 0.1), **FIST)
FA_TOP = P(FA_WIND, rot=4, hips=(0, -10, 0), chest=(0, 0, 0), handR=(0.05, 0.55, -0.02), hdirR=(0.2, 1, 0))
FA_HIT = P(FA_WIND, rot=22, hips=(16, 0, 0), chest=(14, 10, 0), head=(-14, 4, 0), handR=(0.52, 0.12, -0.08), hdirR=(1, 0, 0), hbackR=(0, 1, 0),
           handL=(-0.3, -0.2, 0.2), footL=('b', -0.3, -0.55, 0.12))
FA_LOW = P(FA_HIT, rot=30, handR=(0.42, -0.36, -0.06), hdirR=(0.6, -1, 0))
A['fair'] = dict(length=51, keys=[(0, AIR), (5, P(FA_WIND, rot=-6)), (11, FA_WIND), (13, P(FA_WIND, rot=-18, handR=(-0.34, 0.26, 0.08))), (14, FA_WIND),
                                  (14, FA_TOP, 'lin'), (15, FA_HIT, 'lin'), (19, FA_LOW, 'out'), (31, P(FA_LOW, rot=20)), (51, AIR)])
# back air: three back kicks with the body laid out (high, low, then a strong mid kick)
BA_PRE = P(AIR, rot=20, hips=(20, -10, 0), footR=('b', 0.3, -0.4, 0.1), footL=('b', 0.25, -0.45, 0.12), kneeR=(1, 1, 0.1), kneeL=(1, 1, 0.1),
           head=(-10, 70, 0), neck=(-6, 40, 0), face='focus')
BA_HI = P(BA_PRE, pos=(0, 0.1), rot=78, footL=('b', 0.0, -0.84, 0.08), fpL=-30, kneeL=(1, 0, 0.1), footR=('b', 0.3, -0.35, 0.1), face='yell')
BA_LO = P(BA_PRE, pos=(0, 0.06), rot=96, footR=('b', 0.0, -0.84, 0.1), fpR=-30, kneeR=(1, 0, 0.1), footL=('b', 0.3, -0.35, 0.12), face='yell')
BA_MID = P(BA_PRE, pos=(0, 0.1), rot=88, footL=('b', 0.04, -0.86, 0.08), fpL=-30, kneeL=(1, 0, 0.1), footR=('b', 0.32, -0.4, 0.1), face='yell')
A['bair'] = dict(length=40, keys=[(0, AIR), (3, BA_PRE), (5, BA_HI, 'snap'), (6, BA_PRE), (7, BA_LO, 'snap'), (9, BA_PRE), (11, BA_MID, 'snap'),
                                  (19, BA_MID), (30, P(AIR, rot=20)), (40, AIR)])
# up air: backflip kick, the near foot sweeping from in front, over his head, to behind
UA_K = P(AIR, face='yell', footR=('b', 0.62, -0.16, 0.08), fpR=20, kneeR=(0, 1, 0.1), footL=('b', 0.2, -0.45, 0.12), kneeL=(1, 1, 0.1),
         handR=(-0.15, -0.2, 0.3), handL=(-0.15, -0.25, 0.3), **FIST)
A['uair'] = dict(length=20, keys=[(0, AIR), (2, P(TUCK, rot=-10)), (3, P(UA_K, rot=-45), 'snap'), (5, P(UA_K, rot=-130), 'lin'), (8, P(UA_K, rot=-215), 'lin'),
                                  (14, P(TUCK, rot=-320)), (20, P(AIR, rot=-360))])
# down air: knees up, then a two-footed stomp with the arms flung up
DR_G = P(TUCK, hips=(-4, -10, 0), chest=(-8, 0, 0), head=(4, 10, 0), footR=('b', 0.26, -0.3, 0.1), footL=('b', 0.2, -0.34, 0.14),
         handR=(0.1, 0.25, 0.25), handL=(-0.1, 0.25, 0.28), face='focus')
DR_S = P(AIR, hips=(-6, -10, 0), chest=(-10, 0, 0), head=(10, 10, 0), face='yell', footR=('b', 0.06, -0.86, 0.06), footL=('b', 0.02, -0.86, 0.08),
         fpR=-45, fpL=-45, kneeR=(1, 0, 0.1), kneeL=(1, 0, 0.1), handR=(0.15, 0.45, 0.25), handL=(-0.1, 0.45, 0.28), hdirR=(0, 1, 0.4), hdirL=(0, 1, 0.4), **FIST)
A['dair'] = dict(length=43, keys=[(0, AIR), (5, P(DR_G, footR=('b', 0.2, -0.45, 0.1))), (10, DR_G), (14, DR_S, 'snap'), (23, DR_S), (33, P(AIR, hips=(0, -14, 0))), (43, AIR)])

# ---------------------------------------------------------------- smash attacks
# forward smash, Home Run: two-handed bat swing (held back while charging at frame 12)
def bat(f, u, c, tw, bdir, kdir, **kw):
    hd, hb = hand_for(-V(*bdir), V(*kdir))   # the bat runs out of the fist along the hand's -X
    g = GRIP(f, u, c, tw)
    return dict(g, hdirR=(-hd[1], hd[2], -hd[0]), hbackR=(-hb[1], hb[2], -hb[0]), hdirL=(-hd[1], hd[2], hd[0]), hbackL=(-hb[1], hb[2], hb[0]), **kw)
BATP = dict(props=('bat',), curlR=1, thumbR=0.9, curlL=1, thumbL=0.9)
FS_0 = P(STANCE, **BATP, **bat(0.12, -0.25, -0.05, -34, (0.2, 1, 0.1), (1, 0, 0)))
FS_W = P(STANCE, pos=(-0.06, -0.1), hips=(4, -70, 0), chest=(-2, -24, 0), head=(-6, 70, 0), face='focus', footR=('w', 0.24, 0.13, 0.1), fpR=-25, toeR=25,
         **BATP, **bat(-0.18, 0.08, -0.3, -94, (-0.5, 0.7, -0.3), (0, 0.3, -1)))
FS_HIT = P(STANCE, pos=(0.14, -0.1), hips=(10, 10, 0), chest=(8, 20, 0), head=(-8, -10, 0), face='yell', footR=('w', 0.34, 0.095, 0.1),
           footL=('w', -0.06, 0.15, 0.14), fpL=-40, toeL=40, **BATP, **bat(0.4, -0.12, 0.0, 30, (1, 0.05, 0.0), (0, 1, 0)))
FS_FT = P(FS_HIT, hips=(8, 30, 0), chest=(4, 30, 0), head=(-6, -20, 0), face='smile', **BATP, **bat(0.15, 0.15, 0.25, 60, (-0.6, 0.6, 0.4), (0, 1, 0)))
A['fsmash'] = dict(length=54, keys=[(0, FS_0), (6, P(FS_W, hips=(4, -55, 0))), (12, FS_W), (15, P(FS_W, pos=(-0.07, -0.11))), (17, FS_HIT, 'lin'),
                                    (20, P(FS_HIT, **bat(0.3, -0.05, 0.15, 45, (0.6, 0.2, 0.7), (0, 1, 0)))), (30, FS_FT, 'out'), (44, FS_FT),
                                    (54, P(STANCE, pos=(0.14, -0.055)))])
# up smash, Slam Dunk: gather the ball low, leap, slam it overhead
BALLP = dict(props=('ball',))
US_G = P(CROUCH, pos=(0.0, -0.3), hips=(24, -24, 0), face='focus', handR=(0.32, -0.38, 0.05), hdirR=(1, 0, 0), hbackR=(0, -1, 0), curlR=0.25,
         handL=(0.3, -0.3, -0.2), hdirL=(0.6, 0, -0.8), hbackL=(0, 0, -1), curlL=0.2, **BALLP)
US_UP = P(JUMP_UP, pos=(0.0, 0.3), hips=(-6, -20, 0), chest=(-10, -8, 0), head=(-16, 12, 0), face='yell', handR=(0.1, 0.56, -0.06), hdirR=(0.2, 1, 0),
          hbackR=(-1, 0, 0), curlR=0.25, handL=(0.1, 0.52, -0.2), hdirL=(0.2, 1, 0), curlL=0.2, footR=('b', 0.1, -0.84, 0.1), footL=('b', -0.1, -0.84, 0.12), **BALLP)
US_SL = P(US_UP, pos=(0.04, 0.26), hips=(16, -20, 0), chest=(12, -8, 0), head=(-4, 12, 0), handR=(0.45, 0.25, -0.06), hdirR=(1, 0.4, 0), handL=(0.4, 0.2, -0.2))
A['usmash'] = dict(length=44, keys=[(0, STANCE), (4, P(US_G, pos=(0, -0.2))), (9, US_G), (11, US_G), (14, US_UP, 'snap'), (17, US_SL), (22, P(US_SL, pos=(0.04, 0.2))),
                                    (30, P(LANDP, props=())), (44, STANCE)])
# down smash, All In: poker chips lifted overhead, then shoved into the floor in front
CHIPS = dict(props=('chips',), curlR=0.2, thumbR=0.2)
DS_UP = P(STANCE, pos=(0, -0.02), hips=(-6, -20, 0), chest=(-10, -8, 0), head=(-14, 12, 0), face='focus', handR=(0.12, 0.5, -0.12), hdirR=(0.2, 1, 0),
          hbackR=(0, 0, -1), handL=(0.1, 0.46, -0.26), hdirL=(0.2, 1, 0), hbackL=(0, 0, -1), curlL=0.25, **CHIPS)
DS_DN = P(CROUCH, pos=(0.04, -0.48), hips=(44, -16, 0), chest=(12, -4, 0), head=(-26, 10, 0), face='yell', handR=(0.55, -0.32, -0.1), hdirR=(1, -0.4, 0),
          hbackR=(0, 1, 0), handL=(0.5, -0.34, -0.22), hdirL=(1, -0.4, 0), hbackL=(0, 1, 0), curlL=0.2, **CHIPS)
A['dsmash'] = dict(length=46, keys=[(0, P(STANCE, **CHIPS)), (4, P(DS_UP, pos=(0, -0.04))), (9, DS_UP), (11, P(DS_UP, pos=(0, 0.0))), (13, DS_DN, 'in'),
                                    (24, DS_DN), (32, P(DS_DN, props=(), pos=(0.04, -0.4))), (46, STANCE)])
