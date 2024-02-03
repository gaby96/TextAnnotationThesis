// middleware/auth.js
import { useAuthStore } from '@/stores/auth';
export default defineNuxtRouteMiddleware((to, from) => {
    if (process.client) { // Ensure this code runs only on the client side
        // Access the global Nuxt app instance
        const auth = useAuthStore();
      
        // Check if accessToken exists in localStorage
        const accessToken = localStorage.getItem('accessToken');
      
        // If there's no accessToken and the user is not trying to access the login page, redirect to login
        if (!accessToken && to.path !== 'auth/login') {
          return navigateTo('auth/login');
        }
      
        // If there's an accessToken, you might want to validate it or ensure the user isn't navigating to the login page
        if (accessToken && to.path === 'auth/login') {
          return navigateTo('/emptydashboard'); // Redirect to the homepage or dashboard
        }
      }
  });