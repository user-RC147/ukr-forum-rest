<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: { type: Object, required: true },
})

// DRF может вернуть images как строку (первый URL) или массив объектов
const imageUrl = computed(() => {
  const img = props.product.images
  if (!img) return null
  if (typeof img === 'string') return img
  if (Array.isArray(img) && img.length) return img[0]?.url ?? img[0]?.image ?? null
  return null
})

const currency = computed(() => {
  const c = props.product.country
  return c?.currency_symbol || c?.currency || ''
})

const location = computed(() => {
  const { city, region, country } = props.product
  if (city?.name && region?.name) return `${city.name}, ${region.name}`
  if (region?.name)               return region.name
  return 'Адреса не вказана'
})

const displayDate = computed(() =>
  props.product.date_update || props.product.date || ''
)
</script>

<template>
  <router-link
    :to="{
      name: 'shop-product',
      params: {
        categorySlug: product.category?.slug,
        pk:           product.id,
        productSlug:  product.slug,
      },
    }"
    class="block group"
  >
    <div class="bg-white border border-gray-100 rounded-2xl shadow-sm
                hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col h-full">

      <!-- Фото -->
      <div class="overflow-hidden bg-gray-50">
        <img
          v-if="imageUrl"
          :src="imageUrl"
          :alt="product.name"
          class="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        <div v-else class="w-full h-40 flex items-center justify-center">
          <svg class="w-12 h-12 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
      </div>

      <!-- Текст -->
      <div class="p-3 flex flex-col flex-1">
        <h3 class="text-sm font-medium text-gray-800 line-clamp-2 leading-snug mb-2 group-hover:text-blue-600 transition-colors duration-200">
          {{ product.name }}
        </h3>
        <p class="font-bold text-gray-900 mt-auto text-sm">
          {{ product.price }} {{ currency }}
        </p>
        <p class="text-xs text-gray-400 mt-1 truncate">
          {{ location }} · {{ displayDate }}
        </p>
      </div>

    </div>
  </router-link>
</template>