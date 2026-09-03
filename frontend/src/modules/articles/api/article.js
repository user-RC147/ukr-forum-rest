import api from '@/api/axios';

export const getArticles = () => {
    return api.get('/article');
};

export const createArticle = (data) => api.post('/article/create/', data);
