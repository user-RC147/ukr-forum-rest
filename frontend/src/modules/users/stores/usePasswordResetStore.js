import { defineStore } from 'pinia';
import { ref } from 'vue';
import { requestPasswordReset, confirmPasswordReset } from '../api/users';

export const usePasswordResetStore = defineStore('passwordReset', () => {
    const loading = ref(false);
    const error = ref(null);
    const success = ref(false);

    async function request(email) {
        loading.value = true;
        error.value = null;
        success.value = false;

        try {
            await requestPasswordReset({ email });
            success.value = true;
        } catch (e) {
            error.value = e.response?.data?.detail || 'Не вдалося надіслати лист';
        } finally {
            loading.value = false;
        }
    }

    async function confirm(payload) {
        loading.value = true;
        error.value = null;
        success.value = false;

        try {
            await confirmPasswordReset(payload);
            success.value = true;
        } catch (e) {
            error.value = e.response?.data;
        } finally {
            loading.value = false;
        }
    }

    return { loading, error, success, request, confirm };
});