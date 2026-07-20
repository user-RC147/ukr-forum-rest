import api from '@/api/axios' // Використовуємо єдиний налаштований клієнт

/**
 * Отримати список усіх одиниць виміру.
 * Django URL: GET /api/v1/household/unit-of-measure/
 * @returns {Promise}
 */
export const getUnitsOfMeasure=()=> api.get('/household/unit-of-measure/')