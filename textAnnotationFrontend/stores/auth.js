// stores/auth.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore(
  "auth",
  () => {
    const accessToken = ref("");
    const refreshToken = ref("");
    const isLoading = ref(false);
    const isLoggedIn = ref(false);

    async function setTokens({ accessToken, refreshToken }) {
      accessToken.value = accessToken;
      refreshToken.value = refreshToken;
    }

    async function clearTokens() {
      accessToken.value = null;
      refreshToken.value = null;

      if (typeof window !== "undefined") {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
      }
    }

    async function isAuthenticated() {
      let authToken = accessToken.value;
      if (authToken) {
        return True;
      } else {
        return False;
      }
    }
    async function login(credentials, apiUrl) {
      try {
        this.isLoading = true;
        const response = await fetch(`http://localhost:8000/auth/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify(credentials),
        });
        const data = await response.json();

        if (response.ok) {
          this.accessToken = data.access;
          this.refreshToken = data.refresh;
          this.isLoggedIn = true;
          this.isLoading = false;
          return true;
        } else {
          throw new Error(data.detail || "Login failed");
        }
      } catch (error) {
        console.log(error);
        // console.error("Login error:", error.message);
        throw error;
      } finally {
        this.isLoading = false;
      }
    }
    async function logout() {
      this.clearTokens();
      // Additional logout actions like redirecting the user
    }
    return {
      accessToken,
      refreshToken,
      isLoading,
      isLoggedIn,
      setTokens,
      clearTokens,
      isAuthenticated,
      login,
      logout,
    };
  },
  { persist: { persist: true } }
);
