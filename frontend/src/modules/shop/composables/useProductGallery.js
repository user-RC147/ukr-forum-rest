import { ref, computed } from 'vue'

/**
 * Управление галереей картинок товара.
 * Вместо jQuery — просто Vue reactivity.
 */
export function useProductGallery(images) {
  const currentIndex = ref(0)

  const total = computed(() => images.value?.length ?? 0)

  function show(index) {
    if (!total.value) return
    currentIndex.value = ((index % total.value) + total.value) % total.value
  }

  function next() {
    show(currentIndex.value + 1)
  }

  function prev() {
    show(currentIndex.value - 1)
  }

  function isActive(index) {
    return index === currentIndex.value
  }

  return { currentIndex, total, show, next, prev, isActive }
}