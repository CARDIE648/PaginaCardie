<script>
  // Video en loop del hero (renderizado en Blender: art/build_hero_video.py).
  // Más ligero que el 3D en vivo: el celular solo decodifica un video corto.
  // Se pausa fuera de pantalla y respeta "reducir movimiento".
  import { onMount } from "svelte";

  /** @type {HTMLVideoElement} */
  let video;

  onMount(() => {
    const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let visible = true;
    const sync = () => {
      if (motion.matches || !visible || document.hidden) video.pause();
      else video.play().catch(() => {});
    };
    const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; sync(); });
    io.observe(video);
    motion.addEventListener("change", sync);
    document.addEventListener("visibilitychange", sync);
    sync();
    return () => {
      io.disconnect();
      motion.removeEventListener("change", sync);
      document.removeEventListener("visibilitychange", sync);
    };
  });
</script>

<div class="absolute inset-0 z-[-1] overflow-hidden bg-[#2d4f57]">
  <video
    bind:this={video}
    class="absolute inset-0 w-full h-full object-cover object-[62%_center]"
    poster="/video/hero-spine-poster.webp"
    muted
    loop
    playsinline
    autoplay
    preload="auto"
    disablepictureinpicture
    aria-hidden="true"
    tabindex="-1"
  >
    <source src="/video/hero-spine-sm.mp4" type="video/mp4" media="(max-width: 767px)" />
    <source src="/video/hero-spine.mp4" type="video/mp4" />
  </video>
  <!-- Velo para que el texto blanco siempre se lea -->
  <div
    class="absolute inset-0 pointer-events-none bg-gradient-to-r from-[#0d2a33]/45 via-[#0d2a33]/10 to-transparent lg:from-[#0d2a33]/40"
  ></div>
</div>
