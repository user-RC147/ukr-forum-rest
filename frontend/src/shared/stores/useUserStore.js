import { defineStore } from 'pinia'
import { loginUser, getProfile } from '../../modules/users/api/users'

/**
 * Глобальний стор керування станом користувача.
 * Центр безпеки та авторизації додатка.
 */
export const useUserStore = defineStore('user', {
    state: () => ({
        // Дані профілю користувача з Django. null — якщо гість.
        user: null,
        
        // КРИТИЧНО: Прапорець завершення ініціалізації сесії (F5).
        // Роутер чекає, поки він стане true, перш ніж малювати сторінки.
        ready: false,
    }),

    getters: {
        /**
         * Перевірка авторизації.
         * Перетворює об'єкт користувача у булеве значення (true/false).
         */
        isAuthenticated: (state) => state.user !== null,
    },

    actions: {
        /**
         * Процедура авторизації користувача.
         */
        async login(credentials) {
            // 1. Відправляємо логін/пароль на Django
            await loginUser(credentials)
            
            // 2. Одразу завантажуємо профіль (Django вже встановив HttpOnly куки)
            await this.fetchProfile()
        },

        /**
         * Завантаження або відновлення профілю з бекенду.
         */
        async fetchProfile() {
            try {
                const response = await getProfile()
                this.user = response.data
            } catch (error) {
                // Якщо сесія застаріла (401) — гарантовано зачищаємо локальний стан
                if (error.response?.status === 401) {
                    this.logout()
                }
                // Прокидаємо помилку далі для перехоплення в initAuth.js або компонентах
                throw error
            }
        },

        /**
         * Скидання стану при виході або анулюванні сесії.
         */
        logout() {
            this.user = null
        },
    },
})