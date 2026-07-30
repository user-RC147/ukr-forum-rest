//usePurchaseItem.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getPurchaseItems } from '../api/purchase_items';

export const usePurchaseItemStore = defineStore('purchaseItem', () => {
    const purchaseItems = ref([]);
    const paginator = ref(null);
    const loading = ref(false);
    const error = ref(null);

    async function fetchPurchaseItems(page = 1, page_size = 5, date_from, date_to) {
        loading.value=true;
        error.value=null;
        try{
            const response = await getPurchaseItems(page,page_size,date_from, date_to);
            // тут треба зберегти дані
            purchaseItems.value = response.data.results;
            paginator.value = response.data.paginator;

        } catch (e) {
            error.value = 'Помилка завантаження покупок';
        } finally {
            loading.value = false;
        }        
    }

    return {purchaseItems,paginator,loading,error,fetchPurchaseItems};

});
