<template>
  <v-app>
    <!-- <the-header class="" /> -->
    <slot />
    <!-- <the-footer /> -->
  </v-app>
</template>
  
<script>
//   import TheFooter from '@/components/layout/TheFooter'
import TheHeader from '@/components/TheHeader'

export default {
  components: {
    //   TheFooter,
    TheHeader
  }
}
</script>