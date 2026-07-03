import api from '../../../api/axios' // ← 3 уровня вверх до src/api/axios.js

export const getCountries = async () => {
  const { data } = await api.get('/geo/countries/')
  return data
}

export const getRegions = async (countryCode) => {
  const { data } = await api.get('/geo/regions/', {
    params: { country_code: countryCode },
  })
  return data
}

export const getCities = async (regionId) => {
  const { data } = await api.get('/geo/cities/', {
    params: { region: regionId },
  })
  return data
}

export const searchCountries = async (q = '') => {
  const { data } = await api.get('/geo/countries/search/', {
    params: q ? { q } : {},
  })
  return data
}

export const getCountryById = async (countryId) => {
  const { data } = await api.get(`/geo/countries/${countryId}/`)
  return data
}

export const searchCities = async (query, countryCode = null) => {
  const params = { q: query }
  if (countryCode) params.country_id= countryCode

  const { data } = await api.get('/geo/cities/search/', { params })
  return data
}