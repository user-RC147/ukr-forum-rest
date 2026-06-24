<script setup>
defineProps({
  autocomplete: { type: Object, required: true },
})
</script>

<template>
  <div class="relative">
    <label class="mb-2 block text-sm font-medium text-gray-700">
      Місто <span class="text-red-500">*</span>
    </label>

    <input
      type="text"
      autocomplete="off"
      placeholder="Введіть місто"
      :value="autocomplete.query"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
      @input="autocomplete.onInput($event.target.value)"
      @focus="autocomplete.onFocus()"
    />

    <ul
      v-if="autocomplete.isOpen"
      class="absolute left-0 z-50 mt-1 max-h-48 w-full overflow-y-auto rounded-xl border border-gray-200 bg-white shadow-lg"
    >
      <li
        v-for="city in autocomplete.suggestions"
        :key="city.id"
        tabindex="0"
        class="cursor-pointer px-4 py-2 text-sm text-gray-800 transition hover:bg-blue-50 hover:text-blue-700"
        @click="autocomplete.select(city)"
      >
        {{ city.city ?? city.name }}
        <span v-if="city.region" class="text-xs text-gray-400">({{ city.region }})</span>
      </li>
      <li v-if="!autocomplete.suggestions.length" class="px-4 py-2 text-sm text-gray-500">
        Нічого не знайдено
      </li>
    </ul>
  </div>
</template>