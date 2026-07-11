<template>
    <div class="container">
        <div class="text-container shadow-lg shadow-md p-4" ref="textContainer">
            <div class="pagination-controls mb-4">
                <button class="page-button" :disabled="pageOffset === 0" @click="goToPreviousPage">Previous</button>
                <span class="page-status">{{ pageStatus }}</span>
                <button class="page-button" :disabled="nextOffset === null" @click="goToNextPage">Next</button>
            </div>
            <div class="words-content">
                <template v-for="(word, index) in words" :key="index">
                    <span class="word text-lg" :class="getWordClasses(word, index)" :data-word-index="index"
                        @mousedown.prevent="handleWordMouseDown(index, $event)" @mouseenter="handleWordMouseEnter(index)"
                        @mouseup.stop="handleWordMouseUp(index)" @dblclick="handleDoubleClick(index)"
                        :style="{
                            backgroundColor: getWordBackgroundColor(word, index),
                            borderRadius: getWordBorderRadius(word, index)
                        }">
                        {{ word.text }}<span v-if="word.annotated && !isAnnotationEnd(index)"
                            class="word-space">&nbsp;</span>
                        <span v-if="word.annotated && word.showAnnotationLabel" class="annotation-label text-xs"
                            :style="{ backgroundColor: word.label.background_color }">
                            {{ word.label.text }}
                            <button class="remove-btn" @click="removeAnnotation(index)">X</button>
                        </span>
                    </span>
                    <span v-if="shouldShowWordGap(index)" class="word-gap">&nbsp;</span>
                </template>
            </div>
        </div>

        <div>
            <DropdownMenu v-if="showDropdown" :labels="labels" ref="dropdownMenu" :position="dropdownPosition"
                @label-selected="applyLabel" />
        </div>


        <div class="labels-container ml-6">
            <div class="grid grid-cols-3 gap-y-4 gap-x-0.5">
                <div v-for="label in labels" :key="label.id">
                    <div class="preview-chip"
                        :style="{ backgroundColor: label.background_color, color: label.text_color }">
                        {{ label.text }}
                        <span v-if="label.suffix_key" class="preview-avatar">{{ label.suffix_key }}</span>
                    </div>
                </div>
            </div>

            <!-- component -->
            <div class="min-h-screen py-6 flex flex-col justify-center relative overflow-hidden sm:py-12">
                <div
                    class="border relative px-4 pt-7 pb-8 bg-white shadow-xl w-full max-w-md mx-auto sm:px-10 rounded-b-md">

                    <label for="dropdown" class="block">Model</label>
                    <select id="dropdown" class="border w-full h-10 px-3 mb-5 rounded-md" v-model="selectedModel">
                        <option value="">Select an option</option>
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
                    </select> -->

                    <!-- <label for="slider1" class="block">Temperature: <span id="slider1Value"
                            class="text-red-500">0.00</span></label>
                    <input type="range" id="slider1"
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer mb-5" min="0" max="1"
                        step="0.01" value="0"
                        oninput="document.getElementById('slider1Value').innerText = parseFloat(this.value).toFixed(2);">
                    <div class="flex justify-between text-xs text-gray-600">
                        <span>0.00</span>
                        <span>1.00</span>
                    </div> -->

                    <!-- <label for="slider2" class="block">Epochs: <span id="slider2Value"
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
                        class="mt-5 bg-green-500 hover:bg-blue-700 shadow-xl text-white uppercase text-sm font-semibold px-14 py-3 rounded">Predict</button>

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
import { selectedRect } from "@tiptap/pm/tables";

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
            pageOffset: 0,
            pageLimit: 8000,
            totalTextLength: 0,
            nextOffset: null,
            previousOffset: null,
            words: [],
            selectedModel: null,
            startWordIndex: -1,
            endWordIndex: -1,
            isSelecting: false,
            dragStartWordIndex: -1,
            dragEndWordIndex: -1,
        };
    },
    computed: {

        annotateId() {
            return this.$route.params.annotate_id;
        },

        projectId() {
            return this.$route.params.id;
        },

        exampleId() {
            return this.$route.params.example_id;
        },

        pageStatus() {
            if (!this.totalTextLength) {
                return 'Page 0 of 0';
            }
            const start = this.pageOffset + 1;
            const end = Math.min(this.pageOffset + (this.fullText || '').length, this.totalTextLength);
            return `${start}-${end} of ${this.totalTextLength}`;
        },
    },
    methods: {
        // This method fetches the labels that are going to be used to annotate the data (PER, ORG, etc)
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
                // console.log(data)
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
                    `${config.public.baseURL}/project/dataset/${this.projectId}/examples/${this.exampleId}/page?offset=${this.pageOffset}&limit=${this.pageLimit}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const data = await response.json();
                this.fullText = data.text;
                this.pageOffset = data.offset;
                this.totalTextLength = data.total;
                this.nextOffset = data.next_offset;
                this.previousOffset = data.previous_offset;
                this.processText(this.fullText);
                this.fetchAnnotations();
            } catch (error) {
                console.error("Error fetching example data:", error);
                // Handle error accordingly
            }
        },

        // Fetch data about annotations made ({start_offset, label, end_offset, example_id or the full text})
        async fetchAnnotations() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const start = this.pageOffset;
                const end = this.pageOffset + (this.fullText || '').length;
                const response = await fetch(
                    `${config.public.baseURL}/project/annotation/${this.projectId}/examples/${this.exampleId}/spans?start=${start}&end=${end}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const annotations = await response.json();
                console.log(annotations)
                this.applyAnnotations(annotations);
            } catch (error) {
                console.error("Error fetching annotations:", error);
            }
        },


        applyAnnotations(annotations) {
            //fetches annotations from API
            this.annotations = annotations;

            // Loop through annotations
            annotations.forEach(annotation => {
                const label = this.labels.find(l => l.id === annotation.label);  // Get the label for the annotation
                if (!label) return;  // Skip if the label is not found

                // Loop through words and apply annotations
                this.words.forEach(word => {
                    // Check if the word's start and end offsets overlap with the annotation's offsets
                    if (
                        (word.startOffset < annotation.end_offset && word.endOffset > annotation.start_offset)  // Word overlaps annotation
                    ) {
                        word.annotated = true;  // Mark the word as annotated
                        word.label = label;     // Assign the label to the word
                        word.annotation_id = annotation.id;  // Set the annotation ID
                        word.showAnnotationLabel = false;
                    }
                });
                const coveredWords = this.words.filter(word => word.annotation_id === annotation.id);
                if (coveredWords.length) {
                    coveredWords[coveredWords.length - 1].showAnnotationLabel = true;
                }
            });
        },
        processText(text) {
            let offset = 0;
            this.words = [];

            const wordRegex = /\S+/g;  // Matches any sequence of non-whitespace characters (a word)

            let match;
            while ((match = wordRegex.exec(text)) !== null) {
                const word = match[0];  // Captures the word
                const startOffset = this.pageOffset + match.index;  // Absolute start offset
                const endOffset = startOffset + word.length;  // Exclusive absolute end offset

                const wordObj = {
                    text: word,
                    annotated: false,
                    label: null,
                    startOffset: startOffset,
                    endOffset: endOffset,
                    annotation_id: null,
                    showAnnotationLabel: false
                };

                this.words.push(wordObj);
            }
        },

        handleDoubleClick(index) {
            // Handle double click event on a specific word (index)
            this.startWordIndex = index;
            this.endWordIndex = index;
            this.calculateDropdownPosition(index);
            this.showDropdown = true; // Show dropdown menu
        },

        handleWordMouseDown(index, event) {
            if (event.button !== 0) {
                return;
            }

            this.showDropdown = false;
            this.isSelecting = true;
            this.dragStartWordIndex = index;
            this.dragEndWordIndex = index;
            this.startWordIndex = index;
            this.endWordIndex = index;
        },

        handleWordMouseEnter(index) {
            if (!this.isSelecting) {
                return;
            }

            this.dragEndWordIndex = index;
            this.startWordIndex = Math.min(this.dragStartWordIndex, this.dragEndWordIndex);
            this.endWordIndex = Math.max(this.dragStartWordIndex, this.dragEndWordIndex);
        },

        handleWordMouseUp(index) {
            if (!this.isSelecting) {
                return;
            }

            this.dragEndWordIndex = index;
            this.startWordIndex = Math.min(this.dragStartWordIndex, this.dragEndWordIndex);
            this.endWordIndex = Math.max(this.dragStartWordIndex, this.dragEndWordIndex);
            this.isSelecting = false;
            this.calculateDropdownPosition(this.endWordIndex);
            this.showDropdown = true;
        },

        finishWordSelection() {
            this.isSelecting = false;
        },

        getWordBackgroundColor(word, index) {
            if (this.isWordSelected(index)) {
                return '#bfdbfe';
            }
            return word.annotated ? word.label.background_color : '';
        },

        getWordClasses(word, index) {
            return {
                'annotation-start': word.annotated && this.isAnnotationStart(index),
                'annotation-middle': word.annotated && !this.isAnnotationStart(index) && !this.isAnnotationEnd(index),
                'annotation-end': word.annotated && this.isAnnotationEnd(index),
            };
        },

        getWordBorderRadius(word, index) {
            if (!word.annotated && !this.isWordSelected(index)) {
                return '';
            }

            if (this.isWordSelected(index)) {
                return '8px';
            }

            const isStart = this.isAnnotationStart(index);
            const isEnd = this.isAnnotationEnd(index);

            if (isStart && isEnd) {
                return '8px';
            }
            if (isStart) {
                return '8px 0 0 8px';
            }
            if (isEnd) {
                return '0 8px 8px 0';
            }
            return '0';
        },

        isSameAnnotation(index, comparisonIndex) {
            const word = this.words[index];
            const comparisonWord = this.words[comparisonIndex];
            return Boolean(
                word &&
                comparisonWord &&
                word.annotation_id &&
                word.annotation_id === comparisonWord.annotation_id
            );
        },

        isAnnotationStart(index) {
            return !this.isSameAnnotation(index, index - 1);
        },

        isAnnotationEnd(index) {
            return !this.isSameAnnotation(index, index + 1);
        },

        shouldShowWordGap(index) {
            const word = this.words[index];
            return !word?.annotated || this.isAnnotationEnd(index);
        },

        isWordSelected(index) {
            return this.startWordIndex !== -1 && this.endWordIndex !== -1 && index >= this.startWordIndex && index <= this.endWordIndex;
        },

        calculateDropdownPosition(index) {
            // Calculate position based on the index of the word
            const spanElement = this.$refs.textContainer.querySelector(`[data-word-index="${index}"]`);
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
                const selectedWords = this.words.slice(this.startWordIndex, this.endWordIndex + 1);
                if (!selectedWords.length) {
                    return;
                }

                const annotation = {
                    label: label.id,
                    start_offset: selectedWords[0].startOffset,
                    end_offset: selectedWords[selectedWords.length - 1].endOffset,
                    example: parseInt(this.exampleId),
                    word: selectedWords.map(word => word.text).join(' ')
                };
                await this.saveAnnotation(annotation);
                this.markWordsAnnotated(this.startWordIndex, this.endWordIndex, label, annotation.id);

                // Reset selection and hide dropdown
                this.startWordIndex = -1;
                this.endWordIndex = -1;
                this.dragStartWordIndex = -1;
                this.dragEndWordIndex = -1;
                this.showDropdown = false;
                window.getSelection()?.removeAllRanges();

                // Log the updated array of labeled words
                //console.log(this.labeledWordsArray);
            }
        },

        markWordsAnnotated(startIndex, endIndex, label, annotationId) {
            for (let i = startIndex; i <= endIndex; i++) {
                this.words[i].annotated = true;
                this.words[i].label = label;
                this.words[i].annotation_id = annotationId;
                this.words[i].showAnnotationLabel = i === endIndex;
            }
        },

        // Save annotation object which contains the start_offset, end_offset, label, data
        async saveAnnotation(annotation) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            console.log(annotation)
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
                    throw new Error("Failed to save annotation");
                }
                const data = await response.json();
                annotation.id = data.id;
                this.labeledWordsArray.push(annotation);
            } catch (error) {
                console.error("Error saving annotation:", error);
                // Handle error accordingly
            }
        },

        removeAnnotation(index) {
            const word = this.words[index];
            if (word.annotated) {
                const annotationId = word.annotation_id;
                this.deleteAnnotation(annotationId);
                this.words.forEach(currentWord => {
                    if (currentWord.annotation_id === annotationId) {
                        currentWord.annotated = false;
                        currentWord.label = null;
                        currentWord.annotation_id = null;
                        currentWord.showAnnotationLabel = false;
                    }
                });
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
            if (dropdownMenu && !dropdownMenu.$el.contains(event.target) && !this.$refs.textContainer.contains(event.target)) {
                this.showDropdown = false;
                this.startWordIndex = -1;
                this.endWordIndex = -1;
                this.dragStartWordIndex = -1;
                this.dragEndWordIndex = -1;
            }
        },

        async handlePredict() {
            await this.fetchLabels();
            const authStore = useAuthStore();
            let userObject = authStore.user;
            const fullExampleText = await this.fetchFullExampleText();
            if (this.labels.length > 0 && fullExampleText) {
                const combinedData = {
                    data1: this.labels,
                    data2: fullExampleText,
                    exampleId: parseInt(this.exampleId),
                    selectedModel: this.selectedModel,
                    userId: userObject.id
                };
                await this.handleLLMAnnotate(combinedData);
            } else {
                console.log('One or both data sets are not available for processing');
            }
        },

        async fetchFullExampleText() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
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
            return data.text;
        },

        async handleLLMAnnotate(combinedData) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;

            try {
                const config = useRuntimeConfig();
                const response = await fetch(
                    `${config.public.baseURL}/project/dataset/examples/llmannotate`,
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
                this.fetchDataThatMightBeAnnotated();
                console.log("LLM Annotation Response:", newAnnotations);
            } catch (error) {
                console.error("Error during LLM annotation:", error);
            }
        },

        userId() {
            const userStoreInstance = userStore();
            console.log(userStoreInstance.userObject);
            return userStoreInstance.userObject;
        },

        async goToPreviousPage() {
            if (this.previousOffset === null) return;
            this.pageOffset = this.previousOffset;
            await this.fetchDataThatMightBeAnnotated();
        },

        async goToNextPage() {
            if (this.nextOffset === null) return;
            this.pageOffset = this.nextOffset;
            await this.fetchDataThatMightBeAnnotated();
        },
    },
    async mounted() {
        await this.fetchLabels();
        await this.fetchDataThatMightBeAnnotated();
        document.addEventListener('click', this.handleClickOutside);
        document.addEventListener('mouseup', this.finishWordSelection);
    },

    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
        document.removeEventListener('mouseup', this.finishWordSelection);
    },
};
</script>



<style scoped>
.container {
    display: flex;
    width: 100%;
    min-width: 0;
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
    user-select: text;
    box-sizing: border-box;
    min-width: 0;
    overflow-wrap: anywhere;
    word-break: break-word;
}

.pagination-controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.page-button {
    background-color: #16a34a;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 14px;
    cursor: pointer;
}

.page-button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
}

.page-status {
    color: #374151;
    font-size: 14px;
}

.labels-container {
    width: 40%;
    box-sizing: border-box;
    min-width: 0;
    flex-shrink: 0;
}

.words-content {
    font-size: 0;
    max-width: 100%;
    white-space: normal;
    overflow-wrap: anywhere;
    word-break: break-word;
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
    cursor: text;
    display: inline;
    font-size: 1.125rem;
    padding: 0 1px;
    overflow-wrap: anywhere;
    word-break: break-word;
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
    border-radius: 0 8px 8px 0;
    font-size: 10px;
    color: #fff;
}

.word-gap {
    font-size: 1.125rem;
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
