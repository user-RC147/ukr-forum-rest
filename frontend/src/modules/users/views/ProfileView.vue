<script setup>
    import { ref, onMounted, computed, watch } from 'vue';
    import { useRouter } from 'vue-router';
    import { useUserStore } from '@/shared/stores/useUserStore';
    import { updateProfile } from '../api/users';

    import { useGeoSelector } from '@/shared/composables/geo/useGeoSelector';

    const { countries, regions, cities, loadCountries, onCountryChange, onRegionChange } = useGeoSelector();

    const router = useRouter();
    const userStore = useUserStore();

    // прапорець "ще триває первинне завантаження форми" —
    // поки true, watch-и на country_id/region_id нічого не роблять,
    // щоб не затирати щойно завантажені значення локації
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

    // Викликається при виході з поля
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

    // Коли вибрали країну → завантажуємо регіони
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

        // перевіряємо всі поля перед відправкою
        Object.keys(fieldErrors.value).forEach((field) => {
            fieldErrors.value[field] = validate[field](form.value[field]);
        });

        // якщо є помилки — зупиняємо
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
</script>

<template>
    <div class="flex items-center justify-center mt-8 p">
        <div class="rounded-lg shadow-md w-full max-w-sm">
            <fieldset class="border-t border-gray-400 px-6 flex items-center justify-center">
                <legend class="px-2 text-gray-700 text-sm lg:text-base">Мій профіль</legend>
            </fieldset>

            <p v-if="!userStore.user" class="text-gray-500 text-center">Завантаження...</p>

            <form v-else @submit.prevent="handleSubmit" class="space-y-4 p-6">
                <!-- повідомлення -->
                <p v-if="successMessage" class="text-green-600 text-sm text-center">
                    {{ successMessage }}
                </p>
                <p v-if="errorMessage" class="text-red-500 text-sm text-center">
                    {{ errorMessage }}
                </p>

                <!-- логін — тільки читання -->
                <div>
                    <label class="block text-sm text-gray-500 mb-1">Логін</label>
                    <p class="font-medium text-gray-800 bg-gray-50 p-4 rounded">
                        {{ userStore.user.username }}
                    </p>
                </div>

                <!-- email — тільки читання -->
                <div class="">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <div class="flex justify-between items-center">
                        <input
                            v-model="form.email"
                            type="text"
                            placeholder="Ваша електронна пошта"
                            @blur="onBlur('email')"
                            :class="[
                                'p-2 w-full rounded focus:outline-none focus:ring-2',
                                fieldErrors.email
                                    ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                                    : 'bg-amber-100 focus:ring-amber-400',
                            ]"
                        />
                        <p v-if="fieldErrors.email" class="text-red-500 text-xs mt-1">
                            {{ fieldErrors.email }}
                        </p>
                        <div class="shrink-0 ml-2 h-5">
                            <input v-model="form.email_public" type="checkbox" />
                        </div>
                    </div>
                </div>

                <!-- публічне ім'я -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Публічне ім'я (нікнейм)</label>
                    <input
                        v-model="form.display_name"
                        type="text"
                        placeholder="Ваше публічне ім'я"
                        @blur="onBlur('display_name')"
                        :class="[
                            'p-2 w-full rounded focus:outline-none focus:ring-2',
                            fieldErrors.display_name
                                ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                                : 'bg-amber-100 focus:ring-amber-400',
                        ]"
                    />
                    <p v-if="fieldErrors.display_name" class="text-red-500 text-xs mt-1">
                        {{ fieldErrors.display_name }}
                    </p>
                </div>

                <!-- вік -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Дата народження</label>
                    <div class="flex justify-between items-center gap-2">
                        <input
                            v-model="form.date_of_birth"
                            type="date"
                            min="0"
                            max="120"
                            placeholder="Ваш вік"
                            @blur="onBlur('date_of_birth')"
                            :class="[
                                'p-2 w-full rounded focus:outline-none focus:ring-2',
                                fieldErrors.date_of_birth
                                    ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                                    : 'bg-amber-100 focus:ring-amber-400',
                            ]"
                        />
                        <p v-if="fieldErrors.date_of_birth" class="text-red-500 text-xs mt-1">
                            {{ fieldErrors.date_of_birth }}
                        </p>
                        <div v-if="age !== null" class="text-sm text-gray-500 mt-1 text-center">{{ age }} років</div>

                        <div class="shrink-0 ml-2 h-5">
                            <input v-model="form.date_of_birth_public" type="checkbox" />
                        </div>
                    </div>
                </div>

                <!-- телефон -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
                    <div class="flex justify-between items-center">
                        <input
                            v-model="form.phone_number"
                            type="text"
                            placeholder="+380..."
                            @blur="onBlur('phone_number')"
                            :class="[
                                'p-2 w-full rounded focus:outline-none focus:ring-2',
                                fieldErrors.phone_number
                                    ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                                    : 'bg-amber-100 focus:ring-amber-400',
                            ]"
                        />
                        <p v-if="fieldErrors.phone_number" class="text-red-500 text-xs mt-1">
                            {{ fieldErrors.phone_number }}
                        </p>

                        <div class="shrink-0 ml-2 h-5">
                            <input v-model="form.phone_public" type="checkbox" class="" />
                        </div>
                    </div>
                </div>

                <!-- соц.мережа -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Соц.мережа</label>
                    <div class="flex justify-between items-center">
                        <input
                            v-model="form.social_network"
                            type="text"
                            placeholder="Посилання на профіль"
                            @blur="onBlur('social_network')"
                            :class="[
                                'p-2 w-full rounded focus:outline-none focus:ring-2',
                                fieldErrors.social_network
                                    ? 'bg-red-50 focus:ring-red-400 border border-red-300'
                                    : 'bg-amber-100 focus:ring-amber-400',
                            ]"
                        />
                        <p v-if="fieldErrors.social_network" class="text-red-500 text-xs mt-1">
                            {{ fieldErrors.social_network }}
                        </p>
                        <div class="shrink-0 ml-2 h-5">
                            <input v-model="form.social_public" type="checkbox" class="" />
                        </div>
                    </div>
                </div>

                <!-- referal_code -->
                <div class="flex justify-around p-1">
                    <div class="border p-1 cursor-pointer">Реферальний код</div>
                </div>

                <!-- кнопка додати іншу локацію -->
                <button
                    type="button"
                    @click="router.push({ name: 'location' })"
                    class="text-sm text-amber-600 hover:underline mt-1"
                >
                    + Додати іншу локацію
                </button>

                <!-- ЛОКАЦІЯ -->
                <fieldset class="border-t pt-4">
                    <legend class="text-sm font-medium text-gray-700 mb-3">Ваше місце локації</legend>

                    <!-- Країна -->
                    <div class="">
                        <label class="block text-sm text-gray-600 mb-1">Країна</label>
                        <div class="flex justify-between items-center mb-3">
                            <select
                                v-model="form.country_id"
                                class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                            >
                                <option :value="null">Оберіть країну</option>
                                <option v-for="c in countries" :key="c.id" :value="c.id">
                                    {{ c.flag_emoji }} {{ c.name_ua }}
                                </option>
                            </select>

                            <div class="shrink-0 ml-2 h-5">
                                <input v-model="form.country_public" type="checkbox" class="" />
                            </div>
                        </div>
                    </div>

                    <!-- Регіон -->
                    <div class="mb-3">
                        <label class="block text-sm text-gray-600 mb-1">Регіон</label>
                        <div class="flex justify-between items-center">
                            <select
                                v-model="form.region_id"
                                :disabled="!form.country_id"
                                class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-50"
                            >
                                <option :value="null">Оберіть регіон</option>
                                <option v-for="r in regions" :key="r.id" :value="r.id">
                                    {{ r.name }}
                                </option>
                            </select>
                            <div class="shrink-0 ml-2 h-5">
                                <input v-model="form.region_public" type="checkbox" class="" />
                            </div>
                        </div>
                    </div>

                    <!-- Місто -->
                    <div class="mb-3">
                        <label class="block text-sm text-gray-600 mb-1">Місто</label>
                        <div class="flex justify-between items-center">
                            <select
                                v-model="form.city_id"
                                :disabled="!form.region_id"
                                class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-50"
                            >
                                <option :value="null">Оберіть місто</option>
                                <option v-for="c in cities" :key="c.id" :value="c.id">
                                    {{ c.name }}
                                </option>
                            </select>
                            <div class="shrink-0 ml-2 h-5">
                                <input v-model="form.city_public" type="checkbox" class="" />
                            </div>
                        </div>
                    </div>
                </fieldset>

                <!-- кнопки -->
                <div class="flex justify-between gap-4 pt-2">
                    <button
                        type="button"
                        @click="router.push({ name: 'home' })"
                        class="bg-[#CEC526] rounded px-6 py-2 text-gray-800 hover:bg-[#F2E70A] transition text-sm lg:text-base"
                    >
                        Повернутися
                    </button>
                    <button
                        type="submit"
                        :disabled="isLoading"
                        class="bg-[#CEC526] rounded px-6 py-2 text-gray-800 hover:bg-[#F2E70A] disabled:opacity-50 transition text-sm lg:text-base"
                    >
                        {{ isLoading ? 'Збереження...' : 'Зберегти зміни' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
