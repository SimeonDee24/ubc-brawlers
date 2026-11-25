// MARC SOLOMOSI — a ski bum who never misses a party. His side special is a
// straight-line ski run and his down special is Zeid's bomb; the rest are
// drinks: a shotgunned beer (hold it all the way and he blows himself up,
// like Hero's Kamikaze), a shaken can he rides up, a bottle, a pint.
// He shares every normal attack, grab and throw with Simeon (same skeleton,
// same animations); his look, a few stats, his smash attacks and his four
// specials are his own.
import { px } from '../engine/fixed.js';
import { anim } from '../engine/skeleton.js';
import { SIMEON } from './simeon.js';
import { ZEID } from './zeid.js';
import { MAX } from './max.js';

const stats = {
  ...SIMEON.stats,
  weight: 102,              // a bit sturdier
  runSpeed: px(2.9),
  airSpeed: px(2.75),
};

// ---------------------------------------------------------------------------
// Body parts: pixel art at 2 art pixels per world pixel, facing right.
// Messy, spiky near-black hair, tanned skin. The eyes use their own letters
// so one palette can put his sports sunglasses on: F / Y = frame (his brows
// and skin when the glasses are off), M / E = lenses (the whites and pupils).
// The black tee with the silver chain is Simeon's (shared torso).
// ---------------------------------------------------------------------------
const HEAD = [
  '...kkkkkkk....',
  '.kkkkkkkkkkk..',
  'kKkkkkkkkkkkl.',
  'kKkkkkkkkkkkl.',
  'KKkkkkkkkFFFF.',
  'KKkkkkkkYMMEY.',
  'KkKqkkkkYMEEk.',
  'KkKqkkkkkkkkkl',
  'KKkKKkkkkkkkKl',
  'KKkKkkkkkkkkk.',
  '.KKkkkkkkkkpk.',
  '.KKkkkkkkkkk..',
  '..KKkkkkkkkk..',
  '....KKKKKkK...',
];
const face = (...edits) => {
  const rows = HEAD.map((r) => r.split(''));
  for (const [r, c, str] of edits) for (let i = 0; i < str.length; i++) rows[r][c + i] = str[i];
  return { pivot: [5, 14], px: rows.map((r) => r.join('')) };
};
// (hair column = head column + 1, row = head row + 5): a row taller than
// Simeon's, all spikes on top and loose strands over the forehead
const HAIR = [
  '.....h...h....h...',
  '..h.hh..hhh..hh...',
  '..hhhhhhhhhhhhhhh.',
  '.hhhnhhhHhhhnhhhhh',
  'hhhHhhhHnhhhhHhhhh',
  'hhhhhHhhhhHnhhhHhh',
  'hhHnhhhhHhhhhHhhhh',
  'hhhhhHhhhhhHhhhHh.',
  'hhhHhhhhh.h.hh.h..',
  'hhhhhh.......h....',
  'hhhh..............',
  'hhhh..............',
  '.hhh..............',
  '.hh...............',
  '..h...............',
];
const parts = {
  ...SIMEON.parts,   // tee with the chain, arms, hands, jeans, sneakers
  head_neutral: face([10, 10, 'qp']),                          // a half smirk
  head_smile: face([10, 9, 'kmmp']),                           // a big grin
  head_yell: face([9, 10, 'rrk'], [10, 10, 'rrr'], [11, 10, 'rr']),
  head_hurt: face([10, 10, 'rr']),
  hair: { pivot: [6, 19], px: HAIR },
};

const darker = (hex, k) => '#' + [1, 3, 5].map((i) => Math.round(parseInt(hex.slice(i, i + 2), 16) * k).toString(16).padStart(2, '0')).join('');
const BASE_COLORS = {
  ...SIMEON.palettes[0].colors,
  k: '#d9a57c', K: '#b9845f', l: '#e8bf98', q: '#9e6a4c', p: '#a8664f',   // tanned skin, lips
  h: '#17110e', H: '#2a1f1a', n: '#3d2f27',                               // near-black hair
  F: '#17110e', M: '#ffffff', E: '#1b1310', Y: '#d9a57c',                 // brows, eyes, skin (glasses off)
  g: '#2d2d37',
};
const SHADES = { F: '#f6f6f2', Y: '#f6f6f2', M: '#b8f03a', E: '#d63fd0' };   // white frames, rainbow mirror lenses
const alt = (name, shirt, jeans, extra = {}) => ({
  name,
  colors: { ...BASE_COLORS, t: shirt[0], T: shirt[1], u: shirt[2], x: darker(shirt[1], 0.72), j: jeans[0], J: jeans[1], i: jeans[2], y: darker(jeans[1], 0.78), ...extra },
});
const BLACK_TEE = ['#2d2d37', '#1d1d26', '#41414e'];
const palettes = [
  alt('Night Out', BLACK_TEE, ['#2c2f44', '#1d1f30', '#3e425c']),
  alt('Shades On', BLACK_TEE, ['#3f6fb8', '#2c5190', '#5b8cd4'], SHADES),
];

// ---------------------------------------------------------------------------
// Poses and animations.
// ---------------------------------------------------------------------------
const FISTS = { handF: 'fist', handB: 'fist' };
const STAND = { torso: 2, armF: [4, 10], armB: [-6, 8], legF: [5, -4], legB: [-6, -2] };
const AIR = { torso: 6, armF: [75, 20], armB: [-80, 15], legF: [18, -28], legB: [-14, -18], footF: 25, footB: 35 };
// low ski tuck: knees bent, chest down over them, poles tucked under his arms
const TUCK = { hip: [1, 10], torso: 42, head: -26, armF: [55, 35], armB: [45, 40], legF: [72, -122], legB: [52, -112], footF: 50, footB: 60, ...FISTS };
// a can held up and spraying straight down under him
const SPRAY = { torso: -4, head: 10, armF: [-6, 4], armB: [-150, -20], legF: [24, -40], legB: [-12, -30], footF: 30, footB: 40, ...FISTS, face: 'yell' };
const PINT_UP = { hip: [0, -1], torso: -6, head: -14, armF: [174, 2], armB: [-30, 30], legF: [8, -4], legB: [-8, -4], handF: 'fist', face: 'yell' };

const animations = {
  // Shotgun: the can at his lips (Zeid's vape pull), then a huge burp.
  shotgun: ZEID.animations.cloudChaser,
  // Send It: plants his poles, then drops into a tuck and bombs straight ahead.
  sendIt: anim(false, [
    [5, { hip: [0, 3], torso: 14, armF: [-30, 40], armB: [-44, 40], legF: [24, -40], legB: [-6, -30], ...FISTS }],
    [6, { hip: [0, 5], torso: 26, head: -10, armF: [-60, 20], armB: [-70, 20], legF: [36, -70], legB: [10, -60], ...FISTS, face: 'yell' }],
    [22, TUCK],
    [10, { ...TUCK, hip: [0, 4], torso: 20, head: -10, legF: [30, -60], legB: [14, -50] }],
    [12, { torso: 6, armF: [30, 30], armB: [-30, 30], legF: [14, -12], legB: [-12, -8], ...FISTS }],
    [1, STAND],
  ]),
  // Shaken Up: shakes a can hard, points it at the floor and rides the spray up.
  shakenUp: anim(false, [
    [3, { torso: 4, armF: [60, 110], armB: [-20, 30], legF: [8, -6], legB: [-8, -4], ...FISTS }],
    [3, { torso: 4, armF: [110, 50], armB: [-20, 30], legF: [8, -6], legB: [-8, -4], ...FISTS }],
    [3, { torso: 4, armF: [60, 110], armB: [-20, 30], legF: [8, -6], legB: [-8, -4], ...FISTS, face: 'yell' }],
    [3, { hip: [0, 5], torso: 16, head: 14, armF: [-10, 10], armB: [-40, 40], legF: [44, -86], legB: [26, -74], ...FISTS }],
    [22, SPRAY],
    [10, { ...SPRAY, armF: [40, 30], face: 'smile' }],
    [16, AIR],
  ]),
  // Kamikaze: arms thrown wide, glowing, then he goes off.
  kamikaze: anim(false, [
    [6, { hip: [0, 2], torso: -8, head: -16, armF: [100, 20], armB: [-100, -20], legF: [16, -10], legB: [-16, -10], handF: 'open', handB: 'open', face: 'yell' }],
    [10, { hip: [0, 3], torso: -12, head: -22, armF: [130, 10], armB: [-130, -10], legF: [22, -14], legB: [-22, -14], handF: 'open', handB: 'open', face: 'yell' }],
    [30, { hip: [0, 3], torso: -12, head: -22, armF: [134, 10], armB: [-134, -10], legF: [22, -14], legB: [-22, -14], handF: 'open', handB: 'open', face: 'yell' }],
  ]),
  // Bomb: Zeid's, exactly.
  bomb: ZEID.animations.bomb,
  itemToss: ZEID.animations.itemToss,
  // --- Smash attacks ---
  // Bottle Smash: a beer bottle raised behind him and slammed down in front (Max's swing).
  fsmash: MAX.animations.fsmash,
  // Cheers: dips with a pint, then thrusts it straight up and it slops over.
  usmash: anim(false, [
    [5, { torso: 4, armF: [40, 100], armB: [-20, 30], legF: [8, -6], legB: [-8, -4], handF: 'fist', face: 'smile' }],
    [5, { hip: [0, 4], torso: 12, head: 6, armF: [20, 120], armB: [-30, 40], legF: [24, -40], legB: [-6, -30], handF: 'fist' }],
    [2, { hip: [0, 4], torso: 12, head: 6, armF: [18, 122], armB: [-30, 40], legF: [24, -40], legB: [-6, -30], handF: 'fist', face: 'yell' }],
    [3, { ...PINT_UP, armF: [130, 20] }],
    [14, PINT_UP],
    [10, { torso: 2, armF: [60, 60], armB: [-20, 30], legF: [8, -6], legB: [-8, -4], handF: 'fist', face: 'smile' }],
    [6, STAND],
  ]),
  // Spill: crouches and sloshes a pitcher round in a low circle (Zeid's crouch).
  dsmash: ZEID.animations.dsmash,
};

// ---------------------------------------------------------------------------
// Moves. See simeon.js for the hitbox format.
// ---------------------------------------------------------------------------
const hit = (from, to, at, r, damage, angle, bkb, kbg, extra = {}) => ({
  frames: [from, to], at, r, damage: Math.round(damage * 10), angle, bkb, kbg, ...extra,
});
const hits = (from, to, list, damage, angle, bkb, kbg, extra) =>
  list.map(([at, r]) => hit(from, to, at, r, damage, angle, bkb, kbg, extra));

const moves = {
  // Neutral special: Shotgun. Hold the button and he keeps chugging; let go
  // and he burps: 9% on a tap, up to 20% after a long chug. He heals 3% when
  // he finishes (at most once every 10 seconds). Keep holding for the full
  // 3 seconds and he goes Kamikaze (like Hero's): he glows, can't be hit,
  // then blows up in a huge blast (40%, KOs early) and loses a stock himself.
  shotgun: { faf: 46, charge: { at: 10, max: 180 }, variant: { minCharge: 180, move: 'kamikaze' },
    gear: { kind: 'beercan', from: 0, to: 30, active: [17, 28] },
    heal: { frame: 14, amount: 30, every: 600 },
    hitboxes: [
      hit(17, 20, 'neck', 9, 9, 45, 40, 78, { off: [12, 2], chargeScale: [90, 200] }),
      hit(17, 22, 'neck', 7, 6, 45, 30, 70, { off: [24, 4], chargeScale: [60, 140] }),
    ] },
  // (picks up on frame 11, when the full charge lets go)
  kamikaze: { faf: 60, intangible: 40, gear: { kind: 'kamikaze', from: 11, to: 32 },
    spawn: { frame: 30, from: 'chest', projectile: 'kamikaze' }, selfKo: 32, hitboxes: [] },

  // Side special: Send It. Clicks into his skis and bombs straight ahead in
  // a tuck, very fast (11%, ski tips first). Stays on the floor when used
  // there; once per jump in the air. Stops dead if it connects.
  sendIt: { faf: 56, landLag: 14, once: true, noDrift: true, float: { gravity: 20, fall: 25 },
    gear: { kind: 'skis', from: 4, to: 46, active: [11, 33] },
    rocket: { frame: 11, frames: 22, speed: [px(4.8), px(4.8)], lift: 0, gravity: 28, drag: 9, bounce: [px(0.9), px(1.6)], ground: true },
    ledgeGrab: { from: 24 },
    hitboxes: [
      ...hits(11, 22, [['toeF', 8], ['footF', 7], ['hip', 8]], 11, 40, 55, 78, { off: [6, 0] }),
      ...hits(23, 33, [['toeF', 7], ['footF', 6], ['hip', 7]], 8, 50, 45, 70, { off: [6, 0] }),
    ] },

  // Up special: Shaken Up. Shakes a can and points it at the floor: the spray
  // blasts him straight up, steering freely. The foam under him hits a few
  // times (2% each) and pops them up at the top (5%). Falls helpless after.
  shakenUp: { faf: 60, landLag: 16, helpless: true, gear: { kind: 'beerjet', from: 0, to: 36, active: [12, 34] },
    fly: { frame: 12, frames: 20, rise: px(4.6), accel: px(1.5), drift: px(1.4), steer: px(0.14) },
    ledgeGrab: { from: 12, rising: true },
    hitboxes: [
      ...[0, 1, 2, 3].map((i) => hit(13 + i * 4, 14 + i * 4, 'hip', 11, 2, 90, 0, 100, { fkb: 40, group: i, off: [0, 14] })),
      hit(30, 32, 'hip', 12, 5, 80, 50, 72, { group: 4, off: [0, 10] }),
    ] },

  // Down special: Bomb. Zeid's, exactly (see zeid.js).
  bomb: ZEID.moves.bomb,
  itemToss: ZEID.moves.itemToss,

  // --- Smash attacks (see simeon.js for how they are performed) ---
  // Forward: Bottle Smash. A beer bottle slammed down in front: 17%.
  fsmash: { faf: 54, charge: { at: 14, max: 60, smash: true }, gear: { kind: 'beerBottle', from: 0, to: 46, active: [20, 30] },
    trail: { part: 'weaponF', from: 18, to: 23, width: 9, arc: true }, hitboxes: [
      ...hits(19, 22, [['weaponF', 9], ['weaponMidF', 7], ['fistF', 6]], 17, 361, 34, 97, { chargeScale: [170, 238], lagMult: 150 }),
    ] },
  // Up: Cheers. A pint thrust straight up, slopping over: 15% at the glass,
  // a weaker 10% in the splash above it (one or the other).
  usmash: { faf: 47, charge: { at: 11, max: 60, smash: true }, gear: { kind: 'pint', from: 0, to: 40, active: [15, 30] }, hitboxes: [
      hit(15, 19, 'fistF', 8, 15, 88, 34, 96, { group: 0, chargeScale: [150, 210], lagMult: 150 }),
      hit(15, 19, 'fistF', 7, 15, 88, 34, 96, { group: 0, off: [0, -8], chargeScale: [150, 210], lagMult: 150 }),
      hit(15, 24, 'fistF', 10, 10, 85, 30, 90, { group: 0, off: [0, -16], chargeScale: [100, 140], lagMult: 130 }),
    ] },
  // Down: Spill. Sloshes beer low across the floor on both sides: 14%.
  dsmash: { faf: 48, charge: { at: 11, max: 60, smash: true }, gear: { kind: 'spill', from: 4, to: 30, active: [13, 26] }, hitboxes: [
      hit(13, 16, 'hip', 11, 14, 30, 30, 94, { off: [18, 9], radial: true, chargeScale: [140, 196], lagMult: 150 }),
      hit(13, 16, 'hip', 11, 14, 30, 30, 94, { off: [-18, 9], radial: true, chargeScale: [140, 196], lagMult: 150 }),
    ] },
};

export const MARC = {
  ...SIMEON,
  id: 'marc',
  name: 'MARC',
  lastName: 'SOLOMOSI',
  heightInches: 71,
  stats,
  parts,
  palettes,
  trailColors: ['#d98a1c', '#ffd25a', '#fffdf2'],   // lager amber, gold, foam
  animations: { ...SIMEON.animations, ...animations },
  moves: { ...SIMEON.moves, ...moves },
  specials: { neutral: 'shotgun', side: 'sendIt', up: 'shakenUp', down: 'bomb' },
  projectiles: {
    bomb: ZEID.projectiles.bomb,
    // the Kamikaze blast: goes off the moment it appears
    kamikaze: { draw: 'kamikaze', silent: true, r: 1, hitPad: 0, speed: [0, 0], chargeSpeed: [0, 0],
      gravity: 0, maxFall: 0, bounce: 0, bounceKeepX: 0, minBounce: 0, maxBounces: 0,
      rollFriction: 0, minRollSpeed: 0, popUp: 0, life: 1, fadeFrames: 999, hit: { damage: 0, angle: 0, bkb: 0, kbg: 0 },
      explode: { r: 58, frames: 28, hit: { damage: 400, angle: 50, bkb: 95, kbg: 78 } } },
  },
};
