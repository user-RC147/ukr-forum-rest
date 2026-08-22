import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router/index.js'
import App from './App.vue'
import './assets/css/style.css'
import './assets/css/my_style.css'
import { initAuth } from './app/initAuth.js'

const startApp = async () => {
  const app = createApp(App)

  const pinia = createPinia()
  app.use(pinia)

  app.use(router)

  app.mount('#app')

  await initAuth(pinia)
}

startApp()