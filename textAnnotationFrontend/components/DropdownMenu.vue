<template>
  <div class="dropdown-menu" :style="{ top: position.y + 'px', left: position.x + 'px' }">
    <ul>
      <li v-for="label in labels" :key="label.id" @click="selectLabel(label)">
        {{ label.text }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    labels: Array,
    position: Object,
  },
  emits: ['label-selected'],
  methods: {
    selectLabel(label) {
      this.$emit('label-selected', label);
    },
  },
};
</script>

<style scoped>
.dropdown-menu {
  position: absolute;
  background-color: white;
  border: 1px solid #ddd;
  z-index: 1000;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  padding: 0;
  border-radius: 8px;
  overflow: hidden;
  min-width: 150px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

li:hover {
  background-color: #f1f1f1;
}
</style>
