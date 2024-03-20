<template>
    <div>
        <editor-content :editor="editor" />
    </div>
</template>

<script>
import { EditorContent, Editor } from '@tiptap/vue-3';
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import Collaboration from '@tiptap/extension-collaboration'
import * as Y from 'yjs';

//import { TiptapCollabProvider } from '@hocuspocus/provider';

export default {
    components: {
        EditorContent,
    },
    data() {
        return {
            editor: null, // Initialize editor as null
            ydoc: new Y.Doc(), // Y.Doc instance
            provider: null, // TiptapCollabProvider instance
        };
    },
    mounted() {
        //console.log(this.ydoc)

        //  this.provider = new TiptapCollabProvider({
        //     name: "document.name", // Unique document identifier for syncing. This is your document name.
        //     appId: 'j9ynyzk1', // Your Cloud Dashboard AppID or `baseURL` for on-premises
        //     token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTA5NDkwODQsIm5iZiI6MTcxMDk0OTA4NCwiZXhwIjoxNzExMDM1NDg0LCJpc3MiOiJodHRwczovL2Nsb3VkLnRpcHRhcC5kZXYiLCJhdWQiOiJqOXlueXprMSJ9.rsL5iEukcd0JRcZHwOtmAV7Dv87H7UmIEabY6xfoUPg', // Your JWT token
        //     document: this.ydoc,
        // })
        this.editor = new Editor({
            extensions: [
                Document,
                Paragraph,
                Text,
                Collaboration.configure({
                    document: this.ydoc // Configure Y.Doc for collaboration
                })
            ],
            content: '<p>I’m running Tiptap with Vue.js. 🎉</p>',
        });

        console.log(this.editor);
    },


    beforeUnmount() {
        this.editor.destroy()
    },
}
</script>
