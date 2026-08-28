import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/shared/stores/useUserStore'

export const RADII = [10, 25, 50, 100, 200]

function readUserLocationValue(userStore, key) {
  if (!userStore?.isAuthenticated || !userStore?.user) return ''

  const nested = userStore.user.location || {}
  const locationMap = {
    country_id: nested.country?.id ?? userStore.user.country_id ?? '',
    country_name: nested.country?.name_ua || nested.country?.name || userStore.user.country_name || '',
    city_id: nested.city?.id ?? userStore.user.city_id ?? '',
    city_name: nested.city?.name_ua || nested.city?.name || userStore.user.city_name || '',
  }

  const value = locationMap[key]
  return value == null || value === '' ? '' : value
}

function buildFilters(query, userStore) {
  return {
    q: query.q || '',
    category_id: query.category_id || '',
    country_id: query.country_id || readUserLocationValue(userStore, 'country_id'),
    country_name: query.country_name || readUserLocationValue(userStore, 'country_name'),
    city_id: query.city_id || readUserLocationValue(userStore, 'city_id'),
    city_name: query.city_name || readUserLocationValue(userStore, 'city_name'),
    radius: query.radius || '',
    status: query.status || '',
    date_sort: query.date_sort || '',
  }
}

const FILTER_KEYS = [
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

const sharedFilters = reactive({
  q: '',
  category_id: '',
  country_id: '',
  country_name: '',
  city_id: '',
  city_name: '',
  radius: '',
  status: '',
  date_sort: '',
})

let isInitialized = false

const DEFAULTS = { date_sort: '' }

function hasFilterQuery(query) {
  return FILTER_KEYS.some((key) => query[key] != null && query[key] !== '')
}

export function useSearchFilters() {
  const route = useRoute()
  const router = useRouter()
  const userStore = useUserStore()
  if (route.name === 'shop-search' && hasFilterQuery(route.query)) {
    Object.assign(sharedFilters, buildFilters(route.query, userStore))
    isInitialized = true
  } else if (!isInitialized) {
    Object.assign(sharedFilters, buildFilters(route.query, userStore))
    isInitialized = true
  }
  watch(
    () => route.query,
    (newQuery) => {
      if (route.name === 'shop-search' && hasFilterQuery(newQuery)) {
        Object.assign(sharedFilters, buildFilters(newQuery, userStore))
      }
    },
    { deep: true },
  )

  function buildQuery() {
    const query = {}
    Object.entries(sharedFilters).forEach(([key, value]) => {
      if (!FILTER_KEYS.includes(key)) return
      if (value !== '' && value != null && DEFAULTS[key] !== value) query[key] = value
    })
    return query
  }

  function applyFilters() {
    router.push({ name: 'shop-search', query: buildQuery() })
  }

  function resetFilters() {
    Object.assign(sharedFilters, buildFilters({}, null))
    if (route.name === 'shop-search') {
      router.push({ name: 'shop-search', query: {} })
    }
  }

  return { filters: sharedFilters, RADII, applyFilters, resetFilters }
}