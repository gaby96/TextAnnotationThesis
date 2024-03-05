<template>
    <section class="bg-gray-50 dark:bg-gray-50">
      <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:h-screen">
        <a href="#" class="flex items-center mb-2 text-2xl font-semibold text-gray-900 dark:text-black">
         Add user
        </a>
        <div
          class="w-full bg-white rounded-lg shadow white:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-white dark:border-white">
          <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
  
            <form @submit.prevent="registerUser" class="space-y-4 md:space-y-6" action="#">
              <div>
                <label for="first-name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">First
                  Name</label>
                <input type="text" name="first-name" id="first-name" v-model="firstName"
                  class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="John">
              </div>
              <div>
                <label for="last-name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Last
                  Name</label>
                <input type="text" name="last-name" id="last-name" v-model="lastName"
                  class="bg-white border border-gray-500 text-moniquegray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="Doe">
              </div>
              <div>
                <label for="user-name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">
                  Username</label>
                <input type="text" name="user-name" id="user-name" v-model="username"
                  class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="ferrari98">
              </div>
              <div>
      <p class="text-gray-500">
      Select Project Type
    </p>
      <div class='relative'>
        <select
            class="w-full rounded-lg border-gray-200 p-4 mt-5 text-sm shadow-sm focus:ring-blue-500 focus:border-blue-500"
            v-model="selectedRole"
          >
          <option disabled value="">Select Role</option>
          <option v-for="roleObject in roleTypes" :value="roleObject.id" :key="roleObject.id">
            {{ roleObject.name }}
          </option>
          </select>

      </div>
          </div>
              <div>
                <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Email</label>
                <input type="email" name="email" id="email" v-model="email"
                  class="bg-white border border-gray-500 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="johndoe@example.com">
              </div>
              <div>
                <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-black">Password</label>
                <input type="password" name="password" id="password" v-model="password" placeholder="••••••••"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500">
              </div>
              <button type="submit" style="background-color: #047857;" @click="addUser()"
                class="w-full text-white hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:hover:bg-green-700 dark:focus:ring-green-800">Add user</button>
  
            </form>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
import { useAuthStore } from '@/stores/auth';
  export default{
    name: "CreateMember",
    data(){

      return {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        username: '',
        selectedRole: null,
        roleTypes: [],

      };
``
    },

    methods:{
        async addUser(){
          const apiUrl = this.$config.public.baseURL;
          const authStore = useAuthStore();
          const token = authStore.accessToken;
          console.log(token)
          try{
            const userResponse = await fetch(`${apiUrl}/auth/signup`,{
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', // Correct content type for JSON
                'Authorization': `Bearer ${token}`,
              },
              body: JSON.stringify({
                first_name: this.firstName,
                last_name: this.lastName,
                email: this.email,
                password: this.password,
                username: this.username
              }),

            });

            const data = await userResponse.json();
            console.log(data)
            if(userResponse.error){
              console.log(userResponse.error);
              alert('Something went wrong');
              return;
            }
            
            console.log(userResponse)
            const addMemberResponse = await fetch(`${apiUrl}/project/projects/${this.projectId}/members`, {
              headers: {
                'Content-Type': 'application/json', // Correct content type for JSON
                'Authorization': `Bearer ${token}`,
              },
              method: 'POST',
              body:JSON.stringify({
                user: data.id,
                role: this.selectedRole
              })
            });

            if(addMemberResponse.error){
              console.log(addMemberResponse.error);
              alert('The user was not added to the project')
              return;
            }

            alert('Registration and adding member to a project was successful');
            
          }
          catch(error){
            console.error('Registration or project assignment error:', error);
            alert('An error occurred. Please try again.');
          }
          
        },

      async displayRoles(){
        const apiUrl = this.$config.public.baseURL;
        const authStore = useAuthStore()
        const token = authStore.accessToken
        try{

          const rolesResponse = await fetch(`${apiUrl}/roles/roles`,{
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
            });

            const data = await rolesResponse.json();
            this.roleTypes = data;
            console.log(this.roleTypes);
            if(rolesResponse.error){
              console.log(rolesResponse.error);
              alert('Something went wrong');
              return;
            }

        }
        catch(error){
            console.error('Registration or project assignment error:', error);
           
          }
      },
    },

    mounted(){
      this.displayRoles();
    },

    computed: {
      projectId() {
      return this.$route.params.id
    },
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




<!-- import { ref } from 'vue'
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
      console.log(error.value)
      alert('An error occurred. Please try again.')
    } else {
      alert('Registration successful!')
      // Redirect or clear form here
    }
  } -->