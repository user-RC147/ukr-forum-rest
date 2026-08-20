// modules/shop/composables/useCityAutocomplete.js
import { ref, reactive } from 'vue'
import { searchCities } from '@/modules/geo/api/geo'
import { useToast } from '@/shared/composables/useToast'

const DEBOUNCE_MS = 250

/**
 * Автокомплит міста. Завжди прив'язаний до обраної країни — без countryId
 * пошук не виконується (як і в оригінальному create_product.js / update_product.js).
 *
 * Регіон НЕ вибирається окремо користувачем — він "приклеєний" до міста
 * і дістається з відповіді /api/geo/cities/search/ (поле city.region).
 * Це аналог денормалізованого поля в Django: region_id заповнюється
 * автоматично при збереженні залежно від вибраного міста.
 *
 * @param {{ id?: number|string, name?: string, regionId?: number|string, regionName?: string }} initial
 * @param {import('vue').Ref<string|number>} countryIdRef
 */
export function useCityAutocomplete(initial = {}, countryIdRef) {
  const { showToast } = useToast()

  const query = ref(initial.name || '')
  const cityId = ref(initial.id || '')
  const regionId = ref(initial.regionId ?? '')
  const regionName = ref(initial.regionName ?? '')
  const suggestions = ref([])
  const isOpen = ref(false)
  const isLoading = ref(false)

  let debounceTimer = null
  let requestToken = 0

  // Витягує region_id/region_name з об'єкта міста незалежно від того,
  // в якому форматі бекенд його віддав (об'єкт {id, name} чи плоскі поля).
  function extractRegion(city) {
    const region = city.region
    if (region && typeof region === 'object') {
      return {
        id: region.id ?? '',
        name: region.name_ua || region.name || '',
      }
    }
    return {
      id: city.region_id ?? '',
      name: typeof region === 'string' ? region : '',
    }
  }

  async function fetchAndShow(q) {
    // Фиксируем страну на момент запроса — если пользователь успеет
    // переключить страну пока летит запрос, устаревший ответ не применится.
    const requestedCountryId = countryIdRef.value
    const token = ++requestToken
    isLoading.value = true
    try {
      const results = await searchCities(q, requestedCountryId)

      if (token !== requestToken || countryIdRef.value !== requestedCountryId) return

      // "Защита от дурака": даже если backend вдруг вернёт город не из
      // запрошенной країни — отфильтровываем его на фронте.
      suggestions.value = results.filter(
        (c) => String(c.country_id) === String(requestedCountryId),
      )
      isOpen.value = suggestions.value.length > 0
    } finally {
      if (token === requestToken) isLoading.value = false
    }
  }

  function onInput(value) {
    requestToken++
    query.value = value
    cityId.value = ''
    regionId.value = ''
    regionName.value = ''

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
    requestToken++
    // "Защита от дурака": если city.country_id не совпадает с обраною
    // країною (наприклад, бо список не встиг оновитися) — не дозволяємо вибір.
    if (countryIdRef.value && city.country_id != null && String(city.country_id) !== String(countryIdRef.value)) {
      showToast('Це місто не належить обраній країні, оберіть інше', 'error')
      reset()
      return
    }

    const region = extractRegion(city)
    if (!region.id) {
      // Без region_id товар не збереже бекенд — краще одразу попередити,
      // ніж дати дійти до помилки валідації на сабміті.
      showToast('Не вдалося визначити регіон для цього міста', 'error')
      reset()
      return
    }

    query.value = city.name_ua || city.name || city.city
    cityId.value = city.id ?? ''
    regionId.value = region.id
    regionName.value = region.name
    isOpen.value = false
  }

  function close() {
    requestToken++
    clearTimeout(debounceTimer)
    isOpen.value = false
  }

  /** Сбросить город (и регион) — вызывается при смене страны. */
  function reset() {
    requestToken++
    query.value = ''
    cityId.value = ''
    regionId.value = ''
    regionName.value = ''
    suggestions.value = []
    isOpen.value = false
  }

  return reactive({
    query,
    cityId,
    regionId,
    regionName,
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