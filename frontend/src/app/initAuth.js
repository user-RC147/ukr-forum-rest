import { useUserStore } from '@/modules/users/stores/useUserStore'

export async function initAuth(pinia) {
  const userStore = useUserStore(pinia)

  // если есть сохранённый токен — восстанавливаем пользователя
  if (userStore.accessToken) {
    try {
      await userStore.fetchProfile()
    } catch (error) {
      console.error('Failed to restore auth:', error)
      // если токен протух — очищаем
      userStore.logout()
    }
  }

  // ✅ ВАЖНО: сигнализируем что init завершён
  userStore.ready = true
}