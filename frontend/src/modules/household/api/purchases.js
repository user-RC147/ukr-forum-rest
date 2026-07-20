import api from '@/api/axios';

export const getPurchase = () => api.get('/household/purchases/');
export const createPurchase = (data) => api.post('/household/purchases/', data);
