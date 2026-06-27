<script setup>
defineProps({
  autocomplete: { type: Object, required: true },
})

const emit = defineEmits(['select'])

function handleSelect(country) {
  // autocomplete.select() уже обновляет внутреннее состояние,
  // событие наружу нужно только чтобы родитель мог сбросить зависимое поле (город).
  emit('select', country)
}
</script>

<template>
  <div class="relative">
    <label class="mb-2 block text-sm font-medium text-gray-700">
      Країна <span class="text-red-500">*</span>
    </label>

    <input
      type="text"
      autocomplete="off"
      placeholder="Оберіть країну..."
      :value="autocomplete.query"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
      aria-autocomplete="list"
      aria-haspopup="listbox"
      @input="autocomplete.onInput($event.target.value)"
      @focus="autocomplete.onFocus()"
    />

    <ul
      v-if="autocomplete.isOpen"
      class="absolute left-0 z-50 mt-1 max-h-48 w-full overflow-y-auto rounded-xl border border-gray-200 bg-white shadow-lg"
    >
      <li
        v-for="country in autocomplete.suggestions"
        :key="country.id"
        tabindex="0"
        class="cursor-pointer px-4 py-2 text-sm text-gray-800 transition hover:bg-blue-50 hover:text-blue-700"
        @click="autocomplete.select(country); handleSelect(country)"
      >
        {{ country.name }}

          <span
          v-if="country.name_ua"
          class="text-xs text-gray-400"
          >
            — {{ country.name_ua }}
          </span>
        <span v-if="country.code" class="text-xs text-gray-400">({{ country.code }})</span>
      </li>
      <li v-if="!autocomplete.suggestions.length" class="px-4 py-2 text-sm text-gray-500">
        Нічого не знайдено
      </li>
    </ul>
  </div>
</template>