<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/useUserStore'
import { updateProfile, updateLocation } from '../api/users'
import { getCountries, getRegions, getCities } from '../../geo/api/geo'

const router    = useRouter()
const userStore = useUserStore()

const isLoading      = ref(false)
const successMessage = ref('')
const errorMessage   = ref('')

// Форма профілю
const form = ref({
  display_name:   '',
  phone_number:   '',
  age:            null,
  social_network: '',
  country_id:     null,
  region_id:      null,
  city_id:        null,
})

// Гео дані
const countries = ref([])
const regions   = ref([])
const cities    = ref([])

// Помилки валідації
const fieldErrors = ref({
  display_name:   '',
  phone_number:   '',
  age:            '',
  social_network: '',
})

// Правила валідації
const validate = {
  display_name: (val) => {
    if (val && val.length > 100) return 'Максимум 100 символів'
    return ''
  },
  phone_number: (val) => {
    if (val && !/^\+?[\d\s\-()]{7,20}$/.test(val)) return 'Невірний формат телефону'
    return ''
  },
  age: (val) => {
    if (val !== null && val !== '') {
      if (val < 0 || val > 120) return 'Вік має бути від 0 до 120'
    }
    return ''
  },
  social_network: (val) => {
    if (val && val.length > 150) return 'Максимум 150 символів'
    return ''
  },
}

// Викликається при виході з поля
const onBlur = (field) => {
  fieldErrors.value[field] = validate[field](form.value[field])
}

onMounted(async () => {
  await userStore.fetchProfile()

  if (userStore.user) {
    form.value.display_name   = userStore.user.display_name   || ''
    form.value.phone_number   = userStore.user.phone_number   || ''
    form.value.age            = userStore.user.age            || null
    form.value.social_network = userStore.user.social_network || ''
  }

  const res = await getCountries()
  countries.value = res.data
})

// Коли вибрали країну → завантажуємо регіони
watch(() => form.value.country_id, async (countryId) => {
  form.value.region_id = null
  form.value.city_id   = null
  regions.value = []
  cities.value  = []

  if (countryId) {
    const country = countries.value.find(c => c.id === countryId)
    const res = await getRegions(country.code)
    regions.value = res.data.results
  }
})

// Коли вибрали регіон → завантажуємо міста
watch(() => form.value.region_id, async (regionId) => {
  form.value.city_id = null
  cities.value = []

  if (regionId) {
    const res = await getCities(regionId)
    cities.value = res.data.results
  }
})

const handleSubmit = async () => {
  isLoading.value      = true
  successMessage.value = ''
  errorMessage.value   = ''

  // перевіряємо всі поля перед відправкою
  Object.keys(fieldErrors.value).forEach(field => {
    fieldErrors.value[field] = validate[field](form.value[field])
  })

  // якщо є помилки — зупиняємо
  if (Object.values(fieldErrors.value).some(e => e)) {
    isLoading.value = false
    return
  }

  try {
    await updateProfile({
      display_name:   form.value.display_name   || null,
      phone_number:   form.value.phone_number   || null,
      age:            form.value.age            || null,
      social_network: form.value.social_network || null,
    })

    if (form.value.country_id) {
      await updateLocation({
        country_id: form.value.country_id,
        region_id:  form.value.region_id,
        city_id:    form.value.city_id,
      })
    }

    await userStore.fetchProfile()
    successMessage.value = 'Профіль успішно оновлено!'
  } catch (error) {
    errorMessage.value = 'Помилка збереження. Спробуйте ще раз.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center mt-8 p">
    <div class=" rounded-lg shadow-md w-full max-w-sm">

      <fieldset class="border-t border-gray-400  px-6  flex items-center justify-center">
        <legend class="px-2 text-gray-700 text-sm lg:text-base">Мій профіль</legend>
      </fieldset>

      <p v-if="!userStore.user" class="text-gray-500 text-center">
        Завантаження...
      </p>

      <form v-else @submit.prevent="handleSubmit" class="space-y-4 p-6">

        <!-- повідомлення -->
        <p v-if="successMessage" class="text-green-600 text-sm text-center">
          {{ successMessage }}
        </p>
        <p v-if="errorMessage" class="text-red-500 text-sm text-center">
          {{ errorMessage }}
        </p>

        <!-- логін — тільки читання -->
        <div>
          <label class="block text-sm text-gray-500 mb-1">Логін</label>
          <p class="font-medium text-gray-800 bg-gray-50 p-2 rounded">
            {{ userStore.user.username }}
          </p>
        </div>

        <!-- email — тільки читання -->
        <div>
          <label class="block text-sm text-gray-500 mb-1">Email</label>
          <div class="font-medium text-gray-800 bg-gray-50 p-2 rounded">
            {{ userStore.user.email || "" }}
          </div>
        </div>

        <!-- публічне ім'я -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Публічне ім'я (нікнейм)
          </label>
          <input
            v-model="form.display_name"
            type="text"
            placeholder="Ваше публічне ім'я"
            @blur="onBlur('display_name')"
            :class="[
              'p-2 w-full rounded focus:outline-none focus:ring-2',
              fieldErrors.display_name
                ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                : 'bg-amber-100 focus:ring-amber-400'
            ]"
          />
          <p v-if="fieldErrors.display_name" class="text-red-500 text-xs mt-1">
            {{ fieldErrors.display_name }}
          </p>
        </div>

        <!-- вік -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Вік</label>
          <input
            v-model="form.age"
            type="number"
            min="0"
            max="120"
            placeholder="Ваш вік"
            @blur="onBlur('age')"
            :class="[
              'p-2 w-full rounded focus:outline-none focus:ring-2',
              fieldErrors.age
                ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                : 'bg-amber-100 focus:ring-amber-400'
            ]"
          />
          <p v-if="fieldErrors.age" class="text-red-500 text-xs mt-1">
            {{ fieldErrors.age }}
          </p>
        </div>

        <!-- телефон -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
          <input
            v-model="form.phone_number"
            type="text"
            placeholder="+380..."
            @blur="onBlur('phone_number')"
            :class="[
              'p-2 w-full rounded focus:outline-none focus:ring-2',
              fieldErrors.phone_number
                ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                : 'bg-amber-100 focus:ring-amber-400'
            ]"
          />
          <p v-if="fieldErrors.phone_number" class="text-red-500 text-xs mt-1">
            {{ fieldErrors.phone_number }}
          </p>
        </div>

        <!-- соц.мережа -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Соц.мережа</label>
          <input
            v-model="form.social_network"
            type="text"
            placeholder="Посилання на профіль"
            @blur="onBlur('social_network')"
            :class="[
              'p-2 w-full rounded focus:outline-none focus:ring-2',
              fieldErrors.social_network
                ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                : 'bg-amber-100 focus:ring-amber-400'
            ]"
          />
          <p v-if="fieldErrors.social_network" class="text-red-500 text-xs mt-1">
            {{ fieldErrors.social_network }}
          </p>
        </div>

        <!-- кнопка додати іншу локацію -->
        <button
          type="button"
          @click="router.push({ name: 'location' })"
          class="text-sm text-amber-600 hover:underline mt-1"
        >
          + Додати іншу локацію
        </button>

        <!-- ЛОКАЦІЯ -->
        <fieldset class="border-t pt-4">
          <legend class="text-sm font-medium text-gray-700 mb-3">
            Ваше місце локації
          </legend>

          <!-- Країна -->
          <div class="mb-3">
            <label class="block text-sm text-gray-600 mb-1">Країна</label>
            <select
              v-model="form.country_id"
              class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
            >
              <option :value="null">Оберіть країну</option>
              <option v-for="c in countries" :key="c.id" :value="c.id">
                {{ c.flag_emoji }} {{ c.name }}
              </option>
            </select>
          </div>

          <!-- Регіон -->
          <div class="mb-3">
            <label class="block text-sm text-gray-600 mb-1">Регіон</label>
            <select
              v-model="form.region_id"
              :disabled="!form.country_id"
              class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-50"
            >
              <option :value="null">Оберіть регіон</option>
              <option v-for="r in regions" :key="r.id" :value="r.id">
                {{ r.name }}
              </option>
            </select>
          </div>

          <!-- Місто -->
          <div class="mb-3">
            <label class="block text-sm text-gray-600 mb-1">Місто</label>
            <select
              v-model="form.city_id"
              :disabled="!form.region_id"
              class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-50"
            >
              <option :value="null">Оберіть місто</option>
              <option v-for="c in cities" :key="c.id" :value="c.id">
                {{ c.name }}
              </option>
            </select>
          </div>

        </fieldset>

        <!-- кнопки -->
        <div class="flex justify-between gap-4 pt-2">
          <button
            type="button"
            @click="router.push({ name: 'home' })"
            class="bg-[#CEC526] rounded px-6 py-2 text-gray-800 hover:bg-[#F2E70A] transition text-sm lg:text-base"
          >
            Повернутися
          </button>
          <button
            type="submit"
            :disabled="isLoading"
            class="bg-[#CEC526] rounded px-6 py-2 text-gray-800 hover:bg-[#F2E70A] disabled:opacity-50 transition text-sm lg:text-base"
          >
            {{ isLoading ? 'Збереження...' : 'Зберегти зміни' }}
          </button>
        </div>

      </form>
    </div>
  </div>
</template>