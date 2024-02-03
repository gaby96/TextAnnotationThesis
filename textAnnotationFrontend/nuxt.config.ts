// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-socket-io',
    '@pinia/nuxt',
  ],


  plugins: [
    '~/plugins/socket.io.js',
  ],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  io: {
    // module options
    sockets: [{
      name: 'main',
      url: 'http://localhost:3000'
    }]
  },

  runtimeConfig: {
    public: {
      baseURL: process.env.BASE_URL // The actual API URL
    }
  },
  
})
