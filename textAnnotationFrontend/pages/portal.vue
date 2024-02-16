<template>
    <div class="">
        <nav class="py-2 px-4 flex justify-between  border-b sticky top-0 bg-white">
            <div class="">
                <img class="" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" />
            </div>
            <div class="flex items-center">
                <a href="" class="mr-4">Projects
                    <UIcon name="i-heroicons-chevron-down-solid" class="relative top-0.5" />
                </a>
                <a href="" class="mr-4">History</a>
                <div class=" rounded-full flex justify-center items-center bg-blue-300 aspect-square w-8">CA</div>
            </div>
        </nav>
        <div class="side w-[300px] flex flex-col justify-between h-full fixed py-5 px-2 border-r">
            <div class="">
                <!-- <img class="ml-3 mb-5" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" /> -->
                <UVerticalNavigation :links="links" />
            </div>

            <div class="">
                <UVerticalNavigation :links="otherLinks" />
            </div>
        </div>
        <div class=" w-full content ml-auto min-h-[100%] p-5">
            <NuxtPage />
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    redirect: '/portal/dashboard'
})
const links = [
    {
        label: 'Home',
        icon: 'i-heroicons-home',
        to: '/portal/home'
    },
    {
        label: 'Datasets',
        icon: 'i-heroicons-circle-stack',
        to: '/portal/dashboard'
    },
    {
        label: 'Labels',
        icon: 'i-heroicons-tag',
        to: '/portal/dashboard'
    },
    {
        label: 'Members',
        icon: 'i-heroicons-users',
        to: '/portal/dashboard'
    },
    {
        label: 'Comments',
        icon: 'i-heroicons-chat-bubble-bottom-center-text',
        to: '/portal/dashboard'
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
    width: calc(100% - 300px)
}

.side {
    height: calc(100% - 50px);
}
</style>