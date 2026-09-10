<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../api/users'
import { useUserStore } from '@/shared/stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()

const showPassword = ref(false)
const togglePassword = () => {
    showPassword.value = !showPassword.value
}

const form = ref({
    username: '',
    display_name: '',
    email: '',
    password: '',
    password_confirm: '',
    consent_given: false,
})

const errors = ref({})
const isLoading = ref(false)

const handleSubmit = async () => {
    isLoading.value = true
    errors.value = {}

    try {
        await registerUser(form.value)
        

        // await userStore.login({
        //     username: form.value.username,
        //     password: form.value.password,
        // })

        //router.push({ name: 'home' })

        router.push({ name: 'check-email' })
    } catch (error) {
        if (error.response?.data) {
            errors.value = error.response.data
        }
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <div class="flex items-center justify-center min-h-[calc(100vh-56px)] px-4 py-8 bg-gray-50/50">
        <div class="bg-white rounded-2xl border border-gray-200 shadow-xs w-full max-w-md p-6 sm:p-8">

            <!-- Заголовок -->
            <div class="mb-6 text-center">
                <h1 class="text-2xl font-bold text-gray-900">Створення акаунту</h1>
                <p class="text-sm text-gray-500 mt-1">Заповніть дані для реєстрації в системі</p>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-4">

                <!-- Загальні помилки (non_field_errors) -->
                <div v-if="errors.non_field_errors" class="p-3.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-sm font-medium">
                    {{ errors.non_field_errors[0] }}
                </div>

                <!-- Username -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Логін <span class="text-rose-500">*</span>
                    </label>
                    <input
                        v-model="form.username"
                        type="text"
                        placeholder="Ваш унікальний логін"
                        :class="[
                            'w-full px-3.5 py-2.5 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                            errors.username
                                ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200'
                        ]"
                    />
                    <p v-if="errors.username" class="text-rose-500 text-xs mt-1">
                        {{ errors.username[0] }}
                    </p>
                </div>

                <!-- Display Name -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Публічне ім'я
                    </label>
                    <input
                        v-model="form.display_name"
                        type="text"
                        placeholder="Ім'я, яке бачитимуть інші"
                        :class="[
                            'w-full px-3.5 py-2.5 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                            errors.display_name
                                ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200'
                        ]"
                    />
                    <p v-if="errors.display_name" class="text-rose-500 text-xs mt-1">
                        {{ errors.display_name[0] }}
                    </p>
                </div>

                <!-- Email -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Email <span class="text-rose-500">*</span>
                    </label>
                    <input
                        v-model="form.email"
                        type="email"
                        autocomplete="email"
                        required
                        placeholder="your@email.com"
                        :class="[
                            'w-full px-3.5 py-2.5 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                            errors.email
                                ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200'
                        ]"
                    />
                    <p v-if="errors.email" class="text-rose-500 text-xs mt-1">
                        {{ errors.email[0] }}
                    </p>
                </div>

                <!-- Password -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Пароль <span class="text-rose-500">*</span>
                    </label>
                    <div class="relative">
                        <input
                            v-model="form.password"
                            :type="showPassword ? 'text' : 'password'"
                            placeholder="Мінімум 8 символів"
                            :class="[
                                'w-full px-3.5 py-2.5 pr-10 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                errors.password
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200'
                            ]"
                        />
                        <button
                            type="button"
                            @click="togglePassword"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer text-sm select-none"
                        >
                            {{ showPassword ? '🙈' : '👁️' }}
                        </button>
                    </div>
                    <p v-if="errors.password" class="text-rose-500 text-xs mt-1">
                        {{ errors.password[0] }}
                    </p>
                    <p v-else class="text-xs text-gray-400 mt-1">
                        Повинен містити не менше 8 символів
                    </p>
                </div>

                <!-- Password Confirm -->
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Підтвердження паролю <span class="text-rose-500">*</span>
                    </label>
                    <div class="relative">
                        <input
                            v-model="form.password_confirm"
                            :type="showPassword ? 'text' : 'password'"
                            placeholder="Повторіть пароль"
                            :class="[
                                'w-full px-3.5 py-2.5 pr-10 text-sm rounded-lg border transition focus:outline-none focus:ring-2',
                                errors.password_confirm
                                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-400'
                                    : 'border-gray-300 focus:border-amber-500 focus:ring-amber-200'
                            ]"
                        />
                        <button
                            type="button"
                            @click="togglePassword"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer text-sm select-none"
                        >
                            {{ showPassword ? '🙈' : '👁️' }}
                        </button>
                    </div>
                    <p v-if="errors.password_confirm" class="text-rose-500 text-xs mt-1">
                        {{ errors.password_confirm[0] }}
                    </p>
                </div>

                <!-- Consent Given -->
                <div class="pt-2">
                    <label class="inline-flex items-start gap-2.5 cursor-pointer text-sm text-gray-600">
                        <input
                            v-model="form.consent_given"
                            type="checkbox"
                            class="mt-0.5 rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                        />
                        <span>Я погоджуюся з <a href="#" class="text-amber-600 hover:underline font-medium">правилами використання</a> сервісу</span>
                    </label>
                    <p v-if="errors.consent_given" class="text-rose-500 text-xs mt-1">
                        {{ errors.consent_given[0] }}
                    </p>
                </div>

                <!-- Кнопка сабміту -->
                <button
                    type="submit"
                    :disabled="isLoading"
                    class="w-full mt-2 py-3 px-4 text-sm font-semibold text-gray-900 bg-amber-400 hover:bg-amber-500 disabled:opacity-50 rounded-lg shadow-xs transition cursor-pointer"
                >
                    {{ isLoading ? 'Завантаження...' : 'Зареєструватися' }}
                </button>

                <!-- Посилання на логін -->
                <p class="text-center text-sm text-gray-500 pt-2">
                    Вже є акаунт?
                    <RouterLink to="/auth/login" class="font-medium text-amber-600 hover:text-amber-700 hover:underline">
                        Увійти
                    </RouterLink>
                </p>

            </form>
        </div>
    </div>
</template>