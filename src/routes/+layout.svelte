<script>
  import "../app.css";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import { SITE_URL, clinic, faqs } from "$lib/clinic.js";

  let { children } = $props();

  const title = "Quiropráctico en Zinacantepec, cerca de Toluca | CARDIE";
  const description = `Clínica quiropráctica en Zinacantepec: alivio al dolor de espalda, cuello y ciática, y corrección de postura. Consulta $${clinic.price}. Agenda por WhatsApp.`;
  const ogImage = `${SITE_URL}/og-image.jpg`;

  // Datos estructurados: sitio, clínica (negocio local) y preguntas frecuentes
  const clinicId = `${SITE_URL}/#clinic`;
  const graph = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": `${SITE_URL}/#website`,
        name: clinic.name,
        alternateName: ["CARDIE", "Clínica CARDIE", "cardiequiropráctico.com"],
        url: `${SITE_URL}/`,
        inLanguage: "es-MX",
        publisher: { "@id": clinicId },
      },
      {
        "@type": ["MedicalClinic", "LocalBusiness"],
        "@id": clinicId,
        name: clinic.name,
        alternateName: "Quiropráctico CARDIE",
        description:
          "Clínica quiropráctica en Zinacantepec, Estado de México: evaluación postural, ajuste quiropráctico específico y fortalecimiento muscular.",
        url: `${SITE_URL}/`,
        image: ogImage,
        logo: `${SITE_URL}/LogoIcono.png`,
        telephone: clinic.phones[0],
        email: clinic.email,
        priceRange: `$${clinic.price} MXN`,
        currenciesAccepted: "MXN",
        medicalSpecialty: "Chiropractic",
        address: {
          "@type": "PostalAddress",
          streetAddress: `${clinic.address.street}, ${clinic.address.neighborhood}`,
          addressLocality: clinic.address.city,
          addressRegion: clinic.address.region,
          postalCode: clinic.address.postalCode,
          addressCountry: clinic.address.country,
        },
        geo: { "@type": "GeoCoordinates", latitude: clinic.geo.lat, longitude: clinic.geo.lng },
        hasMap: clinic.mapsUrl,
        areaServed: [
          { "@type": "City", name: "Zinacantepec" },
          { "@type": "City", name: "Toluca" },
        ],
        contactPoint: clinic.phones.map((telephone) => ({
          "@type": "ContactPoint",
          telephone,
          contactType: "reservations",
          availableLanguage: "es",
        })),
        sameAs: clinic.social,
        makesOffer: {
          "@type": "Offer",
          price: clinic.price,
          priceCurrency: "MXN",
          itemOffered: { "@type": "MedicalProcedure", name: "Consulta quiropráctica" },
        },
        employee: clinic.practitioners.map((name) => ({ "@type": "Person", name, jobTitle: "Quiropráctico" })),
      },
      {
        "@type": "FAQPage",
        "@id": `${SITE_URL}/#faq`,
        mainEntity: faqs.map((f) => ({
          "@type": "Question",
          name: f.q,
          acceptedAnswer: { "@type": "Answer", text: f.a },
        })),
      },
    ],
  };
  const jsonLd = JSON.stringify(graph).replace(/</g, "\\u003c");
</script>

<svelte:head>
  <link rel="icon" href="/LogoNavegador.png" type="image/png" />
  <link rel="apple-touch-icon" href="/LogoNavegador.png" />
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta
    name="keywords"
    content="quiropráctico Zinacantepec, quiropráctico Toluca, quiropráctico cerca de mí, ajuste quiropráctico, dolor de espalda, dolor de cuello, ciática, postura, CARDIE"
  />
  <meta name="geo.region" content="MX-MEX" />
  <meta name="geo.placename" content="Zinacantepec" />
  <meta name="geo.position" content="{clinic.geo.lat};{clinic.geo.lng}" />
  <meta name="ICBM" content="{clinic.geo.lat}, {clinic.geo.lng}" />

  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="es_MX" />
  <meta property="og:url" content="{SITE_URL}/" />
  <meta property="og:image" content={ogImage} />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Portada de CARDIE Quiropráctico en Zinacantepec" />
  <meta property="og:site_name" content={clinic.name} />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={ogImage} />
  <meta name="application-name" content={clinic.name} />
  <link rel="canonical" href="{SITE_URL}/" />
  {@html `<script type="application/ld+json">${jsonLd}<\/script>`}
</svelte:head>

<div
  class="min-h-screen bg-cardie-dark text-base-content flex flex-col font-sans selection:bg-primary selection:text-primary-content antialiased"
>
  <Navbar />
  <main class="flex-grow">
    {@render children()}
  </main>
  <Footer />
</div>
