<template>
  <v-main>
    <p>This is the project - {{ $route.params.id }}</p>
  </v-main>
</template>

<script>
definePageMeta({
  layout: 'portal'
})

import { useAuthStore } from '@/stores/auth';
import { useRuntimeConfig } from '#imports'; // Nuxt 3 auto-imports
// import Portal from '@/pages/project/[id]/portal.vue';
export default {
  data() {
    return {
      Project: [],
      projectId: this.$route.params.id, // Initialize projectId from route params
      dropdownVisible: false, // Controls the visibility of the dropdown
    };
  },
  async mounted() {
    await this.fetchProject();
  },
  methods: {

    async fetchProject() {
      const authStore = useAuthStore();
      const token = authStore.accessToken;
      const config = useRuntimeConfig();

      if (!token) {
        throw new Error('Authentication token not found');
      }

      try {
        const response = await fetch(`${config.public.baseURL}/project/projects/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error(errorData.message || 'Failed to fetch members');
        }
        const data = await response.json();
        console.log(this.data)
      }

      catch (error) {

      }
    },
  }


    

};

</script>