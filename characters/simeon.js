// SIMEON — all-rounder, and the first fighter with a 3D model.
//
// He is still pure data for the engine: stats, skeleton, moves. His
// animations are baked out of the Blender rig (characters/simeon-anims.js,
// one integer pose per frame) so hitboxes and hurtboxes follow the 3D motion
// exactly while the simulation stays deterministic. The model itself
// (assets/models/simeon.glb) is drawn by render/model3d.js; if WebGL2 isn't
// available he falls back to the 2D paper doll, driven by the same poses.
//
// The 2D cast no longer copies from this file: they build on characters/base.js.
import { px } from '../engine/fixed.js';
import { BASE } from './base.js';
import { SIMEON_ANIMS } from './simeon-anims.js';

// Body proportions measured off the 3D model (1.78 m = 42 px, so 23.6 px per metre).
const skeleton = {
  ...BASE.skeleton,
  hipY: 22, torso: 12, shoulderDrop: 2, shoulderOff: 1, hipOff: 1,
  upperArm: 7, lowerArm: 6, upperLeg: 10, lowerLeg: 10,
  headRadius: 4, torsoRadius: 3, armRadius: 2, legRadius: 2,
};

const hit = (from, to, at, r, damage, angle, bkb, kbg, extra = {}) => ({
  frames: [from, to], at, r, damage: Math.round(damage * 10), angle, bkb, kbg, ...extra,
});
const hits = (from, to, parts, damage, angle, bkb, kbg, extra) =>
  parts.map(([at, r]) => hit(from, to, at, r, damage, angle, bkb, kbg, extra));

// Moves that changed with the new animations. Everything else keeps its
// frame data from the base moveset (characters/base.js).
const BACK = { dir: -1 };
const moves = {
  // Getup attack: a sweep along the floor in front, then he spins and sweeps
  // behind with the same leg (the near one), so both hits follow toeF.
  getupAttack: { ...BASE.moves.getupAttack, trail: { part: 'toeF', from: 16, to: 24 }, hitboxes: [
    ...hits(18, 19, [['toeF', 6], ['shinF', 5]], 7, 361, 80, 50),
    ...hits(22, 23, [['toeF', 6], ['shinF', 5]], 7, 361, 80, 50, BACK),
  ] },
  // Neutral air: a tuck into a full spinning kick with the near leg straight out.
  // Out on frame 6 now (was 12): 7% clean on frames 6-8, 5% late on 9-14.
  nair: { faf: 30, landLag: 6, autoCancel: [3, 24], trail: { part: 'toeF', from: 6, to: 15, width: 6 }, hitboxes: [
    ...hits(6, 8, [['toeF', 7], ['shinF', 6], ['kneeF', 5], ['chest', 8]], 7, 70, 45, 80),
    ...hits(9, 14, [['toeF', 6], ['shinF', 5], ['chest', 7]], 5, 70, 35, 70),
  ] },
};

export const SIMEON = {
  ...BASE,
  id: 'simeon',
  name: 'SIMEON',
  lastName: 'DEE',
  skeleton,
  animations: { ...BASE.animations, ...SIMEON_ANIMS },
  moves: { ...BASE.moves, ...moves },
  // The 3D model. Colours by material name; alt 0 keeps the model's own.
  model3d: {
    url: 'assets/models/simeon.glb',
    palettes: [
      {},
      { Shirt: '#cc363c', Jeans: '#2c2f44', ShoeGreen: '#962330' },
    ],
  },
};
