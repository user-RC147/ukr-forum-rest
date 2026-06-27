import { useUserStore } from '@/shared/stores/useUserStore'

/**
 * Сервіс ініціалізації авторизації при старті додатка (F5).
 * Завжди робить запит до Django для перевірки наявності HttpOnly Cookies.
 * * @param {Object} pinia - Екземпляр сховища Pinia, переданий з main.js
 */
export async function initAuth(pinia) {
  const userStore = useUserStore(pinia)

  try {
    // JavaScript не бачить HttpOnly куки, тому ми завжди робимо "сліпий" запит профілю.
    // Завдяки `withCredentials: true` в axios.js, браузер сам прикріпить куку до запиту.
    await userStore.fetchProfile()
  } catch (error) {
    // Якщо Django повернув 401 (кука застаріла або відсутня) — спокійно розлогінюємо користувача.
    // Консоль лог не засмічуємо критичними помилками, це стандартна поведінка для неавторизованого гостя.
    userStore.logout()
  } finally {
    // ЗАЛІЗОБЕТОННО: Сигналізуємо системі та роутеру, що перевірка завершена,
    // незалежно від того, успішний запит чи ні.
    userStore.ready = true
  }
}