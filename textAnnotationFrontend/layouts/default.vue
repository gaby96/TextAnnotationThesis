<template>
 
     <the-header class="" v-if="!useAuthStore().accessToken" />
    <slot />
    <!-- <the-footer /> -->
</template>
  
<script>
//   import TheFooter from '@/components/layout/TheFooter'
import TheHeader from '@/components/TheHeader'
import { useAuthStore } from '#imports';

export default {
  components: {
    //   TheFooter,
    TheHeader
  }
}
</script>