import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router/index.js'
import App from './App.vue'
import './style.css'

const app = createApp(App)

// підключаємо pinia — state management
app.use(createPinia())

// підключаємо router — маршрутизація
// router підключаємо після pinia бо navigation guard використовує store
app.use(router)

app.mount('#app')