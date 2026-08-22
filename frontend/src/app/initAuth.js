import { useUserStore } from '@/shared/stores/useUserStore'
import api from '@/api/axios' // путь поправь под свою структуру

/**
 * Сервіс ініціалізації авторизації при старті додатка (F5).
 * Спочатку отримуємо CSRF-cookie (потрібна для подальших
 * state-changing запитів — logout, refresh тощо),
 * потім завжди робимо запит до Django для перевірки наявності HttpOnly Cookies.
 *
 * @param {Object} pinia - Екземпляр сховища Pinia, переданий з main.js
 */
export async function initAuth(pinia) {
  const userStore = useUserStore(pinia)

  try {
    // Отримуємо CSRF-cookie ДО будь-яких state-changing запитів.
    // Django виставить non-httpOnly cookie `csrftoken` у відповіді,
    // яку axios-interceptor далі підставлятиме в заголовок X-CSRFToken.
    await api.get('/auth/csrf/')
  } catch (error) {
    // Не блокуємо ініціалізацію через це — якщо бекенд недоступний,
    // наступний запит (fetchProfile) однаково впаде своєю помилкою.
    console.error('Не вдалося отримати CSRF-токен:', error)
  }

  try {
    // JavaScript не бачить HttpOnly куки, тому ми завжди робимо "сліпий" запит профілю.
    // Завдяки `withCredentials: true` в axios.js, браузер сам прикріпить куку до запиту.
    await userStore.fetchProfile()
  } catch (error) {
    // fetchProfile вже сам зробив clearLocalSession() при 401 —
    // тут нічого додатково робити не потрібно
  } finally {
    // ЗАЛІЗОБЕТОННО: Сигналізуємо системі та роутеру, що перевірка завершена,
    // незалежно від того, успішний запит чи ні.
    userStore.ready = true
  }
}