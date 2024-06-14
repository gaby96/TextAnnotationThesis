<template>
    <div class="p-4 border-b border-gray-300">
      <div class="flex items-center">
        <div class="flex flex-wrap gap-2">
          <div
            v-for="(cl, index) in classes"
            :key="cl.id"
            class="flex items-center border rounded p-2 cursor-pointer"
            :class="{ 'bg-gray-200': cl.id === currentClass.id }"
            :style="{ borderColor: cl.color.replace('11', '12'), backgroundColor: cl.color.replace('11', '12') + '33' }"
            @click="setCurrentClass(index)"
          >
            <div
              class="flex items-center justify-center w-6 h-6 rounded-full text-white mr-2"
              :style="{ backgroundColor: cl.color.replace('11', '12') }"
            >
              <span v-if="cl.id === currentClass.id">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <p class="mb-0">{{ cl.name }}</p>
            <button
              v-if="showDeleteButtons"
              class="ml-2 text-gray-500 hover:text-red-500"
              @click.stop="handleRemoveClass(cl.id, cl.name)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="flex-grow"></div>
        <div class="mx-4">
          <input
            v-if="showNewClassInput || classes.length === 0"
            v-model="newClassName"
            type="text"
            placeholder="Enter a NER Tag and click [+] to add it"
            class="border rounded p-2 text-sm"
            @keyup.enter="saveNewClass"
          />
          <div v-if="showNewClassInput || classes.length === 0" class="flex mt-2">
            <button
              class="btn btn-primary mx-1"
              @click="saveNewClass"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
            </button>
            <button
              class="btn btn-secondary mx-1"
              @click="showNewClassInput = false"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="flex gap-2">
          <button
            class="btn btn-outline"
            @click="showNewClassInput = true"
          >
            New Tag
          </button>
          <button
            class="btn btn-outline"
            @click="showDeleteButtons = !showDeleteButtons"
          >
            {{ showDeleteButtons ? 'Lock Tags' : 'Edit Tags' }}
          </button>
        </div>
      </div>
    </div>
  </template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useClassesStore } from '@/stores/classes';
import { useProjectsStore } from '@/stores/projects';

const classesStore = useClassesStore();

const showNewClassInput = ref(false);
const newClassName = ref('');
const showDeleteButtons = ref(false);

const classes = computed(() => classesStore.classes);
const currentClass = computed(() => classesStore.currentClass);
const enableKeyboardShortcuts = computed(() => classesStore.enableKeyboardShortcuts);

watch(newClassName, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    newClassName.value = newVal.toUpperCase();
  }
});

onMounted(() => {
  document.addEventListener('keydown', keypress);
});

function keypress(event) {
  if (!enableKeyboardShortcuts.value) {
    return;
  }
  const key = parseInt(event.key, 10);
  if (!key || key > classes.value.length) {
    return;
  }
  setCurrentClass(key - 1);
}

function setCurrentClass(index) {
  classesStore.setCurrentClass(index);
}

async function handleRemoveClass(classId, className) {
  const sure = await confirmAction(className);
  if (sure) {
    classesStore.deleteClass(classId);
  }
}

async function confirmAction(className) {
  return new Promise((resolve) => {
    const result = confirm(
      `Are you sure you want to remove the tag ${className}?\nNOTE: This will NOT affect previously tagged entities.`
    );
    resolve(result);
  });
}

function saveNewClass() {
  if (!newClassName.value) {
    return;
  }
  classesStore.createNewClass(newClassName.value).then(() => {
    showNewClassInput.value = false;
    newClassName.value = '';
  });
}
</script>


<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border: 1px solid transparent;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline {
  border-color: #ccc;
  color: #333;
}

.btn-outline:hover {
  background-color: #e5e5e5;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-secondary {
  background-color: #f44336;
  color: white;
}

.btn-secondary:hover {
  background-color: #e31b0c;
}
</style>


  
  