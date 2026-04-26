<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '',
  password: '',
})

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
  <fieldset class="border-y p-8 mx-auto mt-8 max-w-md shadow-xl">
    <legend class="mx-5 text-gray-700">Для входу в систему</legend>

    <form @submit.prevent="handleSubmit" class="max-w-sm mx-auto bg-white p-6 rounded shadow-md space-y-4 mb-5">

      <!-- помилка логіну -->
      <p v-if="errors.detail" class="text-red-600 text-sm font-medium">
        Невірний логін або пароль
      </p>

      <!-- username -->
      <div>
        <input
          v-model="form.username"
          type="text"
          placeholder="Введіть логін"
          class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
        />
        <p v-if="errors.username" class="text-red-500 text-sm mt-1">
          {{ errors.username[0] }}
        </p>
      </div>

      <!-- password -->
      <div>
        <input
          v-model="form.password"
          type="password"
          placeholder="Введіть пароль"
          class="bg-amber-100 p-2 w-full mt-1 rounded focus:outline-none focus:ring-2 focus:ring-amber-400"
        />
        <p v-if="errors.password" class="text-red-500 text-sm mt-1">
          {{ errors.password[0] }}
        </p>
      </div>

      <!-- кнопка -->
      <button
        type="submit"
        :disabled="isLoading"
        class="bg-[#CEC526] w-full rounded mx-auto p-2 text-gray-800 text-lg hover:bg-[#F2E70A] disabled:opacity-50 transition"
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
  </fieldset>
</template>