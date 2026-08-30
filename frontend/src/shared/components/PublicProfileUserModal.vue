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

    <div>Hallo User</div>
</template>