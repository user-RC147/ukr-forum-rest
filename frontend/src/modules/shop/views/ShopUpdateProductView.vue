<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import ProductForm from '@/modules/shop/components/ProductForm.vue'
import { getProductDetail } from '@/modules/shop/api/shop'
import { useToast } from '@/shared/composables/useToast'

const route = useRoute()
const { error: showError } = useToast()

const product = ref(null)
const isLoading = ref(true)
const loadError = ref(false)

async function loadProduct(pk) {
  isLoading.value = true
  loadError.value = false
  product.value = null
  try {
    const response = await getProductDetail(pk)
    product.value = response.data
  } catch {
    loadError.value = true
    showError('Не вдалося завантажити товар')
  } finally {
    isLoading.value = false
  }
}

watch(() => route.params.pk, (pk) => { if (pk) loadProduct(pk) }, { immediate: true })
</script>

<template>
  <main class="px-4 py-6">
    <div v-if="isLoading" class="mx-auto max-w-6xl animate-pulse rounded-2xl bg-white p-10 shadow-lg">
      <div class="mb-6 h-8 w-64 rounded bg-gray-200"></div>
      <div class="mb-4 h-12 rounded bg-gray-100"></div>
      <div class="mb-4 h-12 rounded bg-gray-100"></div>
      <div class="h-32 rounded bg-gray-100"></div>
    </div>

    <p v-else-if="loadError" class="mx-auto max-w-6xl rounded-2xl bg-white p-10 text-center text-red-500 shadow-lg">
      Товар не знайдено або сталася помилка завантаження.
    </p>

    <ProductForm v-else mode="update" :product="product" />
  </main>
</template>