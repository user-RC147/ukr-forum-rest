import { defineStore } from "pinia";
import { ref } from "vue";
import { getMarketExpenses } from "../api/market_expenses";


export const useMarketExpensesStore=defineStore('marketExpenses', () =>{
    const marketExpenses =ref([]);
    const paginator =ref(null);
    const loading =ref(false);
    const error = ref(null);

    async function fetchMarketExpenses(page=1,page_size=3,date_from,date_to){
        loading.value =true;
        error.value=null;

        try{
            const response = await getMarketExpenses(page,page_size,date_from,date_to);

            marketExpenses.value=response.data.results;
            paginator.value = response.data.paginator;
        }catch (e) {
            error.value = 'Помилка завантаження витрат по магазинам';
        } finally {
            loading.value = false;
        }    
    }
    return {marketExpenses,paginator,loading,error,fetchMarketExpenses};
});