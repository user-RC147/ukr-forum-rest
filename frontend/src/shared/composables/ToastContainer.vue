<script setup>
import { useToast } from '@/shared/composables/useToast'

const { toasts, remove } = useToast()

const colors = {
  success: 'bg-emerald-500',
  error: 'bg-red-500',
  warning: 'bg-amber-500',
  info: 'bg-blue-500',
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 left-4 sm:left-auto z-[9999] flex w-full max-w-sm flex-col gap-3">
      <TransitionGroup name="toast" tag="div" class="flex flex-col gap-3">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[colors[toast.type], 'flex items-start gap-3 rounded-xl px-5 py-4 text-white shadow-lg shadow-black/10 ring-1 ring-black/5 cursor-pointer transition-all']"
          @click="remove(toast.id)"
        >
          <span class="text-xl leading-none">{{ toast.icon }}</span>
          <p class="flex-1 text-sm leading-relaxed">{{ toast.message }}</p>
          <button
            class="text-lg leading-none text-white/80 hover:text-white"
            @click.stop="remove(toast.id)"
          >
            ×
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(2rem);
}
</style>