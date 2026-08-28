export function normalizeProductText(value, fallback = '') {
  if (value === null || value === undefined) return fallback

  const text = String(value)
    .replace(/\u00A0/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()

  if (!text) return fallback

  if (text.length > 1200) {
    return `${text.slice(0, 1200).trim()}…`
  }

  return text
}

export function getProductTitle(value) {
  return normalizeProductText(value, 'Товар без назви')
}

export function getProductDescription(value) {
  return normalizeProductText(value, 'Опис відсутній')
}
