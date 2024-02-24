<template>
    <div>
      <!-- Conditional rendering based on projects array length -->
      <div v-if="hasLabels" >
        <Portal/>
        <Labels />
      </div>
      <NoLabelFound v-else />
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  import { useLabelStore } from '@/stores/labels';
  import NoLabelFound from '@/components/NoLabelFound.vue';
  import Labels from '@/pages/project/[id]/label/[label_id]/Labels.vue';
  import Portal from '@/pages/project/[id]/portal.vue';
  
  const labelsStore = useLabelStore();
  
  // Using a computed property to reactively check if projects array is empty
  const hasLabels = computed(() => labelsStore.labels.length > 0);
  
  // Fetch projects when the component mounts
  </script>
  
  <style scoped>
  /* Your CSS here */
  </style>
  