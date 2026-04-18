import daisyui from "daisyui";

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,svelte,js,ts}'],
  theme: {
    extend: {
      colors: {
        'cardie-dark': '#060a14',
        blue: {
          50: '#f2f7f6',
          100: '#dfece9',
          200: '#c0dbd5',
          300: '#9bc4bb',
          400: '#83B7AB', // Secundario
          500: '#538f83',
          600: '#215A69', // Principal
          700: '#1d4957',
          800: '#1a3d48',
          900: '#18343d',
          950: '#0d2027',
          brand1: '#215A69',
          brand2: '#83B7AB',
        },
        
      }
    },
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["light", "corporate"], // Temas médicos claros y luminosos
  }
}
