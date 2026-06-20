import axios from 'axios'

// Створює інстанс axios з попередньо налаштованими параметрами
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // дозволяє відправляти cookies з запитами (якщо потрібно для сесійної автентифікації) 
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

export default api