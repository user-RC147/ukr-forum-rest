<script setup>
    import { onMounted } from 'vue';
    import { useArticleStore } from '@/modules/articles/stores/useArticleStore';

    const articleStore = useArticleStore();

    onMounted(() => {
        articleStore.fetchArticles();
    });
</script>


<template>
    <RouterView />
</template>

