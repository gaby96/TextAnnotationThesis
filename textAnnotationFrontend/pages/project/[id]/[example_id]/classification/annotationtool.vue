<template>
    <div class="annotation-container">
      <div class="classes-block">
        <ClassesBlock />
      </div>
      <div class="tokens-container p-4 h-60 overflow-y-scroll">
        <component
          :is="t.type === 'token' ? 'Token' : 'TokenBlock'"
          v-for="t in tokens"
          :key="t.start"
          :token="t"
          :background-color="t.backgroundColor"
          @remove-block="removeBlock"
        />
      </div>
      <div class="actions-container p-4 border-t border-gray-300">
        <button
          class="btn btn-outline-red mx-2"
          @click="resetBlocks"
        >
          Reset
        </button>
        <button
          class="btn btn-outline-gray mx-2"
          :class="{'text-gray-300': isDarkMode, 'text-gray-900': !isDarkMode}"
          :disabled="currentIndex === 0"
          @click="backOneSentence"
        >
          Back
        </button>
        <button
          class="btn btn-outline-gray mx-2"
          :class="{'text-gray-300': isDarkMode, 'text-gray-900': !isDarkMode}"
          @click="skipCurrentSentence"
        >
          Skip
        </button>
        <button
          class="btn btn-outline-green mx-2"
          @click="saveTags"
        >
          Save
        </button>
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
  import { useClassesStore } from '~/stores/classes'
  import Token from '@/components/Token.vue'
  import TokenBlock from '@/components/TokenBlock.vue'
  import ClassesBlock from '@/components/ClassesBlock.vue'
  import TokenManager from '@/components/token-manager'
  import TreebankTokenizer from 'treebank-tokenizer'
  
  const store = useClassesStore()
  const tokenizer = new TreebankTokenizer()
  
  const currentSentence = ref({})
  const tokens = ref([])
  const isDarkMode = computed(() => useColorMode().value === 'dark')
  
  const tokenizeCurrentSentence = () => {
    currentSentence.value = store.inputSentences[store.currentIndex]
  
    let tokenized, spans
    if (store.annotationPrecision === 'char') {
      tokenized = currentSentence.value.text.split('')
      spans = tokenized.map((_, i) => [i, i + 1])
    } else {
      tokenized = tokenizer.tokenize(currentSentence.value.text)
      spans = tokenizer.span_tokenize(currentSentence.value.text)
    }
  
    const combined = tokenized.map((t, i) => ({
      start: spans[i][0],
      end: spans[i][1],
      text: t,
      type: 'token',
      backgroundColor: 'transparent',
    }))
  
    tokens.value = combined
  }
  
  const selectTokens = () => {
    const selection = window.getSelection()
    if (selection.rangeCount > 0 && !selection.isCollapsed) {
      const range = selection.getRangeAt(0)
      const start = range.startOffset
      const end = range.endOffset
  
      // Add new block logic here
    }
  }
  
  onMounted(() => {
    if (store.inputSentences.length) {
      tokenizeCurrentSentence()
    }
    document.addEventListener('mouseup', selectTokens)
  })
  
  onBeforeUnmount(() => {
    document.removeEventListener('mouseup', selectTokens)
  })
  
  const resetBlocks = () => {
    tokens.value.forEach((token) => {
      token.backgroundColor = 'transparent'
    })
  }
  
  const skipCurrentSentence = () => {
    store.nextSentence()
    tokenizeCurrentSentence()
  }
  
  const backOneSentence = () => {
    store.previousSentence()
    tokenizeCurrentSentence()
  }
  
  const saveTags = () => {
    store.addAnnotation({
      text: currentSentence.value.text,
      entities: tokens.value,
    })
    store.nextSentence()
    tokenizeCurrentSentence()
  }
  </script>
  
  
  <style scoped>
.annotation-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tokens-container {
  height: 60vh;
  overflow-y: scroll;
}

.actions-container {
  display: flex;
  justify-content: flex-start;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline-red {
  border-color: red;
  color: red;
}

.btn-outline-red:hover {
  background-color: red;
  color: white;
}

.btn-outline-gray {
  border-color: gray;
  color: gray;
}

.btn-outline-gray:hover {
  background-color: gray;
  color: white;
}

.btn-outline-green {
  border-color: green;
  color: green;
}

.btn-outline-green:hover {
  background-color: green;
  color: white;
}

.mx-2 {
  margin-left: 0.5rem;
  margin-right: 0.5rem;
}

.text-gray-300 {
  color: #d1d5db;
}

.text-gray-900 {
  color: #111827;
}

.p-4 {
  padding: 1rem;
}

.h-60 {
  height: 15rem;
}

.overflow-y-scroll {
  overflow-y: scroll;
}

.border-t {
  border-top: 1px solid;
}

.border-gray-300 {
  border-color: #d1d5db;
}
</style>

  