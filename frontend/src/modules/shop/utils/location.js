export const ADDRESS_ERROR = 'Помилка адреси'

export function localizedName(value) {
  if (typeof value === 'string' && value.trim()) return value.trim()
  if (!value || typeof value !== 'object') return ADDRESS_ERROR
  return value.name_ua?.trim() || value.name?.trim() || value.city?.trim() || ADDRESS_ERROR
}

export function formatAddress({ city, region, country }, includeRegion = false) {
  const parts = includeRegion ? [city, region, country] : [city, country]
  if (parts.some((part) => localizedName(part) === ADDRESS_ERROR)) return ADDRESS_ERROR
  return parts.map(localizedName).join(', ')
}
