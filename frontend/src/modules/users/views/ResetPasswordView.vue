<script setup>
    import { ref, onMounted } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import { confirmPasswordReset } from '../api/users';

    const route = useRoute();
    const router = useRouter();

    const token = ref(null);
    const tokenMissing = ref(false);

    const form = ref({
        new_password: '',
        new_password_confirm: '',
    });

    const errors = ref({});
    const isLoading = ref(false);
    const successMessage = ref('');

    const showNewPassword = ref(false);
    const showNewPasswordConfirm = ref(false);

    const toggleNewPassword = () => {
        showNewPassword.value = !showNewPassword.value;
    };
    const toggleNewPasswordConfirm = () => {
        showNewPasswordConfirm.value = !showNewPasswordConfirm.value;
    };

    onMounted(() => {
        token.value = route.query.token || null;
        if (!token.value) {
            tokenMissing.value = true;
        }
    });

    const handleSubmit = async () => {
        errors.value = {};
        isLoading.value = true;

        try {
            await confirmPasswordReset({
                token: token.value,
                new_password: form.value.new_password,
                new_password_confirm: form.value.new_password_confirm,
            });

            successMessage.value = 'Пароль успішно змінено. Тепер ви можете увійти.';

            setTimeout(() => {
                router.push({ name: 'login' });
            }, 2000);
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
    <div class="flex items-center justify-center min-h-[calc(100vh-56px)] px-4 py-8 bg-gray-50/50">
        <div class="bg-white rounded-2xl border border-gray-200 shadow-xs w-full max-w-md p-6 sm:p-8">
            <!-- Заголовок -->
            <div class="mb-6 text-center">
                <h1 class="text-2xl font-bold text-gray-900">Відновлення паролю до акаунту</h1>
                <p class="text-sm text-gray-500 mt-1">Заповніть дані для відновлення доступу в системі</p>
            </div>

            <div v-if="tokenMissing" class="text-center text-rose-500">
                Посилання недійсне. Перевірте, чи скопіювали повне посилання з листа.
            </div>
            <div v-else-if="successMessage" class="text-center text-green-600">
                {{ successMessage }}
            </div>
            <form v-else @submit.prevent="handleSubmit" class="space-y-4">
                <!-- NEW Password -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Новий пароль
                        <span class="text-rose-500">*</span>
                    </label>
                    <div class="relative">
                        <input
                            v-model="form.new_password"
                            :type="showNewPassword ? 'text' : 'password'"
                            placeholder="Мінімум 8 символів"
                            :class="[
                                'w-full px-3.5 py-2.5 pr-10 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                errors.new_password
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <button
                            type="button"
                            @click="toggleNewPassword"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer text-sm select-none"
                        >
                            {{ showNewPassword ? '🙈' : '👁️' }}
                        </button>
                    </div>
                    <p v-if="errors.new_password" class="text-rose-500 text-xs mt-1">
                        {{ errors.new_password[0] }}
                    </p>
                    <p v-else class="text-xs text-gray-400 mt-1">Повинен містити не менше 8 символів</p>
                </div>

                <!-- Password Confirm -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Підтвердження паролю
                        <span class="text-rose-500">*</span>
                    </label>
                    <div class="relative">
                        <input
                            v-model="form.new_password_confirm"
                            :type="showNewPassword ? 'text' : 'password'"
                            placeholder="Повторіть пароль"
                            :class="[
                                'w-full px-3.5 py-2.5 pr-10 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                errors.new_password_confirm
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200',
                            ]"
                        />
                        <button
                            type="button"
                            @click="toggleNewPassword"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer text-sm select-none"
                        >
                            {{ showNewPassword ? '🙈' : '👁️' }}
                        </button>
                    </div>
                    <p v-if="errors.new_password_confirm" class="text-rose-500 text-xs mt-1">
                        {{ errors.new_password_confirm[0] }}
                    </p>
                </div>
                <button
                    type="submit"
                    :disabled="isLoading"
                    class="w-full bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
                >
                    {{ isLoading ? 'Збереження...' : 'Змінити пароль' }}
                </button>
            </form>
        </div>
    </div>
</template>
