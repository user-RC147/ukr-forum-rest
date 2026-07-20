import api from '@/api/axios'

export const getCategories =() => api.get('/household/categories/')