<template>
  <div>
    <!-- Conditional rendering based on projects array length -->
    <div v-if="hasLabels">
      <Labels />
    </div>
    <div v-else>
      <NoLabelFound />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { usecurrentProjectStore } from "@/stores/currentproject";
import { useLabelStore } from '@/stores/labels';
import NoLabelFound from '@/pages/project/[id]/label/NoLabelFound.vue';
import Labels from '@/pages/project/[id]/label/Labels.vue';
// import Portal from '@/pages/project/[id]/portal.vue';

definePageMeta({
  layout: 'portal'
});

export default defineComponent({
  name: 'LabelHome',
  components: {
    NoLabelFound,
    Labels
  },
  data() {
    return {
      hasLabels: null,
      project: null,
      labels: []
    };
  },

  computed: {
    projectId() {
      return this.$route.params.id;
    },
  },

  methods: {
    async fetchProject() {
      const projectStore = usecurrentProjectStore();
      await projectStore.fetchProjectById(this.projectId);
      this.project = projectStore.project;
     // console.log(this.project);
    },

    async fetchLabelData() {
      const authStore = useAuthStore();
      const token = authStore.accessToken;
      const config = useRuntimeConfig();
      
      let url;
      if (this.project.project_type === 'DocumentClassification') {
        url = `${config.public.baseURL}/project/${this.projectId}/category-types`;
      } else if (this.project.project_type === 'SequenceLabeling') {
        url = `${config.public.baseURL}/project/${this.projectId}/span-types`;
      }

      if (url) {
        try {
          const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
          });
          const data = await response.json();
          this.labels = data
          if(this.labels.length > 0){
            this.hasLabels  = true
          }
         // console.log(data);
        } catch (error) {
          console.error('Error fetching label data:', error);
          // Handle error accordingly
        }
      }
    },

    
  },

  async mounted() {
    await this.fetchProject();
    await this.fetchLabelData();
    
  }
});
</script>

<style scoped>
/* Your CSS here */
</style>
