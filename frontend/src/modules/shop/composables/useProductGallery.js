import { ref, computed, reactive, watch } from 'vue'

/**
 * Управление галереей картинок товара.
 * reactive() на возврате — чтобы gallery.currentIndex / gallery.total
 * разворачивались сами, без .value, и в script, и в template.
 */
export function useProductGallery(images) {
  const currentIndex = ref(0)

  const total = computed(() => images.value?.length ?? 0)

  // Сменился набор фото (другой товар) — индекс может выйти за границы
  watch(total, () => {
    currentIndex.value = 0
  })

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

  return reactive({ currentIndex, total, show, next, prev, isActive })
}