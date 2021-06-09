module.exports = {
  mode: 'jit',
  purge: [
      './templates/*.html',
      './templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [
    // require('@tailwindcss/custom-forms'),
    require('@tailwindcss/typography'),
    // require('tailwindcss-debug-screens'),
  ]
}
