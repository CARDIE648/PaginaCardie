<script>
    import '../app.css';
    import Navbar from '$lib/components/Navbar.svelte';
    import Footer from '$lib/components/Footer.svelte';
    
    let { children } = $props();
</script>

<svelte:head>
  <title>CARDIE | Clínica Quiropráctica y Ajuste Espinal</title>
  <meta name="description" content="Encuentra alivio al dolor de espalda, cuello y mejora tu postura con los especialistas de CARDIE. Agenda tu cita quiropráctica hoy mismo." />
  <meta name="keywords" content="quiropráctico, ajuste espinal, dolor de espalda, postura, CARDIE, clínica quiropráctica" />

  <meta property="og:title" content="CARDIE | Tu Clínica Quiropráctica" />
  <meta property="og:description" content="Especialistas en bienestar físico y corrección de postura. Dile adiós al dolor." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://cardiequiropráctico.com" />
  {@html `<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MedicalClinic",
    "name": "CARDIE",
    "description": "Clínica especializada en ajustes quiroprácticos y bienestar integral.",
    "url": "https://cardiequiropráctico.com",
    "telephone": "+52 729 114 3732",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Av. 16 de Septiembre 339-A, Interior 1, Vista Nevado I",
      "addressLocality": "San Miguel Zinacantepec",
      "addressRegion": "Estado de México",
      "postalCode": "51350",
      "addressCountry": "MX"
    },
    "medicalSpecialty": "Chiropractic"
  }
  </script>`}
</svelte:head>

<div class="min-h-screen bg-cardie-dark text-base-content flex flex-col font-sans selection:bg-primary selection:text-primary-content antialiased">
    <Navbar />
    <main class="flex-grow">
        {@render children()}
    </main>
    <Footer />
</div>
