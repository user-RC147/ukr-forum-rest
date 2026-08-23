<script setup>
const emit = defineEmits(['submit', 'cancel'])

function handleSubmit() {
    emit('submit')
}

function handleCancel() {
    emit('cancel')
}
</script>

<template>
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl">
            <h3 class="text-lg font-bold text-gray-900 mb-2">Видалити профіль?</h3>
            <p class="text-sm text-gray-500 mb-6">
                Акаунт буде деактивовано. Ви впевнені?
            </p>
            <div class="flex justify-end gap-3">
                <button
                    type="button"
                    @click="handleCancel"
                    class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium transition"
                >
                    Скасувати
                </button>
                <button
                    type="button"
                    @click="handleSubmit"
                    class="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-xl text-sm font-medium transition cursor-pointer"
                >
                    Так, видалити
                </button>
            </div>
        </div>
    </div>
</template>