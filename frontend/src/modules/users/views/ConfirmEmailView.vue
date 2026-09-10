<script setup>
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useEmailConfirmationStore } from '../stores/useEmailConfirmationStore';

const route = useRoute();
const router = useRouter();
const emailConfirmationStore = useEmailConfirmationStore();

onMounted(() => {
    const token = route.query.token;
    if (token) {
        emailConfirmationStore.confirm(token);
    }
});

function goToLogin() {
    router.push({ name: 'login' });
}
</script>

<template>
    <div class="min-h-screen flex items-center justify-center p-4">
        <div class="max-w-md w-full text-center">

            <div v-if="emailConfirmationStore.loading">
                Підтвердження email...
            </div>

            <div v-else-if="emailConfirmationStore.success">
                <h1 class="text-xl font-semibold text-green-600 mb-4">Email підтверджено!</h1>
                <p class="mb-4">Тепер ви можете увійти у свій акаунт.</p>
                <button
                    type="button"
                    @click="goToLogin"
                    class="bg-amber-500 text-white px-4 py-2 rounded-lg cursor-pointer"
                >
                    Перейти до входу
                </button>
            </div>

            <div v-else-if="emailConfirmationStore.error">
                <h1 class="text-xl font-semibold text-rose-600 mb-4">Помилка підтвердження</h1>
                <p>{{ emailConfirmationStore.error }}</p>
            </div>

        </div>
    </div>
</template>