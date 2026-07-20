import axios from 'axios'

const BASE_URL = '/api'

/**
 * Глобальний інфраструктурний адаптер Axios.
 * Налаштовує єдину точку зв'язку з Django REST Framework бекендом.
 *
 * Аутентифікація повністю на httpOnly + Secure cookies:
 * access_token і refresh_token браузер підставляє сам через withCredentials.
 * Жодних токенів у JS (localStorage/Pinia) більше немає.
 */
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // КРИТИЧНО ДЛЯ БЕЗПЕКИ: дозволяє браузеру автоматично додавати
  // HttpOnly cookies (access_token, refresh_token) до кожного запиту
  withCredentials: true,
})

/**
 * "Чистий" інстанс без інтерцепторів — використовується ЛИШЕ для запиту
 * оновлення токена. Критично: якщо викликати refresh через `api`,
 * а refresh-токен невалідний (сервер поверне 401 на сам /token/refresh/),
 * той самий response-interceptor знову спробує зробити refresh —
 * і піде в нескінченний цикл запитів.
 */
const rawApi = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
})

/**
 * Читає значення cookie за ім'ям.
 */
function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

/**
 * Перехоплювач вихідних запитів (Request Interceptor).
 * Підставляє X-CSRFToken на кожен state-changing запит (POST/PUT/PATCH/DELETE).
 * GET/HEAD/OPTIONS пропускаємо — Django CSRF middleware їх не перевіряє.
 */
api.interceptors.request.use(
  (config) => {
    const method = config.method?.toUpperCase()

    if (method && !['GET', 'HEAD', 'OPTIONS'].includes(method)) {
      const csrfToken = getCookie('csrftoken')
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Стан для запобігання "гонці" запитів на оновлення токена.
 * Якщо декілька запитів одночасно впали з 401 — refresh має піти лише один раз.
 */
let isRefreshing = false
let refreshSubscribers = []

function subscribeTokenRefresh(callback) {
  refreshSubscribers.push(callback)
}

function onRefreshed() {
  refreshSubscribers.forEach((callback) => callback())
  refreshSubscribers = []
}

function onRefreshFailed(error) {
  refreshSubscribers.forEach((callback) => callback(error))
  refreshSubscribers = []
}

/**
 * Перехоплювач вхідних відповідей (Response Interceptor).
 * Спрацьовує автоматично при отриманні будь-якої відповіді від Django.
 */
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config

    if (!error.response) {
      return Promise.reject(error)
    }

    const isAuthEndpoint = originalRequest.url?.includes('/token/refresh/')

    if (
      error.response.status === 401 &&
      !originalRequest._retry &&
      !isAuthEndpoint
    ) {
      originalRequest._retry = true

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          subscribeTokenRefresh((refreshError) => {
            if (refreshError) {
              reject(refreshError)
            } else {
              resolve(api(originalRequest))
            }
          })
        })
      }

      isRefreshing = true

      try {
        // Браузер сам відправить refresh cookie, CSRF-заголовок теж
        // підставиться інтерцептором rawApi нижче
        await rawApi.post(
          '/users/token/refresh/',
          {},
          { headers: { 'X-CSRFToken': getCookie('csrftoken') } }
        )

        isRefreshing = false
        onRefreshed()

        return api(originalRequest)
      } catch (refreshError) {
        isRefreshing = false
        onRefreshFailed(refreshError)

        // window.location.href = "/auth/login"

        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api