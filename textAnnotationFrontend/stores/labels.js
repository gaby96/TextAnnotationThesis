// stores/labels.js
import { defineStore } from 'pinia';
import { ref } from 'vue';


export const useLabelStore = defineStore('labels', () => { 

  const labels = ref([])

  async function fetchLabels(projectId) {   
    try {
      
      const authStore = useAuthStore()
      const token = authStore.accessToken
      const response = await fetch(`http://127.0.0.1:8000/project/${projectId}/span-types`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}` 
          }
      });
      if (!response.ok) {
        throw new Error('Failed to fetch labels');
      }
      const data = await response.json();
      this.labels = data;
    } catch (error) {
      console.error('Error fetching labels:', error);
    }
  }
  return { fetchLabels, labels }
}, { persist: { persist: true } } )
