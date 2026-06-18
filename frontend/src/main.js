import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router/index.js'
import App from './App.vue'
import './assets/css/style.css'
import './assets/css/my_style.css'
import { initAuth } from './app/initAuth.js' // ✅ ДОБАВЛЕНО

// ✅ ИСПРАВЛЕНО: обернуть в async function
const startApp = async () => {
  const app = createApp(App)

  const pinia = createPinia()
  app.use(pinia)
  app.use(router)

  // 🔥 КРИТИЧНО: дождаться восстановления auth ПЕРЕД mount
  await initAuth(pinia)

  // mount ТОЛЬКО после этого
  app.mount('#app')
}

startApp()