import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getGroups, createGroup } from '../api/groups.js'

export const useGroupStore = defineStore('groups', () => {
  const groups = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchGroups() {
    loading.value = true
    error.value = null
    try {
      const response = await getGroups()
      groups.value = response.data
    } catch (e) {
      error.value = 'Помилка завантаження груп'
    } finally {
      loading.value = false
    }
  }

  async function addGroup(name){
    const response = await createGroup(name)
    groups.value.push(response.data) // одразу додаємо в список без нового запиту
    return response.data
  }



  return { groups, loading, error, fetchGroups,addGroup }
})