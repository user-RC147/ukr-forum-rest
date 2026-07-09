<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/shared/stores/useUserStore.js'
import ToastContainer from '@/shared/composables/ToastContainer.vue'

const userStore = useUserStore()

onMounted(() => {
  if (userStore.accessToken) {
    userStore.fetchProfile()
  }
})
</script>

<template>
  <RouterView />
  <ToastContainer />
</template>