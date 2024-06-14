<template>
  <div class="text-container" @mouseup="checkSelection" ref="textContainer">
    <span v-html="renderedText" class="text-lg"></span>
  </div>
  <DropdownMenu v-if="showDropdown" :labels="labels" :position="dropdownPosition" @label-selected="applyLabel" />
</template>

<script>
import DropdownMenu from '@/components/DropdownMenu.vue';

export default {
  components: {
    DropdownMenu,
  },
  data() {
    return {
      showDropdown: false,
      dropdownPosition: { x: 0, y: 0 },
      labels: [
        { id: 1, text: 'Label 1', color: '#33FFF9' },
        { id: 2, text: 'Label 2', color: '#336EFF' },
      ],
      annotations: [],
      fullText: "The Diploma thesis proposal is the basis for the Assignment of the diploma thesis and at the same time, it is used for the progress supervision of the diploma thesis elaboration. The Diploma thesis proposal is drawn up by a student when the diploma thesis topic choice is made. The student presents it to the potential thesis supervisor. During the subsequent consultations with the potential thesis supervisor, the diploma thesis proposal is further specified.",
      tokens: [],
      selectedRange: null,
    };
  },
  computed: {
    renderedText() {
      this.tokenizeText();
      const textParts = [];
      let lastIndex = 0;

      this.annotations
        .sort((a, b) => a.start - b.start) // Ensure annotations are processed in order
        .forEach((anno) => {
          const { start, end, label } = anno;
          const backgroundColor = `${label.color}44`;
          const textColor = this.getContrastYIQ(label.color);
          const annotatedText = `<span class="annotated-word" style="background-color: ${backgroundColor}; color: ${textColor};">${this.escapeHtml(this.fullText.slice(start, end))}<span class="annotation-label" style="color: ${textColor}; background-color: ${backgroundColor}; margin-left: 4px;">${label.text}</span></span>`;

          // Push the text before the annotation
          textParts.push(this.escapeHtml(this.fullText.slice(lastIndex, start)));
          // Push the annotated text
          textParts.push(annotatedText);
          // Update the last index
          lastIndex = end;
        });

      // Push any remaining text after the last annotation
      textParts.push(this.escapeHtml(this.fullText.slice(lastIndex)));

      return textParts.join('');
    },
  },
  methods: {
    tokenizeText() {
      this.tokens = [];
      let start = 0;
      const regex = /(\s+|[.,!?;:\(\)\[\]{}"'])/; // Split on whitespace or punctuation
      this.fullText.split(regex).forEach((segment) => {
        if (segment.length > 0) {
          this.tokens.push({ word: segment, start, end: start + segment.length });
        }
        start += segment.length;
      });
    },
    checkSelection() {
      const selection = window.getSelection();
      if (selection.rangeCount > 0 && !selection.isCollapsed) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        const startOffset = this.getOffsetInText(range.startContainer, range.startOffset);
        const endOffset = this.getOffsetInText(range.endContainer, range.endOffset);

        this.dropdownPosition.x = rect.left + window.scrollX;
        this.dropdownPosition.y = rect.bottom + window.scrollY;
        this.selectedRange = { start: this.findTokenStart(startOffset), end: this.findTokenEnd(endOffset) };
        this.showDropdown = true;
      } else {
        this.showDropdown = false;
      }
    },
    findTokenStart(offset) {
      for (const token of this.tokens) {
        if (token.start <= offset && token.end >= offset) {
          return token.start;
        }
      }
      return offset;
    },
    findTokenEnd(offset) {
      for (const token of this.tokens) {
        if (token.start <= offset && token.end >= offset) {
          return token.end;
        }
      }
      return offset;
    },
    getOffsetInText(node, offset) {
      let totalOffset = 0;
      const walker = document.createTreeWalker(this.$refs.textContainer, NodeFilter.SHOW_TEXT, null, false);
      let currentNode;

      while ((currentNode = walker.nextNode())) {
        if (currentNode === node) {
          totalOffset += offset;
          break;
        }
        totalOffset += currentNode.nodeValue.length;
      }

      return totalOffset;
    },
    getContrastYIQ(hexcolor) {
      hexcolor = hexcolor.replace("#", "");
      const r = parseInt(hexcolor.substr(0, 2), 16);
      const g = parseInt(hexcolor.substr(2, 2), 16);
      const b = parseInt(hexcolor.substr(4, 2), 16);
      const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
      return (yiq >= 128) ? 'black' : 'white';
    },
    applyLabel(label) {
      if (this.selectedRange && this.selectedRange.start !== this.selectedRange.end) {
        const { start, end } = this.selectedRange;

        // Remove any existing annotations that overlap with the new range
        this.annotations = this.annotations.filter(anno => !(start < anno.end && end > anno.start));

        // Add the new annotation
        const text = this.fullText.slice(start, end);
        this.annotations.push({ text, label, start, end });

        // Reset selection and hide dropdown
        this.showDropdown = false;
        this.selectedRange = null;
      }
    },
    escapeHtml(unsafe) {
      return unsafe.replace(/[&<"']/g, (m) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      }[m]));
    }
  },
};
</script>

<style>
.text-container {
  position: relative;
}

.annotated-word {
  padding: 0 4px;
  border-radius: 4px;
  margin: 0 2px;
  position: relative;
  display: inline-block;
}

.annotation-label {
  font-size: 10px;
  text-align: center;
  margin-left: 4px;
  border-radius: 4px;
  padding: 0 2px;
  display: inline-block;
}
</style>
