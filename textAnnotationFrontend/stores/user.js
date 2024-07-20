
//stores/user.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth';

export const userStore = defineStore('user', () => {

  const userFirstname = ref('')
  const userLastname = ref('')
  const userObject = ref({})

  async function user() {
    try {
      this.isLoading = true
      const authStore = useAuthStore();
      const token = authStore.accessToken;
      const response = await fetch(`http://localhost:8000/auth/current`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json', // Correct content type for JSON
          'Authorization': `Bearer ${token}`,
        },
      })
      const data = await response.json()
      console.log(data)
      if (response.ok) {
        this.userFirstname = data.first_name
        this.userLastname = data.last_name
        this.userObject = data
        console.log(this.userObject)
        return true;
      } else {
        throw new Error(data.detail || 'Could not fetch user data')
      }
    } catch (error) {
      console.error('No User data', error.message)
      throw error
    }
  };

  return {
    user,
    userFirstname,
    userLastname,
    userObject
  };

  
},
  { persist: { persist: true } }
);