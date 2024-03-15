<template>
  <div class="flex justify-center"> <!-- Center the textarea horizontally -->
    <div class="collaborative-textbox w-full md:w-2/3 lg:w-1/2"> <!-- Adjust width responsively -->
      <textarea 
        ref="textarea" 
        v-model="text"
        @focus="onFocus"  
        @input="handleInput" 
        @select="handleCursorMove"
        @keyup="handleCursorMove"
        @click="handleCursorMove"
        class="w-full h-64 p-4 text-base text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
      </textarea>
      <div v-for="(cursor, id) in cursors" :key="id" :style="cursorStyle(cursor)">
        <div class="cursor" :style="{ backgroundColor: cursor.color }"></div>
      </div>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      socket: null,
      text: '',
      cursors: {}, // Object to track multiple cursors with color
      localCursorColor: this.getRandomColor(), // Assign a random color for the local cursor
    };
  },
  mounted() {
//     this.socket = io('http://localhost:3001');

//     this.socket.on('text-change', ({ text, senderId }) => {
//       if (senderId !== this.socket.id) {
//         const currentPos = this.getCurrentCursorPosition();
//         this.text = text;
//         this.setCaretPosition(currentPos);
//       }
//     });

//  this.socket.on('cursor-move', (data) => {
//       if (data.id !== this.socket.id) {
//         // Directly assign new properties to the cursors object
//         this.cursors[data.id] = { position: data.position, color: data.color };
//       }
//     });
  },
  methods: {
    // onFocus(event) {
    //   event.target.style.caretColor = this.getRandomColor();
    // },
    // handleInput(event) {
    //   this.socket.emit('text-change', { text: this.text, senderId: this.socket.id });
    //   this.handleCursorMove();
    // },
    // handleCursorMove() {
    //   this.localCursorColor = this.getRandomColor();
    //   const position = this.getCurrentCursorPosition();
    //   this.socket.emit('cursor-move', { id: this.socket.id, position, color: this.localCursorColor });
    // },
    // cursorStyle(cursor) {
    //   return {
    //     position: 'absolute',
    //     left: `${cursor.position}px`,
    //     color: cursor.color,
    //     userSelect: 'none',
    //     pointerEvents: 'none',
    //   };
    // },
    // getCurrentCursorPosition() {
    //   return this.$refs.textarea.selectionStart;
    // },
    // setCaretPosition(pos) {
    //   this.$refs.textarea.setSelectionRange(pos, pos);
    // },
    // getRandomColor() {
    //   const letters = '0123456789ABCDEF';
    //   let color = '#';
    //   for (let i = 0; i < 6; i++) {
    //     color += letters[Math.floor(Math.random() * 16)];
    //   }
    //   console.log(color)
    //   return color;
    // }
  },
};
</script>

<style>
.collaborative-textbox {
  position: relative;
}
textarea {
  width: 100%;
  height: 200px;
}
.cursor {
  width: 2px;
  height: 1em;
  position: absolute;
  margin-left: -1px;
}
</style>
