import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getMarkets, createMarket } from '../api/markets';

export const useMarketStore = defineStore('markets', () => {
    const markets = ref([]);
    const loading = ref(false);
    const error = ref(null);

    async function fetchMarkets() {
        loading.value = true;
        error.value = null;
        try {
            const response = await getMarkets();
            markets.value = response.data;
        } catch (e) {
            error.value = 'Помилка завантаження магазинів';
        } finally {
            loading.value = false;
        }
    }

    async function addMarket(marketData) {
        loading.value = true;
        try {
            const response = await createMarket(marketData);
            markets.value.push(response.data);
            return response.data;
        } catch (err) {
            console.log(err.response?.data);

            error.value = err.response?.data?.detail || 'Не вдалося створити магазин';
            throw err
        } finally {
            loading.value = false;
        }
    }

    return { markets, loading, error, fetchMarkets, addMarket };
});
