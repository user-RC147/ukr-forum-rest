import { ref } from 'vue';
import { getCountries, getRegions, getCities } from '../../../modules/geo/api/geo';

export function useGeoSelector() {
    const countries = ref([]);
    const regions = ref([]);
    const cities = ref([]);

    const loading = ref(false);
    const error = ref(null);

    async function loadCountries() {
        loading.value = true;
        error.value = null;
        try {
            const response = await getCountries();
            countries.value = response.results || response;
        } catch (e) {
            error.value = 'Помилка завантаження країн';
        } finally {
            loading.value = false;
        }
    }

    async function onCountryChange(countryId) {
        regions.value = [];
        cities.value = [];
        if (!countryId) return;
        try {
            const response = await getRegions(countryId);
            regions.value = response.results || response;
        } catch (e) {
            error.value = 'Помилка завантаження регіонів';
        }
    }

    async function onRegionChange(regionId) {
        cities.value = [];
        if (!regionId) return;
        try {
            const response = await getCities(regionId);
            cities.value = response.results || response;
        } catch (e) {
            error.value = 'Помилка завантаження міст';
        }
    }

    return {countries,regions,cities,loading,error, loadCountries,onCountryChange,onRegionChange};
}
