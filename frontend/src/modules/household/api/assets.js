import api from '@/api/axios.js'

// GET /api/household/assets/?group_id=5 — список активів для конкретної групи
// Додаємо аргумент group_id та передаємо його через params
export const getAssets=(group_id)=>{
    const config={}
    if (group_id){
        config.params={group_id}
    }
    return api.get('/household/assets/', config)
}

// POST /api/household/assets/ — створити актив
export const createAsset = (data) => api.post('/household/assets/', data)





// // GET /api/household/assets/ — список активів
// export const getAssets=()=>api.get('/household/assets/')

// // POST /api/household/assets/ — створити актив
// export const createAsset=(data)=>api.post('/household/assets/',data)