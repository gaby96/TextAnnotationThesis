<template>
    <div class="mx-auto max-w-screen-xl px-4 py-16 sm:px-6 lg:px-8">
        <div class="mx-auto mb-0 mt-12 max-w-md space-y-4">

            <p class="text-gray-500">
                Select File Format
            </p>
            <div class='relative'>
                <select
                    class="w-full rounded-lg border-gray-600 p-4 mt-5 text-sm shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    v-model="selectedFormat">
                    <option disabled value="">Select Format</option>
                    <option v-for="(format, index) in fileFormats" :value="format.name" :key="index">
                        {{ format.name }}
                    </option>
                </select>

            </div>

            <div v-if="selectedFormat">
                <div class='relative'>
                    <select
                        class="w-full rounded-lg border-gray-600 p-4 mt-5 text-sm shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        v-model="selectedEncoding">
                        <option value="utf_8">Select Encoding</option>
                        <option v-for="(item, index) in textFields[0]" :value="item" :key="index">
                            {{ item }}
                        </option>
                    </select>

                </div>

            </div>
            <file-pond v-if="selectedFormat && acceptedFileTypes !== '*'" ref="pond" chunk-uploads="true"
                label-idle="Drop files here..." :allow-multiple="true" :accepted-file-types="acceptedFileTypes"
                :server="server" :files="myFiles" @processfile="handleFilePondProcessFile"
                @removefile="handleFilePondRemoveFile" />
            <file-pond v-if="selectedFormat && acceptedFileTypes === '*'" ref="pond" chunk-uploads="true"
                label-idle="Drop files here..." :allow-multiple="true" :server="server" :files="myFiles"
                @processfile="handleFilePondProcessFile" @removefile="handleFilePondRemoveFile" />

            <div class="space-x-4 mt-8">
                <button type="submit" @click="importDataset()" style="background-color: #047857"
                    class="py-2 px-4 bg-blue-500 text-white rounded disabled:opacity-50">Save</button>
            </div>

        </div>
    </div>
</template>

<script>
import { nextTick } from 'vue';
import { useAuthStore } from '@/stores/auth';
// Import FilePond
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import "filepond/dist/filepond.min.css";
import vueFilePond from "vue-filepond";
const FilePond = vueFilePond(FilePondPluginFileValidateType)

export default {
    components: {
        FilePond
    },
    data() {
        return {
            fileFormats: [],
            selectedFormat: null,
            valid: false,
            selectedEncoding: null,
            myFiles: [],
            uploadedFiles: [],
            taskId: null,
            errors: [],
            option: { column_data: '', column_label: '', delimiter: '' },
            isImporting: false

        }
    },


    methods: {

        async importDataset() {
            this.isImporting = true;
            const item = this.fileFormats.find((item) => item.display_name === this.selectedFormat)
            console.log(item)
            const config = useRuntimeConfig()
            const authStore = useAuthStore();
            const token = authStore.accessToken
            const url = `${config.public.baseURL}/data_import/projects/${this.$route.params.id}/upload`; // Assuming this is the correct endpoint
            const data = {
                format: item.name,
                task: item.task_id,
                uploadIds: this.uploadedFiles.map((item) => item.serverId),
                ...this.option,
            };

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const responseData = await response.json();
                this.taskId = responseData.task_id; // Adjust based on the actual key in the response

            } catch (error) {
                console.error('Error importing dataset:', error);
                // Handle error, e.g., by setting an error state or displaying a message to the user
            } finally {
                this.isImporting = false;
            }
        },


        handleFilePondProcessFile(error, file) {
            console.log(error)
            this.uploadedFiles.push(file)
            this.$nextTick()
        },
        handleFilePondRemoveFile(error, file) {
            console.log(error)
            const index = this.uploadedFiles.findIndex((item) => item.id === file.id)
            if (index > -1) {
                this.uploadedFiles.splice(index, 1)
                this.$nextTick()
            }
        },

        pollData() {
            const get = (taskId) => {
                const config = useRuntimeConfig()
                const authStore = useAuthStore();
                const token = authStore.accessToken
                return fetch(`${this.config.public.baseURL}/tasks/status/${taskId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .catch(error => {
                        console.error('Fetching error:', error);
                        // Consider how to handle errors, e.g., stopping the polling
                    });
            };

            this.polling = setInterval(async () => {
                if (this.taskId) {
                    try {
                        const res = await get(this.taskId);

                        if (res && res.ready) {
                            clearInterval(this.polling); // Stop polling
                            this.taskId = null;
                            this.errors = res.result.error;
                            this.myFiles = [];
                            this.uploadedFiles = [];
                            this.isImporting = false;

                            if (this.errors.length === 0) {
                                navigateTo(`/project/${this.projectId}/label/labelhome`);
                                //this.$router.push(`/projects/${this.$route.params.id}/dataset`);
                            }
                        }
                    } catch (error) {
                        console.error('Error in polling:', error);
                        // Handle error, possibly stop polling
                    }
                }
            }, 3000);
        },

        async revert(serverId) {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const response = await fetch(`${config.public.baseURL}/fp/revert/${file.serverId}`, {
                    method: 'DELETE', // Specify the request method
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    // If your API expects the serverId in the body, uncomment and modify the following line
                    // body: JSON.stringify({ serverId: serverId }),
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }

                // Handle response data if necessary
                const data = await response.json();
                console.log('Delete successful:', data);
            } catch (error) {
                console.error('Error during DELETE request:', error);
            }
        },

        async fetchCatalog() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/data_import/projects/${this.projectId}/catalog`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json();
                this.fileFormats = data

            } catch (error) {
                console.error('Error fetching label data:', error);
                // Handle error accordingly
            }
        }

    },

    watch: {
        selectedFormat() {
            const item = this.fileFormats.find((item) => item.display_name === this.selectedFormat)
            for (const [key, value] of Object.entries(item.properties)) {
                this.option[key] = value.default
                console.log(this.option)
            }

            this.myFiles = []
            this.uploadedFiles.forEach((file) => {
                this.revert(file.serverId).catch(console.error);
            });
            this.uploadedFiles = []
            this.errors = []
        }
    },

    computed: {
        server() {
            const authStore = useAuthStore(); // Access the auth store
            const token = authStore.accessToken; // Get the current token
            const config = useRuntimeConfig()
            return {
                url: `${config.public.baseURL}/data_import/fp`,
                headers: {
                    'Authorization': `Bearer ${token}` // Use the token here
                },
                process: {
                    url: '/process/',
                    method: 'POST'
                },
                patch: '/patch/',
                revert: '/revert/',
                restore: '/restore/',
                load: '/load/',
                fetch: '/fetch/',
            };
        },
        projectId() {
            return this.$route.params.id
        },
        isDisabled() {
            return this.uploadedFiles.length === 0 || this.taskId !== null || !this.valid
        },
        properties() {
            const item = this.fileFormats.find((item) => item.display_name === this.selectedFormat)
            if (item) {
                return item.properties
            } else {
                return {}
            }
        },
        textFields() {
            const asArray = Object.entries(this.properties)

            const textFields = asArray.map(([key, value]) => {
                if ('enum' in value) {
                    return value.enum
                }
            });
            // console.log(textFields)
            return textFields
        },
        selectFields() {
            const asArray = Object.entries(this.properties)
            const textFields = asArray.filter(([_, value]) => 'enum' in value)
            return Object.fromEntries(textFields)
        },
        acceptedFileTypes() {
            const item = this.fileFormats.find((item) => item.display_name === this.selectedFormat)
            if (item) {
                console.log(item.accept_types)
                return item.accept_types
            } else {
                return ''
            }
        },
        example() {
            const item = this.fileFormats.find((item) => item.display_name === this.selectedFormat)
            if (item) {
                const column_data = 'column_data'
                const column_label = 'column_label'
                if (column_data in this.option && column_label in this.option) {
                    return item.example
                        .replaceAll(column_data, this.option[column_data])
                        .replaceAll(column_label, this.option[column_label])
                        .trim()
                } else {
                    return item.example.trim()
                }
            } else {
                return ''
            }
        }
    },



    mounted() {
        this.fetchCatalog();
    },




}

</script>