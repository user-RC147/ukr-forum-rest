// modules/shop/composables/useCountryAutocomplete.js
import { ref, reactive } from 'vue'
import { searchCountries, getCountryById } from '@/modules/geo/api/geo'

const DEBOUNCE_MS = 250

/**
 * Автокомплит страны с подгрузкой валюты.
 * Аналог connect Django-виджета country-input + country-id + country-currency
 * из create_product.html / update_product.html.
 *
 * @param {{ id?: number|string, name?: string, currency?: string }} initial
 */
export function useCountryAutocomplete(initial = {}) {
  const query = ref(initial.name || '')
  const countryId = ref(initial.id || '')
  const currency = ref(initial.currency || '')
  const suggestions = ref([])
  const isOpen = ref(false)
  const isLoading = ref(false)

  let debounceTimer = null
  let requestToken = 0

  async function fetchAndShow(q) {
    const token = ++requestToken
    isLoading.value = true
    try {
      const results = await searchCountries(q)
      if (token !== requestToken) return
      suggestions.value = results
      isOpen.value = results.length > 0
    } finally {
      if (token === requestToken) isLoading.value = false
    }
  }

  function onInput(value) {
    requestToken++
    query.value = value
    countryId.value = ''
    currency.value = ''
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => fetchAndShow(query.value.trim()), DEBOUNCE_MS)
  }

  async function onFocus() {
    if (!suggestions.value.length) await fetchAndShow('')
    else isOpen.value = true
  }

  function select(country) {
    requestToken++
    query.value = country.name
    countryId.value = country.id ?? ''
    currency.value = country.currency ?? ''
    isOpen.value = false
  }

  function close() {
    requestToken++
    clearTimeout(debounceTimer)
    isOpen.value = false
  }

  /** Подгрузить страну по id — используется при заходе на форму редактирования. */
  async function prefillById(id) {
    if (!id) return
    const country = await getCountryById(id)
    if (country) {
      countryId.value = country.id
      query.value = country.name
      currency.value = country.currency ?? ''
    }
  }

  /** Если страна не выбрана из списка, но текст совпадает — попытаться найти её перед отправкой формы. */
  async function ensureSelected() {
    if (countryId.value) return true
    const name = query.value.trim()
    if (!name) return false
    const token = ++requestToken
    const list = await searchCountries(name)
    if (token !== requestToken || query.value.trim() !== name) return false
    if (!list.length) return false
    select(list[0])
    return true
  }

  if (initial.id && !initial.name) {
    prefillById(initial.id)
  }

  return reactive({
    query,
    countryId,
    currency,
    suggestions,
    isOpen,
    isLoading,
    onInput,
    onFocus,
    select,
    close,
    prefillById,
    ensureSelected,
  })
}