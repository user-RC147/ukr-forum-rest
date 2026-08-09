<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/shared/stores/useUserStore'
import { getProductThumbnailUrl } from '@/shared/utils/media'
import { useMyProducts } from '../composables/useMyProducts'

const router = useRouter()
const userStore = useUserStore()

const { products, isLoading, error, page, totalPages, hasNext, hasPrevious, goToPage } =
  useMyProducts(() => userStore.user?.id)

onMounted(() => {
  if (!userStore.isAuthenticated) {
    router.push({ name: 'login' })
  }
})
</script>

<template>
  <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-8">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold text-gray-900">Мої товари</h1>
      <RouterLink
        :to="{ name: 'shop-create-product' }"
        class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors duration-200"
      >
        + Додати товар
      </RouterLink>
    </div>

    <div v-if="isLoading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
      <div v-for="n in 10" :key="n" class="h-64 rounded-lg bg-gray-100 animate-pulse"></div>
    </div>

    <p v-else-if="error" class="text-center text-red-600 py-10">{{ error }}</p>

    <div v-else-if="products.length" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
      <div v-for="p in products" :key="p.id" class="group">
        <RouterLink :to="{ name: 'shop-product', params: { pk: p.id } }" class="block mb-2">
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden flex flex-col h-full transition-shadow duration-200 group-hover:shadow-md">
            <div class="w-full h-40 bg-gray-100 overflow-hidden">
              <img
                v-if="getProductThumbnailUrl(p)"
                :src="getProductThumbnailUrl(p)"
                :alt="p.title"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
            <div class="p-3 flex flex-col flex-1">
              <h3 class="text-sm font-medium text-gray-900 mb-2 line-clamp-2 leading-tight">
                {{ p.title }}
              </h3>
              <p class="mt-auto mb-1 font-semibold text-gray-900">
                {{ p.price }} {{ p.country?.currency }}
              </p>
              <p class="text-xs text-gray-500">
                {{ p.created_at }}
              </p>
            </div>
          </div>
        </RouterLink>
        <div class="flex gap-2">
          <RouterLink
            :to="{ name: 'shop-update-product', params: { pk: p.id } }"
            class="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 rounded transition-colors"
          >
            Редагувати
          </RouterLink>
          <RouterLink
            :to="{ name: 'shop-delete-product', params: { pk: p.id } }"
            class="flex-1 text-center bg-red-600 hover:bg-red-700 text-white text-sm font-medium py-2 rounded transition-colors"
          >
            Видалити
          </RouterLink>
        </div>
      </div>
    </div>

    <p v-else class="text-center font-semibold text-lg italic py-12 text-gray-700">
      У вас ще немає товарів.
      <RouterLink :to="{ name: 'shop-create-product' }" class="text-blue-600 underline hover:opacity-80 ml-1">
        Додайте перший!
      </RouterLink>
    </p>

    <nav v-if="totalPages > 1" class="flex items-center justify-center gap-3 my-4">
      <button :disabled="!hasPrevious" @click="goToPage(page - 1)" class="px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-100 text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
        &laquo; Попередня
      </button>
      <span class="px-2 text-gray-700 font-medium">Сторінка {{ page }} з {{ totalPages }}</span>
      <button :disabled="!hasNext" @click="goToPage(page + 1)" class="px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-100 text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
        Наступна &raquo;
      </button>
    </nav>

    <div class="text-center pt-4">
      <RouterLink :to="{ name: 'shop-index' }" class="text-blue-600 hover:underline font-medium">
        ← Назад до всіх товарів
      </RouterLink>
    </div>
  </main>
</template>