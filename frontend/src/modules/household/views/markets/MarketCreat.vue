<script setup>
import { ref,onMounted,watch } from 'vue';
import {useRouter} from 'vue-router';
import {getCountries,getRegions,getCities} from '../../../geo/api/geo' // Шлях до вашого geo.js
import { useMarketStore } from '../../stores/useMarketStore';

const router=useRouter()
const marketStory=useMarketStore()

// Форма відповідно до структури CreateMarketInDTO на бекенді
const form=ref({
    name:'',
    address_line:null,
    country_id:null,
    region_id:null,
    city_id:null,
})

// Списки даних для випадаючих списків
const countries=ref([])
const regions=ref([])
const cities=ref([])

const isLoading=ref(false)
const successMessage=ref('')
const errorMessage=ref('')

// 1. Завантажуємо країни при старті сторінки
onMounted(async()=>{
    try{
        const res=await getCountries()
        countries.value=res.data // у країнах дані йдуть масивом
    }catch(err){
        console.error('Не вдалося завантажити країни:', err)
    }
})

// 2. Слідкуємо за вибором країни → завантажуємо регіони
watch(()=>form.value.country_id,async (countryId)=>{
    form.value.region_id=null
    form.value.city_id=null
    regions.value=[]
    cities.value=[]

    if (countryId){
        // Шукаємо об'єкт країни, щоб дістати її текстовий код (наприклад, 'UA')
        const country=countries.value.find(c=>c.id === countryId)
        if (country){
            const res=await getRegions(country.code)
            // Оскільки в трейсі було видно .results, використовуємо res.data.results
            regions.value=res.data.results || res.data
        }
    }
})

// 3. Слідкуємо за вибором регіону → завантажуємо міста
watch(()=> form.value.region_id, async (regionId)=>{
    form.value.city_id=null
    cities.value=[]

    if (regionId){
        const res = await getCities(regionId)
        // Використовуємо .results згідно з архітектурою вашого гео-модуля
        cities.value=res.data.results || res.data
    }
})

// 4. Сабміт форми
const handleSubmit = async () => {
    if (!form.value.name.trim()) return

    isLoading.value      = true
    successMessage.value = ''
    errorMessage.value   = ''

    try {
        // Викликаємо метод стору для відправки на бекенд
        await marketStore.createMarket({
            name: form.value.name.trim(),
            address_line: form.value.address_line.trim() || null,
            country_id: form.value.country_id,
            region_id: form.value.region_id,
            city_id: form.value.city_id
        })

        successMessage.value = 'Магазин успішно створено!'
        
        // Повертаємось на головну сторінку household через 1.5 сек
        setTimeout(() => {
            router.push({ name: 'household-index' })
        }, 1500)

    } catch (error) {
        errorMessage.value = 'Помилка створення магазину. Перевірте дані.'
        console.error(error)
    } finally {
        isLoading.value = false
    }
}

</script>

<template>
    <div class="flex items-center justify-center min-h-[calc(100vh-100px)] px-4 py-6">
        <div class="bg-white rounded-3xl shadow-xl w-full max-w-xl p-6 md:p-8 border border-gray-100">

            <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">
                Додати новий магазин
            </h2>

            <p v-if="successMessage" class="text-green-600 bg-green-50 p-3 rounded-xl text-sm text-center mb-5 font-medium">
                {{ successMessage }}
            </p>
            <p v-if="errorMessage" class="text-red-500 bg-red-50 p-3 rounded-xl text-sm text-center mb-5 font-medium">
                {{ errorMessage }}
            </p>

            <form @submit.prevent="handleSubmit" class="space-y-5">
                
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                        Назва магазину *
                    </label>
                    <input
                        type="text"
                        v-model="form.name"
                        required
                        placeholder="Наприклад: Lidl, Сільпо, АТБ"
                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-amber-500 transition"
                    />
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                            Країна
                        </label>
                        <select
                            v-model="form.country_id"
                            class="w-full border border-gray-300 bg-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-amber-500 cursor-pointer"
                        >
                            <option :value="null">Оберіть країну</option>
                            <option v-for="c in countries" :key="c.id" :value="c.id">
                                {{ c.flag_emoji }} {{ c.name_ua || c.name }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                            Область / Регіон
                        </label>
                        <select
                            v-model="form.region_id"
                            :disabled="!form.country_id"
                            class="w-full border border-gray-300 bg-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-amber-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
                        >
                            <option :value="null">Оберіть область</option>
                            <option v-for="r in regions" :key="r.id" :value="r.id">
                                {{ r.name_ua || r.name }}
                            </option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                            Місто
                        </label>
                        <select
                            v-model="form.city_id"
                            :disabled="!form.region_id"
                            class="w-full border border-gray-300 bg-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-amber-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
                        >
                            <option :value="null">Оберіть місто</option>
                            <option v-for="c in cities" :key="c.id" :value="c.id">
                                {{ c.name_ua || c.name }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                            Вулиця, будинок
                        </label>
                        <input
                            type="text"
                            v-model="form.address_line"
                            placeholder="вул. Центральна, 5"
                            class="w-full border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-amber-500 transition"
                        />
                    </div>
                </div>

                <div class="flex justify-between gap-4 pt-4 border-t border-gray-100 mt-6">
                    <button
                        type="button"
                        @click="router.push({ name: 'household-index' })"
                        class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-xl text-sm font-medium transition"
                    >
                        Скасувати
                    </button>
                    <button
                        type="submit"
                        :disabled="isLoading || !form.name.trim()"
                        class="bg-amber-400 hover:bg-amber-500 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed text-gray-900 px-8 py-3 rounded-xl text-sm font-bold transition shadow-sm"
                    >
                        {{ isLoading ? 'Збереження...' : 'Створити магазин' }}
                    </button>
                </div>

            </form>
        </div>
    </div>
</template>