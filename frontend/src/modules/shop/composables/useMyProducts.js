import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getLatestProducts } from '../api/shop'

/**
 * Пагінований список товарів поточного користувача.
 * @param {() => number|string|undefined} getUserId — геттер id користувача
 *   (передаємо функцію, а не значення, щоб завжди читати актуальний userStore.user.id)
 */
export function useMyProducts(getUserId) {
  const route = useRoute()
  const router = useRouter()

  const products = ref([])
  const isLoading = ref(true)
  const error = ref(null)

  const page = ref(Number(route.query.page) || 1)
  const totalPages = ref(1)
  const count = ref(0)
  const hasNext = ref(false)
  const hasPrevious = ref(false)

  let requestToken = 0
  async function fetchProducts(requestedPage) {
    const userId = getUserId()
    if (!userId) return

    const token = ++requestToken
    isLoading.value = true
    error.value = null
    try {
      // Фільтрація по user_id на бекенді — не тягнемо чужі товари
      const { data } = await getLatestProducts({ user_id: userId, page: requestedPage })
      if (token !== requestToken) return
      products.value = data?.items ?? []
      page.value = data?.page ?? requestedPage
      totalPages.value = data?.total_pages ?? 1
      count.value = data?.count ?? products.value.length
      hasNext.value = data?.has_next ?? false
      hasPrevious.value = data?.has_previous ?? false
    } catch (e) {
      if (token !== requestToken) return
      error.value = 'Не вдалося завантажити ваші товари'
      console.error(e)
    } finally {
      if (token === requestToken) isLoading.value = false
    }
  }

  function goToPage(p) {
    router.push({ query: { ...route.query, page: p } })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // immediate: true — сработает и при первом заходе на роут, и при
  // повторной навигации (Vue Router переиспользует компонент)
  watch(() => Number(route.query.page) || 1, (p) => fetchProducts(p), { immediate: true })

  return { products, isLoading, error, page, totalPages, count, hasNext, hasPrevious, goToPage }
}