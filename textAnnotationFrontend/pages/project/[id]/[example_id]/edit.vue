<template>
    <div>
        <form @submit.prevent="editExampleData">
            <div class="w-full mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
                <div class="flex items-center justify-between px-3 py-2 border-b dark:border-gray-600">

                    <button type="button" data-tooltip-target="tooltip-fullscreen"
                        class="p-2 text-gray-500 rounded cursor-pointer sm:ms-auto hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600">
                        <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 19 19">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13 1h5m0 0v5m0-5-5 5M1.979 6V1H7m0 16.042H1.979V12M18 12v5.042h-5M13 12l5 5M2 1l5 5m0 6-5 5" />
                        </svg>
                        <span class="sr-only">Full screen</span>
                    </button>
                    <div id="tooltip-fullscreen" role="tooltip"
                        class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700">
                        Show full screen
                        <div class="tooltip-arrow" data-popper-arrow></div>
                    </div>
                </div>
                <div class="px-4 py-2 bg-white rounded-b-lg dark:bg-gray-800">
                    <label for="editor" class="sr-only">Edit</label>
                    <textarea id="editor" v-model=item.text rows="50"
                        @input="autoGrow"
                        class="block w-full px-0 text-sm text-gray-800 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400"
                        placeholder="Write an article..." required></textarea>
                </div>
            </div>
            <button type="submit" style="background-color: #047857; color: white;"
                class="inline-flex items-center px-5 py-2.5 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:hover:bg-green-700 dark:focus:ring-green-800">
                Save text
            </button>
        </form>
    </div>
</template>

<script>
definePageMeta({
    layout: 'portal'
})

import { useAuthStore } from '@/stores/auth';
import { toast } from 'vue3-toastify';

export default {

    data() {
        return {
            isLoading: false,
            item: {
                text: ''
            },
            project: [],
            example_id: null,
            projectType: null,
        }
    },

    methods: {
        async fetchExampleDataByID() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/project/dataset/${this.projectId}/examples/${this.exampleId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json()
               // console.log(data)
                this.item = data


            } catch (error) {
                console.error('Error fetching label data:', error);
                // Handle error accordingly
            }
        },

        async editExampleData() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/project/dataset/${this.projectId}/examples/${this.exampleId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },

                    body: JSON.stringify({
                        text: this.item.text
                    }),
                });
                const data = await response.json()
                toast.success("Text Successfully Edited")
                console.log(data)

            } catch (error) {
                console.error('Error fetching label data:', error);
                // Handle error accordingly
            }
        },

        autoGrow(event) {
            const textarea = event.target;
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    },

    computed: {
        projectId() {
            return this.$route.params.id
        },

        exampleId() {
            return this.$route.params.example_id;
        },

        uuid() {
            return this.$route.query.uuid;
        }
    },

    mounted() {
        this.fetchExampleDataByID()
    }
}
</script>