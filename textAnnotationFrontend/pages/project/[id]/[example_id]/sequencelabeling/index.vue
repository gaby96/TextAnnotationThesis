<template>
    <p>Sequence Labeling</p>

</template>

<script>
definePageMeta({
    layout: 'portal'
})
import { useAuthStore } from '@/stores/auth';
export default {

    data() {
        return {

            text: null,
        }
    },

    computed: {

        projectId() {
            return this.$route.params.id
        },

        exampleId() {
            return this.$route.params.example_id
        },

    },

    methods: {
        async fetchAnnotatedData() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/dataset/${this.projectId}/examples/${this.exampleId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json();
                console.log(data)
                this.text = data.text;

            } catch (error) {
                console.error('Error fetching example data:', error);
                // Handle error accordingly
            }
        }
    },

    mounted() {
        this.fetchAnnotatedData()
    },


}
</script>