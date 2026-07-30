import api from '@/api/axios';

export const getMarketExpenses = (page, page_size, date_from, date_to) =>
    api.get('household/market-expenses', {
        params: { page, page_size, date_from, date_to },
    });
