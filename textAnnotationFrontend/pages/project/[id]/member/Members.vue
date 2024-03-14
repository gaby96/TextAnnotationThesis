<template>
  <div class="flex flex-col justify-end items-start  items-end">

    <div class="relative inline-block text-left">
      <div class="group ">
        <RouterLink :to="`/project/${projectId}/member/createmember`" class="text-blue-500 hover:text-blue-700">
          <button type="button"
            class="inline-flex justify-center items-center px-4 py-2 text-sm font-medium text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:bg-green-600">
            Add Member
            <!-- Dropdown arrow -->
          </button>
        </RouterLink>

      </div>
    </div>

    <div class="w-full overflow-hidden rounded-lg border border-gray-200 shadow-md my-7 mb-4">
      <div class="overflow-x-auto">
        <table class="w-full border-collapse bg-white text-left text-sm text-gray-500 ">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-4 font-medium text-gray-900">Email</th>
              <th scope="col" class="px-6 py-4 font-medium text-gray-900">Role</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 border-t border-gray-100">
            <tr class="hover:bg-gray-50" v-for="label in labels" :key="label.id">
              <td class="px-6 py-4 font-medium text-gray-900">
                <!-- Update this line -->
                {{ label.text }}
              </td>
              <td class="px-6 py-4">
                <div class="preview-chip" :style="{ backgroundColor: label.background_color, color: label.text_color }">
                  {{ label.text }}
                  <span v-if="label.suffix_key" class="preview-avatar">{{ label.suffix_key }}</span>
                </div>
              </td>
              <td class="px-7 py-4 text-center flex justify-left items-center gap-2">
                <!-- Edit Icon -->
                <RouterLink :to="`/project/${projectId}/label/${label.id}/editlabel`">
                  <a href="#" @click.prevent="editLabel(label.id)">
                    <svg xmlns="http://www.w3.org/2000/svg"
                      class="h-6 w-6 text-blue-500 hover:text-blue-700 cursor-pointer" fill="none" viewBox="0 0 24 24"
                      stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.232 5.232l3.536 3.536m-2.036-4.732a2.25 2.25 0 113.182 3.182L6.75 20.25H3.75v-3l11.482-11.482z" />
                    </svg>
                  </a>
                </RouterLink>
                <!-- Delete Icon -->
                <a href="#" @click.prevent="deleteLabel(label.id)">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="h-6 w-6 text-red-500 hover:text-red-700 cursor-pointer">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                  </svg>
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.color-chip {
  height: 32px;
  width: 32px;
  margin-right: 8px;
  margin-bottom: 8px;
  border-radius: 50%;
  cursor: pointer;
}

/* Avatar style */
.avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #fff;
  /* Avatar background color */
  color: #000;
  /* Avatar text color */
  font-weight: bold;
}

.preview-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.preview-title {
  font-weight: bold;
  color: #000;
  /* Adjust the color as needed */
  margin-bottom: 8px;
  /* Adjust spacing as needed */
}

.preview-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.875rem;
  font-weight: 500;
}

.preview-avatar {
  background-color: white;
  /* Adjust background color as needed */
  color: black;
  /* Adjust text color as needed */
  margin-left: 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 50%;
  font-weight: bold;
}

/* Update dropdown menu styles */
.group-hover:visible,
.absolute {
  /* Set the background color to green */
  background-color: #4CAF50;
  /* Example green color */

  /* Adjust width if necessary to fit content */
  width: auto;
  /* Adjust based on your content's width */

  /* Align the dropdown to the left of the parent container */
  left: 0;

  /* Adjust the position to display just above the table */
  top: 100%;
}

/* Ensure text colors contrast well with the green background */
.group-hover:visible a {
  color: white;
  /* Ensure readability against the green background */
}

/* Hover effect for dropdown items */
.group-hover:visible a:hover {
  background-color: #367c39;
  /* Darker green for hover effect */
}
</style>


<script>
definePageMeta({
  layout: 'portal'
})
import { useAuthStore } from '@/stores/auth';
import { useLabelStore } from '@/stores/labels'; // Ensure this is correctly imported based on your project structure
import { useRuntimeConfig } from '#imports'; // Nuxt 3 auto-imports


export default {
  name: 'Labels',
  data() {
    return {
      members: [],
      projectId: this.$route.params.id, // Initialize projectId from route params
      dropdownVisible: false, // Controls the visibility of the dropdown
    };
  },
  async mounted() {
    await this.fetchMembers();
  },
  methods: {

    async fetchMembers() {
      const authStore = useAuthStore();
      const token = authStore.accessToken;
      const config = useRuntimeConfig();

      if (!token) {
        throw new Error('Authentication token not found');
      }

      try {
        const response = await fetch(`${config.public.baseURL}/project/projects/${this.projectId}/members`, {
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
        this.members = data;
      }

      catch (error) {

      }
    },


    async deleteLabel(id) {
      const authStore = useAuthStore();
      const token = authStore.accessToken;
      const config = useRuntimeConfig();

      if (!token) {
        throw new Error('Authentication token not found');
      }

      try {
        const response = await fetch(`${config.public.baseURL}/project/${this.projectId}/category-types/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to delete label');
        }

        // Update the local labels array to reflect the deletion
        this.labels = this.labels.filter(label => label.id !== id);
        this.fetchLabels();
        console.log('Label deleted successfully');
      } catch (error) {
        console.error('Error deleting label:', error);
      }
    },

    editLabel(labelId) {
      this.$router.push(`/project/${this.projectId}/label/${labelId}/editlabel`);
    }
  },

};
</script>
