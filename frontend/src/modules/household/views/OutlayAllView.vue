<script setup>
    import { ref, computed, watch, onMounted } from 'vue';
    import { useGroupStore } from '../stores/useGroupStore.js';
    import { useUserStore } from '@/shared/stores/useUserStore.js';
    import { useAssetStore } from '../stores/useAssetStore.js';
    import { usePurchaseItemStore } from '../stores/usePurchaseItemStore.js';

    //=====purchaseItems =========
    const currentPage = ref(1);
    const purchaseItemStore = usePurchaseItemStore();

    function goNextPage() {
        currentPage.value += 1;
        purchaseItemStore.fetchPurchaseItems(currentPage.value);
    }

    function goPrevPage() {
        currentPage.value -= 1;
        purchaseItemStore.fetchPurchaseItems(currentPage.value);
    }

    //==============

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
        purchaseItemStore.fetchPurchaseItems(currentPage.value);
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

    const totalSum = computed(() =>
        purchaseItemStore.purchaseItems
            .reduce((s, item) => s + parseFloat(item.quantity) * parseFloat(item.price_per_unit), 0)
            .toFixed(2)
    );
    //const shopsTotal = computed(() => shops.value.reduce((s, i) => s + parseFloat(i.total), 0).toFixed(2));
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
                <div class="flex justify-between">
                    <select class="bg-transparent focus:outline-none text-sm cursor-pointer mx-6 w-full">
                        <option disabled selected>За весь період</option>
                        <option>День</option>
                        <option>Тиждень</option>
                        <option>Місяць</option>
                        <option>Квартал</option>
                        <option>Рік</option>
                    </select>
                    <div class="flex gap-2">
                        <div class="flex items-center justify-end">
                            <span>з</span>
                            <input type="date" class="border border-gray-300 p-1 ml-2 rounded-lg text-sm" />
                        </div>
                        <div class="flex items-center justify-end">
                            <span>по</span>
                            <input type="date" class="border border-gray-300 p-1 ml-2 rounded-lg text-sm" />
                        </div>
                    </div>
                </div>
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
                <div class="text-center">десь тут пагінація</div>
            </div>
        </div>

        <!-- Таблиця магазинів + фільтр -->
        <div class="flex flex-wrap gap-6 items-start">
            <!-- Таблиця магазинів -->
            <div class="flex-1 min-w-75 border border-gray-200 rounded-2xl overflow-hidden bg-white">
                <div class="flex justify-between px-4 py-3 bg-amber-50 border-b border-gray-200 text-sm font-medium">
                    <span>інші магазини</span>
                    <div class="flex justify-between">
                        <select class="bg-transparent focus:outline-none text-sm cursor-pointer mx-6 w-full">
                            <option disabled selected>За весь період</option>
                            <option>День</option>
                            <option>Тиждень</option>
                            <option>Місяць</option>
                            <option>Квартал</option>
                            <option>Рік</option>
                        </select>
                        <div class="flex gap-2">
                            <div class="flex items-center justify-end">
                                <span>з</span>
                                <input type="date" class="border border-gray-300 p-1 ml-2 rounded-lg text-sm" />
                            </div>
                            <div class="flex items-center justify-end">
                                <span>по</span>
                                <input type="date" class="border border-gray-300 p-1 ml-2 rounded-lg text-sm" />
                            </div>
                        </div>
                    </div>
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
    </div>
</template>
