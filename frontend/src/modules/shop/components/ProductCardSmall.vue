<script setup>
import { computed } from 'vue'
import { getProductThumbnailUrl } from '@/shared/utils/media'
import { formatAddress } from '../utils/location'

const props = defineProps({
  product: { type: Object, required: true },
})

const imageUrl = computed(() => getProductThumbnailUrl(props.product))

const currency = computed(() => {
  const c = props.product.country
  return c?.currency_symbol || c?.currency || '₴'
})

const location = computed(() => {
  return formatAddress(props.product)
})

const displayDate = computed(() => {
  return props.product.created_at || ''
})
</script>



<template>
  <router-link
    :to="{
      name: 'shop-product',
      params: { pk: product.id },
    }"
    class="block group"
  >
    <div class="bg-white border border-gray-100 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col h-full">

      <div class="overflow-hidden bg-gray-50">
        <img
          v-if="imageUrl"
          :src="imageUrl"
          :alt="product.title"
          class="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        <div v-else class="w-full h-40 flex items-center justify-center bg-gray-100">
          <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
      </div>

      <div class="p-3 flex flex-col flex-1">
        <h3 class="text-sm font-medium text-gray-800 line-clamp-2 leading-snug mb-2 text-center group-hover:text-blue-600 transition-colors duration-200">
          {{ product.title }}
        </h3>
        <p class="font-bold text-gray-900 mt-auto text-sm text-center">
          {{ product.price }} {{ currency }}
        </p>
        <p class="text-xs text-gray-400 mt-1 truncate text-center" :title="location">
          {{ location }}
        </p>
        <p v-if="displayDate" class="text-xs text-gray-400 truncate text-center" :title="displayDate">
          {{ displayDate }}
        </p>
      </div>

    </div>
  </router-link>
</template>