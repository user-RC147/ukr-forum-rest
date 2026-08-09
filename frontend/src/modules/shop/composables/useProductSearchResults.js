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
    rawResults.value.map((item) => {
      // Берём первый видимый файл; thumbnail если готов, иначе полный файл
      const firstVisible = item.meta?.files?.find((f) => f.visible !== false)
      return {
        id: item.id,
        title: item.title,
        description: item.description,
        price: item.meta?.price,
        image: firstVisible?.thumbnail ?? firstVisible?.file ?? null,
        createdAt: item.meta?.created_at,
        city: item.meta?.city?.name_ua ?? item.meta?.city?.name,
        region: item.meta?.region?.name_ua ?? item.meta?.region?.name,
        country: item.meta?.country?.name_ua ?? item.meta?.country?.name,
        currency: item.meta?.country?.currency,
      }
    })
  )

  function buildParams(query) {
    const params = { page: Number(query.page) || 1 }
    if (query.q) params.q = query.q
    if (query.category_id) params.category_id = query.category_id
    if (query.country_id) params.country_id = query.country_id
    if (query.city_id) params.city_id = query.city_id
    if (query.radius && query.city_id) params.radius = query.radius
    if (query.status) params.status = query.status
    const dateSort = query.date_sort || ''
    if (dateSort === 'date') params.sort = 'newest'
    else if (dateSort === '-date') params.sort = 'oldest'
    return params
  }

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

  watch(() => route.query, fetchProducts, { immediate: true })

  return { products, isLoading, error, page, totalPages, count, hasNext, hasPrevious }
}