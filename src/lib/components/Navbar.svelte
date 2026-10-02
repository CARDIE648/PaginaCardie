<script>
  import { onMount } from "svelte";
  let scrolled = $state(false);
  // Sin scroll los enlaces quedan sobre el video del hero: en blanco para que se lean
  const linkClass = $derived(
    scrolled
      ? "text-[#215A69] hover:text-slate-900"
      : "text-white/90 hover:text-white [text-shadow:0_1px_8px_rgba(8,30,38,.55)]",
  );

  onMount(() => {
    const handleScroll = () => {
      scrolled = window.scrollY > 50;
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  });
</script>

<nav
  class="fixed top-0 left-0 w-full z-50 transition-all duration-700 {scrolled
    ? 'bg-white/95 backdrop-blur-xl border-b border-slate-200 py-3 shadow-sm'
    : 'bg-transparent py-6 border-b border-transparent'} lg:px-16 px-6"
>
  <div class="max-w-[1800px] mx-auto flex justify-between items-center">
    <!-- Left Side: Logo horizontal (icono + nombre) -->
    <a
      href="#hero"
      class="group flex items-center gap-3 md:gap-4 w-fit"
      aria-label="CARDIE Quiropráctico, ir al inicio"
    >
      <img
        src="/LogoIcono.png"
        alt=""
        width="144"
        height="192"
        class="w-auto drop-shadow-sm transition-all duration-500 group-hover:-rotate-3 group-hover:scale-105 {scrolled
          ? 'h-11 md:h-12'
          : 'h-14 md:h-[4.5rem]'}"
      />
      <span
        class="flex flex-col leading-none pl-3 md:pl-4 border-l border-[#215A69]/25"
      >
        <span
          class="font-serif font-semibold text-[#215A69] tracking-[0.06em] transition-all duration-500 {scrolled
            ? 'text-2xl md:text-[1.7rem]'
            : 'text-[1.7rem] md:text-[2.3rem]'}">CARDIE</span
        >
        <span
          class="mt-1 text-[10px] md:text-[12px] font-extrabold uppercase tracking-[0.22em] text-[#215A69]"
          >Quiropráctico</span
        >
        <span
          class="hidden sm:block mt-1 text-[8px] md:text-[9px] font-semibold uppercase tracking-[0.18em] text-[#215A69]/60"
          >Salud vertebral y bienestar</span
        >
      </span>
    </a>

    <!-- Right Side: Clean Navigation Links -->
    <div class="hidden lg:flex items-center gap-12">
      <a
        href="#hero"
        class="text-[12px] font-bold uppercase tracking-[0.15em] transition-colors {linkClass}"
        >Inicio</a
      >
      <a
        href="#about"
        class="text-[12px] font-bold uppercase tracking-[0.15em] transition-colors {linkClass}"
        >Nosotros</a
      >
      <a
        href="#packages"
        class="text-[12px] font-bold uppercase tracking-[0.15em] transition-colors {linkClass}"
        >Servicios</a
      >
      <a
        href="#ubicacion"
        class="text-[12px] font-bold uppercase tracking-[0.15em] transition-colors {linkClass}"
        >Ubicación</a
      >
      <a
        href="#contact"
        class="text-[12px] font-bold uppercase tracking-[0.15em] text-white bg-slate-900 px-6 py-2.5 rounded hover:bg-[#215A69] hover:shadow-lg transition-all"
        >Agendar Cita</a
      >
    </div>

    <!-- Mobile Toggle -->
    <div class="lg:hidden dropdown dropdown-end">
      <div
        tabindex="0"
        role="button"
        class="btn btn-ghost btn-circle text-slate-800"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          ><path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16m-7 6h7"
          ></path></svg
        >
      </div>
      <ul
        tabindex="-1"
        class="menu menu-sm dropdown-content mt-3 z-[1] p-6 shadow-xl bg-white border border-slate-100 w-64 gap-6 rounded-lg"
      >
        <li>
          <a
            href="#hero"
            class="text-slate-600 hover:text-slate-900 text-lg font-medium tracking-wide uppercase px-0"
            >Inicio</a
          >
        </li>
        <li>
          <a
            href="#about"
            class="text-slate-600 hover:text-slate-900 text-lg font-medium tracking-wide uppercase px-0"
            >Nosotros</a
          >
        </li>
        <li>
          <a
            href="#packages"
            class="text-slate-600 hover:text-slate-900 text-lg font-medium tracking-wide uppercase px-0"
            >Servicios</a
          >
        </li>
        <li>
          <a
            href="#ubicacion"
            class="text-slate-600 hover:text-slate-900 text-lg font-medium tracking-wide uppercase px-0"
            >Ubicación</a
          >
        </li>
        <li class="mt-4">
          <a
            href="#contact"
            class="text-white bg-slate-900 font-bold hover:bg-[#215A69] text-center py-3 rounded-lg tracking-wide uppercase px-0 w-full inline-block"
            >Agendar Cita</a
          >
        </li>
      </ul>
    </div>
  </div>
</nav>
