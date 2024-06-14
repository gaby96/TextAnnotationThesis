<template>
    <mark :class="['p-2 relative border rounded', backgroundColorClass]">
      <component
        :is="'Token'"
        v-for="t in token.tokens"
        :id="'t' + t.start"
        :key="t.start"
        :token="t"
      />
      <span class="tag bg-gray-100 p-1 pl-2 border border-gray-300 rounded text-xs">
        {{ token.label }}
        <button
          class="ml-2 text-gray-500"
          @click="$emit('remove-block', token.start)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
    </mark>
  </template>
  
  <script>
  import Token from "./Token";
  
  export default {
    name: "TokenBlock",
    components: {
      Token,
    },
    props: {
      token: {
        type: Object,
        required: true,
      },
      backgroundColor: {
        type: String,
        required: false,
      },
    },
    computed: {
      backgroundColorClass() {
        return this.backgroundColor ? `bg-${this.backgroundColor}` : 'bg-burlywood';
      },
    },
    emits: ["remove-block"],
    data() {
      return {
        showClose: false,
      };
    },
  };
  </script>
  