<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/shared/stores/useUserStore'
import { getLatestProducts } from '../api/shop.js'
import ProductCardSmall from '../components/ProductCardSmall.vue'
import FloatingActions from '../components/FloatingActions.vue'

const userStore = useUserStore()

const products = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await getLatestProducts({
      ordering: '-date',
      page_size: 20,
    })

    products.value = response.data?.results ?? response.data ?? []
  } catch {
    error.value =
      'Не вдалося завантажити дані. Оновіть сторінку або спробуйте пізніше.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-8">

    <!-- Ошибка -->
    <div
      v-if="error"
      class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center text-red-600 font-medium"
    >
      {{ error }}
    </div>

    <!-- Скелетон загрузки -->
    <template v-if="loading">
      <div>
        <div class="h-7 w-56 bg-gray-200 rounded-lg animate-pulse mb-4"></div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div
            v-for="n in 10"
            :key="n"
            class="bg-white rounded-2xl border border-gray-100 overflow-hidden animate-pulse"
          >
            <div class="h-40 bg-gray-200"></div>

            <div class="p-3 space-y-2">
              <div class="h-4 bg-gray-200 rounded w-full"></div>
              <div class="h-4 bg-gray-200 rounded w-2/3"></div>
              <div class="h-3 bg-gray-100 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Основной контент -->
    <template v-else-if="!error">
      <section>
        <h2 class="text-xl font-semibold text-gray-800 mb-4">
          Останні оголошення
        </h2>

        <div
          v-if="products.length"
          class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4"
        >
          <ProductCardSmall
            v-for="product in products"
            :key="product.id"
            :product="product"
          />
        </div>

        <!-- Пустое состояние -->
        <div v-else class="text-center py-20">
          <InboxIcon class="w-16 h-16 mx-auto mb-4 text-gray-200" />

          <p class="text-lg font-semibold text-gray-500">
            Поки оголошень немає — ти можеш бути першим!
          </p>

          <router-link
            v-if="userStore.isAuthenticated"
            :to="{ name: 'shop-create-product' }"
            class="inline-block mt-3 text-blue-600 underline hover:opacity-75 transition-opacity text-sm font-medium"
          >
            Додати свій товар
          </router-link>
        </div>
      </section>
    </template>
  </div>

  <FloatingActions />
</template>