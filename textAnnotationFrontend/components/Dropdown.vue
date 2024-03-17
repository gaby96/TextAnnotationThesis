<template>

    <div class="dropdown absolute bg-white border py-1 w-max right-0">
        <template v-for="project in projectStore.projects" :key="project.id">
            <NuxtLink :to="`/project/${project.id}`" class="py-1 px-5 hover:bg-neutral-100 block"><span
                    class="text-blue-500 hover:text-blue-700">{{
            project.name
        }}</span> - {{ project.project_type
                }}</NuxtLink>
        </template>
    </div>

</template>

<script setup>
const projectStore = useProjectsStore()
</script>

<style scoped></style>