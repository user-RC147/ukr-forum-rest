<script setup>
    import { ref, computed, watch, onMounted } from 'vue';
    import { useGroupStore } from '../stores/useGroupStore.js';
    import { useUserStore } from '@/shared/stores/useUserStore.js';
    import { useAssetStore } from '../stores/useAssetStore.js';

    const groupStore = useGroupStore();
    const selectedGroup = ref(null); // Тут зберігається id вибраної групи

    const userStore = useUserStore(); //ref() // замінити на store.user.username

    const assetStore = useAssetStore();
    const selectedAsset = ref(null);

    // Тільки групи де поточний user є учасником
    // const myGroups = computed(() =>
    //     groupStore.groups.filter((group) => group.members.some((member) => member.user_id === userStore.user?.id))
    // );

    onMounted(() => {
        groupStore.fetchGroups();
        // При старті завантажуємо активи для "Всіх груп" (запит піде без group_id)
        assetStore.fetchAssets();
    });

    watch(selectedGroup, (newGroupId) => {
        // Скидаємо вибраний актив при зміні групи
        selectedAsset.value = null;

        if (newGroupId) {
            // Передаємо id групи в оновлений стор (тепер запит піде як ?group_id=X)
            assetStore.fetchAssets(newGroupId);
        } else {
            // Якщо обрано "Всі групи", викликаємо без аргументів.
            // Бекенд поверне активи всіх груп цього користувача
            assetStore.fetchAssets();
        }
    });

    // Тимчасові дані — замінити на реальні з API
    const purchases = ref([
        { name: 'хліб', unit: 'шт.', qty: '1,0', price: '2,03', total: '2.03' },
        { name: 'булочка', unit: 'шт.', qty: '1,0', price: '2,03', total: '2.03' },
        { name: 'молоко', unit: 'шт.', qty: '1,0', price: '2,03', total: '2.03' },
    ]);

    const shops = ref([
        { name: 'Lidl', location: 'Altenessener Str. 289, Essen', total: '6.09' },
        { name: 'Kaufland', location: 'Strlost Str. 33, Essen', total: '200.2' },
        { name: 'Aldi', location: 'Bonden Str. 2, Essen', total: '300.2' },
    ]);

    const totalSum = computed(() => purchases.value.reduce((s, i) => s + parseFloat(i.total), 0).toFixed(2));
    const shopsTotal = computed(() => shops.value.reduce((s, i) => s + parseFloat(i.total), 0).toFixed(2));
</script>

<template>
    <div class="max-w-5xl mx-auto px-4 py-6">
        <!-- Фільтри -->
        <div class="flex flex-wrap justify-between gap-4 mb-6">
            <!-- Об'єкт -->
            <div class="flex flex-col gap-2">
                <router-link
                    :to="{ name: 'household-asset-create', query: selectedGroup ? { group_id: selectedGroup } : {} }"
                    class="inline-block bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold transition"
                >
                    + Створити об'єкт
                </router-link>

                <div class="bg-amber-100 px-4 py-2 rounded-2xl">
                    <select v-model="selectedAsset" class="bg-transparent focus:outline-none text-sm">
                        <option :value="null">Всі об'єкти</option>
                        <option v-for="asset in assetStore.assets" :key="asset.id" :value="asset.id">
                            {{ asset.name }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- Група -->
            <div class="flex flex-col gap-2">
                <router-link
                    :to="{ name: 'household-group-create' }"
                    class="inline-block bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold transition"
                >
                    + Створити групу
                </router-link>
                <div class="bg-amber-100 px-4 py-2 rounded-2xl">
                    <select v-model="selectedGroup" class="bg-transparent focus:outline-none text-sm">
                        <option :value="null">Всі групи</option>
                        <option v-for="g in groupStore.groups" :key="g.group.id" :value="g.group.id">
                            {{ g.group.name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Кнопка додати чек -->
        <div class="mb-6">
            <router-link
                :to="{ name: 'household-purchases-create',
                    query: { 
                            group_id: selectedGroup, 
                            asset_id: selectedAsset 
                        }
                 }"
                class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold text-sm transition"
            >
                + Додати чек
            </router-link>
        </div>

        <!-- Таблиця витрат -->
        <div class="border border-gray-200 rounded-2xl overflow-hidden bg-white mb-8">
            <div class="flex justify-between items-center px-4 py-3 bg-amber-50 border-b border-gray-200 text-sm">
                <span class="font-medium">Загальні витрати за період</span>
                <select class="bg-transparent focus:outline-none text-sm cursor-pointer">
                    <option disabled selected>За весь період</option>
                    <option>День</option>
                    <option>Тиждень</option>
                    <option>Місяць</option>
                    <option>Квартал</option>
                    <option>Рік</option>
                </select>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full min-w-[600px] text-sm border-collapse">
                    <thead class="bg-gray-50 font-semibold">
                        <tr>
                            <th class="border border-gray-200 px-3 py-2">№</th>
                            <th class="border border-gray-200 px-3 py-2">Найменування товару</th>
                            <th class="border border-gray-200 px-3 py-2">од.виміру</th>
                            <th class="border border-gray-200 px-3 py-2">кількість</th>
                            <th class="border border-gray-200 px-3 py-2">ціна за одиницю</th>
                            <th class="border border-gray-200 px-3 py-2">вартість</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, i) in purchases" :key="i" class="text-center">
                            <td class="border border-gray-200 px-3 py-2">{{ i + 1 }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.name }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.unit }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.qty }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.price }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.total }}</td>
                        </tr>
                    </tbody>
                    <tfoot class="bg-amber-50 font-semibold">
                        <tr>
                            <td colspan="5" class="border border-gray-200 px-3 py-2 text-right">Разом</td>
                            <td class="border border-gray-200 px-3 py-2 text-center">{{ totalSum }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>

        <!-- Таблиця магазинів + фільтр -->
        <div class="flex flex-wrap gap-6 items-start">
            <!-- Таблиця магазинів -->
            <div class="flex-1 min-w-[300px] border border-gray-200 rounded-2xl overflow-hidden bg-white">
                <div class="px-4 py-3 bg-amber-50 border-b border-gray-200 text-sm font-medium">інші магазини</div>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse">
                        <thead class="bg-gray-50 font-semibold">
                            <tr>
                                <th class="border border-gray-200 px-3 py-2">№</th>
                                <th class="border border-gray-200 px-3 py-2">Назва магазину</th>
                                <th class="border border-gray-200 px-3 py-2">Локація</th>
                                <th class="border border-gray-200 px-3 py-2">Всього витрат</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(shop, i) in shops" :key="i" class="text-center">
                                <td class="border border-gray-200 px-3 py-2">{{ i + 1 }}</td>
                                <td class="border border-gray-200 px-3 py-2">{{ shop.name }}</td>
                                <td class="border border-gray-200 px-3 py-2">{{ shop.location }}</td>
                                <td class="border border-gray-200 px-3 py-2">{{ shop.total }}</td>
                            </tr>
                        </tbody>
                        <tfoot class="bg-amber-50 font-semibold">
                            <tr>
                                <td colspan="3" class="border border-gray-200 px-3 py-2 text-right">Разом</td>
                                <td class="border border-gray-200 px-3 py-2 text-center">{{ shopsTotal }}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>

            <!-- Фільтр по датах -->
            <div class="bg-blue-50 rounded-2xl p-4 text-sm min-w-[180px]">
                <div class="font-medium mb-2">Період сортування</div>
                <select class="bg-transparent focus:outline-none text-sm cursor-pointer mb-4 w-full">
                    <option disabled selected>За весь період</option>
                    <option>День</option>
                    <option>Тиждень</option>
                    <option>Місяць</option>
                    <option>Квартал</option>
                    <option>Рік</option>
                </select>
                <div class="flex flex-col gap-2">
                    <span>
                        з
                        <input type="date" class="border border-gray-300 rounded-lg px-2 py-1 text-sm ml-1" />
                    </span>
                    <span>
                        по
                        <input type="date" class="border border-gray-300 rounded-lg px-2 py-1 text-sm ml-1" />
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>
