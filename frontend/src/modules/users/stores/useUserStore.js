import { defineStore } from 'pinia';
import { loginUser, getProfile } from '../api/users';

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
    }),

    getters: {
       isAuthenticated: (state) => state.user !== null,
    },

    actions: {
        async login(credentials) {
            await loginUser(credentials);
            await this.fetchProfile();
            // Токени тепер в cookies — JS їх не бачить
            // Просто відправляємо запит, cookies додаються автоматично
        },

        async fetchProfile() {
            try {
                const response = await getProfile();
                this.user = response.data;
            } catch (error) {
                if (error.response?.status === 401) {
                    this.logout();
                }
                throw error; // ✅ ДОБАВЛЕНО: пробросить ошибку выше
            }
        },

        logout() {
            this.user = null;
        },
    },
});