<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '@/shared/composables/useToast'
import { useProductGallery } from '../composables/useProductGallery'
import { getProductDetail, deleteProduct, createComplaint } from '../api/shop.js'

const route = useRoute()
const { error: showError, success: showSuccess } = useToast()

const product = ref(null)
const loading = ref(true)
const error = ref(null)
const galleryImages = computed(() => product.value?.files ?? [])
const gallery = useProductGallery(galleryImages)

onMounted(async () => {
  try {
    const response = await getProductDetail(route.params.pk)
    product.value = response.data
  } catch (err) {
    error.value = 'Не вдалося завантажити товар'
    showError('Помилка завантаження товару')
  } finally {
    loading.value = false
  }
})

const handleDelete = async () => {
  if (!confirm('Ви впевнені? Це неможливо скасувати.')) return
  
  try {
    await deleteProduct(product.value.id)
    showSuccess('Товар видалено')
    // Редирект на shop
    window.location.href = '/shop'
  } catch (err) {
    showError('Помилка при видаленні')
  }
}

const handleComplaint = async () => {
  try {
    await createComplaint(product.value.id)
    showSuccess('Скарга відправлена')
  } catch (err) {
    showError('Помилка при відправці скарги')
  }
}

const isOwner = computed(() => {
  // TODO: порівняти з currentUser з store
  return false
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-20">
      <p>Завантаження...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded p-4 text-red-600">
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="product" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Галерея -->
      <div class="lg:col-span-2">
        <div class="bg-gray-100 rounded-lg overflow-hidden mb-4">
          <img 
            v-if="product.files?.length"
            :src="product.files[gallery.currentIndex.value].file"
            :alt="product.title"
            class="w-full h-96 object-cover"
          />
          <div v-else class="w-full h-96 flex items-center justify-center">
            <span class="text-gray-500">Нет фото</span>
          </div>
        </div>

        <!-- Миниатюры -->
        <div v-if="product.files?.length > 1" class="flex gap-2">
          <button
            v-for="(file, idx) in product.files"
            :key="idx"
            @click="gallery.show(idx)"
            :class="[
              'h-20 w-20 rounded border-2 overflow-hidden',
              gallery.isActive(idx) ? 'border-blue-500' : 'border-gray-300'
            ]"
          >
            <img :src="file.file" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>

      <!-- Деталь -->
      <div>
        <h1 class="text-3xl font-bold mb-4">{{ product.title }}</h1>
        <p class="text-3xl font-bold text-blue-600 mb-6">{{ product.price }} ₴</p>
        
        <div class="space-y-6 mb-8">
          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Описание</h3>
            <p class="text-gray-600 whitespace-pre-wrap">{{ product.description }}</p>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Локація</h3>
            <p class="text-gray-600">
              📍 {{ product.city?.name }}, {{ product.region?.name }}
            </p>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Дата</h3>
            <p class="text-gray-600">{{ product.created_at }}</p>
          </div>
        </div>

        <!-- Кнопки -->
        <div class="space-y-3">
          <button class="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 font-medium">
            Написати продавцю
          </button>
          
          <button 
            v-if="isOwner"
            @click="handleDelete"
            class="w-full bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 text-sm"
          >
            Видалити товар
          </button>
          
          <button 
            v-if="!isOwner"
            @click="handleComplaint"
            class="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 text-sm"
          >
            Поскаржитись на товар
          </button>
        </div>
      </div>
    </div>
  </div>
</template>