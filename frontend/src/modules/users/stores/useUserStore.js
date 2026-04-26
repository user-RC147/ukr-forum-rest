import { defineStore } from 'pinia'
import { loginUser, getProfile } from '../../../api/users'

export const useUserStore = defineStore('user', {
  // state — це як модель, зберігає дані
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),

  // getters — це як property, обчислюється з state
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  // actions — це як методи, змінюють state
  actions: {
    async login(credentials) {
      const response = await loginUser(credentials)
      
      this.accessToken = response.data.access
      this.refreshToken = response.data.refresh

      // зберігаємо токени в localStorage щоб не загубити після перезавантаження
      localStorage.setItem('access_token', this.accessToken)
      localStorage.setItem('refresh_token', this.refreshToken)
    },

    async fetchProfile() {
      const response = await getProfile()
      this.user = response.data
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})