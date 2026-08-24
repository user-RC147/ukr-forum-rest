<script setup>
    import { onMounted, ref } from 'vue';
    import { useGeoSelector } from '@/shared/composables/geo/useGeoSelector';

    const { countries, regions, cities, loading, loadCountries, onCountryChange, onRegionChange } = useGeoSelector();

    const props = defineProps({
        selectedGroup: {
            type: [Number, Object],
            default: null,
        },
        // countries: { type: Array, default: () => [] },
        // regions: { type: Array, default: () => [] },
        // cities: { type: Array, default: () => [] },
    });

    const emit = defineEmits(['submit', 'cancel']);

    // Завантажуємо країни, коли модалка з'являється на екрані
    onMounted(() => {
        if (typeof loadCountries === 'function') {
            loadCountries();
        }
    });

    const form = ref({
        group_id: props.selectedGroup?.id || null, // Автоматично беремо ID переданої групи
        name: '',
        address_line: '',
        country_id: null,
        region_id: null,
        city_id: null,
    });

    function handleCountryChange() {
        form.value.region_id = null;
        form.value.city_id = null;
        onCountryChange(form.value.country_id);
    }

    function handleRegionChange() {
        form.value.city_id = null;
        onRegionChange(form.value.region_id);
    }

    function handleSubmit() {
        if (!props.selectedGroup) {
            error.value = 'Виберіть групу';
            return;
        }



        if (!form.value.name.trim()) return;
        if (!form.value.country_id) return;
        if (!form.value.region_id) return;
        if (!form.value.city_id) return;
        emit('submit', { ...form.value });
    }

    function handleCancel() {
        emit('cancel');
    }
</script>

<template>
    <div  class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-3xl p-6 w-full max-w-lg shadow-2xl relative">
            <h3 class="text-xl font-bold text-gray-800 mb-4">Новий об'єкт</h3>

            <div class="space-y-4">
                <!-- Група (автоматично з фільтру) -->
                <div class="flex flex-col gap-1">
                    
                    <div class="">
                        <span class="text-sm font-medium">Група:</span>
                        {{ selectedGroup?.name || 'Групу не вибрано' }}
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                        Назва об'єкту/місця *
                    </label>
                    <input
                        type="text"
                        v-model="form.name"
                        placeholder="Наприклад: Meerkamp, Авто, Дача"
                        class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                    />
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                            Країна
                        </label>
                        <select
                            v-model="form.country_id"
                            @change="handleCountryChange"
                            class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                        >
                            <option :value="null">Оберіть країну</option>
                            <option v-for="c in countries" :key="c.id" :value="c.id">
                                {{ c.flag_emoji }} {{ c.name_ua || c.name }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                            Область / Регіон
                        </label>
                        <select
                            v-model="form.region_id"
                            :disabled="!form.country_id"
                            @change="handleRegionChange"
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
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                            Місто
                        </label>
                        <select
                            v-model="form.city_id"
                            :disabled="!form.region_id"
                            class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
                        >
                            <option :value="null">Оберіть місто</option>
                            <option v-for="c in cities" :key="c.id" :value="c.id">
                                
                                {{ c.name_ua || c.name }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                            Вулиця, будинок
                        </label>
                        <input
                            type="text"
                            v-model="form.address_line"
                            placeholder="вул. Головна, 12"
                            class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                        />
                    </div>
                </div>
            </div>

            <div class="flex justify-end gap-3 mt-6 border-t pt-4 border-gray-100">
                <button
                    type="button"
                    @click="handleCancel"
                    class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium transition"
                >
                    Скасувати
                </button>

                <button
                    type="button"
                    @click="handleSubmit"
                    :disabled="!form.name.trim()"
                    class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-5 py-2 rounded-xl text-sm font-semibold transition"
                >
                    Зберегти
                </button>
            </div>
        </div>
    </div>
</template>
