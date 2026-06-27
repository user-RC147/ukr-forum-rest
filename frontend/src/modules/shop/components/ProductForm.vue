<script setup>
import { useProductForm } from '@/modules/shop/composables/useProductForm'
import CountryAutocomplete from './CountryAutocomplete.vue'
import CityAutocomplete from './CityAutocomplete.vue'
import ImageDropzone from './ImageDropzone.vue'

const props = defineProps({
  mode: { type: String, required: true, validator: (v) => ['create', 'update'].includes(v) },
  product: { type: Object, default: null },
})

const form = useProductForm({ mode: props.mode, product: props.product })

const isUpdate = props.mode === 'update'
</script>

<template>
  <form class="mx-auto m-5 max-w-6xl rounded-2xl bg-white p-6 shadow-lg sm:p-10" @submit.prevent="form.submit">
    <h2 class="mb-6 text-2xl font-semibold text-gray-800 sm:text-3xl">
      {{ isUpdate ? 'Редагувати товар' : 'Додати товар' }}
    </h2>

    <p v-if="form.nonFieldError" class="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
      {{ form.nonFieldError }}
    </p>

    <!-- Назва -->
    <label class="mb-2 block font-medium text-gray-700">
      Назва товару<span class="text-red-500">*</span>
    </label>
    <input
      v-model="form.name"
      type="text"
      maxlength="150"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
    />
    <p v-if="form.fieldErrors.name" class="mt-1 text-sm text-red-500">{{ form.fieldErrors.name }}</p>
    <p class="mt-1 text-sm text-gray-400">Максимум 150 символів</p>

    <!-- Опис -->
    <label class="mb-2 mt-6 block font-medium text-gray-700">
      Опис товару<span class="text-red-500">*</span>
    </label>
    <textarea
      v-model="form.description"
      maxlength="1500"
      rows="5"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
    ></textarea>
    <p v-if="form.fieldErrors.description" class="mt-1 text-sm text-red-500">{{ form.fieldErrors.description }}</p>
    <p class="mt-1 text-sm text-gray-400">Максимум 1500 символів</p>

    <!-- Категорія -->
    <label class="mb-2 mt-6 block font-medium text-gray-700">
      Категорія <span class="text-red-500">*</span>
    </label>
    <select
      v-model="form.categoryId"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
    >
      <option value="" disabled>Оберіть категорію</option>
      <option v-for="category in form.categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
    <p v-if="form.fieldErrors.category" class="mt-1 text-sm text-red-500">{{ form.fieldErrors.category }}</p>

    <!-- Ціна -->
    <label class="mb-2 mt-6 block font-medium text-gray-700">
      Ціна <span class="text-red-500">*</span>
    </label>
    <input
      v-model="form.price"
      type="number"
      min="0"
      step="0.01"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
    />
    <p v-if="form.fieldErrors.price" class="mt-1 text-sm text-red-500">{{ form.fieldErrors.price }}</p>

    <!-- Стан -->
    <label class="mb-2 mt-6 block font-medium text-gray-700">
      Стан <span class="text-red-500">*</span>
    </label>
    <select
      v-model="form.status"
      class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800 transition focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
    >
      <option v-for="option in form.statusOptions" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>

    <!-- Валюта -->
    <label class="mb-2 mt-6 block font-medium text-gray-700">Валюта</label>
    <div class="w-full rounded-xl border-2 border-gray-300 px-4 py-3 text-gray-800">
      {{ form.countryAutocomplete.currency || '—' }}
    </div>

    <!-- Країна -->
    <div class="mt-6">
      <CountryAutocomplete :autocomplete="form.countryAutocomplete" @select="form.onCountrySelect" />
      <p v-if="form.fieldErrors.country" class="mt-1 text-sm text-red-500">{{ form.fieldErrors.country }}</p>
    </div>

    <!-- Місто -->
    <div class="mt-6">
      <CityAutocomplete :autocomplete="form.cityAutocomplete" :country-name="form.countryAutocomplete.query" />
      <p v-if="form.fieldErrors.city_id" class="mt-1 text-sm text-red-500">{{ form.fieldErrors.city_id }}</p>
    </div>

    <!-- Фото -->
    <div class="mt-8">
      <ImageDropzone :upload="form.imageUpload" :show-existing="isUpdate" />
    </div>

    <div class="mt-8 flex justify-between">
      <RouterLink
        :to="{ name: 'shop-index' }"
        class="rounded bg-gray-200 px-5 py-2.5 text-gray-800 transition hover:bg-gray-300"
      >
        Назад
      </RouterLink>
      <button
        type="submit"
        :disabled="form.isSubmitting"
        class="rounded px-6 py-2.5 font-medium text-white transition disabled:cursor-not-allowed disabled:opacity-60"
        :class="isUpdate ? 'bg-blue-600 hover:bg-blue-700' : 'bg-green-600 hover:bg-green-700'"
      >
        {{ isUpdate ? 'Зберегти зміни' : 'Додати товар' }}
      </button>
    </div>
  </form>
</template>