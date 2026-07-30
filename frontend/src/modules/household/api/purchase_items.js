import api from '@/api/axios';

export const getPurchaseItems = (page, page_size, date_from, date_to) =>
    api.get('household/purchase-items', {
        params: { page, page_size, date_from, date_to },
    });
