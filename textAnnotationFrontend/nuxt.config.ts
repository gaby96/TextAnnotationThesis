// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    // '@nuxtjs/tailwindcss',
    'nuxt-socket-io',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    '@nuxt/ui',
  ],


  plugins: [
    '~/plugins/socket.io.js',
    '~/plugins/easy-data-table.js'
  ],

  // postcss: {
  //   plugins: {
  //     tailwindcss: {},
  //     autoprefixer: {},
  //   },
  // },

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

  // nuxt/ui only light theme 
  colorMode: {
    preference: 'light'
  }

})
