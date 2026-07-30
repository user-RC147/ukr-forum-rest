import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { searchProducts } from '../api/shop'

export function useProductSearchResults() {
  const route = useRoute()
  const rawResults = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const page = ref(Number(route.query.page) || 1)
  const totalPages = ref(1)
  const count = ref(0)
  const hasNext = ref(false)
  const hasPrevious = ref(false)

  const products = computed(() =>
    rawResults.value.map((item) => ({
      id: item.id,
      title: item.title,
      description: item.description,
      price: item.meta?.price,
      // files теперь массив объектов {id, file, visible}, а не строк —
      // достаём url первого файла так же, как и раньше
      image: item.meta?.files?.[0]?.file ?? null,
      createdAt: item.meta?.created_at,
      city: item.meta?.city?.name_ua ?? item.meta?.city?.name,
      region: item.meta?.region?.name_ua ?? item.meta?.region?.name,
      country: item.meta?.country?.name_ua ?? item.meta?.country?.name,
      currency: item.meta?.country?.currency,
    }))
  )

  function buildParams(query) {
    const params = { page: Number(query.page) || 1 }
    if (query.q) params.q = query.q
    if (query.category_id) params.category_id = query.category_id
    if (query.country_id) params.country_id = query.country_id
    if (query.city_id) params.city_id = query.city_id
    if (query.radius && query.city_id) params.radius = query.radius
    if (query.status) params.status = query.status
    // date_sort: 'date' (нові) / '-date' (старі) / '' (релевантність — sort не шлемо)
    const dateSort = query.date_sort || ''
    if (dateSort === 'date') params.sort = 'newest'
    else if (dateSort === '-date') params.sort = 'oldest'
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
      const requestedPage = Number(query.page) || 1
      const params = buildParams(query)
      const { data } = await searchProducts(params)
      if (token !== requestToken) return

      // ВАЖНО: у /search/list_shop/ пагинация вложена в data.results,
      // а не в корень ответа (в отличие от /shop/products/)
      const pageData = data?.results ?? {}
      rawResults.value = pageData.items ?? []
      page.value = pageData.page ?? requestedPage
      totalPages.value = pageData.total_pages ?? 1
      count.value = pageData.count ?? rawResults.value.length
      hasNext.value = pageData.has_next ?? false
      hasPrevious.value = pageData.has_previous ?? false
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
  watch(() => route.query, fetchProducts, { immediate: true })

  return { products, isLoading, error, page, totalPages, count, hasNext, hasPrevious }
}