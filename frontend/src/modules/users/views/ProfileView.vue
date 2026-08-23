<script setup>
    import { ref, onMounted, computed, watch } from 'vue';
    import { useRouter } from 'vue-router';
    import { useUserStore } from '@/shared/stores/useUserStore';
    import { updateProfile, deleteAccount} from '../api/users';
    import { useGeoSelector } from '@/shared/composables/geo/useGeoSelector';
    import DeleteUserModel from '../components/user/DeleteUserModel.vue';


    const { countries, regions, cities, loadCountries, onCountryChange, onRegionChange } = useGeoSelector();

    const isDeleteUserModalOpen = ref(false);

    const router = useRouter();
    const userStore = useUserStore();

    const isInitializing = ref(true);
    const isLoading = ref(false);
    const successMessage = ref('');
    const errorMessage = ref('');

    // Форма профілю
    const form = ref({
        display_name: '',
        first_name: '',
        first_name_public: false,
        last_name: '',
        last_name_public: false,
        email: '',
        email_public: false,
        phone_number: '',
        phone_public: false,
        date_of_birth: null,
        date_of_birth_public: false,
        social_network: '',
        social_public: false,
        country_id: null,
        country_public: false,
        region_id: null,
        region_public: false,
        city_id: null,
        city_public: false,
    });

    // Помилки валідації
    const fieldErrors = ref({
        display_name: '',
        phone_number: '',
        date_of_birth: '',
        social_network: '',
    });

    // Правила валідації
    const validate = {
        display_name: (val) => {
            if (val && val.length > 100) return 'Максимум 100 символів';
            return '';
        },
        phone_number: (val) => {
            if (val && !/^\+?[\d\s\-()]{7,20}$/.test(val)) return 'Невірний формат телефону';
            return '';
        },
        date_of_birth: (val) => {
            if (val) {
                const birthDate = new Date(val);
                const today = new Date();
                if (birthDate > today) return 'Дата народження не може бути в майбутньому';
            }
            return '';
        },
        social_network: (val) => {
            if (val && val.length > 150) return 'Максимум 150 символів';
            return '';
        },
    };

    const onBlur = (field) => {
        fieldErrors.value[field] = validate[field](form.value[field]);
    };

    const age = computed(() => {
        if (!form.value.date_of_birth) return null;

        const birthDate = new Date(form.value.date_of_birth);
        const today = new Date();

        let years = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            years--;
        }

        return years;
    });

    onMounted(async () => {
        await userStore.fetchProfile();
        await loadCountries();

        if (userStore.user) {
            form.value.display_name = userStore.user.display_name || '';
            form.value.first_name = userStore.user.first_name || '';
            form.value.first_name_public = userStore.user.first_name_public || false;
            form.value.last_name = userStore.user.last_name || '';
            form.value.last_name_public = userStore.user.last_name_public || false;
            form.value.email = userStore.user.email || '';
            form.value.email_public = userStore.user.email_public || false;
            form.value.date_of_birth = userStore.user.date_of_birth || null;
            form.value.date_of_birth_public = userStore.user.date_of_birth_public || false;
            form.value.social_network = userStore.user.social_network || '';
            form.value.social_public = userStore.user.social_public || false;
            form.value.phone_number = userStore.user.phone_number || '';
            form.value.phone_public = userStore.user.phone_public || false;
            form.value.country_public = userStore.user.country_public || false;
            form.value.region_public = userStore.user.region_public || false;
            form.value.city_public = userStore.user.city_public || false;
        }

        if (userStore.user?.location) {
            form.value.country_id = userStore.user.location.country?.id || null;
            form.value.region_id = userStore.user.location.region?.id || null;
            form.value.city_id = userStore.user.location.city?.id || null;

            if (form.value.country_id) {
                await onCountryChange(form.value.country_id);
            }
            if (form.value.region_id) {
                await onRegionChange(form.value.region_id);
            }
        }

        isInitializing.value = false;
    });

    watch(
        () => form.value.country_id,
        (countryId) => {
            if (isInitializing.value) return;
            form.value.region_id = null;
            form.value.city_id = null;
            onCountryChange(countryId);
        }
    );

    watch(
        () => form.value.region_id,
        (regionId) => {
            if (isInitializing.value) return;
            form.value.city_id = null;
            onRegionChange(regionId);
        }
    );

    const handleSubmit = async () => {
        isLoading.value = true;
        successMessage.value = '';
        errorMessage.value = '';

        Object.keys(fieldErrors.value).forEach((field) => {
            fieldErrors.value[field] = validate[field](form.value[field]);
        });

        if (Object.values(fieldErrors.value).some((e) => e)) {
            isLoading.value = false;
            return;
        }

        try {
            await updateProfile(userStore.user.id, {
                display_name: form.value.display_name,
                first_name: form.value.first_name,
                first_name_public: form.value.first_name_public,
                last_name: form.value.last_name,
                last_name_public: form.value.last_name_public,
                email: form.value.email,
                email_public: form.value.email_public,
                date_of_birth: form.value.date_of_birth,
                date_of_birth_public: form.value.date_of_birth_public,
                phone_number: form.value.phone_number,
                phone_public: form.value.phone_public,
                social_network: form.value.social_network,
                social_public: form.value.social_public,
                country_public: form.value.country_public,
                region_public: form.value.region_public,
                city_public: form.value.city_public,
                location: {
                    country_id: form.value.country_id,
                    region_id: form.value.region_id,
                    city_id: form.value.city_id,
                },
            });

            await userStore.fetchProfile();
            successMessage.value = 'Профіль успішно оновлено!';
        } catch (error) {
            errorMessage.value = 'Помилка збереження. Спробуйте ще раз.';
        } finally {
            isLoading.value = false;
        }
    };

    const handleDeleteUser = async () => {
        isDeleteUserModalOpen.value = false;

        try {
            await deleteAccount(userStore.user.id);
            await userStore.logout();
            router.push({ name: 'login' });
        } catch (error) {
            errorMessage.value = 'Не вдалося видалити профіль. Спробуйте ще раз.';
        }
    };


</script>

<template>
    <div class="max-w-4xl mx-auto my-8 px-4">
        <!-- Заголовок сторінки -->
        <div class="mb-6 flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold text-gray-900">Налаштування профілю</h1>
                <p class="text-sm text-gray-500">Керуйте власними даними та їх видимістю для інших користувачів</p>
            </div>
            <button
                type="button"
                @click="router.push({ name: 'home' })"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-xs hover:bg-gray-50 transition"
            >
                Назад
            </button>
        </div>

        <div v-if="!userStore.user" class="flex justify-center items-center p-12 bg-white rounded-xl shadow-xs">
            <p class="text-gray-500 font-medium">Завантаження даних профілю...</p>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Повідомлення про статус -->
            <div
                v-if="successMessage"
                class="p-4 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-xl text-sm font-medium"
            >
                {{ successMessage }}
            </div>
            <div
                v-if="errorMessage"
                class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-sm font-medium"
            >
                {{ errorMessage }}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Секція: Основні дані -->
                <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-xs space-y-4">
                    <h2 class="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-3">
                        Загальна інформація
                    </h2>

                    <!-- Логін -->
                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                            Логін
                        </label>
                        <input
                            type="text"
                            :value="userStore.user.username"
                            disabled
                            class="w-full px-3.5 py-2 bg-gray-100 text-gray-600 rounded-lg border border-gray-200 cursor-not-allowed font-medium text-sm"
                        />
                    </div>

                    <!-- Публічне ім'я -->
                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                            Публічне ім'я (нікнейм)
                        </label>
                        <input
                            v-model="form.display_name"
                            type="text"
                            placeholder="Ваше публічне ім'я"
                            @blur="onBlur('display_name')"
                            :class="[
                                'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                fieldErrors.display_name
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <p v-if="fieldErrors.display_name" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.display_name }}
                        </p>
                    </div>

                    <!-- last_name-->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Прізвище</label>
                            <label
                                class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500 hover:text-gray-700"
                            >
                                <input
                                    v-model="form.last_name_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічний</span>
                            </label>
                        </div>

                        <!-- @blur="onBlur('last_name')" -->
                        <input
                            v-model="form.last_name"
                            type="text"
                            placeholder="Ваше прізвище"
                            
                            :class="[
                                'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                fieldErrors.last_name
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <p v-if="fieldErrors.last_name" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.last_name }}
                        </p>
                    </div>

                    <!-- first_name-->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Ім'я</label>
                            <label
                                class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500 hover:text-gray-700"
                            >
                                <input
                                    v-model="form.first_name_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічний</span>
                            </label>
                        </div>
                        <!-- @blur="onBlur('first_name')" -->
                        <input
                            v-model="form.first_name"
                            type="text"
                            placeholder="Ваше ім'я" 
                            
                            :class="[
                                'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                fieldErrors.first_name
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <p v-if="fieldErrors.first_name" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.first_name }}
                        </p>
                    </div>
                    

                    <!-- Дата народження -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">
                                Дата народження
                            </label>
                            <label
                                class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500 hover:text-gray-700"
                            >
                                <input
                                    v-model="form.date_of_birth_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічне</span>
                            </label>
                        </div>
                        <div class="flex items-center gap-3">
                            <input
                                v-model="form.date_of_birth"
                                type="date"
                                @blur="onBlur('date_of_birth')"
                                :class="[
                                    'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                    fieldErrors.date_of_birth
                                        ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                        : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                                ]"
                            />
                            <span
                                v-if="age !== null"
                                class="shrink-0 text-xs font-semibold bg-amber-50 text-amber-700 px-2.5 py-1 rounded-full border border-amber-200"
                            >
                                {{ age }} років
                            </span>
                        </div>
                        <p v-if="fieldErrors.date_of_birth" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.date_of_birth }}
                        </p>
                    </div>

                    <!-- Реферальний код -->
                    <div class="pt-2">
                        <div
                            class="flex items-center justify-between p-3 bg-amber-50/50 border border-amber-200/60 rounded-lg text-amber-900"
                        >
                            <span class="text-xs font-semibold uppercase tracking-wider">Реферальний код</span>
                            <button
                                type="button"
                                class="text-xs font-medium text-amber-700 hover:text-amber-800 underline cursor-pointer"
                            >
                                Показати / Скопіювати
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Секція: Контакти -->
                <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-xs space-y-4">
                    <h2 class="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-3">Контактні дані</h2>

                    <!-- Email -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Email</label>
                            <label
                                class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500 hover:text-gray-700"
                            >
                                <input
                                    v-model="form.email_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічний</span>
                            </label>
                        </div>
                        <input
                            v-model="form.email"
                            type="email"
                            placeholder="mail@example.com"
                            @blur="onBlur('email')"
                            :class="[
                                'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                fieldErrors.email
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <p v-if="fieldErrors.email" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.email }}
                        </p>
                    </div>

                    <!-- Телефон -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Телефон</label>
                            <label
                                class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500 hover:text-gray-700"
                            >
                                <input
                                    v-model="form.phone_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічний</span>
                            </label>
                        </div>
                        <input
                            v-model="form.phone_number"
                            type="text"
                            placeholder="+380..."
                            @blur="onBlur('phone_number')"
                            :class="[
                                'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                fieldErrors.phone_number
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <p v-if="fieldErrors.phone_number" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.phone_number }}
                        </p>
                    </div>

                    <!-- Соц. мережа -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">
                                Соц. мережа
                            </label>
                            <label
                                class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500 hover:text-gray-700"
                            >
                                <input
                                    v-model="form.social_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічна</span>
                            </label>
                        </div>
                        <input
                            v-model="form.social_network"
                            type="text"
                            placeholder="https://..."
                            @blur="onBlur('social_network')"
                            :class="[
                                'w-full px-3.5 py-2 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                fieldErrors.social_network
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <p v-if="fieldErrors.social_network" class="text-rose-500 text-xs mt-1">
                            {{ fieldErrors.social_network }}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Секція: Локація -->
            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-xs space-y-4">
                <div class="flex items-center justify-between border-b border-gray-100 pb-3">
                    <h2 class="text-lg font-semibold text-gray-900">Місцезнаходження</h2>
                    <button
                        type="button"
                        @click="router.push({ name: 'location' })"
                        class="text-xs font-semibold text-amber-600 hover:text-amber-700 transition"
                    >
                        + Додати іншу локацію
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Країна -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Країна</label>
                            <label class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500">
                                <input
                                    v-model="form.country_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічна</span>
                            </label>
                        </div>
                        <select
                            v-model="form.country_id"
                            class="w-full px-3.5 py-2 text-sm bg-white rounded-lg border border-gray-300 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 focus:outline-none transition"
                        >
                            <option :value="null">Оберіть країну</option>
                            <option v-for="c in countries" :key="c.id" :value="c.id">
                                {{ c.flag_emoji }} {{ c.name_ua }}
                            </option>
                        </select>
                    </div>

                    <!-- Регіон -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Регіон</label>
                            <label class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500">
                                <input
                                    v-model="form.region_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічний</span>
                            </label>
                        </div>
                        <select
                            v-model="form.region_id"
                            :disabled="!form.country_id"
                            class="w-full px-3.5 py-2 text-sm bg-white rounded-lg border border-gray-300 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 focus:outline-none disabled:bg-gray-100 disabled:opacity-60 transition"
                        >
                            <option :value="null">Оберіть регіон</option>
                            <option v-for="r in regions" :key="r.id" :value="r.id">
                                {{ r.name }}
                            </option>
                        </select>
                    </div>

                    <!-- Місто -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="text-xs font-semibold uppercase tracking-wider text-gray-500">Місто</label>
                            <label class="inline-flex items-center gap-1.5 cursor-pointer text-xs text-gray-500">
                                <input
                                    v-model="form.city_public"
                                    type="checkbox"
                                    class="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                                />
                                <span>Публічне</span>
                            </label>
                        </div>
                        <select
                            v-model="form.city_id"
                            :disabled="!form.region_id"
                            class="w-full px-3.5 py-2 text-sm bg-white rounded-lg border border-gray-300 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 focus:outline-none disabled:bg-gray-100 disabled:opacity-60 transition"
                        >
                            <option :value="null">Оберіть місто</option>
                            <option v-for="c in cities" :key="c.id" :value="c.id">
                                {{ c.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Дії та знищення акаунту -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-200">
                <button
                    type="button"
                    @click="isDeleteUserModalOpen = true"
                    class="px-4 py-2 text-xs font-semibold text-rose-600 bg-rose-50 hover:bg-rose-100 rounded-lg border border-rose-200 transition cursor-pointer"
                >
                    Видалити профіль
                </button>

                <div class="flex gap-3">
                    <button
                        type="button"
                        @click="router.push({ name: 'home' })"
                        class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition cursor-pointer"
                    >
                        Скасувати
                    </button>
                    <button
                        type="submit"
                        :disabled="isLoading"
                        class="px-6 py-2.5 text-sm font-semibold text-gray-900 bg-amber-400 hover:bg-amber-500 disabled:opacity-50 rounded-lg shadow-xs transition cursor-pointer"
                    >
                        {{ isLoading ? 'Збереження...' : 'Зберегти зміни' }}
                    </button>
                </div>
            </div>
        </form>

        <DeleteUserModel
            v-if="isDeleteUserModalOpen"
            @submit="handleDeleteUser"
            @cancel="isDeleteUserModalOpen = false"
        />
    </div>
</template>
