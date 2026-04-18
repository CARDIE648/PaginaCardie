<script>
  import { onMount } from "svelte";

  // Control de Video en bucle cinemático
  const videos = ["/Video1.mp4", "/Video2.mp4"];
  let activeIndex = $state(0);
  /** @type {HTMLVideoElement | undefined} */
  let v1_el;
  /** @type {HTMLVideoElement | undefined} */
  let v2_el;

  const handleEnded1 = () => {
    activeIndex = 1;
    if (v2_el) {
      v2_el.currentTime = 0;
      v2_el.play().catch(() => {});
    }
  };
  const handleEnded2 = () => {
    activeIndex = 0;
    if (v1_el) {
      v1_el.currentTime = 0;
      v1_el.play().catch(() => {});
    }
  };

  // Función para scroll suave a la siguiente sección
  const scrollToNext = () => {
    const nextSection = document.getElementById("about");
    if (nextSection) {
      nextSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  onMount(() => {
    // Asegurar que el primer video empiece
    if (v1_el) v1_el.play().catch(() => {});
  });
</script>

<section
  id="hero"
  class="relative min-h-screen w-full flex flex-col lg:flex-row overflow-hidden bg-slate-50"
>
  <!-- Responsive Layout Container -->
  <div class="relative z-10 w-full flex flex-col lg:flex-row min-h-screen">
    <!-- LEFT SIDE: Content & Frosted Glass Layer -->
    <div
      class="relative w-full lg:w-1/2 flex flex-col justify-center px-6 sm:px-12 lg:px-20 xl:pl-32 py-20 lg:py-0 min-h-[50vh] lg:min-h-screen lg:justify-start lg:pt-[35vh]"
    >
      <!-- Milky Glass Overlay (Responsible for the 50% split on large screens) -->
      <div
        class="absolute inset-0 bg-white/80 lg:bg-white/90 backdrop-blur-3xl lg:backdrop-blur-2xl border-b lg:border-r border-slate-200 shadow-2xl z-[-1]"
      ></div>

      <div class="relative flex flex-col lg:items-end">
        <h4
          class="text-slate-500 text-[10px] sm:text-xs lg:text-sm font-bold tracking-[0.4em] uppercase mb-2 lg:mb-4 opacity-80 lg:absolute lg:bottom-full lg:right-4 pl-1 text-center lg:text-right animate-fadeIn"
        >
          Cuidado Exacto Para Tu
        </h4>

        <h1
          class="text-6xl sm:text-7xl md:text-8xl lg:text-[6rem] xl:text-[8rem] font-black uppercase tracking-[-0.05em] leading-[0.8] text-[#215A69] drop-shadow-sm transition-all duration-500 hover:tracking-tight animate-slideRight text-center lg:text-right lg:pr-4"
        >
          COLUMNA
        </h1>

        <h4
          class="text-slate-500 text-[10px] sm:text-xs lg:text-sm font-bold tracking-[0.4em] uppercase mb-2 lg:mb-4 opacity-80 pl-1 text-center lg:text-right animate-fadeIn mt-2"
        >
          CONTIGO EN CADA PASO HACIA TU SALUD VERTEBRAL
        </h4>

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
      class="relative w-full lg:w-1/2 flex flex-col justify-center px-6 sm:px-12 lg:px-20 xl:pr-32 py-20 lg:py-0 min-h-[50vh] lg:min-h-screen lg:justify-start lg:pt-[35vh]"
    >
      <!-- Background Cinematic Videos exclusively on the right side -->
      <div
        class="absolute inset-0 z-[-1] bg-slate-900 overflow-hidden shadow-inner"
      >
        <video
          bind:this={v1_el}
          src={videos[0]}
          onended={handleEnded1}
          autoplay
          muted
          playsinline
          class="absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 {activeIndex ===
          0
            ? 'opacity-100'
            : 'opacity-0'}"
        ></video>
        <video
          bind:this={v2_el}
          src={videos[1]}
          onended={handleEnded2}
          muted
          playsinline
          class="absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 {activeIndex ===
          1
            ? 'opacity-100'
            : 'opacity-0'}"
        ></video>
      </div>

      <div class="relative flex flex-col lg:items-start">
        <h1
          class="text-6xl sm:text-7xl md:text-8xl lg:text-[6rem] xl:text-[8rem] font-black text-white uppercase tracking-[-0.05em] leading-[0.8] mb-8 drop-shadow-2xl animate-slideLeft text-center lg:text-left lg:pl-4"
        >
          BIENESTAR
        </h1>

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

      <!-- Controls & Pagination: Organized globally -->

      <!-- Vertical Pagination (Visible on Desktop/Tablet only) -->
      <div
        class="hidden sm:flex absolute right-6 lg:right-12 top-1/2 -translate-y-1/2 flex-col gap-6 z-30"
      >
        <div
          class="p-1.5 rounded-full border border-white flex items-center justify-center cursor-pointer shadow-lg"
        >
          <div class="w-2 h-2 bg-white rounded-full"></div>
        </div>
        <div
          class="w-2 h-2 bg-white/30 rounded-full mx-auto hover:bg-white transition-all cursor-pointer shadow-md"
        ></div>
        <div
          class="w-2 h-2 bg-white/30 rounded-full mx-auto hover:bg-white transition-all cursor-pointer shadow-md"
        ></div>
      </div>

      <!-- Navigation Arrows: Repositioned for center usability across devices -->
      <div
        class="absolute bottom-8 right-6 sm:bottom-12 sm:right-12 flex gap-3 z-30"
      >
        <button
          onclick={scrollToNext}
          class="w-12 h-12 sm:w-14 sm:h-14 flex items-center justify-center rounded-xl border border-slate-200/50 bg-white/10 backdrop-blur-md text-white hover:bg-white hover:text-slate-900 transition-all shadow-xl hover:-translate-y-1"
          aria-label="Anterior"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            ><path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            /></svg
          >
        </button>
        <button
          onclick={scrollToNext}
          class="w-12 h-12 sm:w-14 sm:h-14 flex items-center justify-center rounded-xl bg-slate-900 text-white hover:bg-[#215A69] transition-all shadow-2xl hover:-translate-y-1"
          aria-label="Siguiente sección"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            ><path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            /></svg
          >
        </button>
      </div>
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
