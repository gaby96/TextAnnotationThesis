<template>
<div class="mx-auto max-w-screen-xl px-4 py-16 sm:px-6 lg:px-8">
  <div class="mx-auto max-w-lg text-center">
    <h1 class="text-2xl font-bold sm:text-3xl">Get started today!</h1>

    <p class="mt-4 text-gray-500">
      Create a project and add members to a project
    </p>
  </div>

  <form action="" class="mx-auto mb-0 mt-12 max-w-md space-y-4">
    <div>
      <label for="project-name" class="sr-only">Project Name</label>

      <div class="relative">
        <input
          type="text"
          class="w-full rounded-lg border-gray-200 p-4 mt-5 pe-12 text-sm shadow-sm"
          placeholder="Enter Project Name"
        />

      </div>
    </div>

    <div>
      <label for="description" class="sr-only">Description</label>

      <div class="relative">
        <input
          type="text"
          class="w-full rounded-lg border-gray-200 mt-5 p-4 pe-12 text-sm shadow-sm"
          placeholder="Enter Project Description"
        />
      </div>
    </div>
    <div>
     
      <div>
        <div class="flex flex-wrap  mt-5 items-center gap-2">
          <template v-for="(tag, index) in selectedTags">
            <span class="flex items-center gap-2 rounded-full bg-blue-100 px-3 py-1 text-sm mt-5 text-blue-800">
              {{ tag }}
              <button
                type="button"
                @click="removeTag(index)"
                class="rounded-full bg-blue-200 p-1 text-blue-500 hover:bg-blue-300 focus:outline-none"
              >
                &times;
              </button>
            </span>
          </template>
          <input
            type="text"
            class="w-full rounded-lg border-gray-200 p-2  mt-5 text-sm shadow-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="Add a tag"
            @keydown.enter.prevent="addTag"
            v-model="newTag"
          />
        </div>
      </div>
    </div>
    <div>
        <div class="relative">
            <div class="flex items-center">
                    <input id="checkbox-1" aria-describedby="checkbox-1" type="checkbox" class="bg-gray-50 border-gray-300 focus:ring-3 mt-5 focus:ring-blue-300 h-5 w-5 rounded" checked="">
                    <label for="checkbox-1" class="text-l ml-3 mt-5 font-medium text-gray-900">Allow single label</label>

            </div>
        </div>
    </div>

    <div>
        <div class="relative">
            <div class="flex items-center">
                    <input id="checkbox-1" aria-describedby="checkbox-1" type="checkbox" class="bg-gray-50 border-gray-300 mt-5 focus:ring-3 focus:ring-blue-300 h-5 w-5 rounded" checked="">
                    <label for="checkbox-1" class="text-l ml-3 mt-5 font-medium text-gray-900">Allow project members to create label types</label>

            </div>
        </div>
    </div>

    <div>
        <div class="relative">
            <div class="flex items-center">
                    <input id="checkbox-1" aria-describedby="checkbox-1" type="checkbox" class="bg-gray-50 border-gray-300 mt-5 focus:ring-3 focus:ring-blue-300 h-5 w-5 rounded" checked="">
                    <label for="checkbox-1" class="text-l ml-3 font-medium mt-5 text-gray-900">Share annotations across all users </label>

            </div>
        </div>
    </div>

    <div>
        <button type="submit" style="background-color: #047857; color: white;" class="w-full text-white hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 mt-5 py-2.5 text-center dark:hover:bg-green-700 dark:focus:ring-green-800">Create</button>
    </div>
  </form>
</div>
</template>


<script>
export default {
  data() {
    return {
      newTag: '',
      selectedTags: [],
    };
  },
  methods: {
    addTag() {
      if (this.newTag.trim() !== '' && !this.selectedTags.includes(this.newTag)) {
        this.selectedTags.push(this.newTag.trim());
        this.newTag = ''; // Reset input after adding
      }
    },
    removeTag(index) {
      this.selectedTags.splice(index, 1);
    },
  },
};
</script>