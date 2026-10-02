# CARDIE · columna 3D local

Versión para revisión, 2 de octubre de 2026. Sin commit ni push.

## Archivos

- `cardie-spine.blend`: escena editable con materiales, iluminación, cámara y animación de inspección de 8 segundos (240 fotogramas a 30 fps).
- `build_spine.py`: generación reproducible en Blender 5.2.
- `pelvis_anatomy.py`: construcción de sacro y huesos coxales con cavidades reales.
- `verify_pelvis.py`: revisión de mallas cerradas sobre el `.blend` guardado.
- `../static/models/cardie-spine.glb`: modelo web con vértebras y discos separados, regiones identificadas y animación exportada.
- `../static/models/spine-poster.png`: respaldo transparente renderizado localmente en Blender.
- `../src/lib/components/SpineScene.svelte`: escena compartida de portada y biomecánica.
- `../src/lib/three/spine-viewer.ts`: iluminación y movimiento interactivo en Three.js.

## Criterio visual y límites

Se conserva la división de portada en dos mitades, titulares, tarjeta translúcida, paleta azul/verde, proporción de la imagen inferior y tarjeta de certificación. Los videos originales y la imagen original siguen disponibles. Los títulos se adaptan al ancho para evitar recortes en escritorio mediano.

Modelo original estilizado de 24 vértebras (7 cervicales, 12 torácicas y 5 lumbares), discos, sacro, cóccix y pelvis. La curva y las regiones son coherentes como ilustración; no es una reconstrucción clínica ni un modelo anatómico validado. No reproduce cráneo, costillas ni las deformaciones/partículas de los videos IA.

En web el movimiento de inspección se calcula sobre el modelo rígido, permitiendo pausar y girar sin deformar vértebras. Los tres puntos destacan regiones; no simulan tratamiento, lesiones ni recuperación. La animación del archivo Blender conserva una alternativa editable del giro.

## Uso

```powershell
npm install
npm run dev -- --host 127.0.0.1
# Generar nuevamente el modelo y respaldo:
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python art/build_spine.py
```

Three.js se carga bajo demanda. Cada escena se inicializa cerca del viewport, pausa su bucle fuera de pantalla o con la pestaña oculta y limita la resolución a 1.5 DPR. Movimiento reducido inicia pausado; puede reanudarse expresamente. Si falla WebGL o la carga del modelo, se conserva el respaldo. Los botones tienen etiquetas, foco visible y estados de selección.

## Validación

- Blender ejecutado, `.blend`, GLB y PNG generados; PNG inspeccionado.
- `svelte-check`: 0 errores y 0 advertencias.
- Build estático de Vite completado. Aviso de tamaño del chunk 3D (~155 KB gzip), ya cargado dinámicamente.
- Navegador local: ambas escenas WebGL cargadas, sin errores de consola; giro, pausa y selección de región comprobados.
- Composición revisada en 1440 × 960 y 390 × 844; móvil sin desbordamiento horizontal.
- No se probó en un teléfono físico. Respaldo por pérdida de contexto y cambio de preferencia de movimiento implementados, sin prueba de inyección de fallos.

Para aprobar: revisar portada, sección de biomecánica y controles en local, y autorizar commit/push. Para cancelar: revertir únicamente los archivos de esta propuesta y sus nuevas dependencias; no borrar cambios posteriores del usuario.

## Refinamiento del sacro y la pelvis

Segunda revisión según las dos láminas aportadas por el usuario. El sacro tiene base S1, alas redondeadas, cuatro pares de orificios, relieves transversales y cresta posterior; cóccix de cuatro segmentos. Los dos huesos coxales incorporan fosas y crestas ilíacas, cavidades acetabulares, ramas púbicas, aberturas obturatrices y tuberosidades isquiáticas. Una superficie discreta representa la sínfisis púbica. También se distinguieron las apófisis espinosas torácicas, más descendentes, de las lumbares, más cortas y romas.

Referencias consultadas: [OpenStax, columna vertebral](https://openstax.org/books/anatomy-and-physiology-2e/pages/7-3-the-vertebral-column) y [OpenStax, cintura pélvica](https://openstax.org/books/anatomy-and-physiology-2e/pages/8-3-the-pelvic-girdle-and-pelvis). Se modeló geometría original; no se descargaron modelos de terceros. Sigue siendo una interpretación estilizada, no una validación anatómica clínica.

GLB actualizado: 1,881,524 bytes. Verificación en Blender del archivo guardado: sacro y ambos coxales con volumen positivo y cero aristas no manifold. Se conserva la animación original. Renders revisados en `review/pelvis-anterior.png`, `review/pelvis-posterior.png` y `review/pelvis-oblique.png`; resultados en `review/geometry-validation.json`. Copia del modelo anterior en `review/spine-before-pelvis-refinement.blend`. Las imágenes y copias de `review/` son para revisión local, no recursos servidos por la web.
