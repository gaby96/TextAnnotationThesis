<template>
    <div class="">
        <nav class="py-2 px-4 flex justify-between  border-b sticky top-0 bg-white">
            <nuxt-link to="/portal/home">
            <div class="">
                <img class="" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" />
            </div>
        </nuxt-link>
            <div class="flex items-center">
                <a href="" class="mr-4">Projects
                    <UIcon name="i-heroicons-chevron-down-solid" class="relative top-0.5" />
                </a>
                <a href="" class="mr-4">History</a>
                <div class=" rounded-full flex justify-center items-center bg-blue-300 aspect-square w-8">CA</div>
            </div>
        </nav>
        <div class="side flex flex-col justify-between h-full fixed py-5 px-2 border-r">
            <div class="space-y-4">
                
                <UVerticalNavigation :links="links" class="space-y-2" />
            </div>

            <div class="mt-8">
                <UVerticalNavigation :links="otherLinks" />
            </div>
        </div>
        <div class=" w-full content ml-auto min-h-[100%] p-5">
            <NuxtPage />
        </div>
    </div>
</template>

<script setup>
const links = [
    {
        label: 'Home',
        icon: 'i-heroicons-home',
        to: '/portal/home'
    },
    {
        label: 'Datasets',
        icon: 'i-heroicons-circle-stack',
        to: '/portal/home'
    },
    {
        label: 'Labels',
        icon: 'i-heroicons-tag',
        to: '/portal/home'
    },
    {
        label: 'Members',
        icon: 'i-heroicons-users',
        to: '/portal/home'
    },
    {
        label: 'Comments',
        icon: 'i-heroicons-chat-bubble-bottom-center-text',
        to: '/portal/home'
    },
]

const otherLinks = [{
    label: 'Settings',
    icon: 'i-heroicons-chart-bar',
    to: '/portal/settings'
}, {
    label: 'Logout',
    icon: 'i-heroicons-arrow-right-on-rectangle-solid',
    to: '/portal/logout',
}]

const navigationLinks = [
    [{
        label: 'Installation',
        icon: 'i-heroicons-home',
        to: '/portal'
    }, {
        label: 'Horizontal Navigation',
        icon: 'i-heroicons-chart-bar',
        to: '/portal'
    }, {
        label: 'Command Palette',
        icon: 'i-heroicons-command-line',
        to: '/portal'
    }], [{
        label: 'Examples',
        icon: 'i-heroicons-light-bulb'
    }, {
        label: 'Help',
        icon: 'i-heroicons-question-mark-circle'
    }]]
</script>

<style scoped>
.content {
    width: calc(100% - 300px); /* Adjust the content width */
}

.side {
    width: 250px; /* Adjust the sidebar width */
    height: calc(100vh - 50px); /* Ensure full height minus nav */
}

@media (max-width: 768px) { /* Adjust for medium devices */
    .side {
        width: 50%; /* Example adjustment */
    }
    .content {
        width: calc(100% - 50%); /* Adjust content width accordingly */
    }
}

@media (max-width: 640px) { /* Adjust for small devices */
    .side {
        width: 75%; /* Example adjustment for smaller screens */
    }
    .content {
        width: calc(100% - 75%); /* Adjust content width accordingly */
    }
}
</style>