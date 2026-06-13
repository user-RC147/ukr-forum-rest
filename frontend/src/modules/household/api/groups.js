import api from '@/api/axios.js'


export const getGroups = () => api.get('/household/groups/')
export const createGroup = (name) => api.post('/household/groups/', { name })