// stores/currentproject.js
import { defineStore } from 'pinia'
import { ref } from 'vue'


export const usecurrentProjectStore = defineStore('currentProject', () => {

  const project = ref(null);

    // Function to fetch a single project by ID
  async function fetchProjectById(projectId) {
    try {
      const authStore = useAuthStore();
      const token = authStore.accessToken;
      const response = await fetch(`http://127.0.0.1:8000/project/projects/${projectId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch project with ID ${projectId}`);
      }
      project.value = await response.json();
    } catch (error) {
      console.error(`Error fetching project with ID ${projectId}:`, error);
    }
  }


    return { fetchProjectById, project };

})