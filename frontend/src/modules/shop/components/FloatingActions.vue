<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/shared/stores/useUserStore'

const userStore = useUserStore()
const isOpen  = ref(false)
const wrapper = ref(null)

function onDocClick(e) {
  if (wrapper.value && !wrapper.value.contains(e.target)) isOpen.value = false
}

onMounted(()  => document.addEventListener('click', onDocClick))
onUnmounted(() => document.removeEventListener('click', onDocClick))
</script>

<template>
  <div ref="wrapper" class="fixed z-50 bottom-4 right-4 flex flex-col items-end gap-2">

    <!-- Раскрывающееся меню -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out origin-bottom-right"
      enter-from-class="opacity-0 scale-90 translate-y-2"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in origin-bottom-right"
      leave-from-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-90 translate-y-2"
    >
      <div v-if="isOpen" class="flex flex-col items-end gap-2">
        <router-link
          :to="{ name: 'shop-my-products' }"
          class="text-sm font-semibold text-white bg-orange-400 hover:bg-orange-500
                 px-5 py-2.5 rounded-xl shadow-lg hover:shadow-xl
                 transition-all duration-200 hover:-translate-y-0.5 active:scale-95"
        >
          Мої товари
        </router-link>
      </div>
    </Transition>

    <!-- Тоглер -->
    <button
      type="button"
      :aria-expanded="isOpen"
      aria-label="Інші дії"
      @click.stop="isOpen = !isOpen"
      class="text-sm font-semibold text-white bg-orange-400/80 hover:bg-orange-500/90
             px-5 py-2.5 rounded-xl shadow-md transition-all duration-200 active:scale-95"
    >
      Інші дії
    </button>

    <!-- Главная кнопка -->
    <router-link
      :to="userStore.isAuthenticated ? { name: 'shop-create-product' } : { name: 'login' }"
      class="font-semibold text-white bg-orange-500 hover:bg-orange-600
             px-6 py-3 rounded-xl shadow-xl hover:shadow-2xl
             transition-all duration-200 hover:-translate-y-0.5 active:scale-95"
    >
      + Додати товар
    </router-link>

  </div>
</template>