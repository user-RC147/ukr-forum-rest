import api from '@/api/axios' // Використовуємо єдиний налаштований клієнт

/**
 * Отримати список усіх товарів домашнього господарства.
 * Django URL: GET /api/v1/household/products/
 * @returns {Promise}
 */
export function getProducts() {
  return api.get('/household/products/')
}

/**
 * Створити новий товар.
 * Django URL: POST /api/v1/household/products/
 * @param {Object} data - Об'єкт із даними товару (наприклад: { name: 'Молоко', category_id: 2 })
 * @returns {Promise}
 */
export function createProduct(data) {
  return api.post('/household/products/', data)
}

/**
 * Оновити дані існуючого товару (повне або часткове оновлення).
 * Django URL: PATCH /api/v1/household/products/{id}/
 * @param {number|string} id - Ідентифікатор товару в базі даних (pk)
 * @param {Object} data - Об'єкт із оновленими полями товару
 * @returns {Promise}
 */
export function updateProduct(id, data) {
  return api.patch(`/household/products/${id}/`, data)
}

/**
 * Видалити товар із бази даних.
 * Django URL: DELETE /api/v1/household/products/{id}/
 * @param {number|string} id - Ідентифікатор товару для видалення (pk)
 * @returns {Promise}
 */
export function deleteProduct(id) {
  return api.delete(`/household/products/${id}/`)
}