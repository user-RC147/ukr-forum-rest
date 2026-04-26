<template>
  <div class="min-h-screen bg-gray-50">

    <!-- навігація -->
    <nav class="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
      <RouterLink to="/" class="font-bold text-lg text-blue-600">
        Ukr Forum
      </RouterLink>

      <button
        @click="handleLogout"
        class="text-sm text-gray-600 hover:text-red-500"
      >
        Вийти
      </button>
    </nav>

    <!-- вміст сторінки -->
    <main class="max-w-4xl mx-auto px-6 py-8">
      <RouterView />
    </main>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../../modules/users/stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'login' })
}
</script>