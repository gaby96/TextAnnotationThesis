<template>
    <div class="editor" v-if="editor">
        <menu-bar class="editor__header" :editor="editor" />
        <editor-content class="editor__content" :editor="editor" />
        <div class="editor__footer">
            <div :class="`editor__status editor__status--${status}`">
                <template v-if="status === 'connected'">
                    {{ this.getUniqueUsers().length }} user{{
        this.getUniqueUsers().length === 1 ? '' : 's' }} online
                </template>
                <template v-else>
                    offline
                </template>
            </div>
            <!-- <div class="editor__name">
                <button @click="setName">
                    {{ currentUser.name }}
                </button>
            </div> -->
        </div>
        <!-- <pre>{{ editor.storage.collaborationCursor.users }}</pre> -->
    </div>
</template>

<script>
definePageMeta({
    layout: 'portal'
})
import { EditorContent, Editor } from '@tiptap/vue-3';
import CharacterCount from '@tiptap/extension-character-count'
import Collaboration from '@tiptap/extension-collaboration'
import CollaborationCursor from '@tiptap/extension-collaboration-cursor'
import Highlight from '@tiptap/extension-highlight'
import TaskItem from '@tiptap/extension-task-item'
import TaskList from '@tiptap/extension-task-list'
import StarterKit from '@tiptap/starter-kit'

import * as Y from 'yjs';

import { TiptapCollabProvider } from '@hocuspocus/provider';
import MenuBar from '@/components/MenuBar.vue'
import { variables } from '@/pages/project/[id]/[example_id]/classification/variables.js'
import { userStore } from '@/stores/user'



//import { HocuspocusProvider } from '@hocuspocus/provider'
const getRandomElement = list => {
    return list[Math.floor(Math.random() * list.length)]
}


const getRandomRoom = () => {
    const roomNumbers = variables.collabRooms?.trim()?.split(',') ?? [10, 11, 12]

    return getRandomElement(roomNumbers.map(number => `rooms.${number}`))
}
export default {
    components: {
        EditorContent,
    },
    data() {
        return {
            editor: null, // Initialize editor as null
            provider: null, // TiptapCollabProvider instance
            currentUser: null,
            status: 'connecting',
            first_name: null,
            last_name: null,
            text: null,
            color: this.getRandomColor(),
            room: getRandomRoom(),
            yMap: null
        };
    },
    async mounted() {


        // const annotatedData = await this.fetchAnnotatedData();
        // console.log(annotatedData)

        this.getUser()
        this.currentUser = userStore().userObject

        const ydoc = new Y.Doc()
        // this.provider = new HocuspocusProvider({
        //     url: 'ws://127.0.0.1:1234',
        //     name: 'example-document',
        //     document: new Y.Doc(),
        //     color: null,
        //     names: null
        // })


        this.provider = new TiptapCollabProvider({
            name: "athirddocument.name", // Unique document identifier for syncing. This is your document name.
            appId: 'j9ynyzk1', // Your Cloud Dashboard AppID or `baseURL` for on-premises
            token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTIzNTcyNDcsIm5iZiI6MTcxMjM1NzI0NywiZXhwIjoxNzEyNDQzNjQ3LCJpc3MiOiJodHRwczovL2Nsb3VkLnRpcHRhcC5kZXYiLCJhdWQiOiJqOXlueXprMSJ9.5tzfyRSd9CKsZcdVQR47tYoItndKQTUVzIp955ab15I', // Your JWT token
            document: ydoc,
        })

        await this.provider.whenSynced;

        this.editor = new Editor({
            extensions: [
                StarterKit.configure({
                    history: false,
                }),
                Highlight,
                TaskList,
                TaskItem,
                Collaboration.configure({
                    document: ydoc,
                }),
                CollaborationCursor.configure({
                    provider: this.provider,
                    user: {
                        id: this.currentUser.id,
                        name: this.currentUser.first_name + " " + this.currentUser.last_name,
                        color: this.color,
                    },
                }),
                CharacterCount.configure({
                    limit: 10000,
                }),
            ],
        });

        if (!ydoc.getMap('config').get('initialContentLoaded')) {
            const annotatedData = await this.fetchAnnotatedData();
            if (annotatedData && this.editor) {
                ydoc.getMap('config').set('initialContentLoaded', true);
                this.editor.commands.setContent(annotatedData);
               // this.yMap.set('initialContentLoaded', true); // Mark that the content has been set
            }
        }

        this.provider.on('status', event => {
            this.status = event.status;
        });

        this.getUniqueUsers()

        //console.log(this.editor.storage.collaborationCursor.users)
        //console.log(this.editor.getHTML());
        // console.log(ydoc)
    },

    methods: {
        async getUser() {
            const config = useRuntimeConfig()
            const currentUserStore = userStore()
            await currentUserStore.user(config.public.baseURL);
        },

        getUniqueUsers() {
            const users = this.editor.storage.collaborationCursor.users;

            // Use a Set to track unique user IDs
            const uniqueUserIds = new Set();
            const uniqueUsers = [];

            users.forEach(user => {
                if (!uniqueUserIds.has(user.id)) {
                    uniqueUsers.push(user);
                    uniqueUserIds.add(user.id);
                }
            });

            // Now, `uniqueUsers` contains only unique users
            console.log(uniqueUsers)
            return uniqueUsers


        },


        getRandomColor() {
            return getRandomElement([
                '#958DF1',
                '#F98181',
                '#FBBC88',
                '#FAF594',
                '#70CFF8',
                '#94FADB',
                '#B9F18D',
            ])
        },



        async fetchAnnotatedData() {
            const authStore = useAuthStore()
            const token = authStore.accessToken
            try {
                const config = useRuntimeConfig()
                const response = await fetch(`${config.public.baseURL}/dataset/${this.projectId}/examples/${this.exampleId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json();
                return data.text

            } catch (error) {
                console.error('Error fetching example data:', error);
                // Handle error accordingly
                return ''
            }
        },
    },

    computed: {

        projectId() {
            return this.$route.params.id
        },

        exampleId() {
            return this.$route.params.example_id
        },

    },

    beforeUnmount() {
        this.editor.destroy()
    },
}
</script>

<style lang="scss">
.editor {
    background-color: #FFF;
    border: 3px solid #0D0D0D;
    border-radius: 0.75rem;
    color: #0D0D0D;
    display: flex;
    flex-direction: column;
    max-height: 26rem;

    &__header {
        align-items: center;
        background: #0d0d0d;
        border-bottom: 3px solid #0d0d0d;
        border-top-left-radius: 0.25rem;
        border-top-right-radius: 0.25rem;
        display: flex;
        flex: 0 0 auto;
        flex-wrap: wrap;
        padding: 0.25rem;
    }

    &__content {
        flex: 1 1 auto;
        overflow-x: hidden;
        overflow-y: auto;
        padding: 1.25rem 1rem;
        -webkit-overflow-scrolling: touch;
    }

    &__footer {
        align-items: center;
        border-top: 3px solid #0D0D0D;
        color: #0D0D0D;
        display: flex;
        flex: 0 0 auto;
        flex-wrap: wrap;
        font-size: 12px;
        font-weight: 600;
        justify-content: space-between;
        padding: 0.25rem 0.75rem;
        white-space: nowrap;
    }

    /* Some information about the status */
    &__status {
        align-items: center;
        border-radius: 5px;
        display: flex;

        &::before {
            background: rgba(#0D0D0D, 0.5);
            border-radius: 50%;
            content: ' ';
            display: inline-block;
            flex: 0 0 auto;
            height: 0.5rem;
            margin-right: 0.5rem;
            width: 0.5rem;
        }

        &--connecting::before {
            background: #616161;
        }

        &--connected::before {
            background: #B9F18D;
        }
    }

    &__name {
        button {
            background: none;
            border: none;
            border-radius: 0.4rem;
            color: #0D0D0D;
            font: inherit;
            font-size: 12px;
            font-weight: 600;
            padding: 0.25rem 0.5rem;

            &:hover {
                background-color: #0D0D0D;
                color: #FFF;
            }
        }
    }
}

/* Give a remote user a caret */
.collaboration-cursor__caret {
    border-left: 1px solid #0D0D0D;
    border-right: 1px solid #0D0D0D;
    margin-left: -1px;
    margin-right: -1px;
    pointer-events: none;
    position: relative;
    word-break: normal;
}

/* Render the username above the caret */
.collaboration-cursor__label {
    border-radius: 3px 3px 3px 0;
    color: #0D0D0D;
    font-size: 12px;
    font-style: normal;
    font-weight: 600;
    left: -1px;
    line-height: normal;
    padding: 0.1rem 0.3rem;
    position: absolute;
    top: -1.4em;
    user-select: none;
    white-space: nowrap;
}

/* Basic editor styles */
.tiptap {
    >*+* {
        margin-top: 0.75em;
    }

    ul,
    ol {
        padding: 0 1rem;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        line-height: 1.1;
    }

    code {
        background-color: rgba(#616161, 0.1);
        color: #616161;
    }

    pre {
        background: #0D0D0D;
        border-radius: 0.5rem;
        color: #FFF;
        font-family: 'JetBrainsMono', monospace;
        padding: 0.75rem 1rem;

        code {
            background: none;
            color: inherit;
            font-size: 0.8rem;
            padding: 0;
        }
    }

    mark {
        background-color: #FAF594;
    }

    img {
        height: auto;
        max-width: 100%;
    }

    hr {
        margin: 1rem 0;
    }

    blockquote {
        border-left: 2px solid rgba(#0D0D0D, 0.1);
        padding-left: 1rem;
    }

    hr {
        border: none;
        border-top: 2px solid rgba(#0D0D0D, 0.1);
        margin: 2rem 0;
    }

    ul[data-type="taskList"] {
        list-style: none;
        padding: 0;

        li {
            align-items: center;
            display: flex;

            >label {
                flex: 0 0 auto;
                margin-right: 0.5rem;
                user-select: none;
            }

            >div {
                flex: 1 1 auto;
            }
        }
    }
}
</style>
