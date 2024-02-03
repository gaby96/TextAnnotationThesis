<template>
    <section class="bg-gray-50 dark:bg-gray-50">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:h-screen">
        <a href="#" class="flex items-center mb-2 text-2xl font-semibold text-gray-900 dark:text-black">
            Login    
        </a>
        <p class="flex items-center mb-2 text-sm font-semibold text-gray-900 dark:text-black">
            We will get you up and running so you can verify your personal <br> information and customize your account
        </p>
        <div class="w-full bg-white rounded-lg shadow white:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-white dark:border-white">
            <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                
                <form @submit.prevent="login" class="space-y-4 md:space-y-6" action="#">
                    <div>
                        <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Username</label>
                        <input type="username" v-model="username" name="username" id="username" class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="name@company.com" >
                    </div>
                    <div>
                        <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Password</label>
                        <input type="password" v-model="password" name="password" id="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500">
                    </div>
                    <div class="flex items-center justify-between">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <div class="flex items-center h-5">
                                    <input id="remember" aria-describedby="remember" type="checkbox" class="checkbox w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-green-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-green-600 dark:ring-offset-gray-800">
                                </div>
                            </div>
                            <div class="ml-3 text-sm">
                                <label for="remember" class="text-dark dark:text-dark">Remember me</label>
                            </div>
                        </div>
                        <a href="#" style="color: #047857" class="text-sm font-medium text-primary-600 hover:underline ">Forgot password?</a>
                    </div>
                    <button type="submit" style="background-color: #047857; color: white;" class="w-full text-white hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:hover:bg-green-700 dark:focus:ring-green-800">{{ auth.isloading ? "Login...." : "Login" }}</button>

                    <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                        Dont have an account yet? <a href="#" style="color: #047857;" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</a>
                    </p>
                </form>
            </div>
        </div>
    </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
const auth = useAuthStore();


const config = useRuntimeConfig()

const username = ref('')
const password = ref('')
const authStore = useAuthStore()

const login = async () => {
  const success = await authStore.login({ username: username.value, password: password.value }, config.public.baseURL);
  if (success) {
    // Redirect to dashboard if login is successful
    navigateTo('/emptydashboard');
  } else {
    // Optionally handle login failure (e.g., show an error message)
    alert('Login failed. Please check your credentials.');
  }
};
</script>


<style scoped>
.checkbox:checked {
  /* Change '#047857' to the green color you want */
  background-color: #047857;
  border-color: #047857;
}
</style>