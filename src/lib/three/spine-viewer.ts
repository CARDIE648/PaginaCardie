import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

/** Regiones que se pueden explorar (las claves vienen de los extras del GLB). */
export type RegionKey = 'Cervical' | 'Thoracic' | 'Lumbar' | 'Pelvis';
export const REGION_KEYS: RegionKey[] = ['Cervical', 'Thoracic', 'Lumbar', 'Pelvis'];

export interface HoverInfo { label: string; region: RegionKey; x: number; y: number }

export interface SpineViewerOptions {
  onHover?(info: HoverInfo | null): void;
  onSelect?(region: RegionKey | null): void;
  onInteract?(): void;
  onFailure?(): void;
  /** Dónde queda la ficha de información: 'right' en escritorio, 'bottom' en celular. */
  panelSide?(): 'right' | 'bottom';
}

export interface SpineViewer {
  select(region: RegionKey | null): void;
  setAutoRotate(value: boolean): void;
  rotate(amount: number): void;
  destroy(): void;
}

const ABBR: Record<string, string> = { Cervical: 'C', Thoracic: 'T', Lumbar: 'L' };
const NAMES: Record<RegionKey, string> = { Cervical: 'Cervical', Thoracic: 'Torácica', Lumbar: 'Lumbar', Pelvis: 'Pelvis' };

function regionOf(o: THREE.Object3D): RegionKey | null {
  const r = o.userData.region as string | undefined;
  if (r === 'Sacral' || r === 'Pelvic') return 'Pelvis';
  return (REGION_KEYS as string[]).includes(r ?? '') ? (r as RegionKey) : null;
}

function labelOf(o: THREE.Object3D, region: RegionKey): string {
  const n = o.name.replace(/[._]\d{3}$/, '');
  let m = n.match(/^(Cervical|Thoracic|Lumbar)_(\d+)$/);
  if (m) return `${ABBR[m[1]]}${m[2]} · ${NAMES[region]}`;
  m = n.match(/^Disc_(Cervical|Thoracic|Lumbar)_(\d+)$/);
  if (m) return `Disco ${ABBR[m[1]]}${m[2]}`;
  if (n.startsWith('Axis')) return `C2 · ${NAMES.Cervical}`;
  if (n.startsWith('Sacrum')) return 'Sacro';
  if (n.startsWith('Coccyx')) return 'Cóccix';
  if (n.startsWith('Pelvis')) return 'Hueso coxal';
  if (n.startsWith('Pubic')) return 'Sínfisis púbica';
  return NAMES[region];
}

export async function createSpineViewer(host: HTMLElement, opts: SpineViewerOptions = {}): Promise<SpineViewer> {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.02;

  const scene = new THREE.Scene();
  // Reflejos suaves de estudio: el hueso deja de verse plano
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTexture = pmrem.fromScene(new RoomEnvironment(), .04).texture;
  scene.environment = envTexture;
  scene.environmentIntensity = .55;
  pmrem.dispose();

  const camera = new THREE.PerspectiveCamera(30, 1, .1, 200);
  const canvas = renderer.domElement;
  canvas.setAttribute('aria-label', 'Columna vertebral 3D interactiva. Arrastra para girarla y toca una zona para ver su información.');
  canvas.setAttribute('role', 'img');
  // En celular el desplazamiento vertical de la página sigue funcionando
  canvas.style.touchAction = 'pan-y';

  scene.add(new THREE.HemisphereLight(0xf1faff, 0x3d5a60, 1.1));
  for (const [p, color, intensity] of [
    [[-6, 9, 10], 0xfff2db, 3.2], [[7, 3, -6], 0xb8f8ec, 4.6], [[4, -5, 8], 0xffffff, 1.0]
  ] as const) {
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.set(p[0], p[1], p[2]); scene.add(light);
  }

  let gltf;
  try { gltf = await new GLTFLoader().loadAsync('/models/cardie-spine.glb'); }
  catch (error) { renderer.dispose(); envTexture.dispose(); throw error; }

  const pivot = new THREE.Group();
  const model = gltf.scene;
  pivot.add(model); scene.add(pivot);
  const bounds = new THREE.Box3().setFromObject(model);
  const center = bounds.getCenter(new THREE.Vector3());
  model.position.sub(center);
  const size = bounds.getSize(new THREE.Vector3());

  type Surface = { mesh: THREE.Mesh; material: THREE.MeshStandardMaterial; base: THREE.Color; region: RegionKey | null; disc: boolean };
  const surfaces: Surface[] = [];
  const byMesh = new Map<THREE.Object3D, Surface>();
  const regionBoxes = new Map<RegionKey, THREE.Box3>();
  scene.updateMatrixWorld(true);
  model.traverse((o) => {
    if (!(o instanceof THREE.Mesh)) return;
    const mat = (o.material as THREE.MeshStandardMaterial).clone();
    o.material = mat;
    let region: RegionKey | null = null;
    for (let p: THREE.Object3D | null = o; p && !region; p = p.parent) region = regionOf(p);
    const disc = /^Disc_/.test(o.name) || /^Disc_/.test(o.parent?.name ?? '');
    if (!disc) { mat.roughness = .55; mat.metalness = 0; }
    const s = { mesh: o, material: mat, base: mat.color.clone(), region, disc };
    surfaces.push(s); byMesh.set(o, s);
    if (region) {
      const box = regionBoxes.get(region) ?? new THREE.Box3();
      box.expandByObject(o); regionBoxes.set(region, box);
    }
  });

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let autoRotate = !reduced;
  let visible = true;
  let last = 0;
  let time = 0;
  let selected: RegionKey | null = null;
  let hovered: RegionKey | null = null;
  let hoverMesh: THREE.Object3D | null = null;
  let idleSince = performance.now();
  const dimColor = new THREE.Color(0x5d8088);

  // Estado animado de cámara y giro (se amortigua hacia el objetivo)
  let yaw = -.35, targetYaw = yaw, yawVelocity = 0;
  let pitch = 0, targetPitch = 0;
  const cam = { y: 0, dist: 30, offsetX: 0, offsetY: 0 };
  const goal = { y: 0, dist: 30, offsetX: 0, offsetY: 0 };

  function fullDistance() {
    const t = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    return Math.max(size.y / (2 * t) * 1.06, size.x / (2 * t * camera.aspect) * 1.5);
  }

  function computeGoal() {
    const w = host.clientWidth, h = host.clientHeight;
    const side = opts.panelSide?.() ?? 'right';
    const box = selected ? regionBoxes.get(selected) : undefined;
    if (box) {
      const c = box.getCenter(new THREE.Vector3()); const s = box.getSize(new THREE.Vector3());
      const t = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
      const span = Math.max(s.y, s.x / Math.max(camera.aspect, .5), 2);
      goal.y = c.y;
      goal.dist = Math.min(fullDistance(), span / (2 * t) * (side === 'bottom' ? 2.3 : 2));
      goal.offsetX = side === 'right' ? w * .2 : 0;
      goal.offsetY = side === 'bottom' ? h * .17 : 0;
    } else {
      goal.y = 0; goal.dist = fullDistance(); goal.offsetX = 0; goal.offsetY = 0;
    }
  }

  function resize() {
    const w = host.clientWidth, h = host.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    canvas.style.width = '100%'; canvas.style.height = '100%';
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const first = cam.dist === 30 && goal.dist === 30;
    computeGoal();
    if (first) Object.assign(cam, goal);
    draw(performance.now(), true);
  }

  const raycaster = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  function pick(clientX: number, clientY: number) {
    const rect = canvas.getBoundingClientRect();
    ndc.set(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
    raycaster.setFromCamera(ndc, camera);
    for (const hit of raycaster.intersectObject(model, true)) {
      const s = byMesh.get(hit.object);
      if (s?.region) return { surface: s, region: s.region };
    }
    return null;
  }

  function paint() {
    const pulse = .5 + .5 * Math.sin(time * 2.4);
    for (const s of surfaces) {
      const isSel = selected !== null && s.region === selected;
      const isHover = hovered !== null && s.region === hovered && !isSel;
      const dim = selected !== null && !isSel;
      s.material.color.copy(s.base);
      if (dim && !s.disc) s.material.color.lerp(dimColor, .62);
      s.material.emissive.setHex(isSel || isHover || s.disc ? 0x4dbaaa : 0x000000);
      s.material.emissiveIntensity = isSel ? (s.disc ? .9 : .3 + (reduced ? 0 : .12 * pulse))
        : isHover ? .12 : s.disc ? (dim ? .04 : .18) : 0;
    }
    const hs = hoverMesh ? byMesh.get(hoverMesh) : undefined;
    if (hs) { hs.material.emissive.setHex(0x8ff5e4); hs.material.emissiveIntensity = .4; }
  }

  function draw(now: number, force = false) {
    if (!force && (!visible || document.hidden)) { last = 0; return; }
    const delta = last ? Math.min((now - last) / 1000, .05) : .016; last = now;
    time += delta;
    // Giro automático solo cuando nadie lo está usando
    if (autoRotate && !dragging && !selected && now - idleSince > 4000) targetYaw += delta * .24;
    if (!dragging && Math.abs(yawVelocity) > .0001) { targetYaw += yawVelocity; yawVelocity *= Math.pow(.004, delta); }
    yaw = THREE.MathUtils.damp(yaw, targetYaw, 9, delta);
    pitch = THREE.MathUtils.damp(pitch, targetPitch, 9, delta);
    for (const k of ['y', 'dist', 'offsetX', 'offsetY'] as const) cam[k] = THREE.MathUtils.damp(cam[k], goal[k], 4, delta);
    pivot.rotation.set(pitch, yaw, 0);
    camera.position.set(0, cam.y + cam.dist * .06, cam.dist);
    camera.lookAt(0, cam.y, 0);
    const w = host.clientWidth, h = host.clientHeight;
    if (Math.abs(cam.offsetX) > .5 || Math.abs(cam.offsetY) > .5) camera.setViewOffset(w, h, cam.offsetX, cam.offsetY, w, h);
    else camera.clearViewOffset();
    paint();
    renderer.render(scene, camera);
  }

  // ── Arrastrar para girar, tocar para seleccionar ───────────────────────────
  let dragging = false, downX = 0, downY = 0, lastX = 0, lastY = 0, moved = 0, pointerId = -1;
  function touched() { idleSince = performance.now(); opts.onInteract?.(); }
  function onDown(e: PointerEvent) {
    if (e.button !== 0) return;
    dragging = true; pointerId = e.pointerId; moved = 0; yawVelocity = 0;
    downX = lastX = e.clientX; downY = lastY = e.clientY;
    touched();
  }
  function onMove(e: PointerEvent) {
    if (dragging && e.pointerId === pointerId) {
      const dx = e.clientX - lastX, dy = e.clientY - lastY;
      lastX = e.clientX; lastY = e.clientY;
      moved = Math.max(moved, Math.hypot(e.clientX - downX, e.clientY - downY));
      if (moved > 5) {
        if (!canvas.hasPointerCapture(e.pointerId)) canvas.setPointerCapture(e.pointerId);
        canvas.style.cursor = 'grabbing';
        const k = 5.5 / Math.max(host.clientWidth, 320);
        targetYaw += dx * k; yawVelocity = dx * k * .5;
        if (e.pointerType === 'mouse') targetPitch = THREE.MathUtils.clamp(targetPitch + dy * k * .5, -.3, .3);
        hovered = null; hoverMesh = null; opts.onHover?.(null);
      }
      touched();
      return;
    }
    if (e.pointerType !== 'mouse') return;
    const hit = pick(e.clientX, e.clientY);
    const rect = host.getBoundingClientRect();
    hovered = hit?.region ?? null; hoverMesh = hit?.surface.mesh ?? null;
    canvas.style.cursor = hit ? 'pointer' : 'grab';
    opts.onHover?.(hit ? { label: labelOf(hit.surface.mesh, hit.region), region: hit.region, x: e.clientX - rect.left, y: e.clientY - rect.top } : null);
  }
  function onUp(e: PointerEvent) {
    if (!dragging || e.pointerId !== pointerId) return;
    dragging = false; canvas.style.cursor = 'grab';
    if (canvas.hasPointerCapture(e.pointerId)) canvas.releasePointerCapture(e.pointerId);
    if (moved <= 6) {
      const hit = pick(e.clientX, e.clientY);
      const next = hit ? hit.region : null;
      api.select(next); opts.onSelect?.(next);
    }
    touched();
  }
  function onCancel() { dragging = false; canvas.style.cursor = 'grab'; }
  function onLeave() { hovered = null; hoverMesh = null; opts.onHover?.(null); }

  function syncLoop() {
    last = 0;
    renderer.setAnimationLoop(visible && !document.hidden ? (now) => draw(now) : null);
  }
  function lost(event: Event) {
    event.preventDefault(); renderer.setAnimationLoop(null); canvas.style.opacity = '0'; opts.onFailure?.();
  }

  const resizeObserver = new ResizeObserver(resize);
  const visibility = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; syncLoop(); });
  host.appendChild(canvas);
  canvas.style.cursor = 'grab';
  resizeObserver.observe(host); visibility.observe(host);
  canvas.addEventListener('pointerdown', onDown);
  canvas.addEventListener('pointermove', onMove);
  canvas.addEventListener('pointerup', onUp);
  canvas.addEventListener('pointercancel', onCancel);
  canvas.addEventListener('pointerleave', onLeave);
  document.addEventListener('visibilitychange', syncLoop);
  canvas.addEventListener('webglcontextlost', lost);
  resize(); syncLoop();

  const api: SpineViewer = {
    select(region) {
      selected = region; computeGoal(); idleSince = performance.now(); targetPitch = 0;
      // Vista 3/4 hacia el frente para que la zona se lea mejor
      if (region) targetYaw = Math.round((targetYaw + .45) / (Math.PI * 2)) * Math.PI * 2 - .45;
    },
    setAutoRotate(value) { autoRotate = value && !reduced; },
    rotate(amount) { targetYaw += amount; touched(); },
    destroy() {
      renderer.setAnimationLoop(null); resizeObserver.disconnect(); visibility.disconnect();
      canvas.removeEventListener('pointerdown', onDown); canvas.removeEventListener('pointermove', onMove);
      canvas.removeEventListener('pointerup', onUp); canvas.removeEventListener('pointercancel', onCancel);
      canvas.removeEventListener('pointerleave', onLeave);
      document.removeEventListener('visibilitychange', syncLoop);
      canvas.removeEventListener('webglcontextlost', lost);
      const geometries = new Set<THREE.BufferGeometry>();
      for (const s of surfaces) { geometries.add(s.mesh.geometry); s.material.dispose(); }
      for (const g of geometries) g.dispose();
      envTexture.dispose(); renderer.dispose(); canvas.remove();
    }
  };
  return api;
}
