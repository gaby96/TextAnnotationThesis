<template>
  <div class="">
    <nav class="py-2 px-4 flex justify-between  border-b sticky top-0 bg-white">
      <nuxt-link to="/portal/home">
        <div class="">
          <img class="" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" />
        </div>
      </nuxt-link>
      <div class="flex items-center text-xl">
        <div class="relative group">
          <a href="" class="">Projects
            <UIcon name="i-heroicons-chevron-down-solid" class="relative top-0.5" />
            <div class="hidden group-hover:block">
              <Dropdown />
            </div>
          </a>
        </div>
        <a href="" class="mx-4">History</a>
        <div class=" rounded-full flex justify-center items-center bg-blue-300 aspect-square w-8">C</div>
      </div>
    </nav>
    <div class="side flex flex-col justify-between fixed  px-2 border-r">
      <!-- Increased vertical spacing for primary links -->
       <div class="vertical-navigation">
      <UVerticalNavigation :links="links" />
    </div>
      <!-- Increased vertical spacing for secondary links -->
      <div class="mt-12 text-xl">
        <UVerticalNavigation :links="otherLinks" class="flex flex-col space-y-8 text-xl" />
      </div>
    </div>
    <div class=" w-full content ml-auto min-h-[100%] py-10 lg:px-14 px-5">
      <!-- <NuxtPage /> -->
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import { useRoute } from '#imports';

export default {
  setup() {
    const route = useRoute();
    const links = ref([]);
    const otherLinks = ref([
      {
        label: 'Settings',
        icon: 'i-heroicons-chart-bar',
        to: '/portal/settings',
      },
      {
        label: 'Logout',
        icon: 'i-heroicons-arrow-right-on-rectangle-solid',
        to: '/portal/logout',
      },
    ]);

    const updateLinks = (projectId) => {
      links.value = [
        { label: 'Home', icon: 'i-heroicons-home', to: '/portal/home' },
      ];

      if (projectId) {
        links.value.push(
          { label: 'Datasets', icon: 'i-heroicons-circle-stack', to: `/project/${projectId}/dataimport/` },
          {
            label: 'Labels',
            icon: 'i-heroicons-tag',
            to: `/project/${projectId}/label/labelhome`,
          },
          { label: 'Members', icon: 'i-heroicons-users', to: `/project/${projectId}/member/members` },
          // {
          //   label: 'Comments',
          //   icon: 'i-heroicons-chat-bubble-bottom-center-text',
          //   to: '/portal/comments',
          // }
        );
      }
    };

    watch(() => route.params.id, (newVal) => {
      updateLinks(newVal);
    }, { immediate: true });

    return { links, otherLinks };
  },
}
</script>

<style scoped>
.content {
  width: calc(100% - 250px);
  /* Adjust the content width */
}

.side {
  width: 250px;
  /* Adjust the sidebar width */
  height: calc(100vh - 50px);
  /* Ensure full height minus nav */
}  

.vertical-navigation {
  display: flex;
  flex-direction: column;
}

.vertical-navigation > * {
  margin-bottom: 20px; /* Add vertical space between links */
}

.vertical-navigation > *:last-child {
  margin-bottom: 0; /* Ensure no margin on the last item */
}

@media (max-width: 768px) {

  /* Adjust for medium devices */
  .side {
    width: 50%;
    /* Example adjustment */
  }

  .content {
    width: calc(100% - 50%);
    /* Adjust content width accordingly */
  }
}

@media (max-width: 640px) {

  /* Adjust for small devices */
  .side {
    width: 75%;
    /* Example adjustment for smaller screens */
  }

  .content {
    width: calc(100% - 75%);
    /* Adjust content width accordingly */
  }
}
</style>