<script setup>
import { ref, onBeforeUnmount, onMounted } from 'vue'

const props = defineProps({
  autocomplete: { type: Object, required: true },
  // Назва обраної країни — в відповіді API міста є лише country_id,
  // самої назви країни там немає, тож беремо її з автокомпліту країни.
  countryName: { type: String, default: '' },
})
const { autocomplete } = props

const root = ref(null)
const activeIndex = ref(-1)
const listboxId = 'shop-city-suggestions'

function closeIfOutside(event) {
  if (root.value && !root.value.contains(event.target)) autocomplete.close()
}

function handleFocusout(event) {
  if (!event.relatedTarget || !root.value?.contains(event.relatedTarget)) autocomplete.close()
}

function handleKeydown(event) {
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

onMounted(() => document.addEventListener('pointerdown', closeIfOutside))
onBeforeUnmount(() => document.removeEventListener('pointerdown', closeIfOutside))
</script>

<template>
  <div ref="root" class="relative" @focusout="handleFocusout">
    <label class="mb-2 block text-sm font-medium text-gray-700">
      Місто <span class="text-red-500">*</span>
    </label>

    <input
      type="text"
      autocomplete="off"
      placeholder="Введіть місто"
      :value="autocomplete.query"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
      aria-autocomplete="list"
      aria-haspopup="listbox"
      :aria-expanded="autocomplete.isOpen"
      :aria-controls="listboxId"
      @keydown="handleKeydown"
      @input="autocomplete.onInput($event.target.value)"
      @focus="autocomplete.onFocus(); activeIndex = -1"
    />

    <ul
      v-if="autocomplete.isOpen"
      :id="listboxId"
      role="listbox"
      class="absolute left-0 z-50 mt-1 max-h-48 w-full overflow-y-auto rounded-xl border border-gray-200 bg-white shadow-lg"
    >
      <li
        v-for="city in autocomplete.suggestions"
        :key="city.id"
        role="option"
        tabindex="-1"
        :aria-selected="city === autocomplete.suggestions[activeIndex]"
        :class="['cursor-pointer px-4 py-2 text-sm text-gray-800 transition hover:bg-blue-50 hover:text-blue-700', city === autocomplete.suggestions[activeIndex] && 'bg-blue-50 text-blue-700']"
        @pointerdown.stop.prevent="autocomplete.select(city)"
      >
        {{ city.name_ua || city.name }}
        <span v-if="city.region || countryName" class="text-xs text-gray-400">
          — {{ city.region?.name_ua || city.region?.name }}<template v-if="city.region && countryName">, </template>{{ countryName }}
        </span>
      </li>
      <li v-if="!autocomplete.suggestions.length" class="px-4 py-2 text-sm text-gray-500">
        Нічого не знайдено
      </li>
    </ul>
  </div>
</template>