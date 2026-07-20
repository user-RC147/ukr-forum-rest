import { defineStore } from 'pinia';
import { getUnitsOfMeasure } from '../api/unit_of_measure';
import { ref } from 'vue';

/**
 * Сховище для керування одиницями виміру у модулі Household.
 */
export const useUnitOfMeasureStore = defineStore('unitOfMeasure', () => {
    const units = ref([]);
    const loading = ref(false);
    const error = ref(null);

    async function fetchUnitOfMeasures() {
        loading.value = true;
        error.value = null;

        try {
            const response = await getUnitsOfMeasure();
            units.value = response.data;
        } catch (e) {
            error.value = 'Помилка завантаження од.виміру';
        } finally {
            loading.value = false;
        }
    }

    return {units, loading, error, fetchUnitOfMeasures};
});
