// stores/projects.js
import { defineStore } from 'pinia';
import { ref } from 'vue';


export const useProjectsStore = defineStore('projects', () => { 

  const projects = ref([])

  async function fetchProjects() {   
    try {
      
      const authStore = useAuthStore()
      const token = authStore.accessToken
      const response = await fetch('http://127.0.0.1:8000/project/projects', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}` 
          }
      });
      if (!response.ok) {
        throw new Error('Failed to fetch projects');
      }
      const data = await response.json();
      this.projects = data;
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  }
  return { fetchProjects, projects }
}, )
