<template>
    <div class="">
      <nav class="py-2 px-4 flex justify-between  border-b sticky top-0 bg-white">
        <nuxt-link to="/portal/home">
          <div class="">
            <img class="" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" />
          </div>
        </nuxt-link>
        <div class="flex items-center ">
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
      <div class="side flex flex-col justify-between h-full fixed py-5 px-2 border-r">
        <div class="space-y-8">
  
          <UVerticalNavigation :links="links" class="space-y-6" />
        </div>
  
        <div class="mt-8">
          <UVerticalNavigation :links="otherLinks" />
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
            {
              label: 'Comments',
              icon: 'i-heroicons-chat-bubble-bottom-center-text',
              to: '/portal/comments',
            }
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