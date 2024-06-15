<template>
  <div>
    <div class="text-container" ref="textContainer">
      <span
        v-for="(word, index) in words"
        :key="index"
        class="word text-lg space-x-10"
        style="padding: 3px; line-height: 35px"
        @dblclick="handleDoubleClick(index)"
        :class="[
          'word',
          { highlighted: index >= startWordIndex && index <= endWordIndex },
          word.annotated ? word.label.colorClass : '',
        ]"
      >
        {{ word.text }}
        <span
          v-if="word.annotated"
          class="annotation-label text-xs rounded-lg"
          :style="{ backgroundColor: word.label.color }"
        >
          {{ word.label.text }}
          <button class="remove-btn" @click="removeAnnotation(index)">X</button>
        </span>
      </span>
    </div>

    <DropdownMenu
      v-if="showDropdown"
      :labels="labels"
      :position="dropdownPosition"
      @label-selected="applyLabel"
    />
  </div>
</template>

<script>
import DropdownMenu from "@/components/DropdownMenu.vue";

export default {
  components: {
    DropdownMenu,
  },
  data() {
    return {
      labeledWordsArray: [],
      showDropdown: false,
      dropdownPosition: { x: 0, y: 0 },
      labels: [
        { id: 1, text: "Label 1", color: "#33FFF9", colorClass: "bg-cyan-100" },
        {
          id: 2,
          text: "Label 2",
          color: "rgb(173, 186, 255)",
          colorClass: "bg-indigo-100",
        },
      ],
      annotations: [],
      fullText:
        "The Diploma thesis proposal is the basis for the Assignment of the diploma thesis and at the same time, it is used for the progress supervision of the diploma thesis elaboration. The Diploma thesis proposal is drawn up by a student when the diploma thesis topic choice is made. The student presents it to the potential thesis supervisor. During the subsequent consultations with the potential thesis supervisor, the diploma thesis proposal is further specified.",
      words: [],
      startWordIndex: -1,
      endWordIndex: -1,
    };
  },
  computed: {
    renderedText() {
      return this.words.map((word) => word.text).join(" ");
    },
  },
  methods: {
    tokenizeText() {
      const regex = /(\s+|[.,!?;:\(\)\[\]{}"'])/;
      let start = 0;
      this.fullText.split(regex).forEach((segment) => {
        if (segment.length > 0) {
          const end = start + segment.length;
          this.words.push({ text: segment, start, end, annotated: false });
        }
        start += segment.length;
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
    applyLabel(label) {
      if (this.startWordIndex !== -1 && this.endWordIndex !== -1) {
        // Apply label to the words from startWordIndex to endWordIndex
        for (let i = this.startWordIndex; i <= this.endWordIndex; i++) {
          if (!this.words[i].annotated) {
            this.words[i].annotated = true;
            this.words[i].label = label;

            // Check if the word is already in labeledWordsArray
            const existingIndex = this.labeledWordsArray.findIndex(
              (item) => item.value === this.words[i].text
            );

            if (existingIndex !== -1) {
              // Update existing entry with the new label
              this.labeledWordsArray[existingIndex].key = label.text;
            } else {
              // Add new entry to labeledWordsArray
              this.labeledWordsArray.push({
                key: label.text,
                value: this.words[i].text,
              });
            }
          }
        }

        // Reset selection and hide dropdown
        this.startWordIndex = -1;
        this.endWordIndex = -1;
        this.showDropdown = false;

        // Log the updated array of labeled words
        console.log(
          this.labeledWordsArray.map((item) => ({
            key: item.key,
            value: item.value,
          }))
        );
      }
    },
    removeAnnotation(index) {
      // Remove annotation from the word at index
      this.words[index].annotated = false;
      this.words[index].label = null;
    },
  },
  mounted() {
    this.tokenizeText();
  },
};
</script>

<style scoped>
.word {
  margin-right: 0px;
  cursor: pointer;
}

.word.highlighted {
}

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
