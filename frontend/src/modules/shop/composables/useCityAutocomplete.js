// modules/shop/composables/useCityAutocomplete.js
import { ref, reactive } from 'vue'
import { searchCities } from '@/modules/geo/api/geo'
import { useToast } from '@/shared/composables/useToast'

const DEBOUNCE_MS = 250

/**
 * Автокомплит міста. Завжди прив'язаний до обраної країни — без countryId
 * пошук не виконується (як і в оригінальному create_product.js / update_product.js).
 *
 * @param {{ id?: number|string, name?: string }} initial
 * @param {import('vue').Ref<string|number>} countryIdRef
 */
export function useCityAutocomplete(initial = {}, countryIdRef) {
  const { showToast } = useToast()

  const query = ref(initial.name || '')
  const cityId = ref(initial.id || '')
  const suggestions = ref([])
  const isOpen = ref(false)
  const isLoading = ref(false)

  let debounceTimer = null

  async function fetchAndShow(q) {
    isLoading.value = true
    try {
      suggestions.value = await searchCities(q, countryIdRef.value)
      isOpen.value = suggestions.value.length > 0
    } finally {
      isLoading.value = false
    }
  }

  function onInput(value) {
    query.value = value
    cityId.value = ''

    if (!countryIdRef.value) {
      showToast('Спочатку оберіть країну', 'warning')
      return
    }

    clearTimeout(debounceTimer)
    if (!value.trim()) {
      suggestions.value = []
      isOpen.value = false
      return
    }
    debounceTimer = setTimeout(() => fetchAndShow(value.trim()), DEBOUNCE_MS)
  }

  function onFocus() {
    if (suggestions.value.length) isOpen.value = true
  }

  function select(city) {
    query.value = city.city ?? city.name
    cityId.value = city.id ?? ''
    isOpen.value = false
  }

  function close() {
    isOpen.value = false
  }

  /** Сбросить город — вызывается при смене страны. */
  function reset() {
    query.value = ''
    cityId.value = ''
    suggestions.value = []
    isOpen.value = false
  }

  return reactive({
    query,
    cityId,
    suggestions,
    isOpen,
    isLoading,
    onInput,
    onFocus,
    select,
    close,
    reset,
  })
}