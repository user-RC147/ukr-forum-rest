import { ref } from 'vue'
import { fetchCategories as fetchCategoriesApi } from '../api/shop'

const categories = ref([])
const isLoading = ref(false)
const error = ref(null)
let loadPromise = null

function load() {
  if (categories.value.length || loadPromise) return loadPromise
  isLoading.value = true
  error.value = null
  loadPromise = fetchCategoriesApi()
    .then(({ data }) => {
      categories.value = data?.results ?? data ?? []
    })
    .catch((e) => {
      error.value = 'Не вдалося завантажити категорії'
      console.error(e)
    })
    .finally(() => {
      isLoading.value = false
    })
  return loadPromise
}

export function useCategories() {
  return { categories, isLoading, error, load }
}