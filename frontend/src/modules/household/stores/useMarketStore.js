import { defineStore } from "pinia";
import {ref} from 'vue';
import api from '@/api/axios.js'
import axios from "axios";  // Або ваш налаштований екземпляр api, наприклад import api from '@/api'

export const useMarketStore=defineStore('marketStore',{
    // 1. Стан сховища (тут зберігаються наші дані)
    state:()=>({
        markets:[],         // Масив, куди завантажаться всі магазини з бази даних
        isLoading:false,    // Індикатор завантаження (для красивого UX)
        error: null         // Помилки, якщо сервер відповість відмовою
    }),

    // 2. Дії (функції для роботи з API)
    actions:{
        // Функція для отримання списку всіх магазинів
        async fetchMarkets(){
            this.isLoading=true;
            this.error=null;
            try{
                // Робимо GET-запит на ендпоінт магазинів
                const response = await api.get('/household/markets/');
                // Записуємо отриманий масив у наш стан
                this.markets = response.data.results || response.data;
            }catch (err){
                this.error = err.message || 'Не вдалося завантажити магазини';
                console.error('Помилка fetchMarkets:', err);
            } finally {
                this.isLoading = false;
            }
        },

        // Функція для створення нового магазину
        async createMarket(marketData){
            this.isLoading=true;
            this.error=null;
            try{
                // Робимо POST-запит, передаючи об'єкт { name: "..." }
                const response = await api.post('/household/markets/', marketData);
                
                // Після успішного створення додаємо новий магазин у наш масив в пам'яті
                this.markets.push(response.data);

                // Повертаємо створений об'єкт, щоб сторінка знала його ID
                return response.data;
            }catch (err){
                this.error = err.message || 'Не вдалося створити магазин';
                console.error('Помилка createMarket:', err);
                throw err; // Прокидаємо помилку далі у компонент
            } finally {
                this.isLoading = false;
            }
        }
    }

});