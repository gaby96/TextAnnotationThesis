<template>
  <div class="overflow-hidden rounded-lg border border-gray-200 shadow-md m-5">
    <table class="w-full border-collapse bg-white text-left text-sm text-gray-500">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-4 font-medium text-gray-900">Name</th>
          <th scope="col" class="px-6 py-4 font-medium text-gray-900">Description</th>
          <th scope="col" class="px-6 py-4 font-medium text-gray-900">Project Type</th>
          <th scope="col" class="px-6 py-4 font-medium text-gray-900">Author</th>
          <th scope="col" class="px-6 py-4 font-medium text-gray-900">Tags</th>
          <th scope="col" class="px-6 py-4 font-medium text-gray-900">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100 border-t border-gray-100">
        <tr class="hover:bg-gray-50" v-for="project in projects" :key="project.id">
          <td class="px-6 py-4 font-medium text-gray-900">{{ project.name }}</td>
          <td class="px-6 py-4">{{ project.description }}</td>
          <td class="px-6 py-4">{{ project.project_type }}</td>
          <td class="px-6 py-4">{{ project.author }}</td>
          <td class="px-6 py-4">
            <div class="flex flex-wrap gap-2">
              <span v-for="tag in project.tags" :key="tag.id" class="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-600">
                {{ tag.text }}
              </span>
            </div>
          </td>
          <td class="px-6 py-4 text-center">
            <a href="#" @click.prevent="deleteProject(project.id)">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6 text-red-500 hover:text-red-700 cursor-pointer">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
            </a>
          
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { useProjectsStore } from '@/stores/projects';

export default {
  name: 'ProjectsTable',
  computed: {
    projects() {
      const projectsStore = useProjectsStore();
      return projectsStore.projects;
    }
  },
  created() {
    const projectsStore = useProjectsStore();
    projectsStore.fetchProjects();
  },
  methods: {
    async deleteProject(id) {
      try {
        // Get the access token from localStorage
        const token = localStorage.getItem('accessToken');
        if (!token) {
          throw new Error('Authentication token not found');
        }

        const response = await fetch(`http://127.0.0.1:8000/project/projects/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to delete project');
        }

        // Optionally: Remove the project from the local state to update the UI
        const projectsStore = useProjectsStore();
        projectsStore.projects = projectsStore.projects.filter(project => project.id !== id);

        // Optionally: Show a success message
        console.log('Project deleted successfully');
      } catch (error) {
        console.error('Error deleting project:', error);
      }
    },
  }
};
</script>
