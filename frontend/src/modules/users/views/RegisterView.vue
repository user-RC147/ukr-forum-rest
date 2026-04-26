<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { registerUser } from '../../../api/users';

    const router = useRouter();

    // ref — це реактивна змінна, коли вона змінюється — Vue оновлює UI
    const form = ref({
        username: '',
        email: '',
        password: '',
    });

    const errors = ref({});
    const isLoading = ref(false);

    const handleSubmit = async () => {
        isLoading.value = true;
        errors.value = {};

        try {
            await registerUser(form.value);
            // після успішної реєстрації — переходимо на логін
            router.push({ name: 'login' });
        } catch (error) {
            // Django повертає помилки як об'єкт { username: [...], password: [...] }
            if (error.response?.data) {
                errors.value = error.response.data;
            }
        } finally {
            // finally виконується завжди — і при успіху і при помилці
            isLoading.value = false;
        }
    };
</script>

<template>
    <fieldset class="border-y p-8 mx-auto mt-8 max-w-md shadow-xl">
        <legend class="mx-5 text-gray-700">Реєстрація нового користувача</legend>

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
                <!-- помилки від Django -->
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
                <input
                    v-model="form.password"
                    type="password"
                    class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    placeholder="Мінімум 8 символів"
                />
                <p v-if="errors.password" class="text-red-500 text-sm mt-1">
                    {{ errors.password[0] }}
                </p>
            </div>

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
                <RouterLink to="/auth/login" class="text-amber-600 hover:underline">Увійти</RouterLink>
            </p>
        </form>
    </fieldset>
</template>
