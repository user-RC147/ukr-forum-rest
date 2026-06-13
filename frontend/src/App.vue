<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/modules/users/stores/useUserStore.js'

const userStore = useUserStore()

onMounted(() => {
  if (userStore.accessToken) {
    userStore.fetchProfile()
  }
})
</script>

<template>
  <RouterView />
</template>