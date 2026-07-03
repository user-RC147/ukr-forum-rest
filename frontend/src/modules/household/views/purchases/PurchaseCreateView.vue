<script setup>

import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

import { useGroupStore } from '../../stores/useGroupStore';
import { useAssetStore } from '../../stores/useAssetStore';
import { useUserStore } from '@/shared/stores/useUserStore';
import { useMarketStore } from '../../stores/useMarketStore';
import {useProductStore} from '../../stores/useProductStore';
import { useUnitOfMeasureStore } from '../../stores/useUnitOfMeasureStore';

// Імпортуємо функції з geo.js
import { getCountries, getRegions, getCities } from '@/modules/geo/api/geo';

// Ініціалізуємо сховища даних
const groupStore = useGroupStore();
const assetStore = useAssetStore();
const userStore = useUserStore();
const marketStore = useMarketStore();
const productStore = useProductStore();
//const unit_of_measureStore = useUnitOfMeasureStore();
const route = useRoute();

// Поля «шапки» чека
const selectedGroup = ref(route.query.group_id ? Number(route.query.group_id) : null);
const selectedAsset = ref(route.query.asset_id ? Number(route.query.asset_id) : null);

// Виправлено: змінна називається selectedMarket, оскільки у шаблоні v-model="selectedMarket"
const selectedMarket = ref(null); 
const checkDate = ref(new Date().toISOString().substr(0, 10));

// Тимчасові реактивні змінні для полів "Додавання товару"
const newProduct = ref({
    name: '',
    unit: 'шт.',
    qty: 1,
    price: 0
});

// Масив уже доданих до чека товарів
const checkItems = ref([
    { name: 'Хліб', unit: 'шт.', qty: 1.0, price: 4.03 },
    { name: 'Булочка', unit: 'шт.', qty: 1.0, price: 2.03 }
]);

// Змінна контролю модалки
const isMarketModalOpen = ref(false);
const isProductModalOpen=ref(false);
const newProductForm=ref({
    name:'',
    unit_of_measure:'шт' // ← точно як у Django моделі
});

// Тимчасові дані для форми створення нового магазину
const newMarketName = ref('');
const streetAndHouse = ref('');

// Списки даних для випадаючих списків у модалку
const countries = ref([]);
const regions   = ref([]);
const cities    = ref([]);

// Стан обраних ID у формі модалки
const modalCountryId = ref(null);
const modalRegionId  = ref(null);
const modalCityId    = ref(null);

// Загальна сума чека
const totalSum = computed(() => {
    return checkItems.value.reduce((sum, item) => sum + (Number(item.qty) * Number(item.price)), 0).toFixed(2);
});

onMounted(async () => {
    await Promise.all([
        groupStore.fetchGroups(),
        assetStore.fetchAssets(),
        //userStore.fetchProfile(),
        marketStore.fetchMarkets(),
        productStore.fetchProducts(),
        unit_of_measureStore.fetchUnitsOfMeasure()
    ]);
});

// Функція збереження нового магазину
const handleCreateMarket = async () => {
    if (!newMarketName.value.trim()) return;

    try {
        const createdMarket = await marketStore.createMarket({
            name: newMarketName.value.trim(),
            address_line: streetAndHouse.value.trim() || '',
            country_id: modalCountryId.value ? Number(modalCountryId.value) : null,
            region_id: modalRegionId.value ? Number(modalRegionId.value) : null,
            city_id: modalCityId.value ? Number(modalCityId.value) : null
        });

        // Автоматично вибираємо щойно створений магазин
        selectedMarket.value = createdMarket.id;

        // Очищаємо поля
        newMarketName.value = '';
        streetAndHouse.value = '';
        modalCountryId.value = null;
        modalRegionId.value = null;
        modalCityId.value = null;

        isMarketModalOpen.value = false;
    } catch (error) {
        console.log('Деталі помилки:', error.response?.data)  // ← додай
        alert('Помилка при створенні магазину');
    }
};

// Функція збереження нового товару
const handleCreateProduct=async()=>{
     // Захист: якщо назва пуста — нічого не робимо
     if(!newProductForm.value.name.trim()) return;

     try{
        // Відправляємо POST запит на бекенд
        const createdProduct = await productStore.addProduct({
            name: newProductForm.value.name.trim(),
            unit_of_measure: newProductForm.value.unit_of_measure
        });

        // Закриваємо модалку
        isProductModalOpen.value=false;

        // Очищаємо форму для наступного разу
        newProductForm.value.name='';
        newProductForm.value.unit_of_measure='шт.';

         console.log('Товар створено:', createdProduct);
    } catch (error) {
        console.log('Деталі помилки:', error.createdProduct?.data)  // ← додай
        // Тут можна додатково обробити помилку, наприклад, показати повідомлення з бекенду;
        alert('Помилка при створенні товару');
    }
};

// 1. Слідкуємо за відкриттям модалки -> вантажимо країни
watch(isMarketModalOpen, async (isOpen) => {
    if (isOpen && countries.value.length === 0) {
        try {
            const res = await getCountries();
            // Захист від пагінації (беремо .results або чистий масив .data)
            countries.value = res.data.results || res.data;
        } catch (err) {
            console.error('Помилка завантаження країн у модалку:', err);
        }
    }
});

// 2. Слідкуємо за вибором країни у модалці -> вантажимо регіони
watch(modalCountryId, async (countryId) => {
    modalRegionId.value = null;
    modalCityId.value   = null;
    regions.value       = [];
    cities.value        = [];

    if (!countryId) return;  // ← ! (заперечення) — виходимо якщо NULL

    const country = countries.value.find(c => Number(c.id) === Number(countryId));

    console.log('Знайдена країна:', country);
    console.log('country.code:', country?.code);

    if (country && country.code) {
        console.log('Викликаю getRegions з кодом:', country.code)  // ← додай
        try {
            const res = await getRegions(country.code);
            console.log('regions response:', res.data);
            regions.value = res.data.results || res.data;
        } catch (err) {
            console.error('Помилка завантаження регіонів:', err);
        }
    }
});

// 3. Слідкуємо за вибором регіону у модалці -> вантажимо міста
watch(modalRegionId, async (regionId) => {
    modalCityId.value = null;
    cities.value      = [];

    if (regionId) {
        try {
            const res = await getCities(Number(regionId));
            cities.value = res.data.results || res.data;
        } catch (err) {
            console.error('Помилка завантаження міст:', err);
        }
    }
});

// Слідкуємо за зміною групи
watch(selectedGroup, (newGroupId) => {
    selectedAsset.value = null;
    if (newGroupId) {
        assetStore.fetchAssets(newGroupId);
    } else {
        assetStore.fetchAssets();
    }
});
</script>


<template>

    <div class="max-w-5xl mx-auto px-4 py-6">

        <!-- Верхній рядок: Повернутися + Зберегти -->
        <div class="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-4 mb-6">
            <router-link :to="{ name: 'household-index' }" 
                class="flex items-center justify-center bg-[#cce9f8] hover:bg-[#aedbf4] text-[#2e332e] px-5 py-3 rounded-xl text-sm font-medium transition transform hover:scale-105 w-full sm:w-auto">
                ← Повернутися
            </router-link>
            
            <button type="submit"
                    class="bg-[#CEC526] hover:bg-[#F2E70A] text-[#33332E] text-lg font-semibold px-5 py-3 rounded-xl transition transform hover:scale-105 w-full sm:w-auto">
                Зберегти
            </button>
        </div>

        <!-- Фільтри це обєкт до якого привязується чек -->
        <div class="flex flex-wrap justify-around mb-8">
            <div class="bg-amber-100 px-4 py-3 rounded-2xl flex min-w-[130px]">
                <select v-model="selectedAsset"
                        class="w-full bg-transparent focus:outline-none">
                    <option :value="null">Всі об'єкти</option>
                    <option 
                            v-for="asset in assetStore.assets"
                            :key="asset.id"
                            :value="asset.id"
                    >
                    {{ asset.name }}
                    </option>
                </select>
                
            </div>

            <div class="bg-amber-100 px-4 py-3 rounded-2xl text-center whitespace-nowrap">
                {{ userStore.user?.username || userStore.user?.display_name || 'Завантаження...' }}
            </div>

            <div class="bg-amber-100 px-4 py-3 rounded-2xl flex min-w-[130px]">
                <select v-model="selectedGroup"
                        class="w-full bg-transparent focus:outline-none">
                    <option :value="null">Всі групи</option>
                    <option 
                            v-for="group in groupStore.groups" 
                            :key="group.id" 
                            :value="group.id"
                        >
                        {{ group.name }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Кнопки створення -->
        <div class="grid grid-cols-2 gap-4 mb-10">
            <button 
                type="button"
                @click="isMarketModalOpen=true"
                class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold text-sm transition"
            >
                створити магазин

            </button>

            <button
                class="bg-amber-50 hover:bg-amber-100 text-center py-4 rounded-2xl transition"
                type="button"
                @click="isProductModalOpen=true">                
                    створити товар
            </button>
        </div>

        <!-- Додавання товару -->
        <div class="mb-12">
            <h2 class="text-lg font-semibold mb-4">Додавання товару</h2>
            
            <div class="overflow-x-auto border border-gray-300 rounded-2xl bg-white">
                <table class="w-full min-w-[650px]">
                    <thead>
                        <tr class="border-b text-center bg-gray-50">
                            <th class="border-r py-3 px-4">№</th>
                            <th class="border-r py-3 px-4">Найменування товару</th>
                            <th class="border-r py-3 px-4">од.виміру</th>
                            <th class="border-r py-3 px-4">кількість</th>
                            <th class="border-r py-3 px-4">ціна за одиницю</th>
                            <th class="py-3 px-4">вартість</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b text-center">
                            <td class="border-r py-4 px-2">1</td>
                            <td class="border-r px-2">
                                <select disabled="disabled">
                                    <option value="">Хліб</option>
                                    <option value="">Хліб2</option>
                                </select>
                            </td>
                            <td class="border-r px-2">
                                <select disabled="disabled">
                                    <option value="">шт.</option>
                                    <option value="">кг.</option>
                                </select>
                            </td>
                            <td class="border-r px-2">
                                <input type="text" class="w-full text-center focus:outline-none">
                            </td>
                            <td class="border-r px-2">
                                <input type="text" class="w-full text-center focus:outline-none">
                            </td>
                            <td class="px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-4">
                <button class="bg-blue-100 hover:bg-blue-200 px-6 py-3 rounded-2xl w-full sm:w-auto transition">
                    + Додати строку
                </button>
            </div>
        </div>

        <!-- Таблиця чека -->
        <div>
            <div class="overflow-x-auto border border-gray-300 rounded-2xl bg-white">
                <table class="w-full min-w-[650px]">
                    <caption class="p-4 border-b bg-amber-50">

                                <div class="flex justify-between sm:flex-row sm:items-center justify-between gap-4">
                                    
                                    <div class="flex items-center gap-2 w-full sm:w-auto">
                                        <span class="text-sm text-gray-600 whitespace-nowrap">Магазин/Місце:</span>
                                        <select 
                                            v-model="selectedMarket" 
                                            class="bg-white border border-gray-300 rounded-xl px-3 py-2 text-sm font-medium focus:outline-none focus:border-amber-400 cursor-pointer w-full sm:w-auto"
                                        >
                                            <option :value="null">-- Оберіть магазин --</option>
                                            <option 
                                                v-for="market in marketStore.markets" 
                                                :key="market.id" 
                                                :value="market.id"
                                            >
                                                {{ market.name || market.market_name }}
                                            </option>
                                        </select>
                                    </div>
                                    <!-- Поле з календарем -->
                                    <div class="flex items-center gap-2">
                                        <span class="text-sm text-gray-600 whitespace-nowrap">Дата чека:</span>
                                        <input 
                                            type="date" 
                                            v-model="checkDate"
                                            class="bg-white border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-amber-400"
                                        >
                                    </div>
                                </div>
                    </caption>
                    
                    <thead>
                        <tr class="border-b text-center bg-gray-50">
                            <th class="border-r py-3 px-4">№</th>
                            <th class="border-r py-3 px-4">Найменування товару</th>
                            <th class="border-r py-3 px-4">од.виміру</th>
                            <th class="border-r py-3 px-4">кількість</th>
                            <th class="border-r py-3 px-4">ціна за одиницю</th>
                            <th class="py-3 px-4">вартість</th>
                        </tr>
                    </thead>
                    <tbody class="text-center">
                        <tr class="border-b"
                            v-for="(item,index) in checkItems"
                            :key="index">
                            <td class="border-r py-3">{{ index+1}}</td>
                            <td class="border-r py-3">{{ item.name }}</td>
                            <td class="border-r py-3">{{ item.unit }}</td>
                            <td class="border-r py-3">{{ Number(item.qty).toFixed(1) }}</td>
                            <td class="border-r py-3">{{ Number(item.price).toFixed(2) }}</td>
                            <td class="py-3">{{ (Number(item.qty)*Number(item.price)).toFixed(2) }}</td>
                        </tr>
                        <tr v-if="checkItems.length === 0">
                            <td colspan="6" class="py-8 text-gray-400 italic bg-gray-50/50">
                                У чеку поки немає товарів. Додайте перший товар вище.
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr class="font-semibold bg-amber-50">
                            <td colspan="5" class="text-right py-4 pr-6 border-t">Разом</td>
                            <td class="py-4 text-center border-t">{{ totalSum }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    <!-- Модалка на створення -->
    <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ МАГАЗИНУ -->
        <!-- Тонкий чорний напівпрозорий фон. Показується лише якщо isMarketModalOpen === true -->
        <div v-if="isMarketModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            
            <div class="bg-white rounded-3xl p-6 w-full max-w-lg shadow-2xl relative">
                
                <h3 class="text-xl font-bold text-gray-800 mb-4">Новий магазин</h3>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Назва магазину/місця *</label>
                        <input 
                            type="text" 
                            v-model="newMarketName"
                            placeholder="Наприклад: Lidl, Aldi, Аптека"
                            class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                        >
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Країна</label>
                            <select 
                                v-model="modalCountryId"
                                class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                            >
                                <option :value="null">Оберіть країну</option>
                                <option v-for="c in countries" :key="c.id" :value="c.id">
                                    {{ c.flag_emoji }} {{ c.name_ua || c.name }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Область / Регіон</label>
                            <select 
                                v-model="modalRegionId"
                                :disabled="!modalCountryId"
                                class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
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
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Місто</label>
                            <select 
                                v-model="modalCityId"
                                :disabled="!modalRegionId"
                                class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
                            >
                                <option :value="null">Оберіть місто</option>
                                <option v-for="c in cities" :key="c.id" :value="c.id">
                                    {{ c.name_ua || c.name }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Вулиця, будинок</label>
                            <input 
                                type="text" 
                                v-model="streetAndHouse"
                                placeholder="вул. Головна, 12"
                                class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="flex justify-end gap-3 mt-6 border-t pt-4 border-gray-100">
                    <button 
                        type="button" 
                        @click="isMarketModalOpen = false"
                        class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium transition"
                    >
                        Скасувати
                    </button>
                    
                    <button 
                        type="button" 
                        @click="handleCreateMarket"
                        :disabled="!newMarketName.trim()"
                        class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-5 py-2 rounded-xl text-sm font-semibold transition"
                    >
                        Зберегти
                    </button>
                </div>
            </div>
        </div>


    <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ ТОВАРУ -->
        <!-- Тонкий чорний напівпрозорий фон. Показується лише якщо isProductModalOpen === true -->
        <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ ТОВАРУ -->
        <div v-if="isProductModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            
            <div class="bg-white rounded-3xl p-6 w-full max-w-lg shadow-2xl relative">
                
                <h3 class="text-xl font-bold text-gray-800 mb-4">Новий товар</h3>
                
                <div class="space-y-4">

                    <!-- Назва товару -->
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                            Назва товару *
                        </label>
                        <input 
                            type="text" 
                            v-model="newProductForm.name"
                            placeholder="Наприклад: Хліб, Молоко, Цукор"
                            class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                        >
                    </div>

                    <!-- Одиниця вимірювання -->
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                            Одиниця вимірювання
                        </label>
                        <select 
                            v-model="newProductForm.unit_of_measure"
                            class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                        >
                            <option value="шт">Штуки (шт)</option>
                            <option value="кг">Кілограми (кг)</option>
                            <option value="г">Грами (г)</option>
                            <option value="л">Літри (л)</option>
                            <option value="мл">Мілілітри (мл)</option>
                            <option value="м">Метри (м)</option>
                            <option value="уп">Упаковка (уп)</option>
                            <option value="кор">Коробка (кор)</option>
                        </select>
                    </div>

                </div>

                <!-- Кнопки -->
                <div class="flex justify-end gap-3 mt-6 border-t pt-4 border-gray-100">
                    <button 
                        type="button" 
                        @click="isProductModalOpen = false"
                        class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium transition"
                    >
                        Скасувати
                    </button>
                    
                    <button 
                        type="button" 
                        @click="handleCreateProduct"
                        :disabled="!newProductForm.name.trim()"
                        class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-5 py-2 rounded-xl text-sm font-semibold transition"
                    >
                        Зберегти
                    </button>
                </div>
            </div>
        </div>
    </div>

</template>