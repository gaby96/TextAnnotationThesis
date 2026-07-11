<template>
    <div v-if="isExportModalVisible" id="crud-modal" tabindex="-1" aria-hidden="true" role="dialog" aria-modal="true"
        class="fixed inset-0 z-50 flex items-center justify-center bg-gray-600 bg-opacity-75">
        <div class="relative p-4 w-full max-w-md max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                        Export Options
                    </h3>
                    <button type="button" @click="closeExportModal"
                        class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                        </svg>
                        <span class="sr-only">Close modal</span>
                    </button>
                </div>
                <!-- Modal body -->
                <div class="p-4 md:p-5">
                    <div class="mb-4">
                        <label for="exportFormat"
                            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select Export
                            Format</label>
                        <select v-model="selectedFormat" id="exportFormat"
                            class="block w-full p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-green-500 focus:border-green-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white">
                            <option value="" disabled>Select format</option>
                            <option value="JSONL">JSONL</option>
                        </select>
                    </div>
                    <button @click="downloadRequest"
                        class="w-full text-white bg-green-500 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">
                        Export
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { toast } from 'vue3-toastify';
import { useAuthStore } from '@/stores/auth'; // Assuming this is the path for the auth store
import { useRuntimeConfig } from '#app'; // Assuming this is how the runtime config is accessed

export default {
    props: {
        isExportModalVisible: {
            type: Boolean,
            required: true
        },
        projectId: {
            type: String,
            required: true
        },
        exampleId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            selectedFormat: '', // Holds the selected export format
            polling: null,
            taskId: '' // Changed from task_id to taskId for consistency
        };
    },
    methods: {
        closeExportModal() {
            this.$emit('close');
        },
        async downloadRequest() {
            if (!this.selectedFormat) {
                alert('Please select an export format.');
                return;
            }
            try {
                const authStore = useAuthStore();
                const token = authStore.accessToken;
                const config = useRuntimeConfig();

                // Data for the request
                const data = {
                    format: this.selectedFormat,
                    exportApproved: false // Corrected 'True' to 'true'
                };

                // Sending export request
                const response = await fetch(
                    `${config.public.baseURL}/export/projects/${this.projectId}/download`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify(data)
                    }
                );

                const responseData = await response.json();
                this.taskId = responseData.task_id;

                this.pollData(); // Start polling for the task status
                this.closeExportModal();
            } catch (error) {
                console.error("Error Exporting Data in downloadRequest method:", error);
            }
        },

        pollData() {
            const get = (taskId) => {
                const config = useRuntimeConfig();
                const authStore = useAuthStore();
                const token = authStore.accessToken;

                return fetch(`${config.public.baseURL}/data_export/tasks/status/${taskId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                       
                        return response.json();
                    })
                    .then(res => {
                        if (res.ready) {
                            console.log("This run")
                            this.download(); // Call the download method if res.ready is true
                        }
                    })
                    .catch(error => {
                        console.error('Fetching error:', error);
                        // Consider how to handle errors, e.g., stopping the polling
                    });
            };

            // Example of starting polling (assuming taskId is already available)
            this.polling = setInterval(async () => {
                if (this.taskId) {
                    try {
                        await get(this.taskId); // Call the get function for task status
                    } catch (error) {
                        console.error('Polling error:', error);
                        clearInterval(this.polling); // Stop polling on error
                    }
                }
            }, 1000); // Polling every 1 second
        },

        async download() {
            try {
                const authStore = useAuthStore();
                const token = authStore.accessToken;
                const config = useRuntimeConfig();

                // Fetching the file
                const response = await fetch(
                    `${config.public.baseURL}/export/projects/${this.projectId}/download?taskId=${this.taskId}`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );

                // Create the download URL from response blob
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', `${this.taskId}.zip`);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link); // Clean up after download

                clearInterval(this.polling); // Stop polling once the file is downloaded

            } catch (error) {
                console.error("Error Exporting Data in download method:", error);
                clearInterval(this.polling); // Stop polling on error
            }
        }

    }
}
</script>
