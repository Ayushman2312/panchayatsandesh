/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",  // Adjust if your templates are in a different directory
    "./static/src/**/*.js",   // If you have any Tailwind directives in JavaScript files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}