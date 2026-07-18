<script setup>
import { ref, watch, toRef, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { MagnifyingGlassIcon, AdjustmentsHorizontalIcon, ChevronDownIcon } from '@heroicons/vue/24/outline'
import { useCategories } from '../composables/useCategories'
import { useSearchFilters } from '../composables/useSearchFilters'
import { useCountryAutocomplete } from '../composables/useCountryAutocomplete'
import { useCityAutocomplete } from '../composables/useCityAutocomplete'

const route = useRoute()
const { filters, RADII, applyFilters, resetFilters } = useSearchFilters()

const { categories, load: loadCategories } = useCategories()
loadCategories()

const filtersOpen = ref(false)

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
})

// Обновляем фильтры при выборе страны
watch(() => countryAutocomplete.countryId, (val) => {
  if (!val) return
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
  if (!val) return
  filters.city_id = val
  filters.city_name = cityAutocomplete.query
})

// Синхронизируем фильтры когда меняется route.query (вернулись на страницу поиска)
watch(() => route.query, () => {
  if (!filters.country_id) {
    countryAutocomplete.query = ''
    countryAutocomplete.countryId = ''
  }
  if (!filters.city_id) {
    cityAutocomplete.reset()
  }
})

function onReset() {
  // Используем методы close/reset которые уже есть в composables
  countryAutocomplete.close()
  cityAutocomplete.reset()
  // Очищаем значения через reactive properties
  countryAutocomplete.query = ''
  countryAutocomplete.countryId = ''
  countryAutocomplete.currency = ''
  resetFilters()
}
</script>

<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 sm:p-6">
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
          class="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-200 shadow-sm"
        >
          <MagnifyingGlassIcon class="w-5 h-5" />
          Пошук
        </button>

        <button
          type="button"
          @click="filtersOpen = !filtersOpen"
          class="inline-flex items-center justify-center gap-2 border border-gray-200 hover:bg-gray-50 text-gray-700 font-medium px-5 py-3 rounded-xl transition-colors duration-200"
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
                  @focus="countryAutocomplete.onFocus()"
                  type="text"
                  autocomplete="off"
                  placeholder="Оберіть країну..."
                  class="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                />
                <ul
                  v-if="countryAutocomplete.isOpen && countryAutocomplete.suggestions.length"
                  class="absolute z-20 mt-1 w-full max-h-52 overflow-y-auto rounded-xl border border-gray-100 bg-white shadow-lg"
                >
                  <li
                    v-for="item in countryAutocomplete.suggestions"
                    :key="item.id"
                    @mousedown.prevent="countryAutocomplete.select(item)"
                    class="px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 cursor-pointer"
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
                  @focus="cityAutocomplete.onFocus()"
                  type="text"
                  autocomplete="off"
                  :disabled="!filters.country_id"
                  :placeholder="filters.country_id ? 'Оберіть місто...' : 'Спочатку оберіть країну'"
                  class="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition disabled:bg-gray-50 disabled:text-gray-400"
                />
                <ul
                  v-if="cityAutocomplete.isOpen && cityAutocomplete.suggestions.length"
                  class="absolute z-20 mt-1 w-full max-h-52 overflow-y-auto rounded-xl border border-gray-100 bg-white shadow-lg"
                >
                  <li
                    v-for="item in cityAutocomplete.suggestions"
                    :key="item.id"
                    @mousedown.prevent="cityAutocomplete.select(item)"
                    class="px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 cursor-pointer"
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

            <div class="flex flex-col sm:flex-row sm:items-center gap-6 pt-1">
              <div class="flex items-center gap-3 flex-wrap">
                <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Дата:</span>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="date" v-model="filters.date_sort" class="text-blue-600 focus:ring-blue-500" />
                  Спочатку нові
                </label>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="-date" v-model="filters.date_sort" class="text-blue-600 focus:ring-blue-500" />
                  Спочатку старі
                </label>
              </div>

              <div class="flex items-center gap-3 flex-wrap">
                <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Ціна:</span>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="" v-model="filters.price_sort" class="text-blue-600 focus:ring-blue-500" />
                  За замовчуванням
                </label>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="-price" v-model="filters.price_sort" class="text-blue-600 focus:ring-blue-500" />
                  Спочатку дорожчі
                </label>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="price" v-model="filters.price_sort" class="text-blue-600 focus:ring-blue-500" />
                  Спочатку дешевші
                </label>
              </div>

              <div class="flex items-center gap-3 flex-wrap">
                <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Стан:</span>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="" v-model="filters.status" class="text-blue-600 focus:ring-blue-500" />
                  Усі
                </label>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="new" v-model="filters.status" class="text-blue-600 focus:ring-blue-500" />
                  Нові
                </label>
                <label class="inline-flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                  <input type="radio" value="used" v-model="filters.status" class="text-blue-600 focus:ring-blue-500" />
                  Вживані
                </label>
              </div>
            </div>

            <div class="flex justify-end gap-3 pt-2">
              <button
                type="button"
                @click="onReset"
                class="px-5 py-2.5 rounded-xl text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors duration-200"
              >
                Скинути
              </button>
              <button
                type="submit"
                class="px-6 py-2.5 rounded-xl text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors duration-200 shadow-sm"
              >
                Застосувати фільтри
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>