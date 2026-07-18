import { ref } from 'vue'
import { searchCountries, searchCities } from '@/modules/geo/api/geo'

export function useGeoAutocomplete(type, countryIdGetter = null) {
  const query = ref('')
  const results = ref([])
  const selected = ref(null)
  const isOpen = ref(false)
  let debounceTimer = null

  async function fetchResults() {
    const q = query.value.trim()
    try {
      if (type === 'city') {
        const countryId = countryIdGetter ? countryIdGetter() : null
        if (!countryId) { results.value = []; return }
        const { data } = await searchCities(countryId, q)
        results.value = Array.isArray(data) ? data : (data?.results ?? [])
      } else {
        const { data } = await searchCountries(q)
        results.value = Array.isArray(data) ? data : (data?.results ?? [])
      }
    } catch (e) {
      console.error(`Помилка автокомпліту (${type}):`, e)
      results.value = []
    }
  }

  function onInput() {
    selected.value = null
    isOpen.value = true
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(fetchResults, 250)
  }

  function onFocus() {
    isOpen.value = true
    if (!results.value.length) fetchResults()
  }

  function onBlur() {
    setTimeout(() => { isOpen.value = false }, 150)
  }

  function select(item) {
    selected.value = item
    query.value = item.name ?? item.city ?? ''
    results.value = []
    isOpen.value = false
  }

  function clear() {
    query.value = ''
    selected.value = null
    results.value = []
    isOpen.value = false
  }

  return { query, results, selected, isOpen, onInput, onFocus, onBlur, select, clear }
}