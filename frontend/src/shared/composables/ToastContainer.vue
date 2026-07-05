<script setup>
import { useToast } from '@/shared/composables/useToast'
import { TransitionGroup } from 'vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
} from '@heroicons/vue/24/outline'

const { toasts, removeToast } = useToast()

const STYLES = {
  success: { bg: 'bg-green-600', icon: CheckCircleIcon },
  error: { bg: 'bg-red-600', icon: ExclamationCircleIcon },
  warning: { bg: 'bg-yellow-500', icon: ExclamationTriangleIcon },
  info: { bg: 'bg-blue-600', icon: InformationCircleIcon },
  loading: { bg: 'bg-gray-700', icon: null },
}

function styleFor(type) {
  return STYLES[type] ?? STYLES.info
}
</script>

<template>
  <div class="pointer-events-none fixed inset-x-4 top-4 z-[999999] flex flex-col items-end gap-2 sm:inset-x-auto sm:right-4">
    <TransitionGroup
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-x-8"
      enter-to-class="opacity-100 translate-x-0"
      leave-active-class="transition-all duration-200 ease-in absolute"
      leave-from-class="opacity-100 translate-x-0"
      leave-to-class="opacity-0 translate-x-8"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-xl px-4 py-3 text-sm font-medium text-white shadow-lg transition-transform hover:scale-[1.02]"
        :class="styleFor(toast.type).bg"
        role="alert"
        @click="removeToast(toast.id)"
      >
        <component
          :is="styleFor(toast.type).icon"
          v-if="styleFor(toast.type).icon"
          class="h-5 w-5 flex-shrink-0"
        />
        <span class="flex-shrink-0 h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" v-else />
        <span class="flex-1 leading-relaxed">{{ toast.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>