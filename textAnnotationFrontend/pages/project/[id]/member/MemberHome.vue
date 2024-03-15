<template>
    <div>
      <!-- Conditional rendering based on projects array length -->
      <div>
        <Portal/>
        <Members />
      </div>
    </div>
  </template>
  
  <script setup>
  import Members from '@/pages/project/[id]/member/Members.vue';
  import Portal from '@/pages/project/[id]/portal.vue';
  
  // Fetch projects when the component mounts
  </script>
  
  <style scoped>
  /* Your CSS here */
  </style>