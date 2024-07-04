<template>
    <div class="container">
        <div class="text-container" ref="textContainer">
            <span v-for="(word, index) in words" :key="index" class="word text-lg space-x-10"
                style="padding: 3px; line-height: 35px" @dblclick="handleDoubleClick(index)" :style="{
                    padding: '3px',
                    lineHeight: '35px',
                    backgroundColor: word.annotated ? word.label.background_color : ''
                }">
                {{ word.text }}
                <span v-if="word.annotated" class="annotation-label text-xs rounded-lg"
                    :style="{ backgroundColor: word.label.background_color }">
                    {{ word.label.text }}
                    <button class="remove-btn" @click="removeAnnotation(index)">X</button>
                </span>
            </span>
        </div>

        <div>
            <DropdownMenu v-if="showDropdown" :labels="labels" ref="dropdownMenu" :position="dropdownPosition"
                @label-selected="applyLabel" />
        </div>

        <div class="divider"></div>

        <div class="labels-container">
            <div class="grid grid-cols-3 gap-y-4 gap-x-0.5">
            <div v-for="label in labels" :key="label.id">
                <div class="preview-chip" :style="{ backgroundColor: label.background_color, color: label.text_color }">
                    {{ label.text }}
                    <span v-if="label.suffix_key" class="preview-avatar">{{ label.suffix_key }}</span>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
definePageMeta({
    layout: 'portal'
});
import DropdownMenu from "@/components/DropdownMenu.vue";
import { useAuthStore } from "@/stores/auth"; // Import useAuthStore if using Pinia
import { userStore } from "@/stores/user";

export default {
    components: {
        DropdownMenu,
    },
    data() {
        return {
            labeledWordsArray: [],
            showDropdown: false,
            dropdownPosition: { x: 0, y: 0 },
            labels: [],
            annotation: {},
            annotations: [],
            fullText: null,
            words: [],
            startWordIndex: -1,
            endWordIndex: -1,
            isSelecting: false,
        };
    },
    computed: {
        renderedText() {
            return this.words.map((word) => word.text).join("");
        },

        annotateId() {
            return this.$route.params.annotate_id;
        },

        projectId() {
            return this.$route.params.id;
        },

        exampleId() {
            return this.$route.params.example_id;
        },

        //   userId() {
        //     const userStore = userStore();
        //     return userStore.userObject;
        //   },
    },
    methods: {

        //This method fetches the labels that are going to be used to annotate the data (PER, ORG, etc)
        async fetchLabels() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;

            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/${this.projectId}/span-types`,
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

            } catch (error) {
                console.error("Error fetching example data:", error);
                // Handle error accordingly
            }
        },



        // this is used to fetch the subject that is to be annotated or might even be annotated
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
                console.log(data)
                this.fullText = data.text;
                this.processText(this.fullText);
                this.fetchAnnotations();
            } catch (error) {
                console.error("Error fetching example data:", error);
                // Handle error accordingly
            }
        },

        //fetch data about annotations made ({start_offset, label, end_offset, example_id or the full text})
        async fetchAnnotations() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/spans`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const annotations = await response.json();
                this.applyAnnotations(annotations);
            } catch (error) {
                console.error("Error fetching annotations:", error);
            }
        },
        applyAnnotations(annotations) {
            this.annotations = annotations;
            this.words = this.calculateOffsets(); // Calculate offsets for all words

            annotations.forEach(annotation => {
                const label = this.labels.find(l => l.id === annotation.label);
                if (!label) return;

                this.words.forEach(word => {
                    if (word.startOffset >= annotation.start_offset && word.endOffset <= annotation.end_offset) {
                        word.annotated = true;
                        word.label = label;
                        word.annotation_id = annotation.id;
                    }
                });
            });
        },
        processText(text) {
            const lines = text.split("\n");
            this.words = lines.flatMap((line) => {
                const wordsInLine = line.split(" ").map((word) => ({
                    text: word,
                    annotated: false,
                    label: null,
                    startOffset: null,
                    endOffset: null,
                    annotation_id: null
                }));
                wordsInLine.push({ text: "\n", annotated: false, label: null, startOffset: null, endOffset: null });
                return wordsInLine;
            });
        },
        handleDoubleClick(index) {
            // Handle double click event on a specific word (index)
            this.startWordIndex = index;
            this.endWordIndex = index;
            this.calculateDropdownPosition(index);
            this.showDropdown = true; // Show dropdown menu
        },

        calculateDropdownPosition(index) {
            // Calculate position based on the index of the word
            const spanElement = this.$refs.textContainer.children[index];
            if (spanElement) {
                const rect = spanElement.getBoundingClientRect();
                this.dropdownPosition.x = rect.left + window.scrollX;
                this.dropdownPosition.y = rect.bottom + window.scrollY;
            }
        },
        calculateOffsets() {
            let offset = 0;
            return this.words.map((word) => {
                const startOffset = offset;
                const endOffset = startOffset + word.text.length;
                offset = endOffset + 1; // +1 for the space or line break
                return { ...word, startOffset, endOffset };
            });
        },
        async applyLabel(label) {
            if (this.startWordIndex !== -1 && this.endWordIndex !== -1) {
                // Apply label to the words from startWordIndex to endWordIndex
                this.words = this.calculateOffsets(); // Calculate offsets for all words

                for (let i = this.startWordIndex; i <= this.endWordIndex; i++) {
                    if (!this.words[i].annotated) {
                        this.words[i].annotated = true;
                        this.words[i].label = label;
                        const annotation = {
                            label: label.id,
                            start_offset: this.words[i].startOffset,
                            end_offset: this.words[i].endOffset,
                            example: parseInt(this.exampleId),
                        };

                        console.log(annotation)
                        // Check if the word is already in labeledWordsArray
                        const existingIndex = this.labeledWordsArray.findIndex(
                            (item) => item.start_offset === annotation.start_offset && item.endOffset === annotation.end_offset
                        );

                        if (this.words[i].annotated) {
                            // If the word is already annotated, update the annotation
                            annotation.id = this.words[i].annotation_id;
                            this.labeledWordsArray[existingIndex] = annotation;
                           // await this.updateAnnotation(annotation);
                        } else {
                            // Add new entry to labeledWordsArray
                            this.words[i].annotated = true;
                            this.words[i].label = label;
                            this.labeledWordsArray.push(annotation);
                            await this.saveAnnotation(annotation);
                        }


                    }
                }

                // Reset selection and hide dropdown
                this.startWordIndex = -1;
                this.endWordIndex = -1;
                this.showDropdown = false;

                // Log the updated array of labeled words
                //console.log(this.labeledWordsArray);
            }
        },

        //save annotation object which contains the start_offset, end_offset, label, data
        async saveAnnotation(annotation) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            //console.log(token)
            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/spans`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },

                        body: JSON.stringify(annotation)
                    }
                );
                if (!response.ok) {
                    console.log(response)
                    throw new Error("Failed to save annotation");
                }
                const data = await response.json();
                annotation.id = data.id;
            } catch (error) {
                console.error("Error saving annotation:", error);
                // Handle error accordingly
            }
        },

        async updateAnnotation(annotation) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;

            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/spans/${annotation.id}`,
                    {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },

                        body: JSON.stringify(annotation)
                    }
                );
                if (!response.ok) {
                    throw new Error("Failed to update Annotation");
                }

            }
            catch (error) {
                console.error("Error updating annotation", error);
            }
        },

        removeAnnotation(index) {
            const word = this.words[index];
            if (word.annotated) {
                this.deleteAnnotation(word.annotation_id);
                word.annotated = false;
                word.label = null;
                word.annotation_id = null; // Clear annotation ID
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



    },
    mounted() {
        this.fetchDataThatMightBeAnnotated();
        this.fetchLabels();
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
    cursor: pointer;
    padding: 3px;
    line-height: 35px;
    transition: background-color 0.3s, box-shadow 0.3s;
    border-radius: 8px;
}

.word:hover {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

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
