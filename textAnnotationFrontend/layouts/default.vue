<template>

    <the-header v-if="!authStore.isLoggedIn" />
    <slot />
    <!-- <the-footer /> -->

</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import TheHeader from '@/components/TheHeader';
import { useAuthStore } from '@/stores/auth';

// Directly use `useAuthStore` to manage authentication state.
const authStore = useAuthStore();




</script>