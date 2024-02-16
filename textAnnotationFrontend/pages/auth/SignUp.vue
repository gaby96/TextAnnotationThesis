<template>
    <section class="bg-gray-50 dark:bg-gray-50">
      <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:h-screen">
          <a href="#" class="flex items-center mb-2 text-2xl font-semibold text-gray-900 dark:text-black">
              Create an account   
          </a>
          <p class="flex items-center mb-2 text-sm font-semibold text-gray-900 dark:text-black">
            We will get you up and running so you can verify your personal <br> information and customize your account
          </p>
          <div class="w-full bg-white rounded-lg shadow white:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-white dark:border-white">
              <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                  
                  <form @submit.prevent="registerUser" class="space-y-4 md:space-y-6" action="#">
                      <div>
                          <label for="first-name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">First Name</label>
                          <input type="text" name="first-name" id="first-name" v-model="firstName" class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="John" >
                      </div>
                      <div>
                          <label for="last-name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Last Name</label>
                          <input type="text" name="last-name" id="last-name" v-model="lastName" class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Doe" >
                      </div>
                      <div>
                          <label for="user-name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black"> Username</label>
                          <input type="text" name="user-name" id="user-name" v-model="username"  class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="ferrari98" >
                      </div>
                      <div>
                          <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Email</label>
                          <input type="email" name="email" id="email" v-model="email" class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="johndoe@example.com" >
                      </div>
                      <div>
                          <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Password</label>
                          <input type="password" name="password" id="password"  v-model="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500">
                      </div>
                      <div class="flex items-center justify-between">
                          <div class="flex items-start">
                              <div class="flex items-center h-5">
                                <div class="flex items-center h-5">
                                    <input id="annoteterms" aria-describedby="annoteterms" type="checkbox" class="checkbox w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-green-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-green-600 dark:ring-offset-gray-800">
                                </div>
                              </div>
                              <div class="ml-3 text-sm">
                                <label for="annoteterms" class="text-dark dark:text-dark">Annote terms and conditions</label>
                              </div>
                          </div>
                      </div>
                      <button type="submit" style="background-color: #047857;" class="w-full text-white hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:hover:bg-green-700 dark:focus:ring-green-800">Sign in</button>
    
                      <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                          Have an account yet? <a href="#" style="color: #047857;" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign in here</a>
                      </p>
                  </form>
              </div>
          </div>
      </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import { useFetch } from 'nuxt/app'

const config = useRuntimeConfig()
const apiUrl = config.public.baseURL

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const username = ref('')

async function registerUser() {
  const { data, error } = await useFetch(`${apiUrl}/auth/signup`, {
    method: 'POST',
    body: JSON.stringify({
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      username: username.value
    }),
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (error.value) {
    alert('An error occurred. Please try again.')
  } else {
    alert('Registration successful!')
    // Redirect or clear form here
  }
}

</script>

<style scoped>
.checkbox:checked {
    /* Change '#047857' to the green color you want */
    background-color: #047857;
    border-color: #047857;
}
</style>