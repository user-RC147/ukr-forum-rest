import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../modules/users/stores/useUserStore';

const routes = [
    {
        path: '/',
        component: () => import('../shared/layouts/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'home',
                component: () => import('../modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'profile',
                name: 'profile',
                component: () => import('../modules/users/views/ProfileView.vue'),
                meta: { requiresAuth: true },
                
            },            
            {
                path: 'geo/location',
                name: 'location',
                component: () => import('../modules/geo/views/LocationView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'shop',
                name: 'shop',
                component: () => import('../modules/users/views/HomeView.vue'), // тимчасово
                meta: { requiresAuth: true },
            },
            {
                path: 'advboard',
                name: 'advboard',
                component: () => import('../modules/users/views/HomeView.vue'), // тимчасово
                meta: { requiresAuth: true },
            },
            {
                path: 'articles',
                name: 'articles',
                component: () => import('../modules/users/views/HomeView.vue'), // тимчасово
                meta: { requiresAuth: true },
            },
            {
                path: 'stories',
                name: 'stories',
                component: () => import('../modules/users/views/HomeView.vue'), // тимчасово
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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to) => {
    const userStore = useUserStore();

    if (to.meta.requiresAuth && !userStore.isAuthenticated) {
        return { name: 'login' };
    }

    if (!to.meta.requiresAuth && userStore.isAuthenticated) {
        return { name: 'home' };
    }
});

export default router;