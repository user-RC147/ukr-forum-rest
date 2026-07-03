import {defineStore} from 'pinia';
import {getUnitsOfMeasure} from '../api/unit_of_measure';

/**
 * Сховище для керування одиницями виміру у модулі Household.
 */
export const useUnitOfMeasureStore = defineStore('unitOfMeasure', {
  state: () => ({
    // Реактивний масив одиниць виміру, який читають компоненти Vue
    unitsOfMeasure: [],
    
    // Стани для відстеження процесу мережевих запитів
    loading: false,
    error: null,
  }),
  
  getters: {
    /**
     * Пошук одиниці виміру в пам'яті за її ID (pk).
     * Дозволяє не робити повторний запит до Django, якщо одиниця уже завантажена.
     */
    getUnitOfMeasureById: (state) => (id) => {
      return state.unitsOfMeasure.find(unit => unit.id === id);
    },
  },

    actions: {
         /**
     * Завантажити всі товари з Django та записати їх у стор.
     */
    async fetchUnitsOfMeasure() {
        this.loading = true;
        this.error = null;
        try {
            const response = await getUnitsOfMeasure();
            this.unitsOfMeasure = response.data; // Записуємо масив із бази даних
        } catch (err) {
            this.error = err.response?.data?.detail || 'Не вдалося завантажити одиниці виміру';
            throw err;
        } finally {
            this.loading = false;
        }
    },

    },
});