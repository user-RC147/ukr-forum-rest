//usePurchaseItem.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getPurchaseItems } from '../api/purchase_items';



export const usePurchaseItemStore = defineStore('purchaseItem', () => {
    const purchaseItem = ref([]);
    const loading = ref(false);
    const error = ref(null);
});
