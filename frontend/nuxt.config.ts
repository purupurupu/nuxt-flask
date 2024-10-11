// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@nuxt/eslint', '@nuxt/ui'],
  eslint: {
    // options here
  },
  css: ['~/assets/css/reset.css'],
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
})