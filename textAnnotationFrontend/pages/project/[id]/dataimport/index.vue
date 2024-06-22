<template>
    <div class="flex justify-center py-10">
        <div class="w-3/5 mb-10">
            <EasyDataTable :headers="headers" :items="items">
                <template #item-text="item">
                    <div class="w-32 truncate">
                        {{ item.text.length > 10 ? item.text.substr(0, 60) + '...' : item.text }}
                    </div>
                </template>
                <template #item-is_confirmed="item">
                    {{ item.is_confirmed ? 'Finished' : 'In progress' }}
                </template>
                <template #item-action="item">
                    <div class=" text-center flex justify-left items-center gap-2">
                        <a href="#" @click.prevent="annotateText(item.id)">
                            <svg xmlns="http://www.w3.org/2000/svg"
                                class="h-6 w-6 text-green-500 hover:text-green-700 cursor-pointer" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M15.172 7l-6.586 6.586a2 2 0 00-.293.293L7 18l3.121-.293a2 2 0 00.293-.293L17 8.828m2-2.828a2 2 0 112 2c-.59-.59-1.418-.59-2 0z" />
                            </svg>
                        </a>
                        <RouterLink :to="`/edit/${item.id}`">
                            <a href="#" @click.prevent="editText(item.id)">
                                <svg xmlns="http://www.w3.org/2000/svg"
                                    class="h-6 w-6 text-blue-500 hover:text-blue-700 cursor-pointer" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M15.232 5.232l3.536 3.536m-2.036-4.732a2.25 2.25 0 113.182 3.182L6.75 20.25H3.75v-3l11.482-11.482z" />
                                </svg>
                            </a>
                        </RouterLink :to="`/edit/${item.id}`">
                        <!-- Delete Icon -->
                        <a href="#" @click.prevent="deleteLabel(item.id)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="h-6 w-6 text-red-500 hover:text-red-700 cursor-pointer">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                            </svg>
                        </a>
                    </div>
                </template>
            </EasyDataTable>
        </div>
    </div>
</template>

<script>
definePageMeta({
    layout: 'portal'
})
import { useAuthStore } from '@/stores/auth';
export default {
    data() {
        return {
            isLoading: false,
            items: [],
            project: [],
            example_id: null,
            projectType: null,
            headers: [
                { text: "Status", value: "is_confirmed", sortable: true },
                { text: "Text", value: "text" },
                { text: "Meta", value: "meta" },
                { text: "Action", value: "action" }
            ],
        }
    },

    methods: {
        async fetchExampleData() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/dataset/${this.projectId}/examples`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json()
                this.items = data


            } catch (error) {
                console.error('Error fetching label data:', error);
                // Handle error accordingly
            }
        },

        async fetchProject() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/project/projects/${this.projectId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json()
                this.project = data
                this.projectType = data.project_type
                //console.log(this.projectType)

            } catch (error) {
                console.error('Error fetching project data:', error);
                // Handle error accordingly
            }
        },


        async annotateText(example_id) {

            if (this.projectType === 'Seq2seq') {
                navigateTo(`/project/${this.projectId}/${example_id}/sequencelabeling`);
            }

            else if (this.projectType === 'DocumentClassification') {
                navigateTo(`/project/${this.projectId}/${example_id}/classification`);
            }
        }

    },

    computed: {
        projectId() {
            return this.$route.params.id
        },
    },

    mounted() {
        this.fetchExampleData();
        this.fetchProject();
    },
}

</script>

<style scoped>
.word {
  margin-right: 0px;
  cursor: pointer;
}

/* .word.highlighted {
} */

.annotation-label {
  font-size: 11px;
  padding: 3px;
  top: 20px;
}

.annotated-word {
  padding: 0 4px;
  border-radius: 4px;
  margin: 0 2px;
  position: relative;
  display: inline-block;
}

.remove-btn {
  font-weight: bold;
  font-size: 9px;
  cursor: pointer;
}

.bg-blue-200 {
  padding: 3px;
  background-color: #33fff9;
  border-radius: 5px;
}

.bg-indigo-200 {
  padding: 3px;
  background-color: #336eff;
  border-radius: 5px;
}
</style>