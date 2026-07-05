<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon,
} from '@heroicons/vue/24/solid'

const props = defineProps({
  toast: { type: Object, required: true },
})
const emit = defineEmits(['close'])

const STYLES = {
  success: { bg: 'bg-gradient-to-r from-emerald-500 to-emerald-600', icon: CheckCircleIcon },
  error: { bg: 'bg-gradient-to-r from-rose-500 to-rose-600', icon: ExclamationCircleIcon },
  warning: { bg: 'bg-gradient-to-r from-amber-400 to-amber-500', icon: ExclamationTriangleIcon },
  info: { bg: 'bg-gradient-to-r from-sky-500 to-sky-600', icon: InformationCircleIcon },
  loading: { bg: 'bg-gradient-to-r from-slate-700 to-slate-800', icon: null },
}

function styleFor(type) {
  return STYLES[type] ?? STYLES.info
}

// Полоса прогресу: старт з "w-full", а на наступному кадрі — перехід
// до "w-0" за час toast.duration. Саме тому потрібен requestAnimationFrame:
// якщо просто одразу поставити shrink = true, браузер побачить
// "кінцевий" стан ще до першого рендера і transition не спрацює візуально.
const shrink = ref(false)

async function startProgress() {
  shrink.value = false
  await nextTick()
  requestAnimationFrame(() => {
    shrink.value = true
  })
}

onMounted(() => {
  if (props.toast.duration > 0) startProgress()
})

// Дублікат того самого тосту рестартує прогрес-бар з нуля —
// resetKey змінюється в useToast.js при повторному showToast().
watch(
  () => props.toast.resetKey,
  () => {
    if (props.toast.duration > 0) startProgress()
  },
)
</script>

<template>
  <div
    class="pointer-events-auto w-full overflow-hidden rounded-2xl shadow-xl ring-1 ring-black/5 transition-transform hover:-translate-y-0.5"
    :class="styleFor(toast.type).bg"
    role="alert"
  >
    <div class="flex items-start gap-3 p-4">
      <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-white/20">
        <component :is="styleFor(toast.type).icon" v-if="styleFor(toast.type).icon" class="h-5 w-5 text-white" />
        <span v-else class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
      </div>

      <div class="min-w-0 flex-1 pt-0.5">
        <p class="font-semibold text-white">
          {{ toast.title }}
          <span v-if="toast.count > 1" class="ml-1 font-normal text-white/70">×{{ toast.count }}</span>
        </p>
        <p class="mt-0.5 text-sm leading-relaxed text-white/90">{{ toast.message }}</p>
      </div>

      <button
        type="button"
        class="flex-shrink-0 rounded-full p-1 text-white/70 transition hover:bg-white/10 hover:text-white"
        @click="emit('close')"
      >
        <XMarkIcon class="h-4 w-4" />
      </button>
    </div>

    <div v-if="toast.duration > 0" class="h-1 w-full bg-black/10">
      <div
        class="h-full rounded-r-full bg-white/70 transition-all ease-linear"
        :class="[shrink ? 'w-0' : 'w-full', `duration-[${toast.duration}ms]`]"
      ></div>
    </div>
  </div>
</template>