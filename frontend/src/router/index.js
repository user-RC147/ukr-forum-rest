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
                //meta: { requiresAuth: true },
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
            // ВАЖНО: маршруты shop — плоские сиблинги, а НЕ children с ShopIndexView
            // в роли родителя. ShopIndexView — это просто страница списка товаров,
            // в ней нет <router-view>, поэтому она не может быть "обёрткой" для
            // вложенных маршрутов (детальная страница, создание, редактирование
            // никогда бы не отрендерились внутри неё).
            {
                path: 'shop',
                name: 'shop-index',
                component: () => import('@/modules/shop/views/ShopIndexView.vue'),
                meta: { title: 'Оголошення', requiresAuth: false },
            },
            {
                path: 'shop/my-products',
                name: 'shop-my-products',
                component: () => import('@/modules/shop/views/ShopMyProductsView.vue'),
                meta: { title: 'Мої товари', requiresAuth: true },
            },
            {
                path: 'shop/create',
                name: 'shop-create-product',
                component: () => import('@/modules/shop/views/ShopCreateProductView.vue'),
                meta: { title: 'Новий товар', requiresAuth: true },
            },
            {
                path: 'shop/:pk/update/:productSlug?',
                name: 'shop-update-product',
                component: () => import('@/modules/shop/views/ShopUpdateProductView.vue'),
                meta: { title: 'Редагування товару', requiresAuth: true },
                props: true,
            },
            // TODO: компонент ShopDeleteProductView.vue ещё не создан — см. отдельную
            // задачу "delete confirmation как отдельный route/view" (по аналогии
            // с delete_product.html). Когда будет готов, добавить сюда маршрут:
            {
                path: 'shop/:pk/delete/:productSlug?',
                name: 'shop-delete-product',
                component: () => import('@/modules/shop/views/ShopDeleteProductView.vue'),
                meta: { title: 'Видалення товару', requiresAuth: true },
                props: true,
            },
            {
                path: '/shop/product/:pk(\\d+)/:categorySlug?/:productSlug?',
                name: 'shop-product',
                component: () => import('@/modules/shop/views/ShopProductDetailView.vue'),
            },
            {
            path: '/shop/search',
            name: 'shop-search',
            component: () => import('@/modules/shop/views/ShopSearchView.vue'),
            },
            
            {
                path: 'advboard',
                name: 'advboard',
                component: () => import('@/modules/users/views/HomeView.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'articles',
                component: () => import('@/modules/articles/views/ArticleView.vue'),
                meta: { requiresAuth: true },
                children:[
                    {
                        path:'',
                        name:'article-index',
                        component: () => import('@/modules/articles/views/articles/ArticleListView.vue'),
                    },
                ]
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
            {
                path: 'reset-password',
                name: 'reset-password',
                component: () => import('@/modules/users/views/ResetPasswordView.vue'),
                meta: {requiresAuth: false},
            }
        ],
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import('@/modules/errors/views/NotFoundView.vue'),
        meta: { title: 'Сторінка не знайдена', requiresAuth: false },
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

    if (to.meta.requiresAuth && !userStore.ready) {
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