 <!-- Модалка на створення -->
    <!-- МОДАЛЬНЕ ВІКНО ДЛЯ СТВОРЕННЯ МАГАЗИНУ -->
        <!-- Тонкий чорний напівпрозорий фон. Показується лише якщо isMarketModalOpen === true -->
        <div v-if="isMarketModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            
            <div class="bg-white rounded-3xl p-6 w-full max-w-lg shadow-2xl relative">
                
                <h3 class="text-xl font-bold text-gray-800 mb-4">Новий магазин</h3>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Назва магазину/місця *</label>
                        <input 
                            type="text" 
                            v-model="newMarketName"
                            placeholder="Наприклад: Lidl, Aldi, Аптека"
                            class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                        >
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Країна</label>
                            <select 
                                v-model="modalCountryId"
                                class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
                            >
                                <option :value="null">Оберіть країну</option>
                                <option v-for="c in countries" :key="c.id" :value="c.id">
                                    {{ c.flag_emoji }} {{ c.name_ua || c.name }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Область / Регіон</label>
                            <select 
                                v-model="modalRegionId"
                                :disabled="!modalCountryId"
                                class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
                            >
                                <option :value="null">Оберіть область</option>
                                <option v-for="r in regions" :key="r.id" :value="r.id">
                                    {{ r.name_ua || r.name }}
                                </option>
                            </select>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Місто</label>
                            <select 
                                v-model="modalCityId"
                                :disabled="!modalRegionId"
                                class="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-blue-500 cursor-pointer disabled:bg-gray-50 disabled:text-gray-400"
                            >
                                <option :value="null">Оберіть місто</option>
                                <option v-for="c in cities" :key="c.id" :value="c.id">
                                    {{ c.name_ua || c.name }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Вулиця, будинок</label>
                            <input 
                                type="text" 
                                v-model="streetAndHouse"
                                placeholder="вул. Головна, 12"
                                class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="flex justify-end gap-3 mt-6 border-t pt-4 border-gray-100">
                    <button 
                        type="button" 
                        @click="isMarketModalOpen = false"
                        class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium transition"
                    >
                        Скасувати
                    </button>
                    
                    <button 
                        type="button" 
                        @click="handleCreateMarket"
                        :disabled="!newMarketName.trim()"
                        class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-5 py-2 rounded-xl text-sm font-semibold transition"
                    >
                        Зберегти
                    </button>
                </div>
            </div>
        </div>