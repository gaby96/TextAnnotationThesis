<template>
  <nav
    class="relative flex w-full flex-wrap items-center justify-between py-2 hover:text-neutral-700 focus:text-neutral-700 lg:py-4"
    data-te-navbar-ref>
    <div class="flex w-full flex-wrap items-center justify-between px-24">
      <div>
        <a class="mx-2 my-1 flex items-center text-neutral-900 hover:text-neutral-900 focus:text-neutral-900 lg:mb-0 lg:mt-0"
          href="#">
          <img class="ml-3" src="~/assets/Logo.png" style="height: 30px" alt="Annote Logo" loading="lazy" />
        </a>
      </div>

      <!-- Hamburger button for mobile view -->
      <button
        class="block border-0 bg-transparent px-2 text-neutral-500 hover:no-underline hover:shadow-none focus:no-underline focus:shadow-none focus:outline-none focus:ring-0 dark:text-neutral-200 lg:hidden"
        type="button" data-te-collapse-init data-te-target="#navbarSupportedContent4"
        aria-controls="navbarSupportedContent4" aria-expanded="false" aria-label="Toggle navigation">
        <!-- Hamburger icon -->
        <span class="[&>svg]:w-7">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-7 w-7">
            <path fill-rule="evenodd"
              d="M3 6.75A.75.75 0 013.75 6h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 6.75zM3 12a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 12zm0 5.25a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75a.75.75 0 01-.75-.75z"
              clip-rule="evenodd" />
          </svg>
        </span>
      </button>

      <!-- Collapsible navbar container -->
      <div class="!visible mt-2 hidden flex-grow basis-[100%] items-center lg:mt-0 lg:!flex lg:basis-auto"
        id="navbarSupportedContent4" data-te-collapse-item>
        <!-- Left links -->
        <ul class="list-style-none mr-auto flex flex-col pl-0 lg:mt-1 lg:flex-row" data-te-navbar-nav-ref>
          <!-- Home link -->

        </ul>

        <div class="flex items-center">
          <div class="divide-x-2 divide-black-300">
            <button type="button" data-te-ripple-init data-te-ripple-color="light"
              class="mr-3 inline-block rounded px-6 pb-1 pt-1 text-base font-medium normal-case leading-normal text-primary transition duration-150 ease-in-out hover:bg-neutral-100 hover:text-primary-600 focus:text-primary-600 focus:outline-none focus:ring-0 active:text-primary-700 motion-reduce:transition-none">
              Support
            </button>


            <nuxt-link to="/auth/login"
              class="mr-3 inline-block rounded px-6 pb-1 pt-1 text-base font-medium normal-case leading-normal text-primary transition duration-150 ease-in-out hover:bg-neutral-100 hover:text-primary-600 focus:text-primary-600 focus:outline-none focus:ring-0 active:text-primary-700 motion-reduce:transition-none">
              Login
            </nuxt-link>
          </div>
          <nuxt-link type="button" to="/auth/signup"
            class="inline-block rounded-lg border border-gray-300 px-3 py-1 text-base font-medium normal-case leading-normal text-neutral-800 transition duration-150 ease-in-out hover:bg-neutral-100 focus:bg-neutral-100 focus:outline-none focus:ring-0 active:bg-neutral-200 ">
            Create free Account
          </nuxt-link>

        </div>
      </div>
    </div>
  </nav>
</template>

<script>



</script>

<style scoped></style>