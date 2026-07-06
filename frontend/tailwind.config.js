/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'solca-azul':    '#003366',
        'solca-blanco':  '#FFFFFF',
        'solca-fila':    '#F5F7FA',
        'solca-verde':   '#27AE60',
        'solca-borde':   '#D0D7DE',
      }
    },
  },
  plugins: [],
}
