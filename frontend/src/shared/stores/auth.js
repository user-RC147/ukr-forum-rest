import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    access: localStorage.getItem('access') || null,
    refresh: localStorage.getItem('refresh') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,
  },

  actions: {
    async login(credentials) {
      const { data } = await axios.post('http://localhost:8000/api/auth/login/', credentials)

      this.access = data.access
      this.refresh = data.refresh

      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)

      await this.fetchUser()
    },

    async fetchUser() {
      if (!this.access) return

      const { data } = await axios.get('http://localhost:8000/api/auth/me/', {
        headers: {
          Authorization: `Bearer ${this.access}`,
        },
      })

      this.user = data
    },

    logout() {
      this.user = null
      this.access = null
      this.refresh = null

      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },

    async refreshToken() {
      if (!this.refresh) return

      const { data } = await axios.post('http://localhost:8000/api/auth/refresh/', {
        refresh: this.refresh,
      })

      this.access = data.access
      localStorage.setItem('access', data.access)
    },
  },
})