import {defineStore} from 'pinia'
import {ref} from 'vue'
import { getAssets, createAsset } from '../api/assets.js'

export const useAssetStore = defineStore('assets',()=>{
     // список активів
     const assets=ref([])
     const loading=ref(false)
     const error=ref(null)

    // завантажити всі активи
    async function fetchAssets(){
        loading.value=true
        error.value=null
        try{
            const response=await getAssets()
            assets.value=response.data
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