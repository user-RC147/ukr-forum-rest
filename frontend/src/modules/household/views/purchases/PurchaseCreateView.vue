<script>
</script>


<template>

    <div class="max-w-5xl mx-auto px-4 py-6">

        <!-- Верхній рядок: Повернутися + Зберегти -->
        <div class="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-4 mb-6">
            <router-link :to="{ name: 'household-group' }" 
                class="flex items-center justify-center bg-[#cce9f8] hover:bg-[#aedbf4] text-[#2e332e] px-5 py-3 rounded-xl text-sm font-medium transition transform hover:scale-105 w-full sm:w-auto">
                ← Повернутися
            </router-link>
            
            <button type="submit"
                    class="bg-[#CEC526] hover:bg-[#F2E70A] text-[#33332E] text-lg font-semibold px-5 py-3 rounded-xl transition transform hover:scale-105 w-full sm:w-auto">
                Зберегти
            </button>
        </div>

        <!-- Фільтри це обєкт до якого привязується чек -->
        <div class="flex flex-wrap justify-around mb-8">
            <div class="bg-amber-100 px-4 py-3 rounded-2xl flex min-w-[130px]">
                <select class="w-full bg-transparent focus:outline-none">
                    <option selected>Всі об'єкти</option>
                    <option>Meerkamp, 32</option>
                    <option>Транспортний,2</option>
                    <option>Кірово,23</option>
                </select>
            </div>

            <div class="bg-amber-100 px-4 py-3 rounded-2xl text-center whitespace-nowrap">
                user.name
            </div>

            <div class="bg-amber-100 px-4 py-3 rounded-2xl flex min-w-[130px]">
                <select class="w-full bg-transparent focus:outline-none">
                    <option selected>my group</option>
                    <option>user1</option>
                    <option>user2</option>
                    <option>user3</option>
                </select>
            </div>
        </div>

        <!-- Кнопки створення -->
        <div class="grid grid-cols-2 gap-4 mb-10">
            <a href="#" 
            class="bg-amber-50 hover:bg-amber-100 text-center py-4 rounded-2xl transition">
                створити магазин
            </a>
            <a href="#" 
            class="bg-amber-50 hover:bg-amber-100 text-center py-4 rounded-2xl transition">
                створити товар
            </a>
        </div>

        <!-- Додавання товару -->
        <div class="mb-12">
            <h2 class="text-lg font-semibold mb-4">Додавання товару</h2>
            
            <div class="overflow-x-auto border border-gray-300 rounded-2xl bg-white">
                <table class="w-full min-w-[650px]">
                    <thead>
                        <tr class="border-b text-center bg-gray-50">
                            <th class="border-r py-3 px-4">№</th>
                            <th class="border-r py-3 px-4">Найменування товару</th>
                            <th class="border-r py-3 px-4">од.виміру</th>
                            <th class="border-r py-3 px-4">кількість</th>
                            <th class="border-r py-3 px-4">ціна за одиницю</th>
                            <th class="py-3 px-4">вартість</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b text-center">
                            <td class="border-r py-4 px-2">1</td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="border-r px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                            <td class="px-2"><input type="text" class="w-full text-center focus:outline-none"></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-4">
                <button class="bg-blue-100 hover:bg-blue-200 px-6 py-3 rounded-2xl w-full sm:w-auto transition">
                    + Додати строку
                </button>
            </div>
        </div>

        <!-- Таблиця чека -->
        <div>
            <div class="overflow-x-auto border border-gray-300 rounded-2xl bg-white">
                <table class="w-full min-w-[650px]">
                    <caption class="p-4 border-b bg-amber-50">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <select class="bg-transparent font-medium focus:outline-none">
                                <option>Lidl - Altenessener Str. 289, 45326 Essen</option>
                                <option>Aldi - Setree Str. 4, 45326 Essen</option>
                            </select>
                            <!-- Поле з календарем -->
                            <div class="flex items-center gap-2">
                                <span class="text-sm text-gray-600 whitespace-nowrap">Дата чека:</span>
                                <input 
                                    type="date" 
                                    name="check_date"
                                    value="2026-05-14" 
                                    class="bg-white border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-amber-400">
                            </div>
                        </div>
                    </caption>
                    
                    <thead>
                        <tr class="border-b text-center bg-gray-50">
                            <th class="border-r py-3 px-4">№</th>
                            <th class="border-r py-3 px-4">Найменування товару</th>
                            <th class="border-r py-3 px-4">од.виміру</th>
                            <th class="border-r py-3 px-4">кількість</th>
                            <th class="border-r py-3 px-4">ціна за одиницю</th>
                            <th class="py-3 px-4">вартість</th>
                        </tr>
                    </thead>
                    <tbody class="text-center">
                        <tr class="border-b">
                            <td class="border-r py-3">1</td>
                            <td class="border-r py-3">хліб</td>
                            <td class="border-r py-3">шт.</td>
                            <td class="border-r py-3">1,0</td>
                            <td class="border-r py-3">2,03</td>
                            <td class="py-3">2.03</td>
                        </tr>
                        <tr class="border-b">
                            <td class="border-r py-3">2</td>
                            <td class="border-r py-3">булочка</td>
                            <td class="border-r py-3">шт.</td>
                            <td class="border-r py-3">1,0</td>
                            <td class="border-r py-3">2,03</td>
                            <td class="py-3">2.03</td>
                        </tr>
                        <tr class="border-b">
                            <td class="border-r py-3">3</td>
                            <td class="border-r py-3">молоко</td>
                            <td class="border-r py-3">шт.</td>
                            <td class="border-r py-3">1,0</td>
                            <td class="border-r py-3">2,03</td>
                            <td class="py-3">2.03</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr class="font-semibold bg-amber-50">
                            <td colspan="5" class="text-right py-4 pr-6 border-t">Разом</td>
                            <td class="py-4 text-center border-t">6.09</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>

    </div>

</template>