import axios from 'axios'

/**
 * Глобальний інфраструктурний адаптер Axios.
 * Налаштовує єдину точку зв'язку з Django REST Framework бекендом.
 */
const api = axios.create({
  // Базовий URL сервера. Всі модульні API дописуватимуть сюди лише свої ендпоінти.
  baseURL: 'http://localhost:8000/api',
  
  // Стандартний заголовок для обміну даними у форматі JSON
  headers: {
    'Content-Type': 'application/json',
  },
  
  // КРИТИЧНО ДЛЯ БЕЗПЕКИ: Дозволяє браузеру автоматично додавати HttpOnly Cookies (де лежить Refresh Token) до запитів
  withCredentials: true,
})

/**
 * Перехоплювач вихідних запитів (Request Interceptor).
 * Спрацьовує автоматично перед тим, як запит полетить у мережу.
 */
api.interceptors.request.use(
  (config) => {
    // Витягуємо короткочасний access_token з локального сховища
    const token = localStorage.getItem('access_token')
    
    if (token) {
      // Прикріплюємо токен у стандартному заголовку авторизації DRF
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Перехоплювач вхідних відповідей (Response Interceptor).
 * Спрацьовує автоматично при отриманні будь-якої відповіді від Django.
 */
api.interceptors.response.use(
  (response) => response, // Якщо HTTP-статус успішний (200-299), просто повертаємо дані далі
  (error) => {
    // Глобальний Гвард безпеки: якщо токен застарів або недійсний (401 Unauthorized)
    if (error.response?.status === 401) {
      // Видаляємо лише локальний access_token. 
      // refresh_token лежить у куках, тому JavaScript його не чіпає — його видалить бекенд при logout запиті.
      localStorage.removeItem('access_token')
      
      // Примусово перенаправляємо на сторінку входу
      window.location.href = '/auth/login'
    }
    
    return Promise.reject(error)
  }
)

export default api