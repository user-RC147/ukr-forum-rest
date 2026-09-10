import { defineStore } from 'pinia';
import { ref } from 'vue';
import { confirmEmail } from '../api/users';

export const useEmailConfirmationStore = defineStore('emailConfirmation', () => {
    const loading = ref(false);
    const error = ref(null);
    const success = ref(false);

    async function confirm(token) {
        loading.value = true;
        error.value = null;
        success.value = false;

        try {
            await confirmEmail(token);
            success.value = true;
        } catch (e) {
            error.value = e.response?.data?.detail || 'Не вдалося підтвердити email';
        } finally {
            loading.value = false;
        }
    }

    return { loading, error, success, confirm };
});