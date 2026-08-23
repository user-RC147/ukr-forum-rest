<script setup>
    import { ref, computed, watch, onMounted } from 'vue';
    import { useRoute } from 'vue-router';


    import { useGroupStore } from '../stores/useGroupStore.js';
    import { useUserStore } from '@/shared/stores/useUserStore.js';
    import { useAssetStore } from '../stores/useAssetStore.js';
    import { usePurchaseItemStore } from '../stores/usePurchaseItemStore.js';

    import PeriodFilter from '../components/filters/PeriodFilter.vue';
    import { useMarketExpensesStore } from '../stores/useMarketExpenses.js';

    import CreateAssetModal from '../components/assets/CreateAssetModel.vue';
    import CreateGroupModel from '../components/groups/CreateGroupModal.vue';

    //======isAssetModalOpen================
    const isAssetModalOpen =ref(false)
    const isGroupModalOpen =ref(false)



    //======================

    //======PeriodFilter================

    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

    const dateTo_items = ref(formatDate(today));
    const dateFrom_items = ref(formatDate(firstDayOfMonth));
    const period_items = ref(null);

    const dateTo_market = ref(formatDate(today));
    const dateFrom_market = ref(formatDate(firstDayOfMonth));
    const period_market = ref(null);

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }


    //======================

    //=====purchaseItems =========
    const currentPageItems = ref(1);
    const pageSizeItems = ref(5);
    const purchaseItemStore = usePurchaseItemStore();

    function goNextItemsPage() {
        currentPageItems.value += 1;
        purchaseItemStore.fetchPurchaseItems(
            currentPageItems.value,
            pageSizeItems.value,
            dateFrom_items.value,
            dateTo_items.value
        );
    }

    function goPrevItemsPage() {
        currentPageItems.value -= 1;
        purchaseItemStore.fetchPurchaseItems(
            currentPageItems.value,
            pageSizeItems.value,
            dateFrom_items.value,
            dateTo_items.value
        );
    }

    //==============

    watch([dateFrom_items, dateTo_items], ([newDateFrom, newDateTo]) => {
        currentPageItems.value = 1;
        purchaseItemStore.fetchPurchaseItems(currentPageItems.value, pageSizeItems.value, newDateFrom, newDateTo);
    });

    //======MarketExpenses===========================
    const currentPageMarkets = ref(1);
    const pageSizeMarkets = ref(5);
    const marketExpensesStore = useMarketExpensesStore();

    watch([dateFrom_market, dateTo_market], ([newDateFrom, newDateTo]) => {
        currentPageMarkets.value = 1;
        marketExpensesStore.fetchMarketExpenses(
            currentPageMarkets.value,
            pageSizeMarkets.value,
            newDateFrom,
            newDateTo
        );
    });
    const marketTotal = computed(() =>
        marketExpensesStore.marketExpenses.reduce((s, item) => s + parseFloat(item.total), 0).toFixed(2)
    );

    function goPrevMarketPage() {
        currentPageMarkets.value -= 1;
        marketExpensesStore.fetchMarketExpenses(
            currentPageMarkets.value,
            pageSizeMarkets.value,
            dateFrom_market.value,
            dateTo_market.value
        );
    }

    function goNextMarketPage() {
        currentPageMarkets.value += 1;
        marketExpensesStore.fetchMarketExpenses(
            currentPageMarkets.value,
            pageSizeMarkets.value,
            dateFrom_market.value,
            dateTo_market.value
        );
    }

    //=================================

    //===Group====
    const groupStore = useGroupStore();
    const selectedGroup = ref(null); // Тут зберігається id вибраної групи
    const activeMember = ref(null);

    const selectedGroupMembers = computed(() => {
        const users = groupStore.groups.find((group) => group.id === selectedGroup.value);

        if (users) {
            // Обгортаємо власника у форму, схожу на GroupMemberOutDTO,
            // щоб <select> міг однаково звертатись через member.user.username
            const ownerAsMember = {
                id: `owner-${users.created_by.id}`, // унікальний id, щоб не перетнутись з id звичайних members
                user: users.created_by,
                role: { id: 0, name: 'creator', name_ua: 'Власник' },
            };

            // concat об'єднує два масиви "на одному рівні" (без вкладеності)
            // тут: масив з одним елементом (власник) + масив звичайних учасників
            return [ownerAsMember].concat(users.members);
        } else {
            return [];
        }
    });

    watch(selectedGroupMembers, (newMembers) => {
        const found = newMembers.find((member) => member.user.id === userStore.user.id);
        activeMember.value = found ? found.id : null;
    });

    //=======

    const userStore = useUserStore(); //ref() // замінити на store.user.username

    const assetStore = useAssetStore();
    const selectedAsset = ref(null);

    onMounted(() => {
        groupStore.fetchGroups();
        // При старті завантажуємо активи для "Всіх груп" (запит піде без group_id)
        assetStore.fetchAssets();
        purchaseItemStore.fetchPurchaseItems(
            currentPageItems.value,
            pageSizeItems.value,
            dateFrom_items.value,
            dateTo_items.value
        );

        marketExpensesStore.fetchMarketExpenses(
            currentPageMarkets.value,
            pageSizeMarkets.value,
            dateFrom_market.value,
            dateTo_market.value
        );
    });

    // Обробник модалки Asset
    async function handleAssetCreated(formData) {
        await assetStore.addAsset(formData);
        isAssetModalOpen.value = false
        
    }

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

    const totalSum = computed(() =>
        purchaseItemStore.purchaseItems
            .reduce((s, item) => s + parseFloat(item.quantity) * parseFloat(item.price_per_unit), 0)
            .toFixed(2)
    );
</script>

<template>
    <div class="max-w-5xl mx-auto px-4 py-6">
        <!-- Фільтри -->
        <div class="flex flex-wrap justify-between gap-4 mb-6">

            <!-- Кнопки створення обєка-asset-->
            <div class="grid grid-cols-2 gap-4 mb-10">
                <button
                    type="button"
                    @click="isAssetModalOpen = true"
                    class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold text-sm transition"
            >
                    + Створити об'єкт
                </button>
              
            </div>

            <!-- Об'єкт -->
            <div class="flex flex-col gap-2">
                <!-- <router-link
                    :to="{ name: 'household-asset-create', query: selectedGroup ? { group_id: selectedGroup } : {} }"
                    class="inline-block bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold transition"
                >
                    + Створити об'єкт
                </router-link> -->

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
                        <option v-for="g in groupStore.groups" :key="g.id" :value="g.id">
                            {{ g.name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Кнопка додати чек -->
        <div class="flex justify-between mb-6">
            <router-link
                :to="{
                    name: 'household-purchases-create',
                    query: {
                        group_id: selectedGroup,
                        asset_id: selectedAsset,
                    },
                }"
                class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold text-sm transition"
            >
                + Додати чек
            </router-link>

            <div class="flex flex-col gap-2 justify-center">
                <select class="border-0" v-model="activeMember">
                    <option class="text-center bg-blue-100" :value="null">Учасники групи</option>
                    <option
                        class="text-center"
                        v-for="member in selectedGroupMembers"
                        :key="member.id"
                        :value="member.id"
                    >
                        {{ member.user.username }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Таблиця витрат -->
        <div class="border border-gray-200 rounded-2xl overflow-hidden bg-white mb-8">
            <div class="flex justify-between items-center px-4 py-3 bg-amber-50 border-b border-gray-200 text-sm">
                <div class="font-medium">Загальні витрати за період</div>
                <PeriodFilter
                    v-model:period="period_items"
                    v-model:date-from="dateFrom_items"
                    v-model:date-to="dateTo_items"
                />
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
                        <tr v-for="(item, i) in purchaseItemStore.purchaseItems" :key="i" class="text-center">
                            <td class="border border-gray-200 px-3 py-2">{{ i + 1 }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.product.name }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.product.unit_of_measure.code }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.quantity }}</td>
                            <td class="border border-gray-200 px-3 py-2">{{ item.price_per_unit }}</td>
                            <td class="border border-gray-200 px-3 py-2">
                                {{ (parseFloat(item.quantity) * parseFloat(item.price_per_unit)).toFixed(2) }}
                            </td>
                        </tr>
                    </tbody>
                    <tfoot class="bg-amber-50 font-semibold">
                        <tr>
                            <td colspan="5" class="border border-gray-200 px-3 py-2 text-right">Разом</td>
                            <td class="border border-gray-200 px-3 py-2 text-center">{{ totalSum }}</td>
                        </tr>
                    </tfoot>
                </table>
                <div class="flex justify-center items-center gap-4 py-3 border-t border-gray-200">
                    <button
                        class="px-2 rounded border"
                        @click="goPrevItemsPage"
                        :disabled="!purchaseItemStore.paginator?.has_previous"
                    >
                        ← Попередня
                    </button>

                    <div v-if="purchaseItemStore.paginator">
                        Сторінка {{ purchaseItemStore.paginator.page }} із
                        {{ purchaseItemStore.paginator.total_pages }}
                    </div>
                    <button
                        class="px-2 rounded border"
                        @click="goNextItemsPage"
                        :disabled="!purchaseItemStore.paginator?.has_next"
                    >
                        Наступна →
                    </button>
                </div>
            </div>
        </div>

        <!-- Таблиця магазинів + фільтр -->
        <div class="flex flex-wrap gap-6 items-start">
            <!-- Таблиця магазинів -->
            <div class="flex-1 min-w-75 border border-gray-200 rounded-2xl overflow-hidden bg-white">
                <div class="flex justify-between px-4 py-3 bg-amber-50 border-b border-gray-200 text-sm font-medium">
                    <span>інші магазини</span>
                    <PeriodFilter
                        v-model:period="period_market"
                        v-model:date-from="dateFrom_market"
                        v-model:date-to="dateTo_market"
                    />
                </div>
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
                            <tr v-for="(market, i) in marketExpensesStore.marketExpenses" :key="i" class="text-center">
                                <td class="border border-gray-200 px-3 py-2">{{ i + 1 }}</td>
                                <td class="border border-gray-200 px-3 py-2">{{ market.name }}</td>
                                <td class="border border-gray-200 px-3 py-2">
                                    {{ market.location.country.name }},
                                    <!-- {{ market.location.region.name}}, -->
                                    {{ market.location.city.name }},
                                    {{ market.address_line }}
                                </td>
                                <td class="border border-gray-200 px-3 py-2">{{ market.total }}</td>
                            </tr>
                        </tbody>
                        <tfoot class="bg-amber-50 font-semibold">
                            <tr>
                                <td colspan="3" class="border border-gray-200 px-3 py-2 text-right">Разом</td>
                                <td class="border border-gray-200 px-3 py-2 text-center">{{ marketTotal }}</td>
                            </tr>
                        </tfoot>
                    </table>
                    <div class="flex justify-center items-center gap-4 py-3 border-t border-gray-200">
                        <button
                            class="px-2 rounded border"
                            @click="goPrevMarketPage"
                            :disabled="!marketExpensesStore.paginator?.has_previous"
                        >
                            ← Попередня
                        </button>

                        <div v-if="marketExpensesStore.paginator">
                            Сторінка {{ marketExpensesStore.paginator.page }} із
                            {{ marketExpensesStore.paginator.total_pages }}
                        </div>
                        <button
                            class="px-2 rounded border"
                            @click="goNextMarketPage"
                            :disabled="!marketExpensesStore.paginator?.has_next"
                        >
                            Наступна →
                        </button>
                    </div>
                </div>
            </div>

            <!-- Фільтр по датах -->
            <!-- <div class="bg-blue-50 rounded-2xl p-4 text-sm min-w-[180px]">
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
            </div> -->
        </div>

         <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ ОБЄКТУ -->
        <CreateAssetModal
            v-if="isAssetModalOpen"
            :selected-group="selectedGroup"
            @submit="handleAssetCreated"
            @cancel="isAssetModalOpen = false"
        />
    </div>
</template>
