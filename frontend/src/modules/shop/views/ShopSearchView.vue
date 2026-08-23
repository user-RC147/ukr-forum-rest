<script setup>
import { useProductSearchResults } from '../composables/useProductSearchResults'
import SearchFiltersBar from '../components/SearchFiltersBar.vue'
import { useRoute, useRouter } from 'vue-router'
import { formatAddress } from '../utils/location'

const route = useRoute()
const router = useRouter()
const { products, isLoading, error, page, totalPages, hasNext, hasPrevious } =
  useProductSearchResults()

function goToPage(p) {
  router.push({ name: 'shop-search', query: { ...route.query, page: p } })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-8">
    <SearchFiltersBar />

    <div v-if="isLoading" class="space-y-3">
      <div v-for="n in 5" :key="n" class="h-32 rounded-md bg-gray-100 animate-pulse"></div>
    </div>

    <p v-else-if="error" class="text-center text-red-600 py-10">{{ error }}</p>

    <div v-else-if="products.length" class="space-y-4">
      <RouterLink
        v-for="p in products" :key="p.id"
        :to="{ name: 'shop-product', params: { pk: p.id } }"
        class="bg-white flex flex-col sm:flex-row border rounded-md overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-200"
      >
        <div class="relative w-full sm:w-48 h-48 sm:h-44 flex-shrink-0 bg-gray-100">
          <img v-if="p.image" :src="p.image" :alt="p.title" class="w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="flex flex-col flex-grow p-4 sm:py-3 min-w-0 justify-between">
          <h3 class="font-semibold text-base sm:text-lg mb-1.5 line-clamp-2">{{ p.title }}</h3>
          <p class="text-xs sm:text-sm text-gray-600 line-clamp-1">
            {{ formatAddress(p, true) }}<span v-if="p.createdAt"> • {{ p.createdAt }}</span>
          </p>
        </div>
        <div class="flex flex-row sm:flex-col items-center sm:items-end justify-between sm:justify-center p-4 sm:py-3 gap-2 sm:min-w-[120px] border-t sm:border-t-0 sm:border-l border-gray-100">
          <p class="text-lg sm:text-xl font-bold text-gray-900">{{ p.price }} {{ p.currency }}</p>
        </div>
      </RouterLink>
    </div>

    <p v-else class="text-center font-semibold text-lg italic py-12 text-gray-700">
      За вашим запитом нічого не знайдено
    </p>

    <nav v-if="totalPages > 1" class="flex items-center justify-center gap-3 my-8">
      <button :disabled="!hasPrevious" @click="goToPage(page - 1)"
              class="cursor-pointer px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-100 text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
        &laquo; Попередня
      </button>
      <span class="px-2 text-gray-700 font-medium">Сторінка {{ page }} з {{ totalPages }}</span>
      <button :disabled="!hasNext" @click="goToPage(page + 1)"
              class="cursor-pointer px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-100 text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
        Наступна &raquo;
      </button>
    </nav>
  </main>
</template>