<template>
    <div class="">
        <div class="w-[300px] flex flex-col justify-between  h-screen fixed py-5 px-2">
            <div class="">
                <img class="ml-3 mb-5" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" />
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
const links = [{
    label: 'Dashboard',
    icon: 'i-heroicons-home',
    to: '/portal/dashboard'
}]

const otherLinks = [{
    label: 'Settings',
    icon: 'i-heroicons-chart-bar',
    to: '/portal/settings'
}, {
    label: 'Logout',
    icon: 'i-heroicons-command-line',
    to: '/portal/logout',
}]
</script>

<style scoped>
.content {
    width: calc(100% - 300px)
}
</style>