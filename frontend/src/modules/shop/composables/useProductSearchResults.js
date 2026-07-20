import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { searchProducts } from '../api/shop'

export function useProductSearchResults() {
  const route = useRoute()
  const rawResults = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const hasNext = ref(false)
  const page = ref(Number(route.query.page) || 1)

  const products = computed(() =>
    rawResults.value.map((item) => ({
      id: item.id,
      title: item.title,
      description: item.description,
      price: item.meta?.price,
      image: item.meta?.files?.[0]?.file ?? null,
      createdAt: item.meta?.created_at,
      city: item.meta?.city?.name_ua ?? item.meta?.city?.name,
      region: item.meta?.region?.name_ua ?? item.meta?.region?.name,
      country: item.meta?.country?.name_ua ?? item.meta?.country?.name,
      currency: item.meta?.country?.currency,
    }))
  )

  function buildParams(query) {
    // Map frontend filter values to backend expected params
    // Backend expects `sort` to be one of: "newest", "oldest", "relevance"
    const params = { page: Number(query.page) || 1 }
    if (query.q) params.q = query.q
    if (query.category_id) params.category_id = query.category_id
    if (query.country_id) params.country_id = query.country_id
    if (query.city_id) params.city_id = query.city_id
    if (query.radius && query.city_id) params.radius = query.radius
    if (query.status) params.status = query.status
    // date_sort values: 'date' (new first), '-date' (old first),
    // '' (relevance — дефолт, radio "За релевантністю")
    // Для relevance параметр sort не відправляємо взагалі — бекенд сам
    // рахує релевантність, коли явного sort немає.
    const dateSort = query.date_sort || ''
    if (dateSort === 'date') {
      params.sort = 'newest'
    } else if (dateSort === '-date') {
      params.sort = 'oldest'
    }
    return params
  }

  // requestToken защищает от гонки: если старый (медленный) запрос
  // ответит позже нового — его результат просто игнорируется
  let requestToken = 0
  async function fetchProducts(query) {
    const token = ++requestToken
    isLoading.value = true
    error.value = null
    try {
      const params = buildParams(query)
      const { data } = await searchProducts(params)
      if (token !== requestToken) return
      rawResults.value = data?.results ?? (Array.isArray(data) ? data : [])
      hasNext.value = rawResults.value.length >= 20
      page.value = Number(query.page) || 1
    } catch (e) {
      if (token !== requestToken) return
      error.value = 'Не вдалося завантажити оголошення'
      console.error(e)
    } finally {
      if (token === requestToken) isLoading.value = false
    }
  }

  // Единственный источник правды — route.query. Работает и при первом
  // заходе (immediate), и при повторной навигации на этот же роут
  // (клик по категории, смена страницы пагинации и т.д.)
  watch(() => route.query, fetchProducts, { immediate: true })

  return { products, isLoading, error, hasNext, page }
}