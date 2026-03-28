import * as THREE from 'three';

// ─────────────────────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────────────────────
const API_BASE         = 'https://ai-lead-responder-production.up.railway.app';
const ROAD_WIDTH       = 6;
const LANE_X           = [-2, 0, 2];
const SEG_LEN          = 20;
const SEG_POOL         = 12;
const OBS_POOL         = 20;
const SPEED_BASE       = 14;
const SPEED_MAX_MULT   = 3.0;
const SCORE_RATE       = 10;
const LANE_TWEEN_SPD   = 9;   // units/sec for lane change tween

const C_BG      = 0x0a0a0a;
const C_RED     = 0xe31e24;
const C_DARK    = 0x111111;
const C_ROAD    = 0x181818;
const C_LINE    = 0xffffff;
const C_VAN     = 0xe31e24;
const C_GLASS   = 0x1a3a5c;
const C_WHEEL   = 0x1a1a1a;
const C_KERB_A  = 0xe31e24;
const C_KERB_B  = 0xeeeeee;
const C_CRATE   = 0xe31e24;
const C_BARREL  = 0xffcc00;
const C_BARRIER = 0xcc2222;

// ─────────────────────────────────────────────────────────────
// RENDERER + SCENE
// ─────────────────────────────────────────────────────────────
const canvas   = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type    = THREE.PCFSoftShadowMap;

const scene  = new THREE.Scene();
scene.background = new THREE.Color(C_BG);
scene.fog        = new THREE.FogExp2(C_BG, 0.02);

const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 260);
camera.position.set(0, 3.6, 7.2);
camera.lookAt(0, 0.4, -6);

function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
resize();
window.addEventListener('resize', resize);

// ─────────────────────────────────────────────────────────────
// LIGHTING
// ─────────────────────────────────────────────────────────────
scene.add(new THREE.AmbientLight(0x111111, 2));

const dirLight = new THREE.DirectionalLight(0xffffff, 1.4);
dirLight.position.set(4, 10, 6);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width  = 1024;
dirLight.shadow.mapSize.height = 1024;
scene.add(dirLight);

const vanGlow = new THREE.PointLight(C_RED, 6, 14);
vanGlow.position.set(0, 0.5, 0);
scene.add(vanGlow);

const overheadSpot = new THREE.SpotLight(0xffffff, 1.2, 50, Math.PI / 8);
overheadSpot.position.set(0, 22, -5);
overheadSpot.target.position.set(0, 0, -20);
scene.add(overheadSpot, overheadSpot.target);

// ─────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────
function toon(color, transparent = false, opacity = 1) {
  return new THREE.MeshToonMaterial({ color, transparent, opacity });
}
function box(w, h, d, mat) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
  m.castShadow = m.receiveShadow = true;
  return m;
}
function cylinder(r, h, seg, mat) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat);
  m.castShadow = true;
  return m;
}

// ─────────────────────────────────────────────────────────────
// VAN
// ─────────────────────────────────────────────────────────────
function buildVan() {
  const g = new THREE.Group();

  // body
  const body = box(2.0, 0.88, 1.08, toon(C_VAN));
  body.position.set(-0.22, 0.44, 0);
  g.add(body);

  // cab
  const cab = box(0.82, 0.72, 1.04, toon(0xcc1a1f));
  cab.position.set(0.82, 0.36, 0);
  g.add(cab);

  // windshield
  const ws = box(0.06, 0.46, 0.82, toon(C_GLASS, true, 0.65));
  ws.position.set(1.17, 0.58, 0);
  ws.rotation.z = 0.38;
  g.add(ws);

  // roof rack
  const rack = box(1.85, 0.07, 0.88, toon(C_DARK));
  rack.position.set(-0.18, 0.91, 0);
  g.add(rack);

  // front bumper
  const bumper = box(0.14, 0.22, 1.0, toon(0x222222));
  bumper.position.set(1.26, 0.11, 0);
  g.add(bumper);

  // headlights
  for (const z of [-0.3, 0.3]) {
    const hl = box(0.07, 0.13, 0.15, new THREE.MeshStandardMaterial({
      color: 0xfff8cc, emissive: 0xfff8cc, emissiveIntensity: 2
    }));
    hl.position.set(1.3, 0.38, z);
    g.add(hl);
  }

  // side mirrors
  for (const z of [-0.56, 0.56]) {
    const mir = box(0.26, 0.1, 0.07, toon(C_DARK));
    mir.position.set(0.9, 0.72, z);
    g.add(mir);
  }

  // wheels
  const wheelMat = toon(C_WHEEL);
  const rimMat   = toon(0x444444);
  const wheelPos = [
    [ 0.76, 0.22,  0.58],
    [ 0.76, 0.22, -0.58],
    [-0.76, 0.22,  0.58],
    [-0.76, 0.22, -0.58],
  ];
  for (const [x, y, z] of wheelPos) {
    const w = cylinder(0.22, 0.2, 14, wheelMat);
    w.rotation.z = Math.PI / 2;
    w.position.set(x, y, z);
    g.add(w);

    const rim = cylinder(0.13, 0.21, 6, rimMat);
    rim.rotation.z = Math.PI / 2;
    rim.position.set(x, y, z);
    g.add(rim);
  }

  // logo stripe
  const stripe = box(1.6, 0.18, 0.02, toon(C_DARK));
  stripe.position.set(-0.2, 0.44, 0.55);
  g.add(stripe);

  return g;
}

const van = buildVan();
van.position.set(0, 0, 0);
scene.add(van);
vanGlow.position.set(0, 0.3, 0);
van.add(vanGlow);

// ─────────────────────────────────────────────────────────────
// ROAD SEGMENTS (object pool)
// ─────────────────────────────────────────────────────────────
function buildSegment() {
  const g = new THREE.Group();

  // asphalt
  const road = new THREE.Mesh(
    new THREE.PlaneGeometry(ROAD_WIDTH, SEG_LEN),
    toon(C_ROAD)
  );
  road.rotation.x = -Math.PI / 2;
  road.receiveShadow = true;
  g.add(road);

  // ground shoulders
  for (const side of [-1, 1]) {
    const shoulder = new THREE.Mesh(
      new THREE.PlaneGeometry(16, SEG_LEN),
      toon(0x0d0d0d)
    );
    shoulder.rotation.x = -Math.PI / 2;
    shoulder.position.x = side * (ROAD_WIDTH / 2 + 8);
    shoulder.receiveShadow = true;
    g.add(shoulder);
  }

  // lane dividers
  for (const x of [-1, 1]) {
    const line = box(0.06, 0.02, SEG_LEN - 1, toon(C_LINE, true, 0.4));
    line.position.set(x, 0.012, 0);
    g.add(line);
  }

  // kerbs (alternating red/white every 2 units)
  const kerbCount = Math.floor(SEG_LEN / 2);
  for (let i = 0; i < kerbCount; i++) {
    const col = i % 2 === 0 ? C_KERB_A : C_KERB_B;
    for (const side of [-1, 1]) {
      const k = box(0.3, 0.1, 1.9, toon(col));
      k.position.set(side * (ROAD_WIDTH / 2 + 0.15), 0.05, -SEG_LEN / 2 + 1 + i * 2);
      g.add(k);
    }
  }

  // side walls (tunnel atmosphere)
  for (const side of [-1, 1]) {
    const wall = box(0.12, 2.8, SEG_LEN, toon(0x0f0f0f));
    wall.position.set(side * (ROAD_WIDTH / 2 + 0.06), 1.4, 0);
    g.add(wall);
  }

  return g;
}

const segments = [];
for (let i = 0; i < SEG_POOL; i++) {
  const seg = buildSegment();
  seg.position.z = -i * SEG_LEN;
  seg.userData.zBase = seg.position.z;
  scene.add(seg);
  segments.push(seg);
}

// ─────────────────────────────────────────────────────────────
// OBSTACLES (object pool)
// ─────────────────────────────────────────────────────────────
function buildCrate() {
  const g = new THREE.Group();
  const body = box(0.82, 0.82, 0.82, toon(C_CRATE));
  g.add(body);
  // X markings
  for (const rot of [Math.PI / 4, -Math.PI / 4]) {
    const b = box(0.08, 0.7, 0.02, toon(C_DARK));
    b.rotation.z = rot;
    b.position.z = 0.42;
    g.add(b);
  }
  g.position.y = 0.41;
  return g;
}

function buildBarrel() {
  const g = new THREE.Group();
  const body = cylinder(0.3, 0.76, 14, toon(C_BARREL));
  g.add(body);
  // dark stripes
  for (const y of [-0.2, 0.2]) {
    const stripe = cylinder(0.31, 0.12, 14, toon(C_DARK));
    stripe.position.y = y;
    g.add(stripe);
  }
  g.position.y = 0.38;
  return g;
}

function buildBarrier() {
  const g = new THREE.Group();
  const body = box(1.7, 0.58, 0.35, toon(C_BARRIER));
  g.add(body);
  // stripes
  for (let i = -3; i <= 3; i += 2) {
    const s = box(0.18, 0.56, 0.36, toon(0xffaa00, true, 0.9));
    s.position.x = i * 0.22;
    g.add(s);
  }
  g.position.y = 0.29;
  return g;
}

const obsPool = [];
for (let i = 0; i < OBS_POOL; i++) {
  const type = i % 3;
  const obj  = type === 0 ? buildCrate() : type === 1 ? buildBarrel() : buildBarrier();
  obj.userData.type   = type;
  obj.userData.active = false;
  obj.visible         = false;
  scene.add(obj);
  obsPool.push(obj);
}

function getObstacle() {
  return obsPool.find(o => !o.userData.active) || null;
}

// ─────────────────────────────────────────────────────────────
// GAME STATE
// ─────────────────────────────────────────────────────────────
let state       = 'IDLE';   // IDLE | PLAYING | DEAD | SUBMITTING
let score       = 0;
let elapsed     = 0;
let lane        = 1;        // 0 = left, 1 = center, 2 = right
let targetX     = LANE_X[1];
let speedMult   = 1;
let lastSegZ    = -(SEG_POOL - 1) * SEG_LEN;
let shakeTimer  = 0;

// HUD elements
const scoreDisplay = document.getElementById('scoreDisplay');
const speedDisplay = document.getElementById('speedDisplay');
const overlay      = document.getElementById('overlay');
const ovTitle      = document.getElementById('ovTitle');
const ovSub        = document.getElementById('ovSub');
const ovScore      = document.getElementById('ovScore');
const nameInput    = document.getElementById('nameInput');
const startBtn     = document.getElementById('startBtn');
const miniLb       = document.getElementById('miniLb');
const miniLbBody   = document.getElementById('miniLbBody');

// ─────────────────────────────────────────────────────────────
// INPUT
// ─────────────────────────────────────────────────────────────
function moveLane(dir) {
  if (state !== 'PLAYING') return;
  lane = Math.max(0, Math.min(2, lane + dir));
  targetX = LANE_X[lane];
}

window.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft'  || e.key === 'a' || e.key === 'A') moveLane(-1);
  if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') moveLane(+1);
  if ((e.key === ' ' || e.key === 'Enter') && state === 'IDLE') startGame();
});

let touchStartX = 0;
window.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
window.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(dx) > 40) moveLane(dx < 0 ? -1 : 1);
});

startBtn.addEventListener('click', () => {
  if (state === 'IDLE') startGame();
});

// ─────────────────────────────────────────────────────────────
// GAME CONTROL
// ─────────────────────────────────────────────────────────────
function resetWorld() {
  for (let i = 0; i < SEG_POOL; i++) {
    segments[i].position.z = -i * SEG_LEN;
    // clear obstacles on segments
    for (const obs of obsPool) {
      obs.userData.active = false;
      obs.visible = false;
    }
  }
  lastSegZ = -(SEG_POOL - 1) * SEG_LEN;
  van.position.x = 0;
  van.position.y = 0;
  van.rotation.set(0, Math.PI, 0);
  lane   = 1;
  targetX = LANE_X[1];
  score  = 0;
  elapsed = 0;
  speedMult = 1;
  shakeTimer = 0;
}

function startGame() {
  resetWorld();
  state = 'PLAYING';
  overlay.classList.add('hidden');
}

function endGame() {
  state = 'DEAD';
  shakeTimer = 0.4;

  ovTitle.textContent = 'GAME OVER';
  ovSub.textContent   = 'Tvoje skóre:';
  ovScore.textContent = Math.floor(score).toLocaleString('cs-CZ');
  ovScore.classList.remove('hidden');
  miniLb.classList.add('hidden');
  startBtn.textContent = 'HRÁT ZNOVU';

  setTimeout(() => {
    overlay.classList.remove('hidden');
    startBtn.onclick = () => submitAndRestart();
  }, 600);
}

async function submitAndRestart() {
  const name = nameInput.value.trim().toUpperCase() || 'ANONYM';
  startBtn.disabled = true;
  startBtn.textContent = 'Ukládám...';
  state = 'SUBMITTING';

  try {
    await fetch(`${API_BASE}/api/leaderboard`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, score: Math.floor(score) }),
    });
    const res    = await fetch(`${API_BASE}/api/leaderboard`);
    const { scores } = await res.json();
    renderMiniLb(scores);
    miniLb.classList.remove('hidden');
  } catch {
    // silently ignore network errors
  }

  startBtn.disabled    = false;
  startBtn.textContent = 'HRÁT ZNOVU';
  startBtn.onclick     = () => startGame();
}

function renderMiniLb(scores) {
  if (!scores || scores.length === 0) {
    miniLbBody.innerHTML = '<tr><td colspan="3" style="color:#555;text-align:center;padding:10px;">Žádné skóre</td></tr>';
    return;
  }
  miniLbBody.innerHTML = scores.slice(0, 5).map((s, i) => {
    const cls = i === 0 ? 'rank-1' : i === 1 ? 'rank-2' : i === 2 ? 'rank-3' : '';
    return `<tr class="${cls}">
      <td>${i + 1}</td>
      <td>${escHtml(s.name.toUpperCase())}</td>
      <td>${Number(s.score).toLocaleString('cs-CZ')}</td>
    </tr>`;
  }).join('');
}

function escHtml(s) {
  return s.replace(/[&<>"']/g, m => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[m]));
}

// ─────────────────────────────────────────────────────────────
// OBSTACLE SPAWNING
// ─────────────────────────────────────────────────────────────
function spawnObstaclesOnSegment(seg) {
  // Probability grows with speedMult, max 2 obstacles per segment
  const prob   = Math.min(0.85, 0.25 + speedMult * 0.18);
  if (Math.random() > prob) return;

  const count  = Math.random() < 0.25 && speedMult > 1.5 ? 2 : 1;
  const freeLanes = [0, 1, 2];

  for (let i = 0; i < count; i++) {
    if (freeLanes.length < 2) break; // always leave at least 1 free
    const idx = Math.floor(Math.random() * freeLanes.length);
    const l   = freeLanes.splice(idx, 1)[0];
    const obs = getObstacle();
    if (!obs) break;

    obs.position.x        = LANE_X[l];
    obs.position.z        = seg.position.z;
    obs.position.y        = 0;
    obs.userData.active   = true;
    obs.userData.laneIdx  = l;
    obs.visible           = true;
  }
}

// ─────────────────────────────────────────────────────────────
// COLLISION (AABB)
// ─────────────────────────────────────────────────────────────
function checkCollision() {
  const vx = van.position.x;
  for (const obs of obsPool) {
    if (!obs.userData.active) continue;
    const dz = Math.abs(obs.position.z - van.position.z);
    if (dz > 1.4) continue;
    const dx = Math.abs(obs.position.x - vx);
    const halfW = obs.userData.type === 2 ? 1.0 : 0.55;
    if (dx < halfW + 0.55) return true;
  }
  return false;
}

// ─────────────────────────────────────────────────────────────
// MAIN LOOP
// ─────────────────────────────────────────────────────────────
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.05);

  if (state === 'PLAYING') {
    elapsed   += dt;
    speedMult  = Math.min(SPEED_MAX_MULT, 1.0 + Math.floor(elapsed / 10) * 0.1);
    const spd  = SPEED_BASE * speedMult;
    score     += SCORE_RATE * speedMult * dt;

    // update HUD
    scoreDisplay.textContent = Math.floor(score).toLocaleString('cs-CZ');
    speedDisplay.textContent = speedMult.toFixed(1) + '×';

    // lane tween
    van.position.x += (targetX - van.position.x) * Math.min(1, LANE_TWEEN_SPD * dt);

    // subtle camera bob
    camera.position.y = 3.6 + Math.sin(elapsed * 7) * 0.018 * speedMult;

    // wheel spin
    van.children.forEach(c => {
      if (c.geometry && c.geometry.type === 'CylinderGeometry' && c.position.y < 0.5) {
        c.rotation.x += spd * dt * 1.8;
      }
    });

    // move road segments
    for (const seg of segments) {
      seg.position.z += spd * dt;
      if (seg.position.z > camera.position.z + SEG_LEN) {
        // recycle to back
        seg.position.z -= SEG_POOL * SEG_LEN;
        spawnObstaclesOnSegment(seg);
      }
    }

    // move obstacles
    for (const obs of obsPool) {
      if (!obs.userData.active) continue;
      obs.position.z += spd * dt;
      if (obs.position.z > camera.position.z + SEG_LEN) {
        obs.userData.active = false;
        obs.visible = false;
      }
    }

    // van glow follows lane
    vanGlow.position.x = van.position.x;

    // collision
    if (checkCollision()) endGame();

  } else if (state === 'IDLE') {
    // idle: road scrolls slowly for visual polish
    const idleSpd = 4;
    for (const seg of segments) {
      seg.position.z += idleSpd * dt;
      if (seg.position.z > camera.position.z + SEG_LEN) {
        seg.position.z -= SEG_POOL * SEG_LEN;
      }
    }
  }

  // shake on death
  if (shakeTimer > 0) {
    shakeTimer -= dt;
    van.position.x = targetX + Math.sin(shakeTimer * 80) * 0.12;
  }

  renderer.render(scene, camera);
}

// ─────────────────────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────────────────────
van.rotation.y = Math.PI; // face forward
animate();
