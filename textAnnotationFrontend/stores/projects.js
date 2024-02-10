// stores/projects.js
import { defineStore } from 'pinia';

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    projects: []
  }),
  actions: {
    async fetchProjects() {   
        try {
          const token = localStorage.getItem('accessToken');
          const response = await fetch('http://127.0.0.1:8000/project/projects', {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${token}` // Correct placement inside headers object
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
  }
});