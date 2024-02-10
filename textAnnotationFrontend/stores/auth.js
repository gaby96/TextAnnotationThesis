// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null, // Initialize as null
    refreshToken: null,
    isLoading: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken, // Checks if accessToken is not null or undefined
  },

  actions: {
    initializeFromLocalStorage() {
      if (typeof window !== "undefined") {
        this.accessToken = localStorage.getItem('accessToken') || null;
        this.refreshToken = localStorage.getItem('refreshToken') || null;
      }
    },
    setTokens({ accessToken, refreshToken }) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;

      if (typeof window !== "undefined") {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
      }
    },
    clearTokens() {
      this.accessToken = null;
      this.refreshToken = null;

      if (typeof window !== "undefined") {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
    },
    async login(credentials, apiUrl) {
      try {
        this.isloading = true
        const response = await fetch(`${apiUrl}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials),
        })
        const data = await response.json()
        if (response.ok) {
          this.setTokens({ accessToken: data.access, refreshToken: data.refresh })
          this.isloading = false
          return true;
        } else {
          throw new Error(data.detail || 'Login failed')
        }
      } catch (error) {
        console.error('Login error:', error.message)
        throw error
      }
    },
    async logout() {
      this.clearTokens()
      // Additional logout actions like redirecting the user
    },
  },
})
