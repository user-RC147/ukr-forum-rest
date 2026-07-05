<script setup>
import { TransitionGroup } from 'vue'
import { useToast } from '@/shared/composables/useToast'
import ToastItem from '@/shared/components/ToastItem.vue'

const { toasts, removeToast } = useToast()
</script>

<template>
  <!--
    top-20 + bottom-4 фіксують висоту блоку — список тостів фізично
    не може залізти під шапку зверху чи вилізти за нижню межу екрана.
  -->
  <div
    class="pointer-events-none fixed inset-x-4 top-20 bottom-4 z-[999999] flex flex-col items-end gap-3 overflow-y-auto sm:inset-x-auto sm:right-4 sm:w-full sm:max-w-sm"
  >
    <TransitionGroup
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-x-8 scale-95"
      enter-to-class="opacity-100 translate-x-0 scale-100"
      leave-active-class="transition-all duration-200 ease-in absolute"
      leave-from-class="opacity-100 translate-x-0"
      leave-to-class="opacity-0 translate-x-8"
    >
      <ToastItem
        v-for="toast in toasts"
        :key="toast.id"
        :toast="toast"
        class="w-full flex-shrink-0"
        @close="removeToast(toast.id)"
      />
    </TransitionGroup>
  </div>
</template>