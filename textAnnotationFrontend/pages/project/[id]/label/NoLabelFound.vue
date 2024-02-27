<template>
    <div>
        <div class="flex flex-col items-center justify-center py-12 h-full mt-40">
            <div>
                <a class="mx-2 my-1 flex items-center text-neutral-900 hover:text-neutral-900 focus:text-neutral-900 lg:mb-0 lg:mt-0"
                    href="#">
                    <img class="ml-3" src="~/assets/searchicon.png" style="height: 70px" alt="Search Logo" loading="lazy" />
                </a>
            </div>
            <h1 class="mt-4 text-black text-2xl font-semibold text-center">No Label found</h1>
            <p class="mt-2 text-black text-center">All your Label will be displayed here
            </p>

            <!-- button -->
            <NuxtLink to=`/project/${this.projectId}/label/createlabel`>
                <button style="background-color: #047857; border-radius: 4px; color: white;"
                    class="mt-6 px-4 py-2 text-white font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-green rounded-lg">
                    <!-- Added rounded-lg for more pronounced curves -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 16 16"
                        class="inline-block w-5 h-5 mr-2 -mt-1">
                        <path
                            d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" />
                    </svg>
                    Add a Label
                </button>
            </NuxtLink>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Labels',
  data() {
    return {
      projectId: this.$route.params.id, // Initialize projectId from route params
    };
  },

}
</script>

<style  scoped></style>