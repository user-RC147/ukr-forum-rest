<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../api/users'
import { useUserStore } from '@/shared/stores/useUserStore'  // ← додали

const router    = useRouter()
const userStore = useUserStore()  // ← додали

const showPassword = ref(false)
const togglePassword = () => {
    showPassword.value = !showPassword.value
}

const form = ref({
    username:  '',
    display_name:'',
    email:     '',
    password:  '',
    password_confirm: '',
    consent_given: false,
})

const errors    = ref({})
const isLoading = ref(false)

const handleSubmit = async () => {
    isLoading.value = true
    errors.value    = {}

    try {
        // реєструємо
        await registerUser(form.value)

        // автологін
        await userStore.login({
            username: form.value.username,
            password: form.value.password,
        })

        // redirect на профіль
        router.push({ name: 'home' })
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
    <div class="flex items-center justify-center min-h-[calc(100vh-56px)] px-4 py-8">
        <div class="bg-white rounded-lg shadow-md w-full max-w-sm p-6 lg:p-8">

            <fieldset class="border-t px-4 pb-2 mb-4">
                <legend class=" px-2 text-gray-700 text-sm lg:text-base">
                    Реєстрація нового користувача
                </legend>
            </fieldset>

            <form @submit.prevent="handleSubmit" class="space-y-4">

                <!-- username -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Логін</label>
                    <input
                        v-model="form.username"
                        type="text"
                        placeholder="Ваш логін"
                        class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    />
                    <p v-if="errors.username" class="text-red-500 text-xs mt-1">
                        {{ errors.username[0] }}
                    </p>
                </div>

                 <!-- display_name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Публічне ім'я</label>
                    <input
                        v-model="form.display_name"
                        type="text"
                        placeholder="Публічне ім'я"
                        class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    />
                    <p v-if="errors.display_name" class="text-red-500 text-xs mt-1">
                        {{ errors.display_name[0] }}
                    </p>
                </div>

                <!-- email -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        Email
                    </label>
                    <input
                        v-model="form.email"
                        type="email"
                        placeholder="your@email.com"
                        class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
                    />
                    <p v-if="errors.email" class="text-red-500 text-xs mt-1">
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
                            placeholder="Мінімум 8 символів"
                            class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 pr-10"
                        />
                        <button
                            type="button"
                            @click="togglePassword"
                            class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500"
                        >
                            <span v-if="!showPassword">👁️</span>
                            <span v-else>🙈</span>
                        </button>
                    </div>
                    <p class="text-xs text-gray-400 mt-1">Мінімум 8 символів.</p>
                    <p v-if="errors.password" class="text-red-500 text-xs mt-1">
                        {{ errors.password[0] }}
                    </p>
                </div>

                <!-- password_confirm -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        Підтвердження паролю
                    </label>
                    <div class="relative">
                        <input
                            v-model="form.password_confirm"
                            :type="showPassword ? 'text' : 'password'"
                            placeholder="Повторіть пароль"
                            class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400 pr-10"
                        />
                        <button
                            type="button"
                            @click="togglePassword"
                            class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500"
                        >
                            <span v-if="!showPassword">👁️</span>
                            <span v-else>🙈</span>
                        </button>
                    </div>
                    <p v-if="errors.password_confirm" class="text-red-500 text-xs mt-1">
                        {{ errors.password_confirm[0] }}
                    </p>
                </div>


                
                <!-- consent_given -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        Погодження з правилами.
                    </label>
                    <input
                        v-model="form.consent_given"       
                        type="checkbox"
                        class=""
                    />
                    <!-- <p v-if="errors.email" class="text-red-500 text-xs mt-1">
                        {{ errors.email[0] }}
                    </p> -->
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
                    <RouterLink to="/auth/login" class="text-amber-600 hover:underline">
                        Увійти
                    </RouterLink>
                </p>

            </form>
        </div>
    </div>
</template>