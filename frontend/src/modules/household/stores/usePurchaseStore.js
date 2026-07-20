import { defineStore } from 'pinia';
import { ref } from 'vue';
import { createPurchase as createPurchaseApi } from '../api/purchases'

export const usePurchaseStore = defineStore('purchase', () => {
    const purchases = ref([]);
    const loading = ref(false);
    const error = ref(null);

    async function createPurchase(purchaseData) {
        loading.value = true;
        error.value = null;
        try {
            const response = await createPurchaseApi(purchaseData);
            purchases.value.push(response.data);
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.detail || 'Не вдалося зберегти чек';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    return { purchases, loading, error, createPurchase };
});
