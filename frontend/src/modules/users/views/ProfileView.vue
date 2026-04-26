<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '../stores/useUserStore'

const userStore = useUserStore()

// onMounted — виконується коли компонент завантажився на сторінку
// як сигнал "сторінка готова — завантажуй дані"
onMounted(async () => {
  await userStore.fetchProfile()
})
</script>

<template>
  <fieldset class="border-y p-8 mx-auto mt-8 max-w-md shadow-xl">
    <legend class="mx-5 text-gray-700">Мій профіль</legend>

    <div class="bg-white p-6 rounded shadow-md space-y-4">

      <!-- поки дані завантажуються -->
      <p v-if="!userStore.user" class="text-gray-500 text-center">
        Завантаження...
      </p>

      <!-- дані профілю -->
      <div v-else class="space-y-3">

        <div>
          <span class="text-sm text-gray-500">Логін:</span>
          <p class="font-medium text-gray-800">{{ userStore.user.username }}</p>
        </div>

        <div>
          <span class="text-sm text-gray-500">Email:</span>
          <p class="font-medium text-gray-800">{{ userStore.user.email }}</p>
        </div>

        <div>
          <span class="text-sm text-gray-500">Публічне ім'я:</span>
          <p class="font-medium text-gray-800">
            {{ userStore.user.display_name || 'не вказано' }}
          </p>
        </div>

        <div>
          <span class="text-sm text-gray-500">Вік:</span>
          <p class="font-medium text-gray-800">
            {{ userStore.user.age || 'не вказано' }}
          </p>
        </div>

      </div>
    </div>
  </fieldset>
</template>