import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getArticles } from '../api/article';

export const useArticleStore = defineStore('article', () => {
    const articles = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const fetchArticles = async () => {
        loading.value = true;
        error.value = null;
        try {
            const response = await getArticles();
            articles.value = response.data.results;
        } catch (err) {
            error.value = err.response?.data?.detail || 'Помилка при завантаженні статей';
        } finally {
            loading.value = false;
        }
    };



    return {articles,loading,error, fetchArticles,};

});
