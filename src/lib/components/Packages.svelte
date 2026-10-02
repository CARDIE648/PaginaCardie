<script>
  import { clinic } from "$lib/clinic.js";

  // Lo que incluye la consulta, en el orden en que sucede la visita
  const steps = [
    { title: "Historia clínica", text: "Conocemos tus síntomas, hábitos y antecedentes." },
    { title: "Examen postural", text: "Revisamos la alineación de tu cuerpo y cómo se mueve." },
    { title: "Pruebas ortopédicas y neurológicas", text: "Ubicamos el origen de la molestia antes de tratarla." },
    { title: "Análisis y ajuste específico", text: "Un ajuste preciso en la zona que lo necesita." },
    { title: "Activación y fortalecimiento muscular", text: "Para que el cambio se sostenga después de la sesión." },
  ];

  const waHref = `https://wa.me/${clinic.whatsapp}?text=${encodeURIComponent(
    "Hola Clínica Cardie, me gustaría agendar una consulta quiropráctica.",
  )}`;
</script>

<section id="packages" class="py-14 sm:py-20 lg:py-24 bg-slate-50 relative overflow-hidden">
  <!-- Decoración sutil superior -->
  <div
    class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent"
  ></div>
  <div class="absolute -top-40 -right-40 w-[28rem] h-[28rem] rounded-full bg-[#83B7AB]/15 blur-[110px]"></div>

  <div class="max-w-[1400px] mx-auto px-6 md:px-12 relative z-10">
    <div class="text-center max-w-3xl mx-auto mb-10 lg:mb-16 space-y-4">
      <h3 class="text-[#215A69] font-bold uppercase tracking-[0.2em] text-sm">
        Consulta Quiropráctica
      </h3>
      <h2 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">
        Una consulta completa, un solo precio
      </h2>
      <p class="text-slate-500 font-light text-lg">
        Evaluación y ajuste en la misma visita, para que salgas sabiendo qué
        tiene tu columna y con un plan claro.
      </p>
    </div>

    <div
      class="max-w-6xl mx-auto grid lg:grid-cols-5 rounded-[2rem] overflow-hidden bg-white shadow-[0_30px_70px_-25px_rgba(33,90,105,0.45)] border border-slate-100"
    >
      <!-- Precio -->
      <div
        class="lg:col-span-2 relative overflow-hidden bg-[#215A69] text-white p-8 sm:p-10 lg:p-12 flex flex-col"
      >
        <div class="absolute -bottom-24 -right-24 w-72 h-72 rounded-full border border-white/10"></div>
        <div class="absolute -bottom-10 -right-10 w-44 h-44 rounded-full border border-white/10"></div>
        <div class="absolute -top-20 -left-20 w-64 h-64 rounded-full bg-[#83B7AB]/20 blur-3xl"></div>

        <span
          class="relative w-fit rounded-full bg-white/10 border border-white/20 px-4 py-1.5 text-[10px] font-bold uppercase tracking-[0.25em] text-[#bfe3da]"
        >
          Precio único
        </span>
        <h3 class="relative mt-6 text-2xl sm:text-3xl font-black uppercase tracking-tight leading-tight">
          Consulta<br />quiropráctica
        </h3>
        <div class="relative mt-8 flex items-end gap-2">
          <span class="text-2xl font-bold text-white/70 mb-3">$</span>
          <span class="text-7xl sm:text-8xl font-black leading-none tracking-tight">{clinic.price}</span>
          <span class="mb-3 text-sm font-semibold uppercase tracking-widest text-white/60">MXN</span>
        </div>
        <p class="relative mt-4 text-white/70 font-light leading-relaxed">
          Todo lo que necesitas en una visita: evaluación completa, ajuste
          específico y ejercicios de activación.
        </p>

        <div class="relative mt-auto pt-10 flex flex-col gap-3">
          <a
            href={waHref}
            target="_blank"
            rel="noopener noreferrer"
            class="group flex items-center justify-center gap-3 w-full py-4 rounded-xl bg-white text-[#215A69] text-sm font-bold uppercase tracking-wider shadow-lg hover:bg-[#83B7AB] hover:text-white transition-all duration-300 hover:-translate-y-0.5"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"
              ><path
                d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.49s1.07 2.89 1.22 3.09c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12 2a10 10 0 0 0-8.6 15.1L2 22l5.04-1.32A10 10 0 1 0 12 2z"
              /></svg
            >
            Agendar por WhatsApp
          </a>
          <a
            href="#ubicacion"
            class="flex items-center justify-center gap-2 w-full py-3 rounded-xl border border-white/25 text-white/90 text-xs font-bold uppercase tracking-[0.18em] hover:bg-white/10 transition-colors"
          >
            Ver ubicación
          </a>
        </div>
      </div>

      <!-- Qué incluye -->
      <div class="lg:col-span-3 p-8 sm:p-10 lg:p-12">
        <p class="text-[11px] font-bold uppercase tracking-[0.25em] text-slate-400">
          ¿Qué incluye tu consulta?
        </p>
        <ol class="mt-8 relative">
          {#each steps as step, i}
            <li class="relative flex gap-5 pb-7 last:pb-0 group">
              {#if i < steps.length - 1}
                <span class="absolute left-5 top-11 bottom-0 w-px bg-gradient-to-b from-[#83B7AB]/60 to-slate-200" aria-hidden="true"></span>
              {/if}
              <span
                class="relative z-10 grid place-items-center shrink-0 w-10 h-10 rounded-full bg-[#215A69]/5 border border-[#83B7AB]/40 text-[#215A69] text-sm font-black group-hover:bg-[#215A69] group-hover:text-white transition-colors"
              >
                {i + 1}
              </span>
              <div class="pt-1.5">
                <h4 class="font-bold text-slate-900">{step.title}</h4>
                <p class="mt-1 text-sm text-slate-500 font-light leading-relaxed">{step.text}</p>
              </div>
            </li>
          {/each}
        </ol>

        <div class="mt-10 pt-6 border-t border-slate-100 flex flex-wrap gap-x-8 gap-y-3 text-xs font-semibold text-slate-500">
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4 text-[#83B7AB]" fill="none" viewBox="0 0 24 24" stroke="currentColor"
              ><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg
            >
            Licenciados con cédula profesional
          </span>
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4 text-[#83B7AB]" fill="none" viewBox="0 0 24 24" stroke="currentColor"
              ><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg
            >
            Sin medicamentos ni procedimientos invasivos
          </span>
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4 text-[#83B7AB]" fill="none" viewBox="0 0 24 24" stroke="currentColor"
              ><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
              /></svg
            >
            Zinacantepec, a minutos de Toluca
          </span>
        </div>
      </div>
    </div>
  </div>
</section>
