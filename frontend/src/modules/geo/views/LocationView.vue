<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getCountries, getRegions, getCities } from '../api/geo'
import { updateLocation } from '../../users/api/users'

const router = useRouter()

const form = ref({
    country_id: null,
    region_id:  null,
    city_id:    null,
})

const countries = ref([])
const regions   = ref([])
const cities    = ref([])

const isLoading      = ref(false)
const successMessage = ref('')
const errorMessage   = ref('')

// Завантажуємо країни при старті
onMounted(async () => {
    const res = await getCountries()
    countries.value = res.data  // ← було res.data.results
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
    isLoading.value     = true
    successMessage.value = ''
    errorMessage.value   = ''

    try {
        await updateLocation(form.value)
        successMessage.value = 'Локацію успішно збережено!'
        // повертаємось на профіль через 1.5 секунди
        setTimeout(() => router.push({ name: 'profile' }), 1500)
    } catch (error) {
        errorMessage.value = 'Помилка збереження. Спробуйте ще раз.'
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <div class="flex items-center justify-center min-h-[calc(100vh-56px)] px-4 py-8">
        <div class="bg-white rounded-lg shadow-md w-full max-w-lg p-6 lg:p-8">

            <h2 class="text-center text-xl font-medium text-gray-700 mb-6">
                Локація
            </h2>

            <!-- повідомлення про успіх -->
            <p v-if="successMessage" class="text-green-600 text-sm text-center mb-4">
                {{ successMessage }}
            </p>

            <!-- повідомлення про помилку -->
            <p v-if="errorMessage" class="text-red-500 text-sm text-center mb-4">
                {{ errorMessage }}
            </p>

            <form @submit.prevent="handleSubmit" class="space-y-5">

                <!-- Країна -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        Країна
                    </label>
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

                <!-- Область / Регіон -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        Область / Регіон
                    </label>
                    <select
                        v-model="form.region_id"
                        :disabled="!form.country_id"
                        class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-50"
                    >
                        <option :value="null">Оберіть область</option>
                        <option v-for="r in regions" :key="r.id" :value="r.id">
                            {{ r.name }}
                        </option>
                    </select>
                </div>

                <!-- Місто -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        Місто
                    </label>
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

                <!-- кнопки -->
                <div class="flex justify-between gap-4 pt-2">
                    <button
                        type="button"
                        @click="router.push({ name: 'profile' })"
                        class="bg-[#CEC526] rounded px-6 py-2 text-gray-800 hover:bg-[#F2E70A] transition"
                    >
                        Повернутися
                    </button>
                    <button
                        type="submit"
                        :disabled="isLoading || !form.country_id"
                        class="bg-[#CEC526] rounded px-6 py-2 text-gray-800 hover:bg-[#F2E70A] disabled:opacity-50 transition"
                    >
                        {{ isLoading ? 'Збереження...' : 'Зберегти зміни' }}
                    </button>
                </div>

            </form>
        </div>
    </div>
</template>