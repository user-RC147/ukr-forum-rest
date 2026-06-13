import api from '@/api/axios.js'

// GET /api/household/assets/ — список активів
export const getAssets=()=>api.get('/household/assets/')

// POST /api/household/assets/ — створити актив
export const createAsset=(data)=>api.post('/household/assets/',data)