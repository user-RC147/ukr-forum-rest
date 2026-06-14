import {defineStore} from 'pinia'
import {ref} from 'vue'
import { getAssets, createAsset } from '../api/assets.js'

export const useAssetStore = defineStore('assets',()=>{
     // список активів
     const assets=ref([])
     const loading=ref(false)
     const error=ref(null)

    // завантажити всі активи
    async function fetchAssets(group_id=null){
        // Перевірку "if (!group_id)" видалено, бо тепер пустий group_id — це легальний запит
        loading.value=true
        error.value=null
        try{
            const response=await getAssets(group_id)

            // Оскільки бекенд тепер повертає об'єкт { results: [...] },
            // зберігаємо у стор саме масив результатів (results)
            assets.value=response.data.results || response.data
        }catch (e){
              error.value = 'Помилка завантаження активів'
        } finally {
            loading.value = false
        }
    }

    // створити новий актив
    async function addAsset(data){
        const response=await createAsset(data)
        assets.value.push(response.data)
        return response.data
    }

    return {assets,loading, error, fetchAssets,addAsset}

})