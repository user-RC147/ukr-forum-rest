import api from '@/api/axios';

export const getPurchaseItems = (page, page_size) =>
    api.get('household/purchase-items', {
        params: { page, page_size },
    });
