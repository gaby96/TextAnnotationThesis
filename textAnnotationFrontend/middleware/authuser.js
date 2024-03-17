// middleware/auth.js
import { useAuthStore } from "@/stores/auth";
import { useProjectsStore } from "@/stores/projects";

export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const projects = useProjectsStore();
    const auth = useAuthStore();
    // Check if accessToken exists in localStorage
    const accessToken = auth.isLoggedIn;

    // If there's no accessToken and the user is not trying to access the login page, redirect to login
    if (!auth.accessToken && to.path !== "auth/login") {
      return navigateTo("auth/login");
    }

    // If there's an accessToken, you might want to validate it or ensure the user isn't navigating to the login page
    if (auth.accessToken && to.path === "auth/login") {
      // Here, we check if the projects array is not empty
      return navigateTo("/portal/home");
    }

    // If there's an accessToken, you might want to validate it or ensure the user isn't navigating to the homepage
    if (auth.accessToken && to.path === "/") {
      // Here, we check if the projects array is not empty
      return navigateTo("/portal/home");
    }
  }
});
