<template>
  <div class="flex justify-end">
    <div class="w-full overflow-hidden rounded-lg">
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 py-4"
      >
        <div
          v-for="project in projects"
          :key="project.id"
          class="bg-white rounded-lg border border-gray-200 shadow-md p-4 hover:bg-gray-50"
        >
          <RouterLink
            :to="`/project/${project.id}`"
            class="text-cyan-500 hover:text-blue-700 text-lg font-bold block mb-2 capitalize"
            >{{ project.name }}</RouterLink
          >
          <p class="capitalize text-md font-semibold text-gray-700">
            description
          </p>
          <p class="text-gray-700 mb-2">{{ project.description }}</p>
          <div class="flex flex-col mb-2">
            <p class="capitalize text-md font-semibold text-gray-700">
              Project Type
            </p>
            <p class="text-gray-700">
              {{ project.project_type }}
            </p>
          </div>
          <div class="flex flex-col mb-2">
            <p class="capitalize text-md font-semibold text-gray-700">Author</p>

            <p class="text-gray-700">{{ project.author }}</p>
          </div>

          <div class="mb-2">
            <p class="capitalize text-md font-semibold text-gray-700">Tags</p>
            <span
              v-for="tag in project.tags"
              :key="tag.id"
              class="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-600"
            >
              {{ tag.text }}
            </span>
          </div>
          <div class="flex items-center justify-end">
            <a
              href="#"
              @click.prevent="deleteProject(project.id)"
              class="text-red-500 hover:block"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="h-4 w-4"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: "authuser",
});

import { useProjectsStore } from "@/stores/projects";
import { onMounted, ref } from "vue";
import { storeToRefs } from "pinia";
const projectStore = useProjectsStore();
const { fetchProjects } = projectStore;
const { projects } = storeToRefs(projectStore);

onMounted(async () => {
  await projectStore.fetchProjects();
});

async function deleteProject(id) {
  try {
    const authStore = useAuthStore();
    const token = authStore.accessToken;
    if (!token) {
      throw new Error("Authentication token not found");
    }

    const response = await fetch(
      `http://127.0.0.1:8000/project/projects/${id}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "Failed to delete project");
    }

    // Optionally: Remove the project from the local state to update the UI
    const projectsStore = useProjectsStore();
    projectsStore.projects = projectsStore.projects.filter(
      (project) => project.id !== id
    );
    // Optionally: Show a success message
    console.log("Project deleted successfully");
  } catch (error) {
    console.error("Error deleting project:", error);
  }
}
</script>
