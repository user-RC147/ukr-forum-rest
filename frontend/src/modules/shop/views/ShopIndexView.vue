<script setup>
import { ref, onMounted } from 'vue'
import { PlusIcon, Bars3Icon } from '@heroicons/vue/24/outline'
import { useUserStore } from '@/shared/stores/useUserStore'
import { getLatestProducts } from '../api/shop.js'
import SearchFiltersBar from '../components/SearchFiltersBar.vue'
import CategoriesSection from '../components/CategoriesSection.vue'
import ProductCardSmall from '../components/ProductCardSmall.vue'

const userStore = useUserStore()

const products = ref([])
const isLoading = ref(true)
const error = ref(null)
const actionsOpen = ref(false)

async function loadLatestProducts() {
  isLoading.value = true
  error.value = null
  try {
    const { data } = await getLatestProducts()
    products.value = data?.items ?? []
  } catch (e) {
    error.value = 'Не вдалося завантажити оголошення'
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadLatestProducts)
</script>

<template>
  <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-8">
    <SearchFiltersBar />
    <CategoriesSection />

    <section>
      <h2 class="text-xl font-semibold text-gray-900 mb-5">Останні оголошення</h2>

      <div v-if="isLoading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <div v-for="n in 10" :key="n" class="h-64 rounded-lg bg-gray-100 animate-pulse"></div>
      </div>

      <p v-else-if="error" class="text-center text-red-600 py-10">{{ error }}</p>

      <div
        v-else-if="products.length"
        class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6"
      >
        <ProductCardSmall
          v-for="p in products"
          :key="p.id"
          :product="p"
        />
      </div>

      <p v-else class="text-center font-semibold text-lg italic py-12 text-gray-700">
        Поки оголошень немає, ти можеш бути першим!
        <RouterLink
          v-if="userStore.isAuthenticated"
          :to="{ name: 'shop-create-product' }"
          class="text-blue-600 underline hover:opacity-80 ml-1"
        >
          Додати свій товар
        </RouterLink>
      </p>
    </section>

    <div class="fixed z-50 bottom-4 right-4 flex flex-col items-end gap-2">
      <div
        class="flex flex-col items-end gap-2 transition-all duration-300 ease-out"
        :class="actionsOpen ? 'opacity-100 translate-y-0 pointer-events-auto' : 'opacity-0 translate-y-4 pointer-events-none'"
      >
        <RouterLink
          v-if="userStore.isAuthenticated"
          :to="{ name: 'shop-my-products' }"
          class="bg-orange-500/70 hover:bg-orange-600/80 text-white text-sm font-semibold px-5 py-2.5 rounded-lg shadow-lg transition-colors duration-200"
        >
          Мої товари
        </RouterLink>
      </div>

      <button
        type="button"
        @click="actionsOpen = !actionsOpen"
        class="inline-flex cursor-pointer items-center gap-2 bg-orange-500/70 hover:bg-orange-600/80 text-white font-semibold px-5 py-3 rounded-lg shadow-lg transition-colors duration-200"
      >
        <Bars3Icon class="w-5 h-5" />
        Інші дії
      </button>

      <RouterLink
        v-if="userStore.isAuthenticated"
        :to="{ name: 'shop-create-product' }"
        class="inline-flex items-center gap-2 bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-lg shadow-xl transition-colors duration-200"
      >
        <PlusIcon class="w-5 h-5" />
        Додати свій товар
      </RouterLink>
    </div>
  </main>
</template>