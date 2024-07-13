import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

const niceColors = [
  "red-11",
  "blue-11",
  "light-green-11",
  "deep-orange-11",
  "pink-11",
  "light-blue-11",
  "lime-11",
  "brown-11",
  "purple-11",
  "cyan-11",
  "yellow-11",
  "grey-11",
  "deep-purple-11",
  "teal-11",
  "amber-11",
  "blue-grey-11",
  "indigo-11",
  "green-11",
  "orange-11",
];

export const useClassesStore = defineStore('classes', {
  state: () => ({
    annotations: [],
    classes: useStorage('tags', []),
    inputSentences: [],
    originalText: "",
    separator: "\n",
    enableKeyboardShortcuts: false,
    annotationPrecision: "word",
    currentAnnotation: {},
    currentClass: null,
    currentIndex: 0,
    currentSentence: "",
  }),
  getters: {},
  actions: {
    setInputSentences(payload) {
      if (!Array.isArray(payload)) {
        this.originalText = payload;
        payload = payload.split(this.separator);
      }
      this.inputSentences = payload.map((s, i) => ({ id: i, text: s }));
    },
    addClass(payload) {
      let existing = this.classes.find((c) => c.name == payload);
      if (existing) {
        return;
      }
      let lastIndex = this.classes.reduce((p, c) => {
        return c.id > p ? c.id : p;
      }, 0);
      let newClass = {
        id: lastIndex + 1,
        name: payload,
        color: niceColors[lastIndex % niceColors.length],
      }
      this.classes.push(newClass);
      if (this.classes.length === 1) {
        this.currentClass = this.classes[0];
      }
    },
    removeClass(payload) {
      this.classes = this.classes.filter((c) => c.id != payload);
      if (this.currentClass.id === payload) {
        this.currentClass = this.classes[0];
      }
    },
    setCurrentClass(payload) {
      this.currentClass = this.classes[payload];
    },
    addAnnotation(payload) {
      this.annotations[this.currentIndex] = payload;
      this.currentAnnotation = payload;
    },
    clearAllAnnotations() {
      this.annotations = [];
      this.currentAnnotation = {};
    },
    setSeparator(payload) {
      this.separator = payload;
      const sentences = this.originalText.split(this.separator);
      this.inputSentences = sentences.map((s, i) => ({ id: i, text: s }));
    },
    setAnnotationPrecision(payload) {
      this.annotationPrecision = payload;
    },
    setKeyboardShortcuts(payload) {
      this.enableKeyboardShortcuts = payload;
    },
    nextSentence() {
      if (this.currentIndex < this.inputSentences.length - 1) {
        this.currentIndex += 1;
        this.currentAnnotation = this.annotations[this.currentIndex] || {};
      } else {
        alert("You have completed all the sentences");
      }
    },
    previousSentence() {
      if (this.currentIndex > 0) {
        this.currentIndex -= 1;
        this.currentAnnotation = this.annotations[this.currentIndex];
      } else {
        alert("You are at the beginning of all sentences");
      }
    },
    resetIndex() {
      this.currentIndex = 0;
    },
    loadClasses(payload) {
      if (!Array.isArray(payload)) {
        throw new Error("loadClasses: payload must be an array");
      }
      let isValid = payload.reduce(
        (acc, curr) =>
          acc &&
          typeof curr === "object" &&
          "id" in curr &&
          "name" in curr &&
          "color" in curr,
        true
      );
      if (!isValid) {
        throw new Error("loadClasses: payload has invalid schema");
      }
      this.classes = payload;
      this.currentClass = this.classes[0];
    },
    loadAnnotations(payload) {
      let isValid = typeof payload === "object" &&
        "annotations" in payload &&
        "classes" in payload;

      if (!isValid) {
        throw new Error("loadAnnotations: payload has invalid schema");
      }

      let annotations = payload.annotations;
      if (!Array.isArray(annotations)) {
        throw new Error("loadAnnotations: payload must be an array");
      }

      let newAnnotations = [];

      for (let i = 0; i < annotations.length; i++) {
        if (annotations[i] == null) continue;
        let annotation = {
          'text': annotations[i][0],
          'entities': annotations[i][1].entities,
        }
        newAnnotations[i] = annotation;
      }
      this.annotations = newAnnotations;
      this.currentAnnotation = this.annotations[this.currentIndex];
    },
    createNewClass(className) {
      return new Promise((resolve, reject) => {
        this.addClass(className);
        try {
          this.classes = useStorage('tags', this.classes);
        } catch (e) {
          reject(e);
        }
        resolve();
      });
    },
    deleteClass(classId) {
      this.removeClass(classId);
      this.classes = useStorage('tags', this.classes);
    },
  }
});

