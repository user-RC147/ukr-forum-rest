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
    // Фиксируем страну на момент запроса — если пользователь успеет
    // переключить страну пока летит запрос, устаревший ответ не применится.
    const requestedCountryId = countryIdRef.value
    isLoading.value = true
    try {
      const results = await searchCities(q, requestedCountryId)

      if (countryIdRef.value !== requestedCountryId) return

      // "Защита от дурака": даже если backend вдруг вернёт город не из
      // запрошенной країни — отфильтровываем его на фронте.
      suggestions.value = results.filter(
        (c) => String(c.country_id) === String(requestedCountryId),
      )
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
    // "Защита от дурака": если city.country_id не совпадает с обраною
    // країною (наприклад, бо список не встиг оновитися) — не дозволяємо вибір.
    if (countryIdRef.value && city.country_id != null && String(city.country_id) !== String(countryIdRef.value)) {
      showToast('Це місто не належить обраній країні, оберіть інше', 'error')
      reset()
      return
    }
    query.value = city.name_ua || city.name || city.city
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