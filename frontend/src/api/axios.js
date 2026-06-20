import axios from 'axios'

// Створює інстанс axios з попередньо налаштованими параметрами
const api = axios.create({
  // базова URL адреса для всіх запитів
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // дозволяє відправляти cookies з запитами (якщо потрібно для сесійної автентифікації) 
})


// експортує налаштований api інстанс для використання в компонентах
export default api