<template>
  <div class="app-bg min-h-screen">

    <!-- НАВІГАЦІЯ -->
    <header class="sticky top-0 shadow-md z-50 w-full">
      <nav class="relative flex w-full items-center bg-[#2e332e] justify-between flex-wrap gap-4 px-3 py-2">

        <!-- ЛОГОТИП -->
        <RouterLink to="/" class="flex items-center">
          <img src="/base/My_for_ukrainischenDesign.png" alt="Коло Українців" class="w-10 lg:w-12 rounded-2xl" />
          <h3 class="text-white text-xl lg:text-2xl px-3 font-thin tracking-tighter hidden lg:block">
            <span class="text-[#fcda00]">Коло</span>
            <span class="text-[#fcda00]"> Українців</span>
          </h3>
        </RouterLink>

        <!-- КНОПКИ -->
        <div class="flex items-center gap-2">
          <RouterLink to="/auth/login"
            class="bg-[#1e7bec] hover:bg-blue-700 text-white text-xs px-4 py-2 rounded transition">
            Увійти
          </RouterLink>
          <RouterLink to="/auth/register"
            class="bg-[#f3d305] rounded-md text-[#33332E] font-medium px-4 py-2 text-xs hover:bg-[#A9A437] transition">
            Реєстрація
          </RouterLink>
        </div>

      </nav>
    </header>

    <!-- КОНТЕНТ — кожен View сам відповідає за свою картку -->
    <main class="w-full">
      <RouterView />
    </main>

  </div>
</template>