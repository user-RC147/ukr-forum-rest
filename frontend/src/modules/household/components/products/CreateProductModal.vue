<script setup>
    import { ref } from 'vue';

    // Оголошуємо які події компонент може кидати назовні
    const emit = defineEmits(['submit', 'cancel']);

    const props = defineProps({
        units: { type: Array, default: () => [] },
        categories: { type: Array, default: () => [] },
    });

    // Локальний стан форми — тільки всередині компонента
    const form = ref({
        name: '',
        category_id: null,
        unit_of_measure_id: null,
    });


    function handleSubmit(){
        if(!form.value.name.trim())return
        emit('submit',{ ...form.value })
    }

    function handleCancel() {
        emit('cancel');
    }
</script>


<template>
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-3xl p-6 w-full max-w-lg shadow-2xl relative">
            <h3 class="text-xl font-bold text-gray-800 mb-4">Новий товар</h3>

            <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                    Категорія
                </label>

                <select
                    v-model="form.category_id"
                    class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                >
                    <option :value="null">
                        Без категорії
                    </option>

                    <option
                        v-for="cat in categories"
                        :key="cat.id"
                        :value="cat.id"
                    >
                        {{ cat.name }}
                    </option>
                </select>
            </div>

            <div class="space-y-4">
                <!-- Назва товару -->
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                        Назва товару *
                    </label>
                    <input
                        type="text"
                        v-model="form.name"
                        placeholder="Наприклад: Хліб, Молоко, Цукор"
                        class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                    />
                </div>

                <!-- Одиниця вимірювання -->
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                        Одиниця вимірювання
                    </label>
                    <select
                        v-model="form.unit_of_measure_id"
                        class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                    >
                        <option v-for="unit in units" :key="unit.id" :value="unit.id">
                            {{ unit.name }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- Кнопки -->
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
