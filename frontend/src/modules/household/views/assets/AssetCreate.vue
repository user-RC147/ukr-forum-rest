<script setup>
import {ref,computed} from 'vue'
import { useAssetStore } from '../../stores/useAssetStore.js';
import { useGroupStore } from '../../stores/useGroupStore.js';
import { useRouter, useRoute} from 'vue-router'  // ← додати

// ref — реактивна змінна для поля вводу
const assetName=ref('')

// error — показуємо якщо щось пішло не так
const error=ref(null)

// loading — щоб заблокувати кнопку поки йде запит
const loading=ref(false)

// router — для переходу на іншу сторінку після створення
const router=useRouter()

const route=useRoute()  // ← читаємо URL параметри 

// store — щоб викликати createAsset і оновити список
const store=useAssetStore()

//група 

const groupStore=useGroupStore()
// беремо групу з URL, наприклад ?group=2
const selectedGroupId=ref(route.query.group ? +route.query.group : null)

// назва вибраної групи для відображення
const selectedGroup = computed(() =>
  groupStore.groups.find(g=>g.id === selectedGroupId.value)
)

async function handleSubmit(){

  console.log('handleSubmit викликано')
    console.log('assetName:', assetName.value)
    console.log('selectedGroupId:', selectedGroupId.value)


    // Проста валідація — не відправляти порожню назву
    if(!assetName.value.trim()){
        error.value ='Введіть назву обєкту'
        return
    }
    if (!selectedGroupId.value){
      error.value='Вибиріть групу'
      return
    }

    loading.value=true
    error.value=null

    try{
        console.log('відправляємо:', { name: assetName.value, group: selectedGroupId.value })
    await store.addAsset({
        name: assetName.value,
        group: selectedGroupId.value
    })
    console.log('успішно збережено')
    router.push({ name: 'household-index' })

    }catch(e){
         error.value = 'Помилка створення обєкту'
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

    <h1 class="text-xl font-semibold mb-6">Створити обєкт</h1>

    <!-- Помилка -->
    <div v-if="error" class="bg-red-100 text-red-600 px-4 py-3 rounded-xl mb-4">
      {{ error }}
    </div>

    <!-- Форма -->
    <div class="flex flex-col gap-4">
     
      <!-- Група (автоматично з фільтру) -->
      <div class="flex flex-col gap-1">
         
          <div class="">
              <span class="text-sm font-medium">Група:</span>
              {{ selectedGroup?.name || 'Групу не вибрано' }}
          </div>
      </div>
      <!-- Назва обєкту -->
      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium">Назва обєкту</label>
        <!-- v-model — двостороннє зв'язування: 
             що вводить користувач — одразу в groupName.value -->
        <input
          v-model="assetName"
          type="text"
          placeholder="Наприклад: Meerkamp, 32"
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