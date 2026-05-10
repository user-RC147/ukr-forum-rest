<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()

const form = ref({ username: '', password: '' })
const errors = ref({})
const isLoading = ref(false)

const handleSubmit = async () => {
  isLoading.value = true
  errors.value = {}
  try {
    await userStore.login(form.value)
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
  <div class="flex items-center justify-center mt-8">
    <div class=" rounded-lg shadow-md w-full max-w-sm">
      <fieldset class="border-t border-gray-400 px-6 flex items-center justify-center">
        <legend class="mx-auto px-4 text-gray-700 text-sm lg:text-base">
          Для входу в систему
        </legend>
      </fieldset>

      <form @submit.prevent="handleSubmit" class="space-y-4 p-6">

        <!-- помилка логіну -->
        <p v-if="errors.detail" class="text-red-600 text-sm font-medium text-center">
          Невірний логін або пароль
        </p>

        <!-- username -->
        <div>
          <input
            v-model="form.username"
            type="text"
            placeholder="Введіть логін"
            class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
          <p v-if="errors.username" class="text-red-500 text-xs mt-1">
            {{ errors.username[0] }}
          </p>
        </div>

        <!-- password -->
        <div>
          <input
            v-model="form.password"
            type="password"
            placeholder="Введіть пароль"
            class="bg-amber-100 p-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
          <p v-if="errors.password" class="text-red-500 text-xs mt-1">
            {{ errors.password[0] }}
          </p>
        </div>

        <!-- кнопка -->
        <button
          type="submit"
          :disabled="isLoading"
          class="bg-[#CEC526] w-full rounded p-2 text-gray-800 text-base lg:text-lg hover:bg-[#F2E70A] disabled:opacity-50 transition"
        >
          {{ isLoading ? 'Завантаження...' : 'Увійти' }}
        </button>

        <!-- посилання на реєстрацію -->
        <p class="text-center text-sm text-gray-600">
          Немає акаунту?
          <RouterLink to="/auth/register" class="text-amber-600 hover:underline">
            Зареєструватися
          </RouterLink>
        </p>

      </form>
    </div>
  </div>
</template>

