// KIERAN ROOKE — photography, cars, pizza and dookie, in a suit and tie. He
// shares every normal attack, grab and throw with Simeon (same skeleton,
// same animations); his look, a few stats, his smash attacks and his four
// specials are his own.
import { px } from '../engine/fixed.js';
import { anim } from '../engine/skeleton.js';
import { SIMEON } from './simeon.js';
import { ZEID } from './zeid.js';
import { MAX } from './max.js';
import { SARA } from './sara.js';
import { MALCOLM } from './malcolm.js';
import { FAYBUA } from './faybua.js';

const stats = {
  ...SIMEON.stats,
  weight: 94,               // a little lighter
  dashSpeed: px(3.2),
  airSpeed: px(2.8),
};

// ---------------------------------------------------------------------------
// Body parts: pixel art at 2 art pixels per world pixel, facing right.
// Fair skin, thick shaggy dark brown hair with a heavy fringe down to his
// brows. Navy suit, light blue shirt (S), a silver tie (Z / z), dark
// lapels (L) and buttons (Q).
// ---------------------------------------------------------------------------
const HEAD = [
  '...kkkkkkk....',
  '.kkkkkkkkkkk..',
  'kKkkkkkkkkkkl.',
  'kKkkkkkkkkkkl.',
  'KKkkkkkkkhhhh.',
  'KKkkkkkkkmmek.',
  'KkKqkkkkkmeek.',
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
// (hair column = head column + 1, row = head row + 4): full and shaggy, a
// few strands sticking up, the fringe right down to his brows
const HAIR = [
  '...h..hh..h.......',
  '..hhhhhhhhhhhh....',
  '.hhhhnhhhhhnhhhh..',
  'hhhhhhhhHhhhhhhhh.',
  'hhhHhhhhhhhhHhhhhh',
  'hhhhhhhHhhhhhhhhhh',
  'hhhhhhhhhhhhhhhhh.',
  'hhhhhhhhhhHhhhhhh.',
  'hhhhhhhhh.hHhhhh..',
  'hhhhhhhh..........',
  'hhhhhhh...........',
  'hhhhhh............',
  '.hhhhh............',
  '..hhh.............',
];
const parts = {
  ...SIMEON.parts,   // hands, legs and shoes are shared
  head_neutral: face(),
  head_smile: face([10, 10, 'qp']),
  head_yell: face([4, 9, 'kkhh'], [5, 9, 'hmek'], [9, 10, 'rrk'], [10, 10, 'rrr'], [11, 10, 'rr']),
  head_hurt: face([4, 9, 'hhkk'], [5, 9, 'kkkk'], [6, 9, 'eeek'], [10, 10, 'rr']),
  hair: { pivot: [6, 18], px: HAIR },
  // suit jacket open in a V over the shirt and tie
  torso: {
    pivot: [6, 26],
    px: [
      '.....kkkk.....',
      '....SSkkSS....',
      '...TTSZZSTu...',
      '..TTtLSZZSLu..',
      '.TTttLSZZSLtu.',
      'TTTttLSZZSLtuu',
      'TTtttLSZZSLtuu',
      'TTtttxLZZLttuu',
      'TTtttLZZLtttuu',
      'TTxtttLZzLttuu',
      'TTTxtttLzLttuu',
      'TTtTxttLLtttuu',
      '.TTttxttQtttu.',
      '.TTtttttttttu.',
      '.TTtttttttxtu.',
      '.TTttttttxttu.',
      '.TTtttttQtttu.',
      '.TTtttttttttu.',
      '.TTxtttttttuu.',
      '.TTtxttttttuu.',
      '.TTtttttttttu.',
      '.xTTttttttttx.',
      '.BBBBBBBBBBBB.',
      '.JJjjjjjjjjii.',
      '.JJjjjjjjjjji.',
      '.JJjjjjjjjjii.',
      '.JJjjjjjjjjii.',
      '..JJjjjjjjii..',
    ],
  },
  // long suit sleeves, a strip of shirt cuff at the wrist
  upperArm: { pivot: [2, 0], px: ['TTtuu', 'TTttu', 'TTttu', 'TTxtu', 'TTttu', 'TTttu', 'TTttu', 'TTxtu', 'TTttu', 'TTttu', 'TTttu', 'TTttu', '.TTt.'] },
  lowerArm: { pivot: [2, 0], px: ['TTttu', 'TTttu', 'TTxtu', 'TTttu', 'TTttu', '.TTtu', '.TTtu', '.TTtu', '.SSS.', '.SSS.', '.Kkl.'] },
};

const darker = (hex, k) => '#' + [1, 3, 5].map((i) => Math.round(parseInt(hex.slice(i, i + 2), 16) * k).toString(16).padStart(2, '0')).join('');
const BASE_COLORS = {
  ...SIMEON.palettes[0].colors,
  h: '#2a1b13', H: '#3d2a1f', n: '#54392a',   // dark brown hair, with a shine
  g: '#1b1b22', w: '#2a2a33', W: '#111116',   // black dress shoes
  B: '#15151b',
};
const alt = (name, suit, shirt, tie, extra = {}) => ({
  name,
  colors: {
    ...BASE_COLORS, t: suit[0], T: suit[1], u: suit[2], x: darker(suit[1], 0.75), L: darker(suit[1], 0.7), Q: darker(suit[1], 0.5),
    j: suit[0], J: suit[1], i: suit[2], y: darker(suit[1], 0.78), S: shirt, Z: tie[0], z: tie[1], ...extra,
  },
});
const palettes = [
  alt('Formal', ['#27324d', '#1a2236', '#38466a'], '#cfe0f2', ['#bcc2cc', '#8e96a3']),
  alt('Black Tie', ['#26262c', '#17171c', '#36363e'], '#f6f6f2', ['#1b1b22', '#0d0d12']),
];

// ---------------------------------------------------------------------------
// Poses and animations.
// ---------------------------------------------------------------------------
const FISTS = { handF: 'fist', handB: 'fist' };
const STAND = { torso: 2, armF: [4, 10], armB: [-6, 8], legF: [5, -4], legB: [-6, -2] };
const AIR = { torso: 6, armF: [75, 20], armB: [-80, 15], legF: [18, -28], legB: [-14, -18], footF: 25, footB: 35 };
// sitting in a seat, legs out in front
const SEATED = { hip: [0, 4], torso: -6, head: -8, armF: [150, 20], armB: [-150, -20], legF: [84, -80], legB: [70, -84], footF: 10, footB: 10, ...FISTS, face: 'yell' };

const animations = {
  // Pizza Toss: a quick sidearm flick (Faybua's cookie toss).
  pizza: FAYBUA.animations.cookie,
  // Drift: drops into the driver's seat and floors it (Sara's suitcase ride).
  drift: SARA.animations.boardingCall,
  // Ejector Seat: a crouch, then a car seat blasts him straight up.
  ejector: anim(false, [
    [4, { hip: [0, 6], torso: 14, armF: [40, 60], armB: [-30, 60], legF: [50, -95], legB: [30, -80], ...FISTS }],
    [4, { ...SEATED, armF: [60, 60], armB: [-60, 60] }],
    [24, SEATED],
    [10, { ...SEATED, armF: [90, 30], armB: [-90, 30], legF: [40, -50], legB: [20, -50] }],
    [14, AIR],
  ]),
  // Dookie: a squat, then he stands back up looking pleased with himself.
  dookie: anim(false, [
    [6, { hip: [0, 6], torso: 20, head: -10, armF: [50, 40], armB: [30, 40], legF: [60, -110], legB: [40, -100], ...FISTS }],
    [8, { hip: [0, 10], torso: 30, head: -20, armF: [70, 30], armB: [50, 30], legF: [80, -140], legB: [60, -130], ...FISTS, face: 'yell' }],
    [6, { hip: [0, 10], torso: 26, head: -16, armF: [70, 30], armB: [50, 30], legF: [80, -140], legB: [60, -130], ...FISTS, face: 'smile' }],
    [8, { hip: [0, 3], torso: 6, armF: [20, 20], armB: [-20, 20], legF: [30, -50], legB: [10, -40], face: 'smile' }],
    [2, STAND],
  ]),
  // --- Smash attacks ---
  // Say Cheese: the camera held out at arm's length (Malcolm's popper pose).
  fsmash: MALCOLM.animations.fsmash,
  // Pizza Peel: a big wooden peel swung over his head, front to back (Max's bottle swing).
  usmash: MAX.animations.usmash,
  // Burnout: a low crouch while tyre smoke and rubber fly out both sides (Zeid's crouch).
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
  // Neutral special: Pizza Toss. Flicks a whole pizza that flies flat and
  // spins (6%). Two at a time at most.
  pizza: { faf: 30, limit: 2, spawn: { frame: 8, from: 'fistF', projectile: 'pizza' }, hitboxes: [] },

  // Side special: Drift. Drives forward in a little sports car (11%). Stays
  // on the floor when used there; once per jump in the air.
  drift: { faf: 54, landLag: 14, once: true, noDrift: true, float: { gravity: 20, fall: 25 },
    gear: { kind: 'car', from: 6, to: 40 },
    rocket: { frame: 12, frames: 24, speed: [px(4.3), px(4.3)], lift: 0, gravity: 30, drag: 10, bounce: [px(0.9), px(1.6)], ground: true },
    ledgeGrab: { from: 26 },
    hitboxes: hits(12, 36, [['kneeF', 10], ['hip', 10]], 11, 45, 52, 78, { off: [8, 4] }) },

  // Up special: Ejector Seat. Blasts straight up on a car seat with a rocket
  // under it, steering freely; the flame hits a few times (2% each) and pops
  // them up at the top (5%). Falls helpless afterwards.
  ejector: { faf: 56, landLag: 16, helpless: true, gear: { kind: 'ejector', from: 6, to: 34, active: [8, 30] },
    fly: { frame: 8, frames: 19, rise: px(4.6), accel: px(1.5), drift: px(1.4), steer: px(0.14) },
    ledgeGrab: { from: 8, rising: true },
    hitboxes: [
      ...[0, 1, 2, 3].map((i) => hit(9 + i * 4, 10 + i * 4, 'hip', 11, 2, 90, 0, 100, { fkb: 40, group: i, off: [0, 12] })),
      hit(26, 28, 'hip', 12, 5, 80, 50, 72, { group: 4, off: [0, 4] }),
    ] },

  // Down special: Dookie. Squats and leaves a dookie on the floor (it drops
  // if he is in the air). It sits there for 6 seconds; whoever steps in it
  // slips and pops up (6%). Two on the stage at most.
  dookie: { faf: 32, limit: 2, spawn: { frame: 14, from: 'hip', projectile: 'dookie' }, hitboxes: [] },

  // --- Smash attacks (see simeon.js for how they are performed) ---
  // Forward: Say Cheese. A camera flash right in their face: 15%.
  fsmash: { faf: 50, charge: { at: 12, max: 60, smash: true }, gear: { kind: 'camera', from: 0, to: 40, active: [16, 28] }, hitboxes: [
      hit(16, 19, 'fistF', 9, 15, 361, 34, 98, { off: [12, -1], chargeScale: [150, 210], lagMult: 150 }),
      hit(16, 19, 'fistF', 10, 13, 361, 30, 94, { off: [25, -3], chargeScale: [130, 182], lagMult: 150 }),
    ] },
  // Up: Pizza Peel. A wooden peel (with a pizza on it) swung over his head,
  // front to back: 15% anywhere along the swing.
  usmash: { faf: 50, charge: { at: 9, max: 60, smash: true }, gear: { kind: 'peel', from: 0, to: 40 },
    trail: { part: 'weaponF', from: 11, to: 19, width: 10, arc: true }, hitboxes: [
      ...hits(11, 19, [['weaponF', 10], ['weaponMidF', 8]], 15, 88, 34, 96, { group: 0, chargeScale: [150, 210], lagMult: 150 }),
    ] },
  // Down: Burnout. Tyre smoke and rubber blast out low on both sides: 14%.
  dsmash: { faf: 48, charge: { at: 11, max: 60, smash: true }, gear: { kind: 'burnout', from: 4, to: 30, active: [13, 26] }, hitboxes: [
      hit(13, 16, 'hip', 11, 14, 35, 30, 94, { off: [18, 8], radial: true, chargeScale: [140, 196], lagMult: 150 }),
      hit(13, 16, 'hip', 11, 14, 35, 30, 94, { off: [-18, 8], radial: true, chargeScale: [140, 196], lagMult: 150 }),
    ] },
};

export const KIERAN = {
  ...SIMEON,
  id: 'kieran',
  name: 'KIERAN',
  lastName: 'ROOKE',
  heightInches: 70,
  stats,
  parts,
  palettes,
  trailColors: ['#e8a23a', '#ffd86a', '#ffffff'],   // crust, cheese, flash
  animations: { ...SIMEON.animations, ...animations },
  moves: { ...SIMEON.moves, ...moves },
  specials: { neutral: 'pizza', side: 'drift', up: 'ejector', down: 'dookie' },
  projectiles: {
    // a whole pizza, flicked flat: flies straight and spins
    pizza: { type: 'dart', draw: 'pizza', r: 5, hitPad: 2, speed: [px(4.6), 0], chargeSpeed: [0, 0], gravity: 0, maxFall: 0,
      life: 44, fadeFrames: 4, hit: { damage: 60, angle: 361, bkb: 28, kbg: 52 } },
    // a dookie: drops to the floor and sits there until someone steps in it
    dookie: { draw: 'dookie', settle: true, r: 3, hitPad: 2, speed: [0, 0], chargeSpeed: [0, 0],
      gravity: px(0.2), maxFall: px(4), bounce: 0, bounceKeepX: 0, minBounce: px(9), maxBounces: 0,
      rollFriction: px(1), minRollSpeed: 0, popUp: px(1), life: 360, fadeFrames: 12,
      hit: { damage: 60, angle: 80, bkb: 50, kbg: 40 }, rollHit: { damage: 60, angle: 80, bkb: 50, kbg: 40 } },
  },
};
