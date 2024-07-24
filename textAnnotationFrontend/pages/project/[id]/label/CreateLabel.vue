<template>
  <div class="p-8 rounded border border-gray-200">
    <h1 class="font-medium text-3xl">Create Label Type</h1>

    <div class="mt-8 grid lg:grid-cols-2 gap-4">
      <div>
        <label for="label-name" class="text-sm text-gray-700 block mb-1 font-medium">Label Name</label>
        <input type="text" v-model="label_name" name="label-name" id="label-name"
          class="bg-gray-100 border border-gray-200 rounded py-1 px-3 block focus:ring-blue-500 focus:border-blue-500 text-gray-700 w-full"
          placeholder="Label Name" />
      </div>

      <div>
        <label for="suffix-key" class="text-sm text-gray-700 block mb-1 font-medium">Suffix Key</label>
        <select v-model="suffixKey" id="suffix-key"
          class="bg-gray-100 border border-gray-200 rounded py-1 px-3 block focus:ring-blue-500 focus:border-blue-500 text-gray-700 w-full">
          <option disabled value="">Choose a Key</option>
          <option v-for="key in availableSuffixKeys" :value="key" :key="key">{{ key }}</option>
        </select>
      </div>

      <div>
        <label for="color" class="text-sm text-gray-700 block mb-1 font-medium">Color</label>
        <input type="text" name="color" id="color" v-model="backgroundColor" :rules="[rules.validColor]"
          @input="$emit('update:backgroundColor', $event)"
          class="bg-gray-100 border border-gray-200 rounded py-1 px-3 block focus:ring-blue-500 focus:border-blue-500 text-gray-700 w-full"
          placeholder="Color" />
      </div>
    </div>

    <div class="mt-4">
      <div class="flex flex-wrap">
        <div v-for="(color, index) in predefinedColors" :key="color" :style="{ backgroundColor: color }"
          @click="setColor(color)" class="color-chip">
        </div>
        <!-- Random Color Button -->
        <button @click="setRandomColor" class="ml-2 bg-gray-200 p-2 rounded">Random Color</button>
      </div>
    </div>

    <div class="preview-container mt-4">
      <label class="preview-title mb-2">Preview</label>
      <div class="preview-chip" :style="{ backgroundColor: backgroundColor, color: textColor }">
        {{ label_name }}
        <span v-if="suffixKey" class="preview-avatar">{{ suffixKey }}</span>
      </div>
    </div>

    <div class="space-x-4 mt-8">
      <button type="submit" @click="submitForm()" style="background-color: #047857"
        class="py-2 px-4 bg-blue-500 text-white rounded disabled:opacity-50">Save</button>

      <!-- Secondary -->
      <button @click="$router.back"
        class="py-2 px-4 bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-100 active:bg-gray-200 disabled:opacity-50">Cancel</button>
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
</style>

<script>
definePageMeta({
  layout: 'portal'
})

import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { usecurrentProjectStore } from "@/stores/currentproject";

export default {
  name: 'CreateLabel',
  data() {
    return {
      label_name: '', // Assuming a model for the input field
      email: '', // Assuming a model for the input field
      job: '', // Assuming a model for the input field
      project: null,
      items: [], // Assuming this is needed for availableSuffixKeys computed property
      suffixKey: '', // Assuming this is needed for availableSuffixKeys computed property
      backgroundColor: '#FFFFFF',
      selectedColorIndex: 0,
      valid: false,
      rules: {
        required: value => !!value || 'Required',
        // Simplified rules for demonstration. You need to implement or correct the actual logic.
        counter: value => (value && value.length <= 100) || 'Label must be less than 100 characters',
        // Placeholder for nameDuplicated and keyDuplicated validations
      },
    };
  },
  computed: {
    availableSuffixKeys() {
      const usedSuffixKeys = this.items
        .map(item => item.suffixKey)
        .filter(item => item !== this.suffixKey);
      const allSuffixKeys = '0123456789abcdefghijklmnopqrstuvwxyz'.split('');
      return allSuffixKeys.filter(item => !usedSuffixKeys.includes(item));
    },

    projectId() {
      //console.log(this.$route.params.id)
      return this.$route.params.id
    },

    predefinedColors() {
      return [
        '#73D8FF',
        '#009CE0',
        '#0062B1',
        '#AEA1FF',
        '#7B64FF',
        '#653294',
        '#FDA1FF',
        '#FA28FF',
        '#AB149E',
        '#68CCCA',
        '#16A5A5',
        '#0C797D',
        '#A4DD00',
        '#68BC00',
        '#194D33',
        '#FCDC00',
        '#FCC400',
        '#FB9E00',
        '#F44E3B',
        '#D33115',
        '#9F0500'
      ]
    },

    textColor() {
      // Implement the logic to determine the text color based on backgroundColor
      // For example, a simple implementation:
      const hex = this.backgroundColor.replace('#', '');
      const r = parseInt(hex.substr(0, 2), 16);
      const g = parseInt(hex.substr(2, 2), 16);
      const b = parseInt(hex.substr(4, 2), 16);
      return (r * 0.299 + g * 0.587 + b * 0.114) > 186 ? '#000000' : '#FFFFFF';
    },
  },

  mounted() {
    this.fetchProject()
  },

  watch: {
    selectedColorIndex(value) {
      if (value < this.predefinedColors.length) {
        this.$emit('update:backgroundColor', this.predefinedColors[this.selectedColorIndex])
      }
    }
  },
  methods: {
    setColor(color) {
      this.backgroundColor = color;
    },

    async fetchProject() {
      const projectStore = usecurrentProjectStore();
      await projectStore.fetchProjectById(this.projectId);
      this.project = projectStore.project;
      console.log(this.project)
    },

    async fetchLabels() {
      const labelStore = useLabelStore();
      await labelStore.fetchLabels(this.projectId);
      this.labels = labelStore.labels; // Assuming labels is an array. Adjust based on your store's structure
    },

    async submitForm() {
      const authStore = useAuthStore()
      const token = authStore.accessToken
      // Prepare the payload including textColor 
      const payload = JSON.stringify({
        text: this.label_name,
        suffix_key: this.suffixKey,
        background_color: this.backgroundColor,
        text_color: this.textColor, // Include the computed textColor here
      });

      if (this.project.project_type === "DocumentClassification") {
        try {
          const config = useRuntimeConfig()
          const response = await fetch(`${config.public.baseURL}/project/${this.projectId}/category-types`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: payload,
          });

          if (!response.ok) {
            console.log(response.error)
            throw new Error('Network response was not ok');

          }

          // Handle success
          const data = await response.json();
          this.fetchLabels();
          // Possibly redirect the user or clear the form
          // Redirect the user to the desired page
          navigateTo(`/project/${this.projectId}/label/labelhome`); // Adjust the path as needed
        } catch (error) {
          console.error('There was a problem with your fetch operation:', error);
          // Handle the error, possibly show user feedback
        }
      }
      else if (this.project.project_type === "SequenceLabeling") {
        try {
          const config = useRuntimeConfig()
          const response = await fetch(`${config.public.baseURL}/project/${this.projectId}/span-types`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: payload,
          });

          if (!response.ok) {
            console.log(response.error)
            throw new Error('Network response was not ok');

          }

          // Handle success
          const data = await response.json();
          this.fetchLabels();
          // Possibly redirect the user or clear the form
          // Redirect the user to the desired page
          navigateTo(`/project/${this.projectId}/label/labelhome`); // Adjust the path as needed
        } catch (error) {
          console.error('There was a problem with your fetch operation:', error);
          // Handle the error, possibly show user feedback
        }
      }
    },

    isUsedName(text) {
      return this.items.filter((item) => item.id !== this.id && item.text === text).length > 0
    },

    isUsedSuffixKey(key) {
      if (key === null) {
        return false
      }
      return this.items.filter((item) => item.id !== this.id && item.suffixKey === key).length > 0
    },

    setRandomColor() {
      const maxVal = 0xffffff
      const randomNumber = Math.floor(Math.random() * maxVal)
      const randomString = randomNumber.toString(16)
      const randColor = randomString.padStart(6, '0')
      this.backgroundColor = `#${randColor.toUpperCase()}`

    }
  },
};

</script>
