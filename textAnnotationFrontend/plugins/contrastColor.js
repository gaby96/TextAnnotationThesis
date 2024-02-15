// plugins/contrastColor.js
export default defineNuxtPlugin(nuxtApp => {
    nuxtApp.provide('contrastColor', (hexString) => {
      const r = parseInt(hexString.substr(1, 2), 16);
      const g = parseInt(hexString.substr(3, 2), 16);
      const b = parseInt(hexString.substr(5, 2), 16);
      return (r * 299 + g * 587 + b * 114) / 1000 < 128 ? '#ffffff' : '#000000';
    });
  });