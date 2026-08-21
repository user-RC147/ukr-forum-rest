<script setup>
import { TagIcon } from '@heroicons/vue/24/outline'
import { useCategories } from '../composables/useCategories'
import { useSearchFilters } from '../composables/useSearchFilters'

const { filters, applyFilters } = useSearchFilters()
const { categories, isLoading, load } = useCategories()
load()

const gradients = [
  'from-blue-500 to-indigo-600',
  'from-emerald-500 to-teal-600',
  'from-orange-500 to-red-500',
  'from-purple-500 to-fuchsia-600',
  'from-amber-500 to-orange-600',
  'from-cyan-500 to-blue-600',
  'from-pink-500 to-rose-600',
  'from-lime-500 to-green-600',
]
const gradientFor = (id) => gradients[id % gradients.length]

function openCategory(category) {
  filters.category_id = category.id
  applyFilters()
}
</script>

<template>
  <section class="mb-10">
    <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-5">Розділи на сервісі</h2>

    <div v-if="isLoading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-3">
      <div v-for="n in 8" :key="n" class="h-24 rounded-2xl bg-gray-100 animate-pulse"></div>
    </div>

    <div
      v-else-if="categories.length"
      class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-3"
    >
      <button
        v-for="category in categories"
        :key="category.id"
        type="button"
        @click="openCategory(category)"
        class="group flex flex-col items-center justify-center gap-2 rounded-2xl bg-white border border-gray-100 shadow-sm px-3 py-4 text-center transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5 hover:border-gray-200"
      >
        <span
          :class="`bg-gradient-to-br ${gradientFor(category.id)}`"
          class="flex items-center justify-center w-11 h-11 rounded-xl text-white shadow-md group-hover:scale-105 transition-transform duration-200"
        >
          <TagIcon class="w-5 h-5" />
        </span>
        <span class="text-xs sm:text-sm font-medium text-gray-800 line-clamp-2 leading-tight">
          {{ category.name }}
        </span>
      </button>
    </div>

    <p v-else class="text-center text-gray-500 italic py-10">
      Якщо тут немає розділів — скористайтеся пошуком вище.
    </p>
  </section>
</template>