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
      <TransitionGroup
        tag="div"
        class="flex flex-col gap-3"
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 translate-x-8"
        enter-to-class="opacity-100 translate-x-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-x-0"
        leave-to-class="opacity-0 translate-x-8"
        move-class="transition-transform duration-300"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[colors[toast.type], 'flex items-start gap-3 rounded-xl px-5 py-4 text-white shadow-lg shadow-black/10 ring-1 ring-black/5 cursor-pointer transition-colors']"
          @click="remove(toast.id)"
        >
          <span class="text-xl leading-none">{{ toast.icon }}</span>
          <p class="flex-1 text-sm leading-relaxed">{{ toast.message }}</p>
          <button
            type="button"
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