<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { registerUser } from '../api/users'
import { getCountries, getRegions, getCities } from '../../geo/api/geo'

const router = useRouter();

const showPassword = ref(false);

const togglePassword = () => {
    showPassword.value = !showPassword.value;
};

const form = ref({
    username: '',
    email: '',
    password: '',
    password2: '',
    country_id: null,
    region_id: null,
    city_id: null,
});

const errors   = ref({});
const isLoading = ref(false);

// Списки для dropdown
const countries = ref([]);
const regions   = ref([]);
const cities    = ref([]);

// Вибрані об'єкти (для відображення назви)
const selectedCountry = ref(null);
const selectedRegion  = ref(null);


// Завантажуємо країни при старті
onMounted(async () => {
    const res = await getCountries();
    countries.value = res.data  //res.data.results;
});

// Коли вибрали країну — завантажуємо регіони
watch(() => form.value.country_id, async (countryId) => {
    form.value.region_id = null;
    form.value.city_id   = null;
    regions.value = [];
    cities.value  = [];

    if (countryId) {
        selectedCountry.value = countries.value.find(c => c.id === countryId);
        const res = await getRegions(selectedCountry.value.code);
        regions.value = res.data.results;
    }
});

// Коли вибрали регіон — завантажуємо міста
watch(() => form.value.region_id, async (regionId) => {
    form.value.city_id = null;
    cities.value = [];

    if (regionId) {
        const res = await getCities(regionId);
        cities.value = res.data.results;
    }
});

const handleSubmit = async () => {
    isLoading.value = true;
    errors.value    = {};

    try {
        await registerUser(form.value);
        router.push({ name: 'login' });
    } catch (error) {
        if (error.response?.data) {
            errors.value = error.response.data;
        }
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <fieldset class="border-y p-8 mx-auto mt-8 max-w-md shadow-xl">
        <legend class="mx-auto px-2 text-gray-700">Реєстрація нового користувача</legend>

        <form @submit.prevent="handleSubmit" class="space-y-4">

            <!-- username -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Логін</label>
                <input
                    v-model="form.username"
                    type="text"
                    class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    placeholder="Ваш логін"
                />
                <p v-if="errors.username" class="text-red-500 text-sm mt-1">
                    {{ errors.username[0] }}
                </p>
            </div>

            <!-- email -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                    v-model="form.email"
                    type="email"
                    class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    placeholder="your@email.com"
                />
                <p v-if="errors.email" class="text-red-500 text-sm mt-1">
                    {{ errors.email[0] }}
                </p>
            </div>

            <!-- password -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
                <div class="relative">
                     <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    type="password"
                    class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    placeholder="Мінімум 8 символів"
                />
                <p class="text-[10px] text-center">Тільки літери, цифри та @/./+/-/_.</p>
                    <button 
                        type="button" 
                        @click="togglePassword"
                        class="absolute right-2 top-1/2 transform -translate-y-1/4 text-gray-500 hover:text-gray-700"
                    >
                        <!-- Іконка (наприклад, око) -->
                        <span v-if="!showPassword">👁️</span>
                        <span v-else>🙈</span>
                    </button>

                </div>
               
                <p v-if="errors.password" class="text-red-500 text-sm mt-1">
                    {{ errors.password[0] }}
                </p>
            </div>

            <!-- password2 -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                    Підтвердження паролю
                </label>
                <div class="relative">
                    <input
                        v-model="form.password2"
                        :type="showPassword ? 'text' : 'password'"
                        type="password"
                        class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                        placeholder="Повторіть пароль"
                    />
                    <p class="text-[10px] text-center">Тільки літери, цифри та @/./+/-/_.</p>
                    <button 
                        type="button" 
                        @click="togglePassword"
                        class="absolute right-2 top-1/2 transform -translate-y-1/4 text-gray-500 hover:text-gray-700"
                    >
                        <!-- Іконка (наприклад, око) -->
                        <span v-if="!showPassword">👁️</span>
                        <span v-else>🙈</span>
                    </button>

                </div>
               
                <p v-if="errors.password2" class="text-red-500 text-sm mt-1">
                    {{ errors.password2[0] }}
                </p>
            </div>

            <!-- Локація -->
            <fieldset class="border-t pt-4">
                <legend class="text-sm font-medium text-gray-700 mb-2">
                    Місце проживання (необов'язково)
                </legend>

                <!-- Країна -->
                <div class="mb-3">
                    <label class="block text-sm text-gray-600 mb-1">Країна</label>
                    <select
                        v-model="form.country_id"
                        class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    >
                        <option :value="null">Оберіть країну</option>
                        <option v-for="c in countries" :key="c.id" :value="c.id">
                            {{ c.flag_emoji }} {{ c.name }}
                        </option>
                    </select>
                </div>

                <!-- Регіон -->
                <div class="mb-3">
                    <label class="block text-sm text-gray-600 mb-1">Регіон</label>
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
                </div>

                <!-- Місто -->
                <div>
                    <label class="block text-sm text-gray-600 mb-1">Місто</label>
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
                </div>
            </fieldset>

            <!-- загальні помилки -->
            <p v-if="errors.non_field_errors" class="text-red-500 text-sm">
                {{ errors.non_field_errors[0] }}
            </p>

            <!-- кнопка -->
            <button
                type="submit"
                :disabled="isLoading"
                class="bg-[#CEC526] w-full rounded p-2 text-gray-800 text-lg hover:bg-[#F2E70A] disabled:opacity-50 transition"
            >
                {{ isLoading ? 'Завантаження...' : 'Зареєструватися' }}
            </button>

            <!-- посилання на логін -->
            <p class="text-center text-sm text-gray-600">
                Вже є акаунт?
                <RouterLink to="/auth/login" class="text-amber-600 hover:underline">
                    Увійти
                </RouterLink>
            </p>
        </form>
    </fieldset>
</template>