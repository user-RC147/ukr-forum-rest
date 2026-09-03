<script setup>
    import { onMounted, ref } from 'vue';
    import { useArticleStore } from '../../stores/useArticleStore';
    import PublicProfileUserModal from '../../../../shared/components/PublicProfileUserModal.vue'; //for modal window userId

    const articleStore = useArticleStore();

    const isUserPublicModalOpen = ref(false); //for modal window userId
    const selectedUserId = ref(null);

    const openUserModal = (userId) => { //for modal window userId
        selectedUserId.value = userId; //for modal window userId
        isUserPublicModalOpen.value = true; //for modal window userId
    }; //for modal window userId

    onMounted(() => {
        articleStore.fetchArticles();
    });
</script>

<template>
    <div>
        <div>
            <div v-for="article in articleStore.articles" :key="article.id" class="p-4 border rounded">
                <p class="font-bold text-lg">{{ article.title }}</p>
                <p>{{ article.description }}</p>
                
                <!-- for modal window userId ------------------>
                <button
                    v-if="article.created_by"
                    type="button"
                    @click="openUserModal(article.created_by.id)"
                    class="cursor-pointer text-blue-600 hover:underline inline-block mt-2"
                >
                    {{ article.created_by.display_name }}
                </button>
                <!-- ------------------------- -->
            </div>
        </div>

        <!-- МОДАЛЬНЕ ВІКНО ДЛЯ ВІДОБРАЖЕННЯ ПУБЛІЧНОГО ПРОФІЛЮ ЮЗЕРА -->
        <PublicProfileUserModal 
            v-if="isUserPublicModalOpen"
            :user-id="selectedUserId"
            @cancel="isUserPublicModalOpen = false" 
        />
    </div>
</template>
