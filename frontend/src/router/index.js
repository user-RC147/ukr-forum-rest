import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../modules/users/stores/useUserStore'

const routes = [
  {
    path: '/',
    component: () => import('../shared/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('../modules/users/views/ProfileView.vue'),
        // meta — додаткова інформація про маршрут
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: '/auth',
    component: () => import('../shared/layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('../modules/users/views/LoginView.vue'),
        meta: { requiresAuth: false },
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('../modules/users/views/RegisterView.vue'),
        meta: { requiresAuth: false },
      },
    ],
  },
]

const router = createRouter({
  // createWebHistory — чисті URL без # (як /login замість /#/login)
  history: createWebHistory(),
  routes,
})

// Navigation guard — це як middleware в Django
// Перевіряє перед кожним переходом чи є права
router.beforeEach((to) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    // якщо сторінка захищена і не залогінений — redirect на логін
    return { name: 'login' }
  }

  if (!to.meta.requiresAuth && userStore.isAuthenticated) {
    // якщо вже залогінений і йде на логін/реєстрацію — redirect на home
    return { name: 'home' }
  }
})

export default router