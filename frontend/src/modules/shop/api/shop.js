import api from '@/api/axios.js'

// Аналог Django view-функций, но только HTTP-слой — бизнес-логика в composables/stores
export const getCategories = () =>
  api.get('shop/categories/')

export const getLatestProducts = (params = {}) =>
  api.get('shop/products/', { params })