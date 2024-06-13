<template>
    <div v-if="opened" class="absolute" :style="{ top: y + 'px', left: x + 'px' }">
      <div class="bg-white shadow-lg rounded-md overflow-hidden" style="min-width: 150px; max-height: 400px;">
        <div class="p-2">
          <input
            ref="autocompleteRef"
            v-model="selectedLabelId"
            class="form-input w-full"
            type="text"
            placeholder="Select a label"
          />
        </div>
        <ul class="overflow-y-auto">
          <li v-for="(label, i) in labels" :key="i" @click="onLabelSelected(label.id)" class="p-2 hover:bg-gray-100 cursor-pointer">
            <div class="flex items-center">
              <div v-if="label.suffixKey" class="mr-2">
                <span :style="{ backgroundColor: label.backgroundColor }" class="text-xs py-1 px-2 rounded-full text-white">{{ label.suffixKey }}</span>
              </div>
              <span>{{ label.text }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      labels: {
        type: Array,
        default: () => [],
        required: true,
      },
      opened: {
        type: Boolean,
        default: false,
        required: true,
      },
      selectedLabel: {
        type: Object,
        default: () => null,
        required: false,
      },
      x: {
        type: Number,
        default: 0,
        required: true,
      },
      y: {
        type: Number,
        default: 0,
        required: true,
      },
    },
    data() {
      return {
        selectedLabelId: this.selectedLabel ? this.selectedLabel.id : null,
        autocompleteRef: null,
      };
    },
    computed: {
      hasAnySuffixKey() {
        return this.labels.some((label) => label.suffixKey !== null);
      },
    },
    watch: {
      selectedLabel: {
        handler(newVal) {
          this.selectedLabelId = newVal ? newVal.id : null;
        },
        immediate: true,
      },
    },
    methods: {
      onLabelSelected(labelId) {
        this.$emit('click:label', labelId);
        this.close();
      },
      close() {
        this.$nextTick(() => {
          if (this.$refs.autocompleteRef) {
            this.$refs.autocompleteRef.value = '';
          }
        });
        this.$emit('close');
      },
    },
    mounted() {
      this.$watch(
        () => this.selectedLabelId,
        (newVal) => {
          if (newVal !== null) this.onLabelSelected(newVal);
        }
      );
    },
  };
  </script>
  
  <style>
  /* Add any component-specific styles here */
  </style>
  