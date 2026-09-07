<script setup>
import { FaceFrownIcon, HomeIcon, ArrowLeftIcon, ShoppingBagIcon, ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'

defineProps({
  code: {
    type: [String, Number],
    default: '404',
  },
  eyebrow: {
    type: String,
    default: 'Сторінка не знайдена',
  },
  title: {
    type: String,
    default: 'Схоже, ця сторінка загубилася',
  },
  message: {
    type: String,
    default: 'Ми перевірили адресу, але не знайшли тут потрібного вмісту. Спробуйте повернутися на головну або продовжити пошук.',
  },
})
</script>

<template>
  <section class="flex min-h-screen items-center justify-center bg-[#f4f7fb]/75 px-4 py-8 sm:px-6">
    <div class="w-full max-w-2xl">
      <div class="overflow-hidden rounded-2xl bg-white shadow-[0_24px_80px_rgba(34,51,73,0.14)]">
        <div class="h-2 bg-[#1e7bec]"></div>
        <div class="h-2 bg-[#f3d305]"></div>

        <div class="px-6 py-10 text-center sm:px-12 sm:py-14">
          <div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-[#f3d305]/20 text-[#1e7bec]">
            <FaceFrownIcon class="h-11 w-11" aria-hidden="true" />
          </div>

          <p class="text-8xl font-black leading-none tracking-tight text-[#dfe5ec] sm:text-9xl">{{ code }}</p>
          <p class="mt-5 text-xs font-bold uppercase tracking-[0.2em] text-[#1e7bec]">{{ eyebrow }}</p>
          <h1 class="mt-3 text-3xl font-bold text-[#33332E] sm:text-4xl">{{ title }}</h1>
          <p class="mx-auto mt-4 max-w-md text-base leading-7 text-[#68717c] sm:text-lg">{{ message }}</p>

          <div class="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <RouterLink
              to="/"
              class="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1e7bec] px-6 py-3 text-sm font-semibold text-white shadow-md transition hover:-translate-y-0.5 hover:bg-[#1768ca] hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-[#1e7bec] focus:ring-offset-2"
            >
              <HomeIcon class="h-5 w-5" aria-hidden="true" />
              На головну
            </RouterLink>
            <button
              type="button"
              class="inline-flex items-center justify-center gap-2 rounded-lg bg-[#eef1f5] px-6 py-3 text-sm font-semibold text-[#4c5662] transition hover:-translate-y-0.5 hover:bg-[#e2e7ed] focus:outline-none focus:ring-2 focus:ring-[#1e7bec] focus:ring-offset-2"
              @click="$router.back()"
            >
              <ArrowLeftIcon class="h-5 w-5" aria-hidden="true" />
              Назад
            </button>
          </div>

          <div class="mt-10 border-t border-[#e5e9ee] pt-7">
            <p class="mb-4 text-sm text-[#7b848e]">Можливо, вам допоможуть ці розділи:</p>
            <div class="flex flex-wrap justify-center gap-2">
              <RouterLink to="/shop" class="inline-flex items-center gap-2 rounded-full bg-[#f3d305]/15 px-4 py-2 text-sm font-semibold text-[#4d535a] transition hover:bg-[#f3d305]/30">
                <ShoppingBagIcon class="h-4 w-4" aria-hidden="true" />
                Барахолка
              </RouterLink>
              <RouterLink to="/articles" class="inline-flex items-center gap-2 rounded-full bg-[#f3d305]/15 px-4 py-2 text-sm font-semibold text-[#4d535a] transition hover:bg-[#f3d305]/30">
                <ChatBubbleLeftRightIcon class="h-4 w-4" aria-hidden="true" />
                Обговорення
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <p class="mt-5 text-center text-sm text-[#7b848e]">Коло Українців · Код помилки: {{ code }}</p>
    </div>
  </section>
</template>
