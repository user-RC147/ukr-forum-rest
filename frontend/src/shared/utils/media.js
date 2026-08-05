
export function getProductThumbnailUrl(product) {
  const firstVisibleFile = product?.files?.find((f) => f.visible !== false)
  if (!firstVisibleFile) return null
  return firstVisibleFile.thumbnail ?? firstVisibleFile.file
}