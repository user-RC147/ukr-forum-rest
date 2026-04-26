<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '../stores/useUserStore'

const userStore = useUserStore()

onMounted(async () => {
  if (!userStore.user) {
    await userStore.fetchProfile()
  }
})
</script>

<template>
  <div class="w-full px-6 py-6">

    <!-- Банер -->
    <div class="bg-white p-6 rounded-3xl shadow-xl border border-gray-100 relative overflow-hidden mb-10">
      <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-blue-500 via-amber-400 to-yellow-300"></div>
      <p class="text-xl leading-relaxed text-gray-800 font-medium italic text-center">
        "Об'єднуємо українців у світі — щоб підтримати, знайти друзів і не втратити себе."
      </p>
      <div class="text-center mt-4">
        <span class="inline-block bg-[#f0e6aa] text-[#33332E] px-4 py-2 rounded-full shadow">
          Приєднуйтесь до нашої спільноти
        </span>
      </div>
    </div>

    <!-- Картки розділів -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

      <RouterLink to="/shop" class="group bg-orange-50 border border-orange-100 p-6 rounded-3xl shadow-sm hover:shadow-md transition-all flex flex-col border-l-8 border-l-orange-400">
        <h3 class="font-bold text-xl text-orange-900 mb-2">🛒 Барахолка</h3>
        <p class="text-gray-700 leading-relaxed text-sm">Купуй і продавай речі в українській спільноті.</p>
      </RouterLink>

      <RouterLink to="/advboard" class="group bg-blue-50 border border-blue-100 p-6 rounded-3xl shadow-sm hover:shadow-md transition-all flex flex-col border-l-8 border-l-blue-400">
        <h3 class="font-bold text-xl text-blue-900 mb-2">📋 Оголошення</h3>
        <p class="text-gray-700 leading-relaxed text-sm">Розміщуй та переглядай оголошення.</p>
      </RouterLink>

      <RouterLink to="/articles" class="group bg-yellow-50 border border-yellow-100 p-6 rounded-3xl shadow-sm hover:shadow-md transition-all flex flex-col border-l-8 border-l-yellow-400">
        <h3 class="font-bold text-xl text-yellow-900 mb-2">💡 Поради</h3>
        <p class="text-gray-700 leading-relaxed text-sm">Корисні статті та поради від спільноти.</p>
      </RouterLink>

      <RouterLink to="/stories" class="group bg-indigo-50 border border-indigo-100 p-6 rounded-3xl shadow-sm hover:shadow-md transition-all flex flex-col border-l-8 border-l-indigo-400">
        <h3 class="font-bold text-xl text-indigo-900 mb-2">📖 Досвід / Розповіді</h3>
        <p class="text-gray-700 leading-relaxed text-sm">Діліться своїм досвідом з іншими.</p>
      </RouterLink>

    </div>
  </div>
</template>