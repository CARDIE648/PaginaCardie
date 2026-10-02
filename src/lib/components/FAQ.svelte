<script>
  // Preguntas frecuentes: las mismas que se publican a Google como FAQPage (+layout.svelte)
  import { faqs } from "$lib/clinic.js";
</script>

<section id="preguntas" class="py-14 sm:py-20 lg:py-24 bg-slate-50 relative overflow-hidden">
  <div class="max-w-[1100px] mx-auto px-6 md:px-12 relative z-10">
    <div class="text-center mb-8 lg:mb-12">
      <h3 class="text-[#215A69] font-bold uppercase tracking-[0.2em] text-sm mb-4">
        Preguntas frecuentes
      </h3>
      <h2 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-[1.1]">
        Antes de tu primera visita
      </h2>
    </div>

    <div class="grid gap-3">
      {#each faqs as f, i}
        <details class="faq group bg-white rounded-2xl border border-slate-100 shadow-sm open:shadow-lg transition-shadow" open={i === 0}>
          <summary class="flex items-center justify-between gap-4 cursor-pointer list-none px-5 py-4 md:px-8 md:py-5">
            <h3 class="text-base md:text-lg font-bold text-slate-900">{f.q}</h3>
            <span
              class="shrink-0 grid place-items-center w-9 h-9 rounded-full border border-slate-200 text-[#215A69] transition-transform duration-300 group-open:rotate-45 group-open:bg-[#215A69] group-open:text-white group-open:border-[#215A69]"
              aria-hidden="true"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                ><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg
              >
            </span>
          </summary>
          <p class="px-5 pb-5 md:px-8 md:pb-6 -mt-1 text-slate-600 font-light leading-relaxed">{f.a}</p>
        </details>
      {/each}
    </div>
  </div>
</section>

<style>
  .faq summary::-webkit-details-marker { display: none; }
</style>
