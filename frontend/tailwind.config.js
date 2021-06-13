module.exports = {
  mode: 'jit',
  purge: [
      './templates/tailwind/*.html',
      './templates/tailwind/**/*.html',
      './templates/tailwind/**/**/*.html',
      './templates/tailwind/**/**/**/*.html',
  ],
  theme: {},
  variants: {},
  plugins: [
    // require('@tailwindcss/custom-forms'),
    require('@tailwindcss/typography'),
    // require('tailwindcss-debug-screens'),
  ]
}
