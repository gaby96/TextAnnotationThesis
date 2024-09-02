<template>
    <div class="button-container grid grid-cols-2 gap-4">
        <!-- Modal toggle -->
        <button @click="openModal"
            class="mt-5 bg-green-500 shadow-xl text-white uppercase text-xs font-semibold px-4 py-2 rounded"
            type="button">
            Add Comment
        </button>

        <button class="mt-5 bg-green-900 shadow-xl text-white uppercase text-xs font-semibold px-4 py-2 rounded"
            type="button">
            Add Guidelines
        </button>
    </div>
    <div class="container">
        <div class="text-container shadow-lg shadow-md p-4" ref="textContainer">
            <span class="word text-lg">
                {{ fullText }}
            </span>
        </div>
        <div class="labels-container ml-6">
            <div class="grid grid-cols-3 gap-y-4 gap-x-0.5">
                <div v-for="label in labels" :key="label.id">
                    <button @click="selectLabel(label)" class="preview-chip"
                        :style="{ backgroundColor: label.background_color, color: label.text_color }">
                        {{ label.text }}
                        <span v-if="label.suffix_key" class="preview-avatar">{{ label.suffix_key }}</span>
                        <span v-if="label.id === selectedLabelID" class="ml-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                            </svg>
                        </span>

                    </button>
                </div>
            </div>

            <!-- component -->
            <div class="min-h-screen py-6 flex flex-col justify-center relative overflow-hidden sm:py-12">
                <div
                    class="border relative px-4 pt-7 pb-8 bg-white shadow-xl w-full max-w-md mx-auto sm:px-10 rounded-b-md">

                    <label for="dropdown" class="block">Model</label>
                    <select id="dropdown" class="border w-full h-10 px-3 mb-5 rounded-md" v-model="selectedModel">
                        <option value="Select an option">Select an option</option>
                        <option value="GPT-4">GPT-4</option>
                        <option value="BERT">BERT</option>
                        <!-- <option value="option3">Option 3</option> -->
                    </select>

                    <!-- <label for="dropdown" class="block">Prompt Technique</label>
                    <select id="dropdown" class="border w-full h-10 px-3 mb-5 rounded-md">
                        <option value="">Select an option</option>
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                        <option value="option3">Option 3</option>
                    </select>

                    <label for="slider1" class="block">Temperature: <span id="slider1Value"
                            class="text-red-500">0.00</span></label>
                    <input type="range" id="slider1"
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer mb-5" min="0" max="1"
                        step="0.01" value="0"
                        oninput="document.getElementById('slider1Value').innerText = parseFloat(this.value).toFixed(2);">
                    <div class="flex justify-between text-xs text-gray-600">
                        <span>0.00</span>
                        <span>1.00</span>
                    </div>

                    <label for="slider2" class="block">Epochs: <span id="slider2Value"
                            class="text-red-500">0.00</span></label>
                    <input type="range" id="slider2"
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer mb-5" min="0" max="1"
                        step="0.01" value="0"
                        oninput="document.getElementById('slider2Value').innerText = parseFloat(this.value).toFixed(2);">
                    <div class="flex justify-between text-xs text-gray-600">
                        <span>0.00</span>
                        <span>1.00</span>
                    </div> -->

                    <button @click="handlePredict"
                        class="mt-5 bg-green-500 shadow-xl text-white uppercase text-sm font-semibold px-14 py-3 rounded">Predict</button>

                </div>
            </div>

        </div>

        <CrudModal :isModalVisible="isModalVisible" :projectId="projectId" :exampleId="exampleId" @close="closeModal" />

    </div>
</template>

<script>
definePageMeta({
    layout: 'portal'
});
import CrudModal from "@/components/CrudModal.vue";
import DropdownMenu from "@/components/DropdownMenu.vue";
import { useAuthStore } from "@/stores/auth"; // Import useAuthStore if using Pinia
import { userStore } from "@/stores/user";
import { toast } from 'vue3-toastify';

export default {
    components: {
        CrudModal,
    },
    data() {
        return {
            labeledWordsArray: [],
            showDropdown: false,
            dropdownPosition: { x: 0, y: 0 },
            labels: [],
            annotation: {},
            annotatedLabel: null,
            fullText: null,
            words: [],
            isModalVisible: false,
            startWordIndex: -1,
            endWordIndex: -1,
            selectedModel: null,
            selectedLabelID: null,
            isSelecting: false,
        };
    },
    computed: {

        projectId() {
            return this.$route.params.id;
        },

        exampleId() {
            return this.$route.params.example_id;
        },

    },
    methods: {
        openModal() {
            this.isModalVisible = true;
        },

        closeModal() {
            this.isModalVisible = false;
        },
        // This method fetches the labels that are going to be used to annotate the data (PER, ORG, etc)
        async fetchCategoryLabels() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;

            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/${this.projectId}/category-types`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const data = await response.json();
                this.labels = data;
                //console.log(this.labels)
            } catch (error) {
                console.error("Error fetching example data:", error);
                // Handle error accordingly
            }
        },

        // This is used to fetch the subject that is to be annotated or might even be annotated
        async fetchDataThatMightBeAnnotated() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/dataset/${this.projectId}/examples/${this.exampleId}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const data = await response.json();
                //console.log(data)
                this.fullText = data.text;
            } catch (error) {
                console.error("Error fetching example data:", error);
                // Handle error accordingly
            }
        },

        // Fetch data about annotations made ({start_offset, label, end_offset, example_id or the full text})
        async fetchAnnotatedLabel() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/categories`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const getLabel = await response.json();
                console.log(getLabel)
                this.selectedLabelID = getLabel[0].label
                //console.log(this.selectedLabelID)
            } catch (error) {
                console.error("Error fetching annotations:", error);
            }
        },


        // Save annotation object which contains the example ID and the label ID
        async saveAnnotation(label_id) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            console.log(label_id)
            const annotationBody = {
                label: label_id,
                example: parseInt(this.exampleId),
            };
            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/categories`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify(annotationBody)
                    }
                );
                if (!response.ok) {
                    throw new Error("Failed to save annotation");
                }
                const data = await response.json();
                // console.log(data)
            } catch (error) {
                console.error("Error saving annotation:", error);
                // Handle error accordingly
            }
        },

        removeAnnotation(index) {
            const word = this.words[index];
            if (word.annotated) {
                this.deleteAnnotation(word.annotation_id);
                word.annotated = false;
                word.label = null;
            }
        },
        async deleteAnnotation(annotation_id) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/spans/${annotation_id}`,
                    {
                        method: "DELETE",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                if (!response.ok) {
                    throw new Error("Failed to delete annotation");
                }
            } catch (error) {
                console.error("Error deleting annotation:", error);
                // Handle error accordingly
            }
        },

        handleClickOutside(event) {
            const dropdownMenu = this.$refs.dropdownMenu;
            if (dropdownMenu && !dropdownMenu.$el.contains(event.target)) {
                this.showDropdown = false;
            }
        },

        async handlePredict() {
            await this.fetchCategoryLabels();
            await this.fetchDataThatMightBeAnnotated();
            const authStore = useAuthStore();
            let userObject = authStore.user;
            if (this.labels.length > 0 && this.fullText) {
                const combinedData = {
                    data1: this.labels,
                    data2: this.fullText,
                    exampleId: parseInt(this.exampleId),
                    selectedModel: this.selectedModel,
                    userId: userObject.id
                };
                //console.log(combinedData)
                await this.handleLLMAnnotate(combinedData);
            } else {
                console.log('One or both data sets are not available for processing');
            }
        },

        async handleLLMAnnotate(combinedData) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;

            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/dataset/examples/docClassllmannotate`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify(combinedData)
                    }
                );
                const data = await response.json();
                const newAnnotations = data.data;
                // console.log(data)
                this.selectedLabelID = newAnnotations[0].label
                toast.success("Text Successfully Annotated")
                console.log("LLM Annotation Response:", this.selectedLabelID);
            } catch (error) {
                console.error("Error during LLM annotation:", error);
            }
        },

        async selectLabel(label) {
            this.selectedLabelID = label.id
            await this.saveAnnotation(this.selectedLabelID)

        },

        userId() {
            const userStoreInstance = userStore();
            console.log(userStoreInstance.userObject);
            return userStoreInstance.userObject;
        },
    },
    mounted() {
        this.fetchDataThatMightBeAnnotated();
        this.fetchCategoryLabels();
        this.fetchAnnotatedLabel();
        document.addEventListener('click', this.handleClickOutside);
    },

    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
};
</script>



<style scoped>
.container {
    display: flex;
}

.preview-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.875rem;
    font-weight: 500;
    margin-right: 0.5rem;
    /* Add spacing between chips */
    /* margin-bottom: 0.5rem; */
    /* Add spacing between rows */
}

.preview-avatar {
    background-color: white;
    /* Adjust background color as needed */
    color: black;
    /* Adjust text color as needed */
    margin-left: 0.5rem;
    padding: 0.25rem 0.5rem;
    border-radius: 50%;
    font-weight: bold;
}

.divider {
    width: 2px;
    background-color: #000000;
    margin: 0 10px;
}

.button-container {
    width: 60%;
    margin-top: auto;
    padding-right: 20px;
}

.text-container {
    width: 60%;
    padding-right: 20px;
    /* Adjust this value to control the spacing between the sections */
}

.labels-container {
    width: 40%;
}

.divider {
    width: 1px;
    /* Thinner border */
    height: 100vh;
    /* Full viewport height */
    background-color: #e5e5e5;
    margin-top: 10vh;
    /* Push the border up */
    margin: 0 10px;
}

.word {
    margin-right: 0px;
    /* cursor: pointer; */
    /* padding: 3px; */
    line-height: 35px;
    transition: background-color 0.3s, box-shadow 0.3s;
    border-radius: 8px;
}

/* .word:hover {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
} */

.annotation-label {
    font-size: 11px;
    padding: 3px;
    top: 20px;
}

.annotation-label {
    display: inline-block;
    margin-left: 5px;
    padding: 3px 5px;
    border-radius: 12px;
    font-size: 10px;
    color: #fff;
}

.annotated-word {
    background-color: #ffeb3b;
    /* Default background color */
    padding: 2px 4px;
    border-radius: 8px;
    display: inline-block;
    transition: background-color 0.3s;
}

.remove-btn {
    background: transparent;
    border: none;
    color: #fff;
    font-weight: bold;
    margin-left: 8px;
    cursor: pointer;
    transition: color 0.2s;
}

.remove-btn:hover {
    color: #ff0000;
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
