import api from '@/api/axios.js'

/**
 * Все эндпоинты модуля "shop" (объявления/товары).
 * Компоненты работают через эти функции, не напрямую с axios.
 */

// GET /api/shop/products/ — список товаров
export const getLatestProducts = (params = {}) =>
  api.get('shop/products/', { params })

// GET /api/shop/products/{id}/ — один товар
export const getProductDetail = (id) =>
  api.get(`shop/products/${id}/`)

// POST /api/shop/products/ — создание товара
export const createProduct = (data) => {
  const formData = new FormData()
  formData.append('title', data.title)
  formData.append('description', data.description)
  formData.append('price', data.price)
  formData.append('country_id', data.country_id)
  formData.append('region_id', data.region_id)
  formData.append('city_id', data.city_id)
  
  if (data.files && Array.isArray(data.files)) {
    data.files.forEach((file) => formData.append('files', file))
  }
  
  return api.post('shop/products/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// PATCH /api/shop/products/{id}/ — редактирование товара
export const updateProduct = (id, data) => {
  const formData = new FormData()
  formData.append('title', data.title)
  formData.append('description', data.description)
  formData.append('price', data.price)
  formData.append('country_id', data.country_id)
  formData.append('region_id', data.region_id)
  formData.append('city_id', data.city_id)
  
  if (data.files && Array.isArray(data.files)) {
    data.files.forEach((file) => formData.append('files', file))
  }
  
  return api.patch(`shop/products/${id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// DELETE /api/shop/products/{id}/ — удаление товара
export const deleteProduct = (id) =>
  api.delete(`shop/products/${id}/`)

// POST /api/moderation/complaints/ — жалоба на товар
export const createComplaint = (productId) =>
  api.post('moderation/complaints/', {
    app_label: 'shop',
    model_name: 'product',
    object_id: productId,
  })