<script setup>
    import { ref, onMounted } from 'vue';
    import { getPublicProfile } from '@/modules/users/api/users'; // вкажіть шлях до вашого API

    const props = defineProps({
        userId: {
            type: [Number, String],
            required: true,
        },
    });

    const emit = defineEmits(['cancel']);

    const user = ref(null);
    const loading = ref(true);
    const error = ref(null);

    const fetchUserProfile = async () => {
        loading.value = true;
        error.value = null;
        try {
            const response = await getPublicProfile(props.userId);
            user.value = response.data.results;
        } catch (err) {
            error.value = err.response?.data?.detail || 'Не вдалося завантажити профіль';
        } finally {
            loading.value = false;
        }
    };

    onMounted(() => {
        fetchUserProfile();
    });

    function handleCancel() {
        emit('cancel');
    }
</script>

<template>
    <div
        class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
        @click.self="handleCancel"
    >
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden relative transition-all">
            <!-- Шапка з градієнтом -->
            <div class="bg-[#cce9f9] h-24 p-4 relative">
                <button
                    type="button"
                    @click="handleCancel"
                    class="absolute top-3 right-3 text-black hover:text-white bg-white/20 hover:bg-white/20 w-8 h-8 rounded-full flex items-center justify-center transition-colors cursor-pointer"
                >
                    ✕
                </button>
            </div>

            <!-- Стан завантаження -->
            <div v-if="loading" class="text-center py-12 text-slate-500 font-medium animate-pulse">
                Завантаження профілю...
            </div>

            <!-- Стан помилки -->
            <div v-else-if="error" class="text-center py-12 px-6 text-red-500 font-medium">
                {{ error }}
            </div>

            <!-- Контент профілю -->
            <div v-else-if="user" class="px-6 pb-6 -mt-10 relative">
                <!-- Аватар та основні дані -->
                <div class="flex items-end space-x-4 mb-6">
                    <div class="mb-1">
                        <h2 class="text-xl font-bold text-slate-900 leading-tight">
                            {{ user.display_name }}
                        </h2>
                        <span
                            class="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-50 text-blue-600 border border-blue-100"
                        >
                            Публічний профіль
                        </span>
                    </div>
                </div>

                <!-- Сітка з картками даних -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                    <!-- ПІБ -->
                    <div class="p-3 rounded-xl bg-slate-50 border border-slate-100 sm:col-span-2">
                        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                            Повне ім'я
                        </span>
                        <p v-if="user.first_name || user.last_name" class="font-medium text-slate-800">
                            {{ [user.first_name, user.last_name].filter(Boolean).join(' ') }}
                        </p>
                        <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                    </div>

                    <!-- Email -->
                    <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
                        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                            Email
                        </span>
                        <p v-if="user.email" class="font-medium text-slate-800 truncate" :title="user.email">
                            {{ user.email }}
                        </p>
                        <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                    </div>

                    <!-- Телефон -->
                    <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
                        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                            Телефон
                        </span>
                        <p v-if="user.phone_number" class="font-medium text-slate-800">
                            {{ user.phone_number }}
                        </p>
                        <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                    </div>

                    <!-- Дата народження -->
                    <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
                        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                            Дата народження
                        </span>
                        <p v-if="user.date_of_birth" class="font-medium text-slate-800">
                            {{ user.date_of_birth }}
                        </p>
                        <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                    </div>
                    <!-- Соцмережі -->
                    <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
                        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                            Соціальні мережі
                        </span>
                        <a
                            v-if="user.social_network"
                            :href="user.social_network"
                            target="_blank"
                            class="text-blue-600 hover:text-blue-700 font-medium hover:underline break-all block"
                        >
                            {{ user.social_network }}
                        </a>
                        <p v-else class="text-slate-400 italic text-xs">Не вказані</p>
                    </div>

                    <!-- Локація -->
                    <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
                        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                            Локація
                        </span>
                        <div>
                            <p
                                v-if="user.location.country"
                                class="font-medium text-slate-800 truncate"
                                :title="user.location.country"
                            >
                                {{ user.location?.country.name || 'Приховане або відсутнє' }}
                            </p>
                            <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                        </div>
                        <div>
                            <p v-if="user.location.region" class="font-medium text-slate-800 truncate">
                                {{ user.location?.region.name || 'Приховане або відсутнє' }}
                            </p>
                            <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                        </div>
                        <div>
                            <p v-if="user.location.city" class="font-medium text-slate-800 truncate">
                                {{ user.location?.city.name || 'Приховане або відсутнє' }}
                            </p>
                            <p v-else class="text-slate-400 italic text-xs">Приховане або відсутнє</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
