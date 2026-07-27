import api from '@/api/axios';


export const getPurchaseItems =()=>api.get('household/purchase-items');