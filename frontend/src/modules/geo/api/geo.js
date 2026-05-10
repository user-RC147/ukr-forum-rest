import api from '../../../api/axios'  // ← 3 рівні вгору до src/api/axios.js

export const getCountries = () =>
    api.get('/geo/countries/')

export const getRegions = (countryCode) =>
    api.get(`/geo/regions/?country_code=${countryCode}`)

export const getCities = (regionId) =>
    api.get(`/geo/cities/?region=${regionId}`)

export const searchCities = (query, countryCode = null) => {
    let url = `/geo/cities/?search=${query}`
    if (countryCode) url += `&country_code=${countryCode}`
    return api.get(url)
}