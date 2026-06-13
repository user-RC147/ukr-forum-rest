<script setup>
import {ref} from 'vue'
import { useGroupStore } from '../../stores/useGroupStore.js';
import { useRouter } from 'vue-router'  // ← додати

// ref — реактивна змінна для поля вводу
const groupName=ref('')

// error — показуємо якщо щось пішло не так
const error=ref(null)

// loading — щоб заблокувати кнопку поки йде запит
const loading=ref(false)

// router — для переходу на іншу сторінку після створення
const router=useRouter()

// store — щоб викликати createGroup і оновити список
const store=useGroupStore()

async function handleSubmit(){
    // Проста валідація — не відправляти порожню назву
    if(!groupName.value.trim()){
        error.value ='Введіть назву групи'
        return
    }

    loading.value=true
    error.value=null

    try{
        // Викликаємо метод стору який робить POST запит
        await store.addGroup(groupName.value)

         // Після успіху — переходимо на список груп
         router.push({name:'household-index'})

    }catch(e){
         error.value = 'Помилка створення групи'
    }finally{
        loading.value=false
    }
}


</script>

<template>
  <div class="max-w-md mx-auto px-4 py-6">

    <!-- Верхній рядок -->
    <div class="flex justify-between items-center mb-6">
      <router-link
        :to="{ name: 'household-index' }"
        class="bg-[#cce9f8] hover:bg-[#aedbf4] text-[#2e332e] px-5 py-3 rounded-xl text-sm font-medium transition">
        ← Повернутися
      </router-link>
    </div>

    <h1 class="text-xl font-semibold mb-6">Створити групу</h1>

    <!-- Помилка -->
    <div v-if="error" class="bg-red-100 text-red-600 px-4 py-3 rounded-xl mb-4">
      {{ error }}
    </div>

    <!-- Форма -->
    <div class="flex flex-col gap-4">

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium">Назва групи</label>
        <!-- v-model — двостороннє зв'язування: 
             що вводить користувач — одразу в groupName.value -->
        <input
          v-model="groupName"
          type="text"
          placeholder="Наприклад: Моя сім'я"
          class="border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-amber-400"
        />
      </div>

      <!-- :disabled — кнопка неактивна поки йде запит -->
      <button
        @click="handleSubmit"
        :disabled="loading"
        class="bg-[#CEC526] hover:bg-[#F2E70A] text-[#33332E] font-semibold px-5 py-3 rounded-xl transition disabled:opacity-50">
        {{ loading ? 'Збереження...' : 'Зберегти' }}
      </button>

    </div>
  </div>
</template>