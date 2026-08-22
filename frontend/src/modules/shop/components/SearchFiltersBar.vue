<script setup>
import { ref, watch, toRef, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { MagnifyingGlassIcon, AdjustmentsHorizontalIcon, ChevronDownIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { useCategories } from '../composables/useCategories'
import { useSearchFilters } from '../composables/useSearchFilters'
import { useCountryAutocomplete } from '../composables/useCountryAutocomplete'
import { useCityAutocomplete } from '../composables/useCityAutocomplete'

const route = useRoute()
const { filters, RADII, applyFilters, resetFilters } = useSearchFilters()

const { categories, load: loadCategories } = useCategories()
loadCategories()

const filterKeys = ['category_id', 'country_id', 'city_id', 'radius', 'status', 'date_sort']
const shouldAutoOpen = ['shop-index', 'shop-search'].includes(route.name)
const filtersOpen = ref(false)
let openTimer = null
const root = ref(null)
const countryActiveIndex = ref(-1)
const cityActiveIndex = ref(-1)
const countryListboxId = 'shop-search-country-suggestions'
const cityListboxId = 'shop-search-city-suggestions'

function hasActiveFilters() {
  return filterKeys.some((key) => filters[key] !== '' && filters[key] != null)
}

function scheduleAutoOpen() {
  clearTimeout(openTimer)
  openTimer = setTimeout(() => {
    filtersOpen.value = true
  }, 180)
}

function closeIfOutside(event) {
  if (root.value && !root.value.contains(event.target)) {
    countryAutocomplete.close()
    cityAutocomplete.close()
  }
}

function handleFocusout(event) {
  if (!event.relatedTarget || !root.value?.contains(event.relatedTarget)) {
    countryAutocomplete.close()
    cityAutocomplete.close()
  }
}

function handleAutocompleteKeydown(event, autocomplete, activeIndex, listboxId) {
  const lastIndex = autocomplete.suggestions.length - 1
  if (event.key === 'Escape') {
    autocomplete.close()
    activeIndex.value = -1
    return
  }
  if (!autocomplete.isOpen || lastIndex < 0) return
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    activeIndex.value = activeIndex.value >= lastIndex ? 0 : activeIndex.value + 1
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    activeIndex.value = activeIndex.value <= 0 ? lastIndex : activeIndex.value - 1
  } else if (event.key === 'Enter' && activeIndex.value >= 0) {
    event.preventDefault()
    autocomplete.select(autocomplete.suggestions[activeIndex.value])
    activeIndex.value = -1
  }
}

// Инициализируем автокомплит с текущими значениями фильтров
const countryAutocomplete = useCountryAutocomplete({
  id: filters.country_id,
  name: filters.country_name,
})

const cityAutocomplete = useCityAutocomplete(
  {
    id: filters.city_id,
    name: filters.city_name,
  },
  toRef(countryAutocomplete, 'countryId'),
)

onMounted(() => {
  // Синхронизируем query'и с фильтрами при загрузке компонента
  if (filters.country_name && !countryAutocomplete.query) {
    countryAutocomplete.query = filters.country_name
  }
  if (filters.city_name && !cityAutocomplete.query) {
    cityAutocomplete.query = filters.city_name
  }
  if (filters.country_id && !countryAutocomplete.countryId) {
    countryAutocomplete.countryId = filters.country_id
  }
  if (filters.city_id && !cityAutocomplete.cityId) {
    cityAutocomplete.cityId = filters.city_id
  }

  if (shouldAutoOpen && hasActiveFilters()) {
    scheduleAutoOpen()
  }
})

watch(hasActiveFilters, (isActive, wasActive) => {
  if (shouldAutoOpen && isActive && !wasActive) {
    scheduleAutoOpen()
  }
})

// Обновляем фильтры при выборе страны
watch(() => countryAutocomplete.countryId, (val) => {
  if (!val) {
    filters.country_id = ''
    filters.country_name = ''
    filters.city_id = ''
    filters.city_name = ''
    filters.radius = ''
    cityAutocomplete.reset()
    return
  }
  filters.country_id = val
  filters.country_name = countryAutocomplete.query
  // Сбрасываем город при смене страны
  filters.city_id = ''
  filters.city_name = ''
  filters.radius = ''
  cityAutocomplete.reset()
})

// Обновляем фильтры при выборе города
watch(() => cityAutocomplete.cityId, (val) => {
  if (!val) {
    filters.city_id = ''
    filters.city_name = ''
    filters.radius = ''
    return
  }
  filters.city_id = val
  filters.city_name = cityAutocomplete.query
})

watch(() => countryAutocomplete.query, (value) => {
  filters.country_name = value
})

watch(() => cityAutocomplete.query, (value) => {
  filters.city_name = value
})

// Синхронизируем фильтры когда меняется route.query (вернулись на страницу поиска)
watch(() => route.query, () => {
  countryAutocomplete.query = filters.country_name
  countryAutocomplete.countryId = filters.country_id
  if (filters.city_id) {
    cityAutocomplete.query = filters.city_name
    cityAutocomplete.cityId = filters.city_id
  } else {
    cityAutocomplete.reset()
  }
}, { deep: true })

onMounted(() => document.addEventListener('pointerdown', closeIfOutside))
onBeforeUnmount(() => {
  clearTimeout(openTimer)
  document.removeEventListener('pointerdown', closeIfOutside)
})

function onReset(event) {
  // Используем методы close/reset которые уже есть в composables
  countryAutocomplete.close()
  cityAutocomplete.reset()
  // Очищаем значения через reactive properties
  countryAutocomplete.query = ''
  countryAutocomplete.countryId = ''
  countryAutocomplete.currency = ''
  resetFilters()
  event.currentTarget?.blur()
}
</script>

<template>
  <div ref="root" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 sm:p-6" @focusout="handleFocusout">
    <form @submit.prevent="applyFilters" class="space-y-4">

      <div class="flex flex-col sm:flex-row gap-3">
        <div class="relative flex-1">
          <MagnifyingGlassIcon class="w-5 h-5 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            v-model="filters.q"
            type="text"
            placeholder="Знайдіть те, що шукаєте..."
            class="w-full pl-11 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          />
        </div>

        <button
          type="submit"
          class="inline-flex cursor-pointer items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-200 shadow-sm"
        >
          <MagnifyingGlassIcon class="w-5 h-5" />
          Пошук
        </button>

        <button
          type="button"
          @click="filtersOpen = !filtersOpen"
          class="inline-flex cursor-pointer items-center justify-center gap-2 border border-gray-200 hover:bg-gray-50 text-gray-700 font-medium px-5 py-3 rounded-xl transition-colors duration-200"
        >
          <AdjustmentsHorizontalIcon class="w-5 h-5" />
          Фільтри
          <ChevronDownIcon :class="['w-4 h-4 transition-transform duration-200', filtersOpen && 'rotate-180']" />
        </button>
      </div>

      <div
        class="grid transition-[grid-template-rows] duration-300 ease-in-out"
        :class="filtersOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
      >
        <div class="overflow-hidden">
          <div class="pt-4 border-t border-gray-100 space-y-5">

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                  Категорія
                </label>
                <select
                  v-model="filters.category_id"
                  class="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                >
                  <option value="">Всі категорії</option>
                  <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
                </select>
              </div>

              <div class="relative">
                <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                  Країна
                </label>
                <input
                  :value="countryAutocomplete.query"
                  @input="countryAutocomplete.onInput($event.target.value)"
                  @keydown="handleAutocompleteKeydown($event, countryAutocomplete, countryActiveIndex, countryListboxId)"
                  @focus="countryAutocomplete.onFocus(); countryActiveIndex = -1"
                  type="text"
                  autocomplete="off"
                  role="combobox"
                  aria-autocomplete="list"
                  aria-haspopup="listbox"
                  :aria-expanded="countryAutocomplete.isOpen"
                  :aria-controls="countryListboxId"
                  placeholder="Оберіть країну..."
                  class="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                />
                <ul
                  v-if="countryAutocomplete.isOpen && countryAutocomplete.suggestions.length"
                  :id="countryListboxId"
                  role="listbox"
                  class="absolute z-20 mt-1 w-full max-h-52 overflow-y-auto rounded-xl border border-gray-100 bg-white shadow-lg"
                >
                  <li
                    v-for="item in countryAutocomplete.suggestions"
                    :key="item.id"
                    @mousedown.prevent="countryAutocomplete.select(item)"
                    role="option"
                    :aria-selected="item === countryAutocomplete.suggestions[countryActiveIndex]"
                    :class="['px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 cursor-pointer', item === countryAutocomplete.suggestions[countryActiveIndex] && 'bg-blue-50 text-blue-700']"
                  >
                    {{ item.name }}
                    <span v-if="item.name_ua" class="text-xs text-gray-400">— {{ item.name_ua }}</span>
                  </li>
                  <li v-if="!countryAutocomplete.suggestions.length" class="px-3 py-2 text-sm text-gray-500">
                    Нічого не знайдено
                  </li>
                </ul>
              </div>

              <div class="relative">
                <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                  Місто
                </label>
                <input
                  :value="cityAutocomplete.query"
                  @input="cityAutocomplete.onInput($event.target.value)"
                  @keydown="handleAutocompleteKeydown($event, cityAutocomplete, cityActiveIndex, cityListboxId)"
                  @focus="cityAutocomplete.onFocus(); cityActiveIndex = -1"
                  type="text"
                  autocomplete="off"
                  role="combobox"
                  aria-autocomplete="list"
                  aria-haspopup="listbox"
                  :aria-expanded="cityAutocomplete.isOpen"
                  :aria-controls="cityListboxId"
                  :disabled="!filters.country_id"
                  :placeholder="filters.country_id ? 'Оберіть місто...' : 'Спочатку оберіть країну'"
                  class="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition disabled:bg-gray-50 disabled:text-gray-400"
                />
                <ul
                  v-if="cityAutocomplete.isOpen && cityAutocomplete.suggestions.length"
                  :id="cityListboxId"
                  role="listbox"
                  class="absolute z-20 mt-1 w-full max-h-52 overflow-y-auto rounded-xl border border-gray-100 bg-white shadow-lg"
                >
                  <li
                    v-for="item in cityAutocomplete.suggestions"
                    :key="item.id"
                    @mousedown.prevent="cityAutocomplete.select(item)"
                    role="option"
                    :aria-selected="item === cityAutocomplete.suggestions[cityActiveIndex]"
                    :class="['px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 cursor-pointer', item === cityAutocomplete.suggestions[cityActiveIndex] && 'bg-blue-50 text-blue-700']"
                  >
                    {{ item.name_ua || item.name || item.city }}
                    <span v-if="item.region" class="text-xs text-gray-400">
                      — {{ item.region?.name_ua || item.region?.name || item.region }}
                    </span>
                  </li>
                  <li v-if="!cityAutocomplete.suggestions.length" class="px-3 py-2 text-sm text-gray-500">
                    Нічого не знайдено
                  </li>
                </ul>
              </div>

              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                  Радіус пошуку
                </label>
                <select
                  v-model="filters.radius"
                  :disabled="!filters.city_id"
                  class="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition disabled:bg-gray-50 disabled:text-gray-400"
                >
                  <option value="">Тільки обране місто</option>
                  <option v-for="r in RADII" :key="r" :value="r">+{{ r }} км</option>
                </select>
              </div>
            </div>

            <div class="grid gap-6 pt-1 lg:grid-cols-[1fr_1fr]">
              <div>
                <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Сортувати по:</span>
                <div class="mt-2 flex flex-wrap gap-2">
                  <label class="cursor-pointer">
                    <input type="radio" value="" v-model="filters.date_sort" class="sr-only peer" />
                    <span class="inline-flex items-center justify-center rounded-full border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 transition hover:border-blue-300 peer-checked:border-blue-600 peer-checked:bg-blue-50 peer-checked:text-blue-700">
                      За релевантністю
                    </span>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" value="date" v-model="filters.date_sort" class="sr-only peer" />
                    <span class="inline-flex items-center justify-center rounded-full border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 transition hover:border-blue-300 peer-checked:border-blue-600 peer-checked:bg-blue-50 peer-checked:text-blue-700">
                      Спочатку нові
                    </span>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" value="-date" v-model="filters.date_sort" class="sr-only peer" />
                    <span class="inline-flex items-center justify-center rounded-full border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 transition hover:border-blue-300 peer-checked:border-blue-600 peer-checked:bg-blue-50 peer-checked:text-blue-700">
                      Спочатку старі
                    </span>
                  </label>
                </div>
              </div>

              <div>
                <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Стан:</span>
                <div class="mt-2 flex flex-wrap gap-2">
                  <label class="cursor-pointer">
                    <input type="radio" value="" v-model="filters.status" class="sr-only peer" />
                    <span class="inline-flex items-center justify-center rounded-full border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 transition hover:border-blue-300 peer-checked:border-blue-600 peer-checked:bg-blue-50 peer-checked:text-blue-700">
                      Усі
                    </span>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" value="new" v-model="filters.status" class="sr-only peer" />
                    <span class="inline-flex items-center justify-center rounded-full border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 transition hover:border-blue-300 peer-checked:border-blue-600 peer-checked:bg-blue-50 peer-checked:text-blue-700">
                      Нові
                    </span>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" value="used" v-model="filters.status" class="sr-only peer" />
                    <span class="inline-flex items-center justify-center rounded-full border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 transition hover:border-blue-300 peer-checked:border-blue-600 peer-checked:bg-blue-50 peer-checked:text-blue-700">
                      Вживані
                    </span>
                  </label>
                </div>
              </div>
            </div>

            <div class="flex justify-end pt-2">
              <button
                type="button"
                @click="onReset"
                :class="hasActiveFilters()
                  ? 'border-blue-600 bg-blue-600 text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-offset-2'
                  : 'border-gray-300 bg-white text-gray-700 shadow-sm hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-offset-2'"
                class="inline-flex cursor-pointer items-center gap-1.5 rounded-xl border px-5 py-2.5 text-sm font-semibold transition-colors duration-200"
              >
                <XMarkIcon class="w-4 h-4" />
                Скинути фільтри
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>