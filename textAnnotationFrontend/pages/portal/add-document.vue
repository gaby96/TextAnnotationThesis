<template>
    <div>
        <div class="flex flex-col items-center justify-center py-12 h-full mt-20">
            <div class="w-[550px] ">
                <h2 class="text-center font-semibold text-4xl mb-3">Welcome to AnnotateText!</h2>
                <p class="text-center text-neutral-500">
                    Your one-stop platform for fast and accurate text annotation. From sentiment analysis to entity
                    identification and collaborative projects, we have you covered.
                </p>

                <!-- div -->
                <div class="my-8 text-neutral-500">
                    <div>
                        We allow only: <span
                            class="rounded-full border text-blue-600 bg-blue-100 p-0.5 px-2 font-light text-sm mr-2 border-blue-200">Word</span>
                        <span
                            class="rounded-full border text-blue-600 bg-blue-100 p-0.5 px-2 font-light text-sm border-blue-200">PDF</span>
                    </div>
                    <div
                        class="border border-dashed flex justify-center items-center p-5 py-14 my-2 rounded-md border-neutral-500">
                        <div class="text-center">
                            <UIcon name="i-heroicons-folder-minus" class="text-3xl" />
                            <p class="my-3">Choose file to upload here</p>
                            <p class="text-sm">Maximum file size is 5MB</p>
                            <button
                                class="border border-primary py-1.5 px-10 rounded-lg text-primary mt-3 hover:bg-primary hover:text-white transition-colors">Browse</button>
                        </div>
                    </div>
                    <p class="mt-2">Hint: You can also drag and drop files into this window!</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    layout: 'portal'
})
</script>

<style scoped></style>