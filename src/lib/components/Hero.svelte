<script>
  import HeroVideo from './HeroVideo.svelte';
</script>

<section
  id="hero"
  class="relative min-h-screen w-full flex flex-col lg:flex-row overflow-hidden bg-slate-50"
>
  <!-- Responsive Layout Container -->
  <div class="relative z-10 w-full flex flex-col lg:flex-row min-h-screen">
    <!-- LEFT SIDE: Content & Frosted Glass Layer -->
    <div
      class="relative w-full lg:w-1/2 flex flex-col justify-center px-6 sm:px-12 lg:px-20 xl:pl-32 pt-28 pb-12 sm:py-20 lg:py-0 sm:min-h-[50vh] lg:min-h-screen lg:justify-start lg:pt-[35vh]"
    >
      <!-- Milky Glass Overlay (Responsible for the 50% split on large screens) -->
      <div
        class="absolute inset-0 bg-white/80 lg:bg-white/90 backdrop-blur-3xl lg:backdrop-blur-2xl border-b lg:border-r border-slate-200 shadow-2xl z-[-1]"
      ></div>

      <div class="relative flex flex-col lg:items-end">
        <p
          class="text-slate-500 text-[10px] sm:text-xs lg:text-sm font-bold tracking-[0.4em] uppercase mb-2 lg:mb-4 opacity-80 lg:absolute lg:bottom-full lg:right-4 pl-1 text-center lg:text-right animate-fadeIn"
        >
          Cuidado Exacto Para Tu
        </p>

        <p
          class="hero-word font-black uppercase tracking-[-0.05em] leading-[0.8] text-[#215A69] drop-shadow-sm transition-all duration-500 hover:tracking-tight animate-slideRight text-center lg:text-right lg:pr-4"
        >
          COLUMNA
        </p>

        <!-- Título principal para Google: lo que la gente busca (servicio + zona) -->
        <h1
          class="text-[#215A69] text-[11px] sm:text-xs lg:text-sm font-extrabold tracking-[0.3em] uppercase pl-1 text-center lg:text-right animate-fadeIn mt-4 lg:pr-4"
        >
          Quiropráctico en Zinacantepec
        </h1>
        <p
          class="text-slate-500 text-[10px] sm:text-xs lg:text-sm font-bold tracking-[0.4em] uppercase mb-2 lg:mb-4 opacity-80 pl-1 text-center lg:text-right animate-fadeIn mt-1 lg:pr-4"
        >
          Contigo en cada paso hacia tu salud vertebral
        </p>

        <!-- Request Consultation specifically for mobile/touch or desktop side links -->
        <div
          class="mt-8 sm:mt-12 flex items-center justify-center lg:justify-end gap-4 lg:pr-4 w-full"
        >
          <div
            class="w-10 h-10 sm:w-12 sm:h-12 rounded-full border-2 border-slate-200 flex items-center justify-center hover:bg-slate-900 hover:text-white hover:border-slate-900 transition-all cursor-pointer text-slate-400 group"
          >
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 group-hover:rotate-90 transition-transform"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              ><path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              /></svg
            >
          </div>
          <a
            href="#contact"
            class="text-slate-800 text-[10px] sm:text-xs font-bold tracking-[0.25em] uppercase border-b-2 border-slate-200 pb-1 hover:border-slate-900 transition-colors"
            >Solicitar Consulta</a
          >
        </div>
      </div>
    </div>

    <!-- RIGHT SIDE: Wellness & Sharp Imagery -->
    <div
      class="relative w-full lg:w-1/2 flex flex-col justify-center px-6 sm:px-12 lg:px-20 xl:pr-32 pt-14 pb-28 sm:py-20 lg:py-0 min-h-[62svh] sm:min-h-[50vh] lg:min-h-screen lg:justify-start lg:pt-[35vh]"
    >
      <HeroVideo />

      <div class="relative flex flex-col lg:items-start pointer-events-none">
        <p
          class="hero-word font-black text-white uppercase tracking-[-0.05em] leading-[0.8] mb-8 drop-shadow-2xl animate-slideLeft text-center lg:text-left lg:pl-4"
        >
          BIENESTAR
        </p>

        <!-- Content Card: Better organized for laptop/mobile readability -->
        <div
          class="bg-slate-900/60 lg:bg-slate-900/40 backdrop-blur-xl p-6 sm:p-8 rounded-2xl max-w-lg border border-white/20 shadow-2xl animate-fadeInDelay lg:ml-4"
        >
          <p
            class="text-white text-sm sm:text-base lg:text-lg leading-relaxed font-light"
          >
            Existe un punto <span class="text-[#83B7AB] font-bold">preciso</span
            >
            donde el cuidado experto y las técnicas avanzadas se encuentran para
            restaurar la alineación natural de tu cuerpo. Experimenta alivio duradero
            y vitalidad óptima.
          </p>
        </div>
      </div>

      <!-- Invitación al explorador 3D de la siguiente sección -->
      <a
        href="#about"
        class="group absolute bottom-6 left-6 sm:left-12 lg:left-20 xl:left-24 lg:bottom-10 z-20 inline-flex items-center gap-3 rounded-full border border-white/30 bg-white/15 pl-2 pr-5 py-2 text-white backdrop-blur-md shadow-xl hover:bg-white hover:text-[#215A69] transition-colors"
      >
        <span class="grid h-9 w-9 place-items-center rounded-full bg-white/20 group-hover:bg-[#215A69] group-hover:text-white transition-colors">
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"
            ><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3zm0 0v18m8-13.5L12 12 4 7.5" stroke-linecap="round" stroke-linejoin="round" /></svg
          >
        </span>
        <span class="text-[11px] font-bold uppercase tracking-[0.2em]">Explora tu columna en 3D</span>
      </a>
    </div>
  </div>

  <!-- Medical Spine Cluster: Floating organized center icon -->
  <div
    class="hidden lg:flex absolute top-32 left-1/2 -translate-x-1/2 z-30 pointer-events-none drop-shadow-2xl"
  >
    <div
      class="flex flex-col gap-2 items-center justify-center opacity-90 scale-125"
    >
      <div class="w-3 h-1.5 bg-[#83B7AB] rounded-full animate-pulse"></div>
      <div class="w-4 h-1.5 bg-slate-600 rounded-full"></div>
      <div class="w-5 h-1.5 bg-[#215A69] rounded-full shadow-lg"></div>
      <div class="w-4 h-1.5 bg-slate-600 rounded-full"></div>
      <div class="w-3 h-1.5 bg-[#83B7AB] rounded-full animate-pulse"></div>
    </div>
  </div>
</section>

<style>
  .hero-word { font-size:clamp(3rem, 9vw, 6rem); }
  @media(min-width:1024px) { .hero-word { font-size:clamp(3.5rem, 5.8vw, 8rem); } }
  @media(prefers-reduced-motion:reduce) { .animate-fadeIn,.animate-fadeInDelay,.animate-slideRight,.animate-slideLeft { animation:none !important; } }
  /* Animations to enhance premium feel on load */
  .animate-fadeIn {
    animation: fadeIn 1s ease-out;
  }
  .animate-fadeInDelay {
    animation: fadeIn 1.5s ease-out both;
  }
  .animate-slideRight {
    animation: slideRight 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .animate-slideLeft {
    animation: slideLeft 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
  @keyframes slideRight {
    from {
      opacity: 0;
      transform: translateX(-30px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  @keyframes slideLeft {
    from {
      opacity: 0;
      transform: translateX(30px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
</style>
