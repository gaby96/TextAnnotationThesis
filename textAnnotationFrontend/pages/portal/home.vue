<template>
  <div>
    <!-- <Portal /> -->
    <!-- Conditional rendering based on projects array length -->
    <div v-if="hasProjects">
      <div class="relative inline-block text-right mt-5">
        <div class="group ">
          <RouterLink :to="`/project/createproject`" class="text-blue-500 hover:text-blue-700">
            <button type="button"
              class="inline-flex justify-center items-center px-4 py-2 text-sm font-medium text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:bg-green-600  xl:ml-96 xs:ml-16 md:ml-32 sm:ml-16">
              Add Project
              <!-- Dropdown arrow -->
            </button>
          </RouterLink>

        </div>
      </div>

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
import Portal from '@/pages/project/[id]/portal.vue';
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
