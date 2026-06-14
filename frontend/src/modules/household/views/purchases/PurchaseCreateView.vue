<script setup>
import {ref,computed,onMounted,watch} from 'vue';
// 1. Імпортуємо useRoute, щоб мати доступ до поточного URL
import {useRoute} from 'vue-router';

import { useGroupStore } from '../../stores/useGroupStore';
import { useAssetStore } from '../../stores/useAssetStore';
import { useUserStore } from '../../../users/stores/useUserStore';

// Ініціалізуємо сховища даних
const groupStore=useGroupStore();
const assetStore = useAssetStore();
const userStore=useUserStore();

// 2. Ініціалізуємо роут
const route=useRoute();

// Поля «шапки» чека
/*****************************************************************
 * 3. ПРИВ'ЯЗУЄМО ДАНІ З URL ДО НАШИХ ЗМІННИХ
 * Якщо в URL є ?group_id=..., ми беремо його і перетворюємо на число (Number).
 * Якщо параметрів немає, залишаємо null.
 *****************************************************************/
const selectedGroup=ref(route.query.group_id ? Number(route.query.group_id):null); // ID обраної сімейної групи
const selectedAsset=ref(route.query.asset_id ? Number(route.query.asset_id):null); // ID обраного об'єкта (активу)

const selectedShop=ref(null); // ID обраного магазину
const checkDate=ref(new Date().toISOString().substr(0,10)); // Поточна дата за замовчуванням (YYYY-MM-DD)

// Тимчасові реактивні змінні для полів "Додавання товару" (новий рядок)
const newProduct=ref({
    name:'',
    unit:'шт.',
    qty:1,
    price:0

});

// Масив уже доданих до чека товарів (динамічна таблиця)
const checkItems=ref([
    // Поки залишаємо тестові дані, щоб бачити їх у таблиці:
    { name: 'Хліб', unit: 'шт.', qty: 1.0, price: 4.03, total: 2.03 },
    { name: 'Булочка', unit: 'шт.', qty: 1.0, price: 2.03, total: 2.03 }
])

// Загальна сума чека
const totalSum=computed(()=>{
    return checkItems.value.reduce((sum,item)=>sum+(Number(item.qty)*Number(item.price)),0).toFixed(2);
});

onMounted(async ()=>{
    // Паралельно завантажуємо групи та активи користувача
    await Promise.all([
        groupStore.fetchGroups(),
        assetStore.fetchAssets(),
        userStore.fetchProfile()
    ]);
});



// Додаємо watch для відстеження зміни вибраної групи
watch(selectedGroup,(newGroupId)=>{
    // Скидаємо вибраний об'єкт, бо він не належить новій групі
    selectedAsset.value=null;

    if (newGroupId){
        // Якщо обрано конкретну групу, вантажимо її активи
        assetStore.fetchAssets(newGroupId);
    }else{
        // Якщо обрано "Всі групи", вантажимо активи всіх доступних груп
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
            <a href="#" 
            class="bg-amber-50 hover:bg-amber-100 text-center py-4 rounded-2xl transition">
                створити магазин
            </a>
            <a href="#" 
            class="bg-amber-50 hover:bg-amber-100 text-center py-4 rounded-2xl transition">
                створити товар
            </a>
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
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
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
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <select class="bg-transparent font-medium focus:outline-none">
                                <option>Lidl - Altenessener Str. 289, 45326 Essen</option>
                                <option>Aldi - Setree Str. 4, 45326 Essen</option>
                            </select>
                            <!-- Поле з календарем -->
                            <div class="flex items-center gap-2">
                                <span class="text-sm text-gray-600 whitespace-nowrap">Дата чека:</span>
                                <input 
                                    type="date" 
                                    name="check_date"
                                    value="2026-05-14" 
                                    class="bg-white border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-amber-400">
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

    </div>

</template>