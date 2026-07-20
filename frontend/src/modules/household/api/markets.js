import api from '@/api/axios'

export const getMarkets=()=>api.get('/household/markets/')

export const createMarket=(data)=>api.post('/household/markets/',data)