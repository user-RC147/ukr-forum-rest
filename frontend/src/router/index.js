import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/shared/stores/useUserStore'

const routes = [
    {
        path: '/',
        component: () => import('@/shared/layouts/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'home',
                component: () => import('@/modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'profile',
                name: 'profile',
                component: () => import('@/modules/users/views/ProfileView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'geo/location',
                name: 'location',
                component: () => import('@/modules/geo/views/LocationView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'shop',
                component: () => import('@/modules/shop/views/ShopIndexView.vue'),
                meta: { title: 'Оголошення', requiresAuth: true },
                children:[
                    {
                        path: '',
                        name: 'shop-index',
                        component: () => import('@/modules/shop/views/ShopIndexView.vue'),
                    },
                    {
                        path: 'shop/:pk',  
                        name: 'shop-product',
                        component: () => import('@/modules/shop/views/ShopProductDetailView.vue'),
                    },
                    {
                        path: 'shop/create',  
                        name: 'shop-create-product',
                        component: () => import('@/modules/shop/views/ShopIndexView.vue'),
                    },

                ],
            },
            
            {
                path: 'advboard',
                name: 'advboard',
                component: () => import('@/modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'articles',
                name: 'articles',
                component: () => import('@/modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'stories',
                name: 'stories',
                component: () => import('@/modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'outlay',
                name: 'outlay',
                component: () => import('@/modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'household',
                component: () => import('@/modules/household/views/HouseHoldIndexView.vue'),
                meta: { requiresAuth: true },
                children: [
                    {
                        path: '',
                        name: 'household-index',
                        component: () => import('@/modules/household/views/OutlayAllView.vue'),
                    },
                    {
                        path: 'unit_of_measure',
                        name: 'unit-of-measure',
                        component: () => import('@/modules/household/views/units/Units.vue'),
                    },
                    {
                        path: 'purchases/create',
                        name: 'household-purchases-create',
                        component: () => import('@/modules/household/views/purchases/PurchaseCreateView.vue'),
                    },
                    {
                        path: 'groups/create',
                        name: 'household-group-create',
                        component: () => import('@/modules/household/views/group/GroupCreate.vue'),
                    },
                    {
                        path: 'assets/create',
                        name: 'household-asset-create',
                        component: () => import('@/modules/household/views/assets/AssetCreate.vue')
                    },
                    {
                        path: 'markets/create',
                        name: 'household-market-create',
                        component: () => import('@/modules/household/views/markets/MarketCreate.vue')
                    },
                ],
            },
        ],
    },
    {
        path: '/auth',
        component: () => import('@/shared/layouts/AuthLayout.vue'),
        children: [
            {
                path: 'login',
                name: 'login',
                component: () => import('@/modules/users/views/LoginView.vue'),
                meta: { requiresAuth: false },
            },
            {
                path: 'register',
                name: 'register',
                component: () => import('@/modules/users/views/RegisterView.vue'),
                meta: { requiresAuth: false },
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

/**
 * Асинхронний Navigation Guard.
 * Запобігає передчасному пропуску користувача, доки триває перевірка сесії (initAuth).
 */
router.beforeEach(async (to, from) => {
    const userStore = useUserStore()

    if (!userStore.ready) {
        await new Promise((resolve) => {
            const unwatch = userStore.$subscribe((mutation, state) => {
                if (state.ready) {
                    unwatch()
                    resolve()
                }
            })
        })
    }

    if (to.meta.requiresAuth && !userStore.isAuthenticated) {
        return { name: 'login' }
    }
})
export default router