import { defineStore } from "pinia";
import { ref } from "vue";
import { getCategories } from "../api/categories";

export const useCategoryStore =defineStore('categories',()=>{
    const categories =ref([])
    const loading = ref(false)
    const error = ref(null)

    async function fetchCategories() {
        loading.value=true
        error.value=null
        try{
            const response = await getCategories()
            categories.value=response.data
        } catch (e) {
      error.value = 'Помилка завантаження категорій'
    } finally {
      loading.value = false
    }
        
    }



    return {categories,loading,error, fetchCategories}
})