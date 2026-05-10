import { defineStore } from 'pinia';
import { loginUser, getProfile } from '../api/users';

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        accessToken: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
    }),

    getters: {
        isAuthenticated: (state) => !!state.accessToken,
    },

    actions: {
        async login(credentials) {
            const response = await loginUser(credentials);
            this.accessToken = response.data.access;
            this.refreshToken = response.data.refresh;
            localStorage.setItem('access_token', this.accessToken);
            localStorage.setItem('refresh_token', this.refreshToken);
        },

        async fetchProfile() {
            try {
                const response = await getProfile();
                this.user = response.data;
            } catch (error) {
                if (error.response?.status === 401) {
                    this.logout();
                }
            }
        },

        logout() {
            this.user = null;
            this.accessToken = null;
            this.refreshToken = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        },
    },
});