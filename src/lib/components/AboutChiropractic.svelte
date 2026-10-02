<script>
  import SpineScene from "./SpineScene.svelte";
</script>

<section id="about" class="py-14 sm:py-20 lg:py-24 bg-white relative overflow-hidden">
  <!-- Clean Medical Background Decor -->
  <div
    class="absolute top-0 right-0 w-1/3 h-full bg-slate-50 -skew-x-12 transform origin-top"
  ></div>
  <div
    class="absolute -bottom-32 -left-32 w-96 h-96 bg-[#215A69]/10 rounded-full blur-[100px]"
  ></div>

  <div class="max-w-[1400px] mx-auto px-6 md:px-12 relative z-10">
    <div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
      <!-- Left: Clinical Image or Abstract Shape -->
      <div class="relative">
        <SpineScene />

      </div>

      <!-- Right: Text Content -->
      <div class="space-y-8 lg:pl-12">
        <div>
          <h3
            class="text-[#215A69] font-bold uppercase tracking-[0.2em] text-sm mb-4"
          >
            ¿Por qué ir a un quiropráctico?
          </h3>
          <h2
            class="text-4xl md:text-5xl font-black text-slate-900 leading-[1.1] tracking-tight"
          >
            La importancia de la <span
              class=" bg-clip-text bg-gradient-to-r text-[#215A69] to-slate-800"
              >Biomecánica</span
            > exacta.
          </h2>
        </div>

        <div
          class="space-y-6 text-slate-600 text-lg font-light leading-relaxed"
        >
          <p>
            El dolor crónico, la fatiga y el estrés físico rara vez desaparecen
            por sí solos. Nuestra columna vertebral es el pilar central del
            sistema nervioso; cuando pierde su alineación geométrica natural,
            todo el cuerpo sufre interferencias nerviosas y mecánicas.
          </p>
          <p>
            Ir al quiropráctico no es solo tronar la espalda. Es un
            procedimiento clínico de <strong class="font-semibold text-slate-800">alta precisión</strong> que restaura la
            movilidad articular neuro-muscular, permitiendo que tu cuerpo active
            sus propios procesos biológicos de sanación celular.
          </p>
        </div>

        <!-- Statistics / Facts grid -->
        <div class="grid grid-cols-2 gap-6 pt-6">
          <div class="border-l-4 border-[#83B7AB] pl-4 py-2">
            <h4 class="text-3xl font-black text-slate-900 mb-1">+90%</h4>
            <p
              class="text-xs uppercase tracking-wider text-slate-500 font-bold"
            >
              Pacientes con alivio post-sesión
            </p>
          </div>
          <div class="border-l-4 border-slate-300 pl-4 py-2">
            <h4 class="text-3xl font-black text-slate-900 mb-1">Cero</h4>
            <p
              class="text-xs uppercase tracking-wider text-slate-500 font-bold"
            >
              Medicamentos o procesos invasivos
            </p>
          </div>
        </div>

        <!-- Certificación (antes flotaba sobre el modelo y tapaba sus controles) -->
        <div
          class="bg-white p-5 rounded-2xl shadow-xl border border-slate-100 max-w-md flex items-start gap-4"
        >
          <div class="flex items-center gap-4 shrink-0">
            <div
              class="w-12 h-12 bg-[#215A69]/10 rounded-full flex items-center justify-center text-green-600"
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
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                /></svg
              >
            </div>
          </div>
          <div>
            <h4 class="text-slate-900 font-bold">Certificación</h4>
            <p class="text-xs text-slate-500 uppercase tracking-wider">
              Profesionales
            </p>
            <p class="text-sm text-slate-600 mt-1">
              Atención quiropráctica de nivel clínico respaldada por la Universidad Estatal del Valle de Toluca.
            </p>
          </div>
        </div>

        <div class="pt-2">
          <a
            href="#contact"
            class="btn btn-outline border-slate-300 text-slate-800 hover:bg-slate-900 hover:text-white hover:border-slate-900 rounded px-10"
            >Evaluación Inicial</a
          >
        </div>
      </div>
    </div>
  </div>
</section>

