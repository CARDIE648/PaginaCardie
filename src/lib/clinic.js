// Datos de la clínica: una sola fuente para la página, el footer y los datos
// estructurados de Google (así nunca se contradicen).
// Horarios: pendientes de confirmar con la clínica; al tenerlos, agregar
// `hours` y se publicarán solos en el JSON-LD (openingHoursSpecification).

export const SITE_URL = "https://xn--cardiequiroprctico-bsb.com";

export const clinic = {
  name: "CARDIE Quiropráctico",
  shortName: "CARDIE",
  phones: ["+52 729 114 3732", "+52 722 387 3457"],
  whatsapp: "527291143732",
  email: "cardie.quiropracticos@gmail.com",
  address: {
    street: "Av. 16 de Septiembre 339-A, Interior 1",
    neighborhood: "Vista Nevado I",
    city: "San Miguel Zinacantepec",
    region: "Estado de México",
    postalCode: "51350",
    country: "MX",
  },
  geo: { lat: 19.2906208, lng: -99.7342157 },
  // Ficha de Google Maps de "Quiropráctico CARDIE"
  mapsUrl: "https://maps.google.com/?cid=14469237074622139271",
  mapsEmbed:
    "https://maps.google.com/maps?q=19.2906208,-99.7342157(Quiropr%C3%A1ctico%20CARDIE)&z=16&output=embed",
  social: [
    "https://www.facebook.com/share/16m2Ka5kbp/",
    "https://www.instagram.com/cardiequiropracticos",
  ],
  price: 400, // consulta quiropráctica (precio único)
  practitioners: [
    "Lic. en Quiropráctica Hugo Diego Esquivel Almazán",
    "Lic. en Quiropráctica Carolina Ocaña Malváez",
  ],
};

export const addressOneLine = `${clinic.address.street}, ${clinic.address.neighborhood}, ${clinic.address.postalCode} ${clinic.address.city}, Méx.`;

export const faqs = [
  {
    q: "¿Dónde está la clínica quiropráctica CARDIE?",
    a: `Estamos en ${addressOneLine}, a unos minutos de Toluca. En el mapa de esta página puedes ver cómo llegar.`,
  },
  {
    q: "¿Cuánto cuesta una consulta con el quiropráctico?",
    a: `La consulta cuesta $${clinic.price} MXN e incluye historia clínica, examen postural, pruebas ortopédicas y neurológicas, ajuste específico y activación muscular.`,
  },
  {
    q: "¿Cómo agendo una cita?",
    a: "Escríbenos por WhatsApp al 729 114 3732 o llámanos al 722 387 3457. Te confirmamos el horario disponible y resolvemos tus dudas antes de tu visita.",
  },
  {
    q: "¿Duele un ajuste quiropráctico?",
    a: "Por lo general no. Durante el ajuste puedes sentir presión y a veces escuchar un chasquido, que es la liberación de gas de la articulación. Antes de cualquier ajuste hacemos una evaluación para elegir la técnica adecuada para ti.",
  },
  {
    q: "¿Cuántas sesiones voy a necesitar?",
    a: "Depende de tu caso. En la primera consulta evaluamos tu postura y tu columna y te proponemos un plan; el seguimiento habitual es semanal.",
  },
  {
    q: "¿Quién me atiende?",
    a: `Te atienden licenciados en Quiropráctica con cédula profesional: ${clinic.practitioners.join(" y ")}.`,
  },
];
