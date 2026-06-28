<script setup>
import { useToast } from '@/shared/composables/useToast'
const { toasts, removeToast } = useToast()
</script>

<template>
  <div class="toast-container">
    <div v-for="toast in toasts" :key="toast.id" class="toast" @click="removeToast(toast.id)">
      {{ toast.message }}
    </div>
  </div>
</template>