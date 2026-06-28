import api from '@/api/axios.js'
import apiClient from '@/api/axios'
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

/**
 * Список категорий для select'а в форме товара.
 * Аналог Django context-переменной {{ Category }}.
 */
export async function getCategories() {
  const { data } = await apiClient.get('/search/category/')
  return data?.results ?? data ?? []
}
 
/**
 * Создать товар.
 * @param {FormData} formData — поля + images[] (File[])
 */
export async function createProduct(formData) {
  const { data } = await apiClient.post('/shop/products/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
 
/**
 * Обновить товар.
 * @param {number|string} id
 * @param {FormData} formData — поля + новые images[] + deleted_images (JSON-строка id'шников)
 */
export async function updateProduct(id, formData) {
  const { data } = await apiClient.patch(`/shop/products/${id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
 
/**
 * Удалить товар целиком.
 * Используется на отдельном экране подтверждения удаления (delete_product.html),
 * а не модалкой — сохраняем оригинальную архитектуру отдельного route/view.
 */
export async function deleteProduct(id) {
  await apiClient.delete(`/shop/products/${id}/`)
}
 
export default { getCategories, createProduct, updateProduct, deleteProduct }

// POST /api/moderation/complaints/ — жалоба на товар
export const createComplaint = (productId) =>
  api.post('moderation/complaints/', {
    app_label: 'shop',
    model_name: 'product',
    object_id: productId,
  })