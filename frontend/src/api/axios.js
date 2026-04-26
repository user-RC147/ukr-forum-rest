import axios from 'axios'

const api = axios.create({
  // адреса Django backend
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor — перед кожним запитом автоматично додає токен
// Це як middleware в Django
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api