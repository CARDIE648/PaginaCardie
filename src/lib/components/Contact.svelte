<script>
  const whatsappNumber = "7291143732"; // Reemplazar con el número real de WhatsApp SIN el signo +
  const msgWhatsApp =
    "Hola Clínica Cardie, me gustaría agendar una evaluación inicial.";
  const encodedMsg = encodeURIComponent(msgWhatsApp);
</script>

<section id="contact" class="py-24 bg-white relative">
  <div class="max-w-[1400px] mx-auto px-6 md:px-12">
    <div
      class="bg-slate-50 border border-slate-100 rounded-3xl p-10 md:p-16 shadow-xl relative overflow-hidden"
    >
      <!-- Medical Decor -->
      <div
        class="absolute top-0 right-0 w-64 h-64 bg-[#215A69]/10 rounded-bl-full opacity-50"
      ></div>

      <div class="grid md:grid-cols-2 gap-12 relative z-10 items-center">
        <!-- Left: Text -->
        <div>
          <h3
            class="text-[#215A69] font-bold uppercase tracking-[0.2em] text-sm mb-4"
          >
            Agenda tu cita
          </h3>
          <h2
            class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-[1.1] mb-6"
          >
            Inicia Tu Camino a la <span
              class="text-transparent bg-clip-text bg-gradient-to-r from-[#215A69] to-slate-800"
              >Recuperación</span
            >
          </h2>
          <p class="text-slate-600 font-light text-lg mb-8">
            No permitas que el dolor limite tu calidad de vida. Contáctanos por
            WhatsApp para resolver tus dudas de inmediato y agendar una
            valoración estructural en nuestra clínica.
          </p>
          <div
            class="flex items-center gap-4 text-slate-500 text-sm font-semibold mb-8"
          >
            <div class="flex items-center gap-2">
              <svg
                class="w-5 h-5 text-[#83B7AB]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                ><path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path></svg
              > Atención Rápida
            </div>
            <div class="flex items-center gap-2">
              <svg
                class="w-5 h-5 text-[#83B7AB]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                ><path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path></svg
              > Especialistas Clínicos
            </div>
          </div>

          <!-- Credenciales Profesionales -->
          <div class="mt-8 pt-6 border-t border-slate-200">
            <h4
              class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-3"
            >
              Responsables Clínicos
            </h4>
            <ul class="text-sm font-medium text-slate-600 space-y-3">
              <li class="flex items-start gap-3">
                <svg
                  class="w-5 h-5 text-[#83B7AB] shrink-0 mt-0.5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  ><path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"
                  ></path></svg
                >
                <div>
                  <span class="text-slate-800 font-bold block"
                    >Lic. en Quiropráctica Hugo Diego Esquivel Almazán</span
                  >
                  <span
                    class="block text-xs text-slate-500 mt-0.5 tracking-wide"
                    >Cédula Profesional: 15513690</span
                  >
                </div>
              </li>
              <li class="flex items-start gap-3">
                <svg
                  class="w-5 h-5 text-[#83B7AB] shrink-0 mt-0.5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  ><path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"
                  ></path></svg
                >
                <div>
                  <span class="text-slate-800 font-bold block"
                    >Lic. en Quiropráctica Carolina Ocaña Malváez</span
                  >
                  <span
                    class="block text-xs text-slate-500 mt-0.5 tracking-wide"
                    >Cédula Profesional: 15513763</span
                  >
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Right: CTA Card -->
        <div class="flex flex-col gap-6 justify-center max-w-sm mx-auto w-full">
          <a
            href={`https://wa.me/${whatsappNumber}?text=${encodedMsg}`}
            target="_blank"
            class="bg-[#215A69] hover:bg-[#83B7AB] text-white p-6 rounded-2xl flex flex-col items-center gap-4 transition-all duration-500 shadow-none hover:-translate-y-2 hover:shadow-[0_20px_40px_rgba(33,90,105,0.6)]"
            aria-label="Contactar por WhatsApp"
          >
            <div
              class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center"
            >
              <svg
                class="w-8 h-8 text-white"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.663-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"
                />
              </svg>
            </div>
            <div class="text-center">
              <h4 class="font-bold text-xl uppercase tracking-wider">
                Mandar WhatsApp
              </h4>
              <p class="text-white/80 text-sm">Respuesta en menos de 10 mins</p>
            </div>
          </a>

          <div
            class="text-center text-slate-500 text-xs font-semibold uppercase tracking-widest mt-2 border-t border-slate-200 pt-4 flex flex-col gap-2"
          >
            <span>O Llámanos:</span>
            <div class="flex flex-col gap-1">
              <span class="text-slate-800 font-bold"
                >+52 {whatsappNumber.replace(
                  /(\d{3})(\d{3})(\d{4})/,
                  "$1 $2 $3",
                )}</span
              >
              <span class="text-slate-800 font-bold">+52 722 387 3457</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Widget Botón Flotante Fijo WhatsApp -->
<a
  href={`https://wa.me/${whatsappNumber}?text=${encodedMsg}`}
  target="_blank"
  class="fixed bottom-6 right-6 z-50 bg-[#83B7AB] hover:bg-[#215A69] text-white p-4 rounded-full shadow-none hover:-translate-y-2 hover:shadow-[0_20px_40px_rgba(33,90,105,0.6)] transition-all duration-500 group"
  aria-label="Contactar por WhatsApp"
>
  <!-- Tooltip -->
  <span
    class="absolute right-full mr-4 top-1/2 -translate-y-1/2 px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap shadow-xl pointer-events-none"
  >
    Agendar Cita Rápidamente
  </span>
  <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
    <path
      d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.663-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"
    />
  </svg>
</a>
