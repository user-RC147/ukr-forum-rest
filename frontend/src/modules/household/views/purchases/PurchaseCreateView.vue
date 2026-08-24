<script setup>
    import { ref, computed, onMounted, watch } from 'vue';
    import { useRoute } from 'vue-router';

    import { useGroupStore } from '../../stores/useGroupStore';
    import { useAssetStore } from '../../stores/useAssetStore';
    import { useUserStore } from '@/shared/stores/useUserStore';
    import { useMarketStore } from '../../stores/useMarketStore';
    import { useProductStore } from '../../stores/useProductStore';
    import { useUnitOfMeasureStore } from '../../stores/useUnitOfMeasureStore';
    import { useCategoryStore } from '../../stores/useCategoryStore';
    import { usePurchaseStore } from '../../stores/usePurchaseStore';

    import CreateProductModal from '../../components/products/CreateProductModal.vue';
    import CreateMarketModal from '../../components/markets/CreateMarketModal.vue';

    // Ініціалізуємо сховища даних
    const purchaseStore = usePurchaseStore();
    const categoryStore = useCategoryStore();
    const groupStore = useGroupStore();
    const assetStore = useAssetStore();
    const userStore = useUserStore();
    const marketStore = useMarketStore();
    const productStore = useProductStore();
    const unit_of_measureStore = useUnitOfMeasureStore();
    const route = useRoute();

    // Поля «шапки» чека
    const selectedGroup = ref(route.query.group_id ? Number(route.query.group_id) : null);
    const selectedAsset = ref(route.query.asset_id ? Number(route.query.asset_id) : null);

    // Виправлено: змінна називається selectedMarket, оскільки у шаблоні v-model="selectedMarket"
    const selectedMarket = ref(null);
    const checkDate = ref(new Date().toISOString().substr(0, 10));

    // Масив чернеток — кожен елемент це один рядок таблиці
    const draftItem = ref({
        product_id: null,
        name: '',
        unit: '',
        qty: 1,
        price: 0,
    });

    function addItemToCheck() {
        if (!draftItem.value.product_id) return;
        if (!draftItem.value.price) return;

        checkItems.value.push({ ...draftItem.value });

        draftItem.value = {
            product_id: null,
            name: '',
            unit: null,
            qty: 1,
            price: 0,
        };
    }

    function removeItemFromCheck(index) {
        checkItems.value.splice(index, 1);
    }

    // Масив уже доданих до чека товарів
    const checkItems = ref([]);

    // Змінна контролю модалки
    const isMarketModalOpen = ref(false);
    const isProductModalOpen = ref(false);
    // const newProductForm=ref({
    //     name:'',
    //     unit_of_measure:'шт' // ← точно як у Django моделі
    // });

    // Тимчасові дані для форми створення нового магазину
    const newMarketName = ref('');
    const streetAndHouse = ref('');

    // Стан обраних ID у формі модалки
    const modalCountryId = ref(null);
    const modalRegionId = ref(null);
    const modalCityId = ref(null);

    // Загальна сума чека
    const totalSum = computed(() => {
        return checkItems.value.reduce((sum, item) => sum + Number(item.qty) * Number(item.price), 0).toFixed(2);
    });

    onMounted(async () => {
        await Promise.all([
            categoryStore.fetchCategories(),
            groupStore.fetchGroups(),
            assetStore.fetchAssets(),
            //userStore.fetchProfile(),
            marketStore.fetchMarkets(),
            productStore.fetchProducts(),
            unit_of_measureStore.fetchUnitOfMeasures(),
        ]);
    });

    // Обробник модалки магазину
    async function handleMarketCreated(formData) {
        await marketStore.addMarket(formData);
        isMarketModalOpen.value = false;
    }

    // Обробник модалки товару
    async function handleProductCreated(formData) {
        await productStore.addProduct(formData);
        isProductModalOpen.value = false;
    }

    // Слідкуємо за зміною групи
    watch(selectedGroup, (newGroupId) => {
        selectedAsset.value = null;
        if (newGroupId) {
            assetStore.fetchAssets(newGroupId);
        } else {
            assetStore.fetchAssets();
        }
    });

    watch(
        () => draftItem.value.product_id,
        (productId) => {
            if (!productId) {
                draftItem.value.name = '';
                draftItem.value.unit = '';
                return;
            }
            const product = productStore.products.find((p) => p.id === productId);
            if (product) {
                draftItem.value.name = product.name;
                draftItem.value.unit = product.unit_of_measure;
            }
        }
    );

    async function handleSavePurchase() {
        if (!selectedMarket.value) return;
        if (!selectedAsset.value) return;
        if (checkItems.value.length === 0) return;

        const payload = {
            asset_id: selectedAsset.value,
            market_id: selectedMarket.value,
            data_purchase: checkDate.value,

            items: checkItems.value.map((item) => ({
                product_id: item.product_id,
                quantity: Number(item.qty),
                price_per_unit: Number(item.price),
            })),
        };

        await purchaseStore.createPurchase(payload);
    }
</script>

<template>
    <div class="max-w-5xl mx-auto px-4 py-6">
        <!-- Верхній рядок: Повернутися + Зберегти -->
        <div class="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-4 mb-6">
            <router-link
                :to="{ name: 'household-index' }"
                class="flex items-center justify-center bg-[#cce9f8] hover:bg-[#aedbf4] text-[#2e332e] px-5 py-3 rounded-xl text-sm font-medium transition transform hover:scale-105 w-full sm:w-auto"
            >
                ← Повернутися
            </router-link>

            <button
                type="button"
                @click="handleSavePurchase"
                :disabled="!selectedAsset || checkItems.length === 0"
                class="bg-[#CEC526] hover:bg-[#F2E70A] text-[#33332E] text-lg font-semibold px-5 py-3 rounded-xl transition transform hover:scale-105 w-full sm:w-auto"
            >
                Зберегти
            </button>
        </div>

        <!-- Фільтри це обєкт до якого привязується чек -->
        <div class="flex flex-wrap justify-around mb-8">
            <div class="bg-amber-100 px-4 py-3 rounded-2xl flex min-w-[130px]">
                <select v-model="selectedAsset" class="w-full bg-transparent focus:outline-none">
                    <option :value="null">Всі об'єкти</option>
                    <option v-for="asset in assetStore.assets" :key="asset.id" :value="asset.id">
                        {{ asset.name }}: {{ asset.location.country.name }}-{{ asset.location.city.name }}
                    </option>
                </select>
            </div>
            <div class="bg-amber-100 px-4 py-3 rounded-2xl flex min-w-[130px]">
                <select v-model="selectedGroup" class="w-full bg-transparent focus:outline-none">
                    <option :value="null">Всі групи</option>

                    <option v-for="group in groupStore.groups" :key="group.id" :value="group.id">
                        {{ group.name }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Кнопки створення магазин,товар-->
        <div class="grid grid-cols-2 gap-4 mb-10">
            <button
                type="button"
                @click="isMarketModalOpen = true"
                class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold text-sm transition"
            >
                створити магазин
            </button>

            <button
                class="bg-amber-50 hover:bg-amber-100 text-center py-4 rounded-2xl transition"
                type="button"
                @click="isProductModalOpen = true"
            >
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
                                <select v-model="draftItem.product_id" class="w-full text-center focus:outline-none">
                                    <option :value="null">-- обрати --</option>
                                    <option v-for="p in productStore.products" :key="p.id" :value="p.id">
                                        {{ p.name }}
                                    </option>
                                </select>
                            </td>
                            <td class="border-r px-2">{{ draftItem.unit?.code }}</td>
                            <td class="border-r px-2">
                                <input
                                    type="number"
                                    v-model="draftItem.qty"
                                    class="w-full text-center focus:outline-none"
                                />
                            </td>
                            <td class="border-r px-2">
                                <input
                                    type="number"
                                    v-model="draftItem.price"
                                    class="w-full text-center focus:outline-none"
                                />
                            </td>
                            <td class="px-2">{{ (Number(draftItem.qty) * Number(draftItem.price)).toFixed(2) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-4">
                <button
                    type="button"
                    @click="addItemToCheck"
                    class="bg-blue-100 hover:bg-blue-200 px-6 py-3 rounded-2xl w-full sm:w-auto transition"
                >
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
                                    <option v-for="market in marketStore.markets" :key="market.id" :value="market.id">
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
                                />
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
                            <th class="py-3 px-4">дія</th>
                        </tr>
                    </thead>
                    <tbody class="text-center">
                        <tr class="border-b" v-for="(item, index) in checkItems" :key="index">
                            <td class="border-r py-3">{{ index + 1 }}</td>
                            <td class="border-r py-3">{{ item.name }}</td>
                            <td class="border-r py-3">{{ item.unit?.code }}</td>
                            <td class="border-r py-3">
                                <input type="number" v-model="item.qty" class="w-full text-center focus:outline-none" />
                            </td>
                            <td class="border-r py-3">
                                <input
                                    type="number"
                                    v-model="item.price"
                                    class="w-full text-center focus:outline-none"
                                />
                            </td>
                            <td class="py-3">{{ (Number(item.qty) * Number(item.price)).toFixed(2) }}</td>
                            <td class="py-3">
                                <button
                                    type="button"
                                    @click="removeItemFromCheck(index)"
                                    class="text-red-500 hover:text-red-700 text-sm"
                                >
                                    ✕
                                </button>
                            </td>
                        </tr>
                        <tr v-if="checkItems.length === 0">
                            <td colspan="6" class="py-8 text-gray-400 italic bg-gray-50/50">
                                У чеку поки немає товарів. Додайте перший товар вище.
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr class="font-semibold bg-amber-50">
                            <td colspan="6" class="text-right py-4 pr-6 border-t">Разом</td>
                            <td class="py-4 text-center border-t">{{ totalSum }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
        <!-- Модалка на створення -->
        <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ МАГАЗИНУ -->
        <!-- Тонкий чорний напівпрозорий фон. Показується лише якщо isMarketModalOpen === true -->
        <!-- <div v-if="isMarketModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            
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
        </div> -->

        <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ ТОВАРУ -->
        <!-- Тонкий чорний напівпрозорий фон. Показується лише якщо isProductModalOpen === true -->
        <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ ТОВАРУ -->

        <CreateProductModal
            v-if="isProductModalOpen"
            :units="unit_of_measureStore.units"
            :categories="categoryStore.categories"
            @submit="handleProductCreated"
            @cancel="isProductModalOpen = false"
        />

        <CreateMarketModal 
            v-if="isMarketModalOpen" 
            @submit="handleMarketCreated" 
            @cancel="isMarketModalOpen = false"
        />
    </div>
</template>
