<script lang="ts">
  // Explorador 3D de la columna (sección "Biomecánica").
  // Three.js y el modelo se cargan solo cuando la sección se acerca a la pantalla.
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import type { SpineViewer, RegionKey, HoverInfo } from '$lib/three/spine-viewer';

  type Region = { key: RegionKey; name: string; range: string; count: string; role: string; signs: string[] };
  const regions: Region[] = [
    {
      key: 'Cervical', name: 'Cervical', range: 'C1 – C7', count: '7 vértebras',
      role: 'Sostiene la cabeza y le da su movilidad. Es la zona más flexible de la columna.',
      signs: ['Dolor o rigidez de cuello', 'Tensión en hombros', 'Dolor de cabeza tensional']
    },
    {
      key: 'Thoracic', name: 'Torácica', range: 'T1 – T12', count: '12 vértebras',
      role: 'Ancla las costillas, protege la caja torácica y da estabilidad al tronco.',
      signs: ['Dolor de espalda alta', 'Rigidez entre omóplatos', 'Postura encorvada']
    },
    {
      key: 'Lumbar', name: 'Lumbar', range: 'L1 – L5', count: '5 vértebras',
      role: 'Carga la mayor parte del peso del cuerpo y permite flexionar y girar el tronco.',
      signs: ['Dolor de espalda baja', 'Dolor que baja a la pierna', 'Molestia al estar sentado']
    },
    {
      key: 'Pelvis', name: 'Pelvis', range: 'Sacro · cóccix · cadera', count: 'Base de la columna',
      role: 'Reparte el peso entre la columna y las piernas; su balance afecta toda la postura.',
      signs: ['Desbalance de cadera', 'Dolor en glúteo o sacro', 'Molestia al caminar']
    }
  ];

  let container: HTMLDivElement;
  let viewer: SpineViewer | undefined;
  let ready = $state(false);
  let failed = $state(false);
  let selected = $state<RegionKey | null>(null);
  let hover = $state<HoverInfo | null>(null);
  let interacted = $state(false);
  let narrow = $state(false);
  const current = $derived(regions.find((r) => r.key === selected) ?? null);

  function choose(key: RegionKey | null) {
    selected = selected === key ? null : key;
    viewer?.select(selected);
    interacted = true;
  }

  onMount(() => {
    let disposed = false;
    const mq = window.matchMedia('(max-width: 639px)');
    narrow = mq.matches;
    const onMq = () => { narrow = mq.matches; viewer?.select(selected); };
    mq.addEventListener('change', onMq);

    const observer = new IntersectionObserver(async ([entry]) => {
      if (!entry.isIntersecting) return;
      observer.disconnect();
      try {
        const { createSpineViewer } = await import('$lib/three/spine-viewer');
        if (disposed) return;
        viewer = await createSpineViewer(container, {
          onHover: (h) => (hover = h),
          onSelect: (r) => { selected = r; interacted = true; },
          onInteract: () => (interacted = true),
          onFailure: () => { ready = false; failed = true; },
          panelSide: () => (mq.matches ? 'bottom' : 'right')
        });
        if (disposed) { viewer.destroy(); return; }
        ready = true;
      } catch (error) {
        failed = true;
        console.warn('CARDIE: se usa la imagen fija de la columna.', error);
      }
    }, { rootMargin: '240px' });
    observer.observe(container);

    return () => {
      disposed = true; observer.disconnect(); mq.removeEventListener('change', onMq); viewer?.destroy();
    };
  });
</script>

<div class="explorer" bind:this={container} data-ready={ready}>
  <img class:hidden={ready} class="poster" src="/models/spine-poster.png" alt="Modelo ilustrativo de la columna vertebral y la pelvis" loading="lazy" />
  <div class="glow" aria-hidden="true"></div>

  <div class="top">
    <span class="kicker">Explora tu columna</span>
    {#if ready && !interacted}
      <span class="hint" transition:fade={{ duration: 300 }}>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12m0-1.5v-2a1.5 1.5 0 0 1 3 0V12m0-1a1.5 1.5 0 0 1 3 0v1.5m0 0a1.5 1.5 0 0 1 3 0V16a6 6 0 0 1-6 6h-2.2a6 6 0 0 1-4.6-2.15L4.6 16.6a1.6 1.6 0 0 1 2.4-2.1L8 15.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
        Arrastra para girar · toca una zona
      </span>
    {/if}
  </div>

  {#if hover && !narrow}
    <span class="tip" style="left:{hover.x}px; top:{hover.y}px">{hover.label}</span>
  {/if}

  {#if current}
    {#key current.key}
      <article class="card" class:bottom={narrow} in:fly={{ x: narrow ? 0 : 24, y: narrow ? 24 : 0, duration: 380 }} aria-live="polite">
        <header>
          <p class="range">{current.range}</p>
          <h3>Región {current.name.toLowerCase()}</h3>
          <p class="count">{current.count}</p>
        </header>
        <p class="role">{current.role}</p>
        <p class="signs-title">Suele relacionarse con</p>
        <ul>
          {#each current.signs as s}<li>{s}</li>{/each}
        </ul>
        <a href="#contact" class="cta">Agendar valoración</a>
        <button class="close" aria-label="Cerrar y ver la columna completa" onclick={() => choose(null)}>×</button>
      </article>
    {/key}
  {/if}

  <div class="bar" role="group" aria-label="Regiones de la columna">
    {#each regions as r}
      <button class:active={selected === r.key} aria-pressed={selected === r.key} disabled={!ready} onclick={() => choose(r.key)}>{r.name}</button>
    {/each}
    <button class="reset" aria-label="Ver columna completa" title="Vista completa" disabled={!ready || !selected} onclick={() => choose(null)}>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4h4" stroke-linecap="round" stroke-linejoin="round" /></svg>
    </button>
  </div>

  {#if failed}<span class="fallback">Columna vertebral · vista ilustrativa</span>{/if}
</div>

<style>
  .explorer { position:absolute; inset:0; overflow:hidden; isolation:isolate; color:#fff;
    background:radial-gradient(ellipse at 50% 30%,#4f8e9f 0%,#286f86 52%,#163f50 100%); }
  .explorer :global(canvas) { position:absolute; inset:0; z-index:1; outline:none; }
  .poster { position:absolute; inset:6% 0 10%; width:100%; height:84%; object-fit:contain; transition:opacity .6s; z-index:1; }
  .poster.hidden { opacity:0; }
  .glow { position:absolute; inset:0; z-index:0; pointer-events:none;
    background:radial-gradient(ellipse 70% 45% at 50% 88%,rgba(131,183,171,.32),transparent 70%); }

  .top { position:absolute; z-index:3; top:20px; left:22px; right:22px; display:flex; flex-direction:column; gap:8px; pointer-events:none; }
  .kicker { font-size:11px; font-weight:800; letter-spacing:.2em; text-transform:uppercase; text-shadow:0 1px 6px #0d3442; }
  .hint { display:inline-flex; align-items:center; gap:8px; width:fit-content; padding:7px 12px; border-radius:999px;
    background:rgba(13,52,66,.55); border:1px solid rgba(255,255,255,.18); backdrop-filter:blur(8px); font-size:12px; }
  .hint svg { width:18px; height:18px; animation:nudge 1.8s ease-in-out infinite; }
  @keyframes nudge { 0%,100% { transform:translateX(-3px) } 50% { transform:translateX(4px) } }

  .tip { position:absolute; z-index:4; transform:translate(14px,-120%); pointer-events:none; white-space:nowrap;
    font-size:12px; font-weight:700; letter-spacing:.04em; padding:5px 10px; border-radius:6px; background:#0f3a48e6; border:1px solid #83b7ab66; }

  .card { position:absolute; z-index:4; top:64px; right:16px; width:min(250px,46%); padding:18px 18px 16px; border-radius:16px; color:#0f2f3a;
    background:rgba(255,255,255,.94); box-shadow:0 18px 40px -12px rgba(8,34,44,.55); backdrop-filter:blur(12px); }
  .card.bottom { top:auto; right:12px; left:12px; bottom:72px; width:auto; padding:14px 16px; }
  .card header { margin-bottom:10px; }
  .range { font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; color:#538f83; }
  .card h3 { font-size:19px; font-weight:900; line-height:1.15; color:#215a69; margin-top:2px; }
  .count { font-size:12px; color:#64748b; }
  .role { font-size:13px; line-height:1.5; color:#334155; }
  .signs-title { margin-top:10px; font-size:10px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color:#64748b; }
  .card ul { margin-top:6px; display:flex; flex-direction:column; gap:4px; }
  .card li { position:relative; padding-left:14px; font-size:13px; color:#1e293b; }
  .card li::before { content:''; position:absolute; left:0; top:.55em; width:6px; height:6px; border-radius:50%; background:#83b7ab; }
  .card.bottom ul { flex-direction:row; flex-wrap:wrap; gap:4px 12px; }
  .card.bottom .role { font-size:12.5px; }
  .cta { display:inline-block; margin-top:12px; font-size:11px; font-weight:800; letter-spacing:.14em; text-transform:uppercase;
    color:#fff; background:#215a69; padding:9px 14px; border-radius:8px; transition:background .2s; }
  .cta:hover { background:#0f172a; }
  .close { position:absolute; top:8px; right:10px; width:28px; height:28px; border-radius:50%; font-size:20px; line-height:1; color:#64748b; }
  .close:hover { background:#f1f5f9; color:#0f172a; }

  .bar { position:absolute; z-index:5; left:12px; right:12px; bottom:14px; display:flex; gap:6px; padding:5px; border-radius:14px;
    background:rgba(13,52,66,.5); border:1px solid rgba(255,255,255,.16); backdrop-filter:blur(10px); }
  .bar button { flex:1; min-height:38px; border-radius:10px; font-size:12px; font-weight:700; letter-spacing:.03em; color:#e2f1ee; transition:background .2s,color .2s; }
  .bar button:hover:not(:disabled) { background:rgba(255,255,255,.14); }
  .bar button.active { background:#fff; color:#215a69; box-shadow:0 4px 14px rgba(0,0,0,.18); }
  .bar button:disabled { opacity:.45; cursor:default; }
  .bar .reset { flex:0 0 40px; display:grid; place-items:center; }
  .bar .reset svg { width:16px; height:16px; }
  button:focus-visible, .cta:focus-visible { outline:2px solid #bfffee; outline-offset:2px; }

  .fallback { position:absolute; z-index:3; bottom:70px; left:22px; font-size:10px; font-weight:600; letter-spacing:.13em; text-transform:uppercase; }
  @media (max-width:639px) { .bar button { font-size:11px; letter-spacing:0; } }
  @media (prefers-reduced-motion:reduce) { .hint svg { animation:none; } }
</style>
