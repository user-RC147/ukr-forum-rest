<script setup>
    import { watch } from 'vue';

    const period = defineModel('period');
    const dateFrom = defineModel('dateFrom');
    const dateTo = defineModel('dateTo');

    const today = new Date();

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    watch(period, (newPeriod) => {
        if (newPeriod === 'day') {
            dateFrom.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate()));
            dateTo.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate()));
        } else if (newPeriod === 'week') {
            dateFrom.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7));
            dateTo.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate()));
        } else if (newPeriod === 'month') {
            dateFrom.value = formatDate(new Date(today.getFullYear(), today.getMonth() - 1, today.getDate()));
            dateTo.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate()));
        } else if (newPeriod === 'quarter') {
            dateFrom.value = formatDate(new Date(today.getFullYear(), today.getMonth() - 3, today.getDate()));
            dateTo.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate()));
        } else if (newPeriod === 'year') {
            dateFrom.value = formatDate(new Date(today.getFullYear()-1, today.getMonth(), today.getDate()));
            dateTo.value = formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate()));
        }
    });
</script>

<template>
    <div class="flex justify-between">
        <select v-model="period" class="bg-transparent focus:outline-none text-sm cursor-pointer mx-6 w-full">
            <option :value="null">За весь період</option>
            <option value="day">День</option>
            <option value="week">Тиждень</option>
            <option value="month">Місяць</option>
            <option value="quarter">Квартал</option>
            <option value="year">Рік</option>
        </select>
        <div class="flex gap-2">
            <div class="flex items-center justify-end">
                <span>з</span>
                <input v-model="dateFrom" type="date" class="border border-gray-300 p-1 ml-2 rounded-lg text-sm" />
            </div>
            <div class="flex items-center justify-end">
                <span>по</span>
                <input v-model="dateTo" type="date" class="border border-gray-300 p-1 ml-2 rounded-lg text-sm" />
            </div>
        </div>
    </div>
</template>
