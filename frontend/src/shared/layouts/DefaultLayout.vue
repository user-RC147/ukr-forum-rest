<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../modules/users/stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()
const mobileMenuOpen = ref(false)

const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="app-bg w-full m-0 p-0">    

    <!-- НАВІГАЦІЯ -->
    <header class="sticky top-0 shadow-md z-50 w-full">
      <nav class="relative flex w-full items-center bg-[#2e332e] justify-between flex-wrap gap-4 px-3">

        <!-- ЛОГОТИП -->
        <div class="flex items-center">
          <RouterLink to="/" class="flex items-center">
            <img src="/base/My_for_ukrainischenDesign.png" alt="Коло Українців" class="w-12 rounded-2xl" />
            <h3 class="text-white text-2xl px-3 font-thin tracking-tighter hidden lg:block">
              <span class="text-[#fcda00]">Коло</span>
              <span class="text-[#fcda00]"> Українців</span>
            </h3>
          </RouterLink>
        </div>

        <!-- ДЕСКТОП МЕНЮ -->
        <div class="hidden lg:flex items-center gap-1">
          <RouterLink to="/shop"
            class="bg-[#f3d305] rounded text-[#33332E] text-xs inline-block min-w-28 py-2 text-center hover:bg-[#A9A437] transition">
            Барахолка
          </RouterLink>
          <RouterLink to="/advboard"
            class="bg-[#f3d305] rounded text-[#33332E] text-xs inline-block min-w-28 py-2 text-center hover:bg-[#A9A437] transition">
            Оголошення
          </RouterLink>
          <RouterLink to="/articles"
            class="bg-[#f3d305] rounded text-[#33332E] text-xs inline-block min-w-28 py-2 text-center hover:bg-[#A9A437] transition">
            Поради
          </RouterLink>
          <RouterLink to="/stories"
            class="bg-[#f3d305] rounded text-[#33332E] text-xs inline-block min-w-28 py-2 text-center hover:bg-[#A9A437] transition">
            Досвід / Розповіді
          </RouterLink>
          <RouterLink to="/household"
            class="bg-[#f3d305] rounded text-[#33332E] text-xs inline-block min-w-28 py-2 text-center hover:bg-[#A9A437] transition">
            ДомВитрати
          </RouterLink>
        </div>

         <!-- БУРГЕР (тільки мобілка) -->
          <button @click="mobileMenuOpen = !mobileMenuOpen"
            class="text-[#f3d305] text-3xl font-bold lg:hidden focus:outline-none">
            ☰
          </button>



        <!-- ПРАВА ЧАСТИНА: username + вийти + бургер -->
        <div class="flex items-center gap-2">

          <!-- username -->
          <RouterLink to="/profile"
            class="bg-[#1e7bec] hover:bg-blue-700 text-white text-xs px-5 py-2 rounded">
            {{ userStore.user?.username || '...' }}
          </RouterLink>

          <!-- кнопка вийти -->
          <button @click="handleLogout"
            class="bg-[#f3d305] rounded-md text-[#33332E] inline-block font-medium p-2 text-center hover:bg-[#A9A437] transition text-xs">
            Вийти
          </button>        

        </div>

        <!-- МОБІЛЬНЕ МЕНЮ -->
        <div v-if="mobileMenuOpen"
          class="absolute bg-[#f7f6f1] top-full left-0 w-full shadow-xl lg:hidden">
          <ul class="flex flex-col p-4 gap-3">
            <li>
              <RouterLink to="/shop" @click="mobileMenuOpen = false"
                class="block py-2 border-b border-amber-400 hover:bg-[#A9A437] transition">
                Барахолка
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/advboard" @click="mobileMenuOpen = false"
                class="block py-2 border-b border-amber-400 hover:bg-[#A9A437] transition">
                Оголошення
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/articles" @click="mobileMenuOpen = false"
                class="block py-2 border-b border-amber-400 hover:bg-[#A9A437] transition">
                Поради
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/stories" @click="mobileMenuOpen = false"
                class="block py-2 border-b border-amber-400 hover:bg-[#A9A437] transition">
                Досвід / Розповіді
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/household" @click="mobileMenuOpen = false"
                class="block py-2 border-b border-amber-400 hover:bg-[#A9A437] transition">
                ДомВитрати
              </RouterLink>
            </li>
          </ul>
        </div>

      </nav>
    </header>

    <!-- ВМІСТ СТОРІНКИ -->
    <main class="w-full">
      <RouterView />
    </main>

  </div>
</template>