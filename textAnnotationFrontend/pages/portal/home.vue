<template>
  <div>
    <!-- Conditional rendering based on projects array length -->
    <div v-if="hasProjects" >
      <ListProjects />
    </div>
    <NoProjectFound v-else />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useProjectsStore } from '@/stores/projects';
import NoProjectFound from '@/components/NoProjectFound.vue';
import ListProjects from '@/components/ListProjects.vue';

const projectsStore = useProjectsStore();

// Using a computed property to reactively check if projects array is empty
const hasProjects = computed(() => projectsStore.projects.length > 0);

// Fetch projects when the component mounts
onMounted(async () => {
  await projectsStore.fetchProjects();
});
</script>

<style scoped>
/* Your CSS here */
</style>
