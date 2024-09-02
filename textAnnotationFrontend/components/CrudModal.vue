<template>
    <div v-if="isModalVisible" id="crud-modal" tabindex="-1" aria-hidden="true" role="dialog" aria-modal="true"
        class="fixed inset-0 z-50 flex items-center justify-center bg-gray-600 bg-opacity-75">
        <div class="relative p-4 w-full max-w-md max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                        Comments
                    </h3>
                    <button type="button" @click="closeModal"
                        class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                        </svg>
                        <span class="sr-only">Close modal</span>
                    </button>
                </div>
                <!-- Modal body -->
                <div class="p-4 md:p-5">
                    <div class="mb-4">
                        <textarea v-model="comment" id="description" rows="4"
                            class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Write comment here"></textarea>
                    </div>
                    <button @click.prevent="submitComment"
                        class="w-full text-white inline-flex items-center bg-green-500 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">
                        <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                                clip-rule="evenodd"></path>
                        </svg>
                        Add Comment
                    </button>

                    <!-- Display the list of comments -->
                    <div class="mt-4">
                        <h4 class="text-md font-semibold text-gray-900 dark:text-white mb-2">Previous Comments</h4>
                        <div v-if="comments.length">
                            <div v-for="(comment, index) in comments" :key="comment.id"
                                class="relative p-2 border-b border-gray-200 dark:border-gray-600">
                                <div class="flex justify-between items-start">
                                    <div class="flex-1">
                                        <!-- Editable comment textarea -->
                                        <textarea v-if="editingIndex === index" v-model="comments[index].text"
                                            class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                        </textarea>
                                        <p v-else class="text-sm text-gray-700 dark:text-gray-300">{{ comment.text }}
                                        </p>
                                        <small class="text-xs text-gray-500 dark:text-gray-400">{{ comment.userId }} -
                                            {{ new Date(comment.created_at).toLocaleString() }}</small>
                                    </div>
                                    <div class="relative">
                                        <!-- Save and Edit/Delete buttons -->
                                        <button v-if="editingIndex !== index" @click="toggleDropdown(index)"
                                            class="text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-500">
                                            ••
                                        </button>
                                        <div v-if="isDropdownOpen === index && editingIndex !== index"
                                            class="absolute right-0 mt-2 w-24 bg-white border border-gray-300 rounded-lg shadow-lg dark:bg-gray-700 dark:border-gray-600">
                                            <ul class="py-1 text-sm text-gray-700 dark:text-gray-200">
                                                <li @click="editComment(index)"
                                                    class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer">
                                                    Edit
                                                </li>
                                                <li @click="deleteComment(comment.id)"
                                                    class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer">
                                                    Delete
                                                </li>
                                            </ul>
                                        </div>
                                        <!-- Save button -->
                                        <button v-if="editingIndex === index" @click="saveEdit(index)"
                                            class="ml-2 text-white bg-green-500 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-2.5 py-1.5 text-center dark:bg-blue-600 dark:hover:bg-green-700 dark:focus:ring-green-800">
                                            Save
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else>
                            <p class="text-sm text-gray-500 dark:text-gray-400">No comments yet.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
import { useAuthStore } from "@/stores/auth";
export default {
    props: {
        isModalVisible: {
            type: Boolean,
            required: true
        },

        projectId: {
            type: String,
            required: true
        },
        exampleId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            comment: '', // Holds the comment text
            comments: [],
            isDropdownOpen: null, // Tracks the index of the dropdown that is open
            editingIndex: null,
        };
    },

    watch: {
        isModalVisible(newValue) {
            if (newValue) {
                this.fetchComments();
            }
        }
    },

    methods: {
        closeModal() {
            this.$emit('close');
        },

        async fetchComments() {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.baseURL}/project/dataset/${this.projectId}/comments?example=${this.exampleId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch comments');
                }

                const result = await response.json();
                this.comments = result; // Assuming the response is an array of comments
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        },

        async submitComment() {
            if (this.comment.trim() === '') {
                alert('Comment cannot be empty');
                return;
            }
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            let userObject = authStore.user;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.baseURL}/project/dataset/${this.projectId}/comments?example=${this.exampleId}`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`,
                        },
                        body: JSON.stringify({
                            text: this.comment,
                            userId: userObject.id
                        })
                    });

                if (!response.ok) {
                    throw new Error('Failed to submit comment');
                }

                const result = await response.json();
                console.log('Comment submitted successfully:', result);
                this.comment = ''; // Clear the comment field after submission
                await this.fetchComments();
            } catch (error) {
                console.error('Error submitting comment:', error);
            }
        },

        toggleDropdown(index) {
            this.isDropdownOpen = this.isDropdownOpen === index ? null : index;
        },

        editComment(index) {
            this.editingIndex = index; // Set the current comment index to editing mode
            this.isDropdownOpen = null; // Close the dropdown
        },

        async saveEdit(index) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            const commentToSave = this.comments[index];
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.baseURL}/project/dataset/${this.projectId}/comments/${commentToSave.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        text: commentToSave.text,
                        userId: commentToSave.userId,
                    }),
                });

                if (!response.ok) {
                    throw new Error('Failed to save comment');
                }

                this.editingIndex = null; // Exit editing mode properly
                await this.fetchComments(); // Refresh comments list after saving
            } catch (error) {
                console.error('Error saving comment:', error);
            }
        },


        async deleteComment(commentId) {
            const authStore = useAuthStore();
            const token = authStore.accessToken;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.baseURL}/project/dataset/${this.projectId}/comments/${commentId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to delete comment');
                }

                console.log('Comment deleted successfully');
                await this.fetchComments(); // Refresh the comments list after deletion
            } catch (error) {
                console.error('Error deleting comment:', error);
            }
        }
    }
};
</script>