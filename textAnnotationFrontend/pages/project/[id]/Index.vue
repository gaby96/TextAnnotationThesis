<template>
  <v-main>
    <p>This is the project - {{ $route.params.id }}</p>
  </v-main>
</template>

<script>
definePageMeta({
  layout: 'portal'
})
// import TheBanner from '@/components/TheBanner'



export default {
  // components: {
  //   FeatureCards,
  //   TheTopBanner,
  //   TheBottomBanner
  // }
}
</script>