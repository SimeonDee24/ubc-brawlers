// A small WebGL2 renderer for skinned glTF fighters (Simeon is the first).
// Render only: the simulation never sees any of this. Hitboxes come from the
// 2D joints baked out of the same animations (characters/simeon-anims.js).
//
// How it fits the 2D renderer: each fighter is drawn into an offscreen WebGL
// canvas through an orthographic camera that matches the bake, then copied
// into the game's canvas with drawImage at the fighter's feet, so effects,
// the HUD and the other (pixel-art) fighters layer exactly as before.

const GL_FLOAT = 5126;

// The game camera used for the bake (tools/blender/export.py): it looks at
// his right side, turned 30 degrees toward his front and 6 degrees down.
const CAM_YAW = 30, CAM_PITCH = 6;
const PX_PER_M = 42 / 1.78;          // he is 42 world pixels tall

const VS = `#version 300 es
precision highp float;
in vec3 aPos; in vec3 aNrm; in vec4 aJnt; in vec4 aWgt;
uniform mat4 uJoints[64];
uniform mat4 uView;          // world (metres, glTF axes) -> clip
uniform mat3 uViewRot;       // world -> view rotation, for normals
uniform float uOutline;      // > 0: inflate along the normal (outline pass), in metres
out vec3 vN; out vec3 vV;
void main() {
  mat4 sk = uJoints[int(aJnt.x)] * aWgt.x + uJoints[int(aJnt.y)] * aWgt.y + uJoints[int(aJnt.z)] * aWgt.z + uJoints[int(aJnt.w)] * aWgt.w;
  vec4 p = sk * vec4(aPos, 1.0);
  vec3 n = normalize(mat3(sk) * aNrm);
  p.xyz += n * uOutline;
  vN = uViewRot * n;
  vV = (uView * p).xyz;
  gl_Position = uView * p;
}`;

const FS = `#version 300 es
precision highp float;
in vec3 vN; in vec3 vV;
uniform vec4 uColor;         // linear base colour
uniform vec2 uMat;           // roughness, metallic
uniform vec4 uFlash;         // rgb + amount (white blink while invincible, etc.)
uniform float uOutlinePass;
out vec4 o;
vec3 toSrgb(vec3 c) { return pow(clamp(c, 0.0, 1.0), vec3(1.0 / 2.2)); }
void main() {
  if (uOutlinePass > 0.5) { o = vec4(0.063, 0.051, 0.086, 1.0); return; }
  vec3 n = normalize(vN);
  if (!gl_FrontFacing) n = -n;
  vec3 V = vec3(0.0, 0.0, 1.0);
  vec3 key = normalize(vec3(0.5, 0.7, 0.6));       // upper front, on the side he faces
  vec3 fill = normalize(vec3(-0.7, 0.1, 0.5));
  float d = dot(n, key);
  // soft two-tone shading: a cel step softened over a short band
  float lit = smoothstep(-0.05, 0.25, d) * 0.55 + max(d, 0.0) * 0.35;
  float f = max(dot(n, fill), 0.0) * 0.18;
  vec3 base = uColor.rgb;
  vec3 col = base * (0.36 + lit + f);
  // specular, tighter on glossy materials
  float gloss = mix(60.0, 6.0, uMat.x);
  vec3 h = normalize(key + V);
  float sp = pow(max(dot(n, h), 0.0), gloss) * (1.0 - uMat.x) * 0.55;
  col += mix(vec3(sp), base * sp * 3.0, uMat.y);
  // rim light: Smash-style edge glow from behind
  float rim = pow(1.0 - max(dot(n, V), 0.0), 3.0) * smoothstep(-0.2, 0.4, dot(n, normalize(vec3(-0.6, 0.4, -0.2))));
  col += vec3(1.0, 0.96, 0.9) * rim * 0.45;
  col = mix(col, uFlash.rgb, uFlash.a);
  o = vec4(toSrgb(col), 1.0);
}`;

// ---------------------------------------------------------------- tiny maths
const m4 = {
  ident: () => new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]),
  mul(a, b, o = new Float32Array(16)) {
    for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
      o[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3];
    }
    return o;
  },
  trs(t, q, s, o = new Float32Array(16)) {
    const [x, y, z, w] = q, x2 = x + x, y2 = y + y, z2 = z + z;
    const xx = x * x2, xy = x * y2, xz = x * z2, yy = y * y2, yz = y * z2, zz = z * z2, wx = w * x2, wy = w * y2, wz = w * z2;
    o[0] = (1 - (yy + zz)) * s[0]; o[1] = (xy + wz) * s[0]; o[2] = (xz - wy) * s[0]; o[3] = 0;
    o[4] = (xy - wz) * s[1]; o[5] = (1 - (xx + zz)) * s[1]; o[6] = (yz + wx) * s[1]; o[7] = 0;
    o[8] = (xz + wy) * s[2]; o[9] = (yz - wx) * s[2]; o[10] = (1 - (xx + yy)) * s[2]; o[11] = 0;
    o[12] = t[0]; o[13] = t[1]; o[14] = t[2]; o[15] = 1;
    return o;
  },
};

function srgbToLinear(h) {
  const c = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
  return c.map((x) => (x > 0.04045 ? ((x + 0.055) / 1.055) ** 2.4 : x / 12.92));
}

// ---------------------------------------------------------------- glTF parsing
function parseGlb(buf) {
  const dv = new DataView(buf);
  if (dv.getUint32(0, true) !== 0x46546c67) throw new Error('not a GLB');
  let off = 12, json = null, bin = null;
  while (off < buf.byteLength) {
    const len = dv.getUint32(off, true), type = dv.getUint32(off + 4, true);
    const data = buf.slice(off + 8, off + 8 + len);
    if (type === 0x4e4f534a) json = JSON.parse(new TextDecoder().decode(data));
    else if (type === 0x004e4942) bin = data;
    off += 8 + len;
  }
  return { json, bin };
}

const COMP = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };
const ARR = { 5120: Int8Array, 5121: Uint8Array, 5122: Int16Array, 5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array };
function accessor(g, i) {
  const a = g.json.accessors[i], bv = g.json.bufferViews[a.bufferView];
  const T = ARR[a.componentType], n = COMP[a.type];
  const stride = bv.byteStride || 0;
  const start = (bv.byteOffset || 0) + (a.byteOffset || 0);
  if (stride && stride !== n * T.BYTES_PER_ELEMENT) {
    const out = new T(a.count * n), src = new DataView(g.bin);
    const get = { 5126: 'getFloat32', 5123: 'getUint16', 5121: 'getUint8', 5125: 'getUint32' }[a.componentType];
    for (let k = 0; k < a.count; k++) for (let c = 0; c < n; c++) out[k * n + c] = src[get](start + k * stride + c * T.BYTES_PER_ELEMENT, true);
    return { data: out, n, count: a.count, type: a.componentType, normalized: !!a.normalized };
  }
  return { data: new T(g.bin, start, a.count * n), n, count: a.count, type: a.componentType, normalized: !!a.normalized };
}

// ---------------------------------------------------------------- the model
export class Model3D {
  constructor() {
    this.ready = false;
    this.failed = false;
    this.canvas = document.createElement('canvas');
    this.canvas.width = this.canvas.height = 2;
    const gl = this.canvas.getContext('webgl2', { alpha: true, premultipliedAlpha: true, antialias: true, preserveDrawingBuffer: true });
    this.gl = gl;
    if (!gl) { this.failed = true; return; }
    this.prog = this.program(VS, FS);
  }

  program(vs, fs) {
    const gl = this.gl;
    const sh = (type, src) => {
      const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    };
    const p = gl.createProgram();
    gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    const u = {};
    for (const n of ['uJoints', 'uView', 'uViewRot', 'uOutline', 'uColor', 'uMat', 'uFlash', 'uOutlinePass']) u[n] = gl.getUniformLocation(p, n);
    return { p, u, a: { aPos: gl.getAttribLocation(p, 'aPos'), aNrm: gl.getAttribLocation(p, 'aNrm'), aJnt: gl.getAttribLocation(p, 'aJnt'), aWgt: gl.getAttribLocation(p, 'aWgt') } };
  }

  async load(url) {
    if (this.failed) return this;
    try {
      const buf = await (await fetch(url)).arrayBuffer();
      this.build(parseGlb(buf));
      this.ready = true;
    } catch (e) {
      console.warn('3D model unavailable, using the 2D sprite', e);
      this.failed = true;
    }
    return this;
  }

  build(g) {
    const gl = this.gl, J = g.json;
    this.nodes = J.nodes.map((n) => ({
      name: n.name, children: n.children || [],
      t: n.translation || [0, 0, 0], r: n.rotation || [0, 0, 0, 1], s: n.scale || [1, 1, 1],
      local: m4.ident(), world: m4.ident(),
    }));
    this.parent = new Int16Array(this.nodes.length).fill(-1);
    this.nodes.forEach((n, i) => n.children.forEach((c) => { this.parent[c] = i; }));
    // order nodes so parents come first
    this.order = [];
    const visit = (i) => { this.order.push(i); for (const c of this.nodes[i].children) visit(c); };
    this.parent.forEach((p, i) => { if (p < 0) visit(i); });
    const skin = J.skins[0];
    this.joints = skin.joints;
    this.ibm = accessor(g, skin.inverseBindMatrices).data;
    this.jointMats = new Float32Array(64 * 16);
    // materials
    this.materials = J.materials.map((m) => {
      const pbr = m.pbrMetallicRoughness || {};
      return { name: m.name, color: (pbr.baseColorFactor || [1, 1, 1, 1]).slice(0, 3), rough: pbr.roughnessFactor ?? 1, metal: pbr.metallicFactor ?? 1 };
    });
    // geometry: one VAO per primitive
    const mesh = J.meshes[0];
    this.prims = mesh.primitives.map((pr) => {
      const vao = gl.createVertexArray(); gl.bindVertexArray(vao);
      const attr = (name, loc, asFloat) => {
        if (loc < 0) return;
        const a = accessor(g, pr.attributes[name]);
        const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
        let data = a.data;
        if (asFloat && !(data instanceof Float32Array)) data = Float32Array.from(data, (v) => (a.normalized ? v / (a.type === 5121 ? 255 : 65535) : v));
        gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(loc);
        if (data instanceof Float32Array) gl.vertexAttribPointer(loc, a.n, GL_FLOAT, false, 0, 0);
        else gl.vertexAttribPointer(loc, a.n, a.type, false, 0, 0);
      };
      const A = this.prog.a;
      attr('POSITION', A.aPos, true); attr('NORMAL', A.aNrm, true);
      attr('JOINTS_0', A.aJnt, false); attr('WEIGHTS_0', A.aWgt, true);
      const ix = accessor(g, pr.indices);
      const ib = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, ix.data, gl.STATIC_DRAW);
      gl.bindVertexArray(null);
      return { vao, count: ix.count, type: ix.type, mat: pr.material ?? 0 };
    });
    // animations: per channel, keyed per node
    this.clips = {};
    for (const an of J.animations || []) {
      const ch = an.channels.map((c) => {
        const s = an.samplers[c.sampler];
        return { node: c.target.node, path: c.target.path, times: accessor(g, s.input).data, values: accessor(g, s.output).data, step: s.interpolation === 'STEP' };
      });
      let len = 0;
      for (const c of ch) len = Math.max(len, c.times[c.times.length - 1]);
      this.clips[an.name] = { ch, len };
    }
  }

  // Sample a clip at a game frame (60 per second) into the node TRS values.
  pose(clipName, frame, loop) {
    const clip = this.clips[clipName] || this.clips.idle;
    for (const n of this.nodes) { n.pt = n.t; n.pr = n.r; n.ps = n.s; }
    if (!clip) return;
    let t = frame / 60;
    if (loop && clip.len > 0) t %= clip.len;
    for (const c of clip.ch) {
      const T = c.times, n = T.length, k = c.path === 'rotation' ? 4 : 3;
      let i = 0;
      if (t >= T[n - 1]) i = n - 1;
      else { let lo = 0, hi = n - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (T[m] <= t) lo = m; else hi = m; } i = lo; }
      const v = c.values, out = new Array(k);
      if (i >= n - 1 || c.step) for (let j = 0; j < k; j++) out[j] = v[i * k + j];
      else {
        const u = (t - T[i]) / (T[i + 1] - T[i]);
        let dot = 0;
        if (k === 4) for (let j = 0; j < 4; j++) dot += v[i * 4 + j] * v[(i + 1) * 4 + j];
        const sgn = dot < 0 ? -1 : 1;
        for (let j = 0; j < k; j++) out[j] = v[i * k + j] * (1 - u) + sgn * v[(i + 1) * k + j] * u;
        if (k === 4) { const l = Math.hypot(...out); for (let j = 0; j < 4; j++) out[j] /= l; }
      }
      const nd = this.nodes[c.node];
      if (c.path === 'translation') nd.pt = out; else if (c.path === 'rotation') nd.pr = out; else if (c.path === 'scale') nd.ps = out;
    }
  }

  updateJoints() {
    for (const i of this.order) {
      const n = this.nodes[i];
      m4.trs(n.pt, n.pr, n.ps, n.local);
      const p = this.parent[i];
      if (p >= 0) m4.mul(this.nodes[p].world, n.local, n.world); else n.world.set(n.local);
    }
    const tmp = new Float32Array(16);
    this.joints.forEach((ni, j) => {
      m4.mul(this.nodes[ni].world, this.ibm.subarray(j * 16, j * 16 + 16), tmp);
      this.jointMats.set(tmp, j * 16);
    });
  }

  // Draw one fighter.
  //   ctx: the game's 2D context, already in world transform (k device px per world px)
  //   x, y: feet in world px; facing: 1 right / -1 left
  //   opts: { colors: { Shirt: '#hex', ... }, flash: '#hex', alpha }
  draw(ctx, k, clip, frame, loop, x, y, facing, opts = {}) {
    if (!this.ready) return false;
    const gl = this.gl;
    // the box drawn around his feet, in world px (room for big swings and props)
    const BW = 120, BH = 110, FX0 = 60, FY0 = 82;
    const scale = Math.min(6, Math.max(1, k));
    const W = Math.ceil(BW * scale), H = Math.ceil(BH * scale);
    if (this.canvas.width !== W || this.canvas.height !== H) { this.canvas.width = W; this.canvas.height = H; }
    this.pose(clip, frame, loop);
    this.updateJoints();
    gl.viewport(0, 0, W, H);
    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL);
    gl.useProgram(this.prog.p);
    const u = this.prog.u;
    // view: glTF axes (x = his left, y = up, z = his front). Camera on his right side, turned toward his front.
    const cy = (CAM_YAW * Math.PI) / 180, cp = (CAM_PITCH * Math.PI) / 180;
    const toCam = [-Math.cos(cy) * Math.cos(cp), Math.sin(cp), Math.sin(cy) * Math.cos(cp)];
    const right = norm(cross([0, 1, 0], toCam)), up = cross(toCam, right);
    // ortho: world metres -> clip. Feet (origin) land at (FX0, FY0) in the box.
    const sx = (PX_PER_M * 2) / BW, sy = (PX_PER_M * 2) / BH;
    const ox = (FX0 / BW) * 2 - 1, oy = 1 - (FY0 / BH) * 2;
    const depth = 1 / 3;
    const view = new Float32Array([
      right[0] * sx, up[0] * sy, -toCam[0] * depth, 0,
      right[1] * sx, up[1] * sy, -toCam[1] * depth, 0,
      right[2] * sx, up[2] * sy, -toCam[2] * depth, 0,
      ox, oy, 0, 1,
    ]);
    gl.uniformMatrix4fv(u.uView, false, view);
    gl.uniformMatrix3fv(u.uViewRot, false, new Float32Array([right[0], up[0], toCam[0], right[1], up[1], toCam[1], right[2], up[2], toCam[2]]));
    gl.uniformMatrix4fv(u.uJoints, false, this.jointMats);
    const fl = opts.flash ? [...srgbToLinear(opts.flash), 0.65] : [0, 0, 0, 0];
    gl.uniform4fv(u.uFlash, fl);
    // outline pass: back faces pushed out along the normal
    gl.enable(gl.CULL_FACE); gl.cullFace(gl.FRONT);
    gl.uniform1f(u.uOutlinePass, 1);
    gl.uniform1f(u.uOutline, (0.85 / PX_PER_M) * Math.min(1.4, 2.2 / scale + 0.35));
    for (const pr of this.prims) {
      const m = this.materials[pr.mat];
      if (m && /^(Highlight|Catch|MouthIn|Teeth|Sclera|Iris|Pupil|LashLine|Lips|Mole)/.test(m.name)) continue;
      gl.bindVertexArray(pr.vao); gl.drawElements(gl.TRIANGLES, pr.count, pr.type, 0);
    }
    gl.disable(gl.CULL_FACE);
    gl.uniform1f(u.uOutlinePass, 0); gl.uniform1f(u.uOutline, 0);
    const over = opts.colors || {};
    for (const pr of this.prims) {
      const m = this.materials[pr.mat] || { color: [1, 1, 1], rough: 1, metal: 0, name: '' };
      const c = over[m.name] ? srgbToLinear(over[m.name]) : m.color;
      gl.uniform4f(u.uColor, c[0], c[1], c[2], 1);
      gl.uniform2f(u.uMat, m.rough, m.metal);
      gl.bindVertexArray(pr.vao); gl.drawElements(gl.TRIANGLES, pr.count, pr.type, 0);
    }
    gl.bindVertexArray(null);
    // copy into the game canvas at his feet, mirrored when facing left
    ctx.save();
    ctx.translate(x, y);
    if (facing < 0) ctx.scale(-1, 1);
    if (opts.alpha !== undefined) ctx.globalAlpha *= opts.alpha;
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(this.canvas, -FX0, -FY0, BW, BH);
    ctx.restore();
    return true;
  }
}

function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
function norm(a) { const l = Math.hypot(...a); return [a[0] / l, a[1] / l, a[2] / l]; }

// One shared model per URL.
const cache = new Map();
export function getModel(url) {
  if (!cache.has(url)) { const m = new Model3D(); cache.set(url, m); m.load(url); }
  return cache.get(url);
}
