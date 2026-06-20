// useProductStore.js
import { defineStore } from 'pinia'
import api from '@/api/axios.js'

export const useProductStore = defineStore('productStore', {
    
    // 1. Стан — що зберігає цей store
    state: () => ({
        products: [],      // список товарів (для пошуку потім)
        isLoading: false,  // індикатор завантаження
        error: null        // помилка якщо щось пішло не так
    }),

    actions: {
        // Створити новий товар в БД
        async createProduct(productData) {
            this.isLoading = true
            this.error = null
            try {
                // POST запит на Django ендпоінт
                const response = await api.post('/household/products/', productData)
                
                // Додаємо створений товар в локальний список
                this.products.push(response.data)
                
                // Повертаємо створений об'єкт — щоб компонент знав його id і назву
                return response.data
            } catch (err) {
                this.error = err.message || 'Не вдалося створити товар'
                console.error('Помилка createProduct:', err)
                throw err  // прокидаємо помилку далі у компонент
            } finally {
                // finally виконується ЗАВЖДИ — і при успіху і при помилці
                this.isLoading = false
            }
        }
    }
})