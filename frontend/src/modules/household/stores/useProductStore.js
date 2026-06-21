import { defineStore } from 'pinia'
import { 
  getProducts, 
  createProduct, 
  updateProduct, 
  deleteProduct 
} from '../api/products'

/**
 * Сховище для керування списком товарів у модулі Household.
 */
export const useProductStore = defineStore('product', {
  state: () => ({
    // Реактивний масив товарів, який читають компоненти Vue
    products: [],
    
    // Стани для відстеження процесу мережевих запитів
    loading: false,
    error: null,
  }),

  getters: {
    /**
     * Пошук товару в пам'яті за його ID (pk).
     * Дозволяє не робити повторний запит до Django, якщо товар уже завантажений.
     */
    getProductById: (state) => (id) => {
      return state.products.find(product => product.id === id)
    },
    
    /**
     * Геттер для підрахунку загальної кількості товарів у базі.
     */
    totalProducts: (state) => state.products.length,
  },

  actions: {
    /**
     * Завантажити всі товари з Django та записати їх у стор.
     */
    async fetchProducts() {
      this.loading = true
      this.error = null
      try {
        const response = await getProducts()
        this.products = response.data // Записуємо масив із бази даних
      } catch (err) {
        this.error = err.response?.data?.detail || 'Не вдалося завантажити товари'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Створити новий товар та локально додати його в масив.
     */
    async addProduct(productData) {
      this.loading = true
      try {
        const response = await createProduct(productData)
        // Django повертає створений об'єкт із правильним ID з PostgreSQL.
        // Додаємо його в кінець масиву — Vue автоматично перемалює екран.
        this.products.push(response.data)
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Не вдалося створити товар'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Оновити товар на бекенді та локально замінити його дані в сторі.
     */
    async editProduct(id, updatedData) {
      this.loading = true
      try {
        const response = await updateProduct(id, updatedData)
        // Знаходимо індекс старого товару в нашому масиві
        const index = this.products.findIndex(p => p.id === id)
        if (index !== -1) {
          // Замінюємо старий об'єкт оновленим від Django
          this.products[index] = response.data
        }
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Не вдалося оновити товар'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Видалити товар із Django та локально відфільтрувати стор.
     */
    async removeProduct(id) {
      this.loading = true
      try {
        await deleteProduct(id)
        // Використовуємо .filter(), щоб викинути видалений товар з пам'яті фронтенду
        this.products = this.products.filter(p => p.id !== id)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Не вдалося видалити товар'
        throw err
      } finally {
        this.loading = false
      }
    },
  },
});
