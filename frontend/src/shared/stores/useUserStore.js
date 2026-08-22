import { defineStore } from 'pinia'
import { loginUser, getProfile, logoutUser } from '../../modules/users/api/users'

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
                this.user = response.data.results
            } catch (error) {
                // Якщо сесія застаріла (401) — гарантовано зачищаємо локальний стан.
                // Викликаємо саме "тихий" варіант — без повторного запиту на /logout/,
                // бо якщо кука вже невалідна, серверний logout все одно нічого не змінить,
                // а тільки додасть зайвий мережевий запит і потенційну помилку.
                if (error.response?.status === 401) {
                    this.clearLocalSession()
                }
                // Прокидаємо помилку далі для перехоплення в initAuth.js або компонентах
                throw error
            }
        },

        /**
         * Повний вихід користувача: анулює сесію на бекенді
         * (стирає HttpOnly cookie, додає refresh token у blacklist)
         * і чистить локальний стан.
         *
         * Викликається явно користувачем (наприклад, кнопка "Вийти").
         */
        async logout() {
            try {
                // POST-запит — потребує CSRF-заголовка,
                // переконайся, що csrftoken cookie вже отримана (initAuth/initCsrf)
                await logoutUser()
            } catch (error) {
                // Навіть якщо запит на бекенд впав (мережа, токен вже невалідний
                // тощо) — все одно чистимо локальний стан, бо користувач
                // однозначно хоче вийти
                console.error('Не вдалося виконати серверний logout:', error)
            } finally {
                this.clearLocalSession()
            }
        },

        /**
         * Локальне очищення стану без звернення до бекенду.
         * Використовується при 401 (сесія вже невалідна на сервері)
         * або як фінальний крок повного logout().
         */
        clearLocalSession() {
            this.user = null
        },
    },
})