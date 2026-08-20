import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/shared/stores/useUserStore'

export const RADII = [10, 25, 50, 100, 200]

function buildFilters(query, userStore) {
  return {
    q: query.q || '',
    category_id: query.category_id || '',
    country_id: query.country_id || userStore?.user?.country_id || '',
    country_name: query.country_name || userStore?.user?.country_name || '',
    city_id: query.city_id || userStore?.user?.city_id || '',
    city_name: query.city_name || userStore?.user?.city_name || '',
    radius: query.radius || '',
    status: query.status || '',
    date_sort: query.date_sort || '',
  }
}

const DEFAULTS = { date_sort: '' }

export function useSearchFilters() {
  const route = useRoute()
  const router = useRouter()
  const userStore = useUserStore()

  const filters = reactive(buildFilters(route.query, userStore))

  // Следим за изменениями URL параметров и обновляем фильтры
  watch(
    () => route.query,
    (newQuery) => {
      Object.assign(filters, buildFilters(newQuery, userStore))
    },
    { deep: true },
  )

  function buildQuery() {
    const query = {}
    const allowedKeys = [
      'q',
      'category_id',
      'country_id',
      'country_name',
      'city_id',
      'city_name',
      'radius',
      'status',
      'date_sort',
    ]

    Object.entries(filters).forEach(([key, value]) => {
      if (!allowedKeys.includes(key)) return
      if (value !== '' && value != null && DEFAULTS[key] !== value) query[key] = value
    })
    return query
  }

  function applyFilters() {
    router.push({ name: 'shop-search', query: buildQuery() })
  }

  function resetFilters() {
    Object.assign(filters, buildFilters({}, null))
    if (route.name === 'shop-search') {
      router.push({ name: 'shop-search', query: {} })
    }
  }

  return { filters, RADII, applyFilters, resetFilters }
}