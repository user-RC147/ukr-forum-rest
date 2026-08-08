import api from '../../../api/axios' // ← 3 уровня вверх до src/api/axios.js

export const getCountries = async () => {
  const { data } = await api.get('/geo/country/')
  return data
}

export const getRegions = async (countryId) => {
  const { data } = await api.get('/geo/region/', {
    params: { country_id: countryId },
  })
  return data
}

export const getCities = async (regionId) => {
  const { data } = await api.get('/geo/city/', {
    params: { region_id: regionId },
  })
  return data
}

export const searchCountries = async (q = '') => {
  const { data } = await api.get('/geo/country/search/', {
    params: q ? { q } : {},
  })
  return data
}

export const getCountryById = async (countryId) => {
  const { data } = await api.get(`/geo/country/${countryId}/`)
  return data
}

export const searchCities = async (query, countryCode = null) => {
  const params = { q: query }
  if (countryCode) params.country_id= countryCode

  const { data } = await api.get('/geo/city/search/', { params })
  return data
}