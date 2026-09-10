<script setup>
import { ref } from 'vue';
import { usePasswordResetStore } from '@/modules/users/stores/usePasswordResetStore';

const emit = defineEmits(['cancel']);

const passwordResetStore = usePasswordResetStore();
const email = ref('');

function handleCancel() {
    emit('cancel');
}

async function handleSubmit() {
    await passwordResetStore.request(email.value);
}
</script>

<template>
    <div
        class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-[50] p-4"
        @click.self="handleCancel"
    >
        <div class="bg-white p-6 rounded-2xl relative max-w-sm w-full">
            <button
                type="button"
                @click="handleCancel"
                class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 w-8 h-8 rounded-full flex items-center justify-center transition-colors cursor-pointer"
            >
                ✕
            </button>

            <h2 class="text-lg font-semibold text-gray-900 mb-4">Відновлення пароля</h2>

            <div v-if="passwordResetStore.success" class="text-center text-green-600 py-4">
                Якщо email зареєстрований, лист із посиланням надіслано.
            </div>

            <form v-else @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                        Email
                    </label>
                    <input
                        v-model="email"
                        type="email"
                        required
                        placeholder="you@example.com"
                        class="w-full px-3.5 py-2.5 text-sm rounded-lg border border-gray-300 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 focus:outline-none"
                    />
                </div>

                <p v-if="passwordResetStore.error" class="text-rose-500 text-xs">
                    {{ passwordResetStore.error }}
                </p>

                <button
                    type="submit"
                    :disabled="passwordResetStore.loading"
                    class="w-full bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
                >
                    {{ passwordResetStore.loading ? 'Надсилання...' : 'Надіслати посилання' }}
                </button>
            </form>
        </div>
    </div>
</template>