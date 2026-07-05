import { reactive } from 'vue'

// Модульный singleton — стейт создаётся один раз при первом импорте
// и переживает все вызовы useToast() в любых компонентах/composables.
const toasts = reactive([])

let idCounter = 0

function showToast(message, type = 'info', duration = null) {
  const id = ++idCounter
  const defaultDurations = { success: 4000, error: 8000, warning: 6000, info: 4000, loading: 0 }
  const finalDuration = duration ?? defaultDurations[type] ?? 4000

  const toast = { id, message, type, duration: finalDuration }
  toasts.push(toast)

  if (finalDuration > 0) {
    setTimeout(() => removeToast(id), finalDuration)
  }

  // Возвращаем объект с .remove() — submit() в useProductForm.js это ожидает
  return { id, remove: () => removeToast(id) }
}

function removeToast(id) {
  const index = toasts.findIndex((t) => t.id === id)
  if (index !== -1) toasts.splice(index, 1)
}

// Удобные ярлыки поверх showToast — многие компоненты (ShopDeleteProductView,
// ShopProductDetailView и т.д.) деструктурируют { success, error } из useToast(),
// а не универсальную showToast(message, type). Без этих методов деструктуризация
// давала undefined и падала при вызове (TypeError: showError is not a function).
function success(message, duration) {
  return showToast(message, 'success', duration)
}

function error(message, duration) {
  return showToast(message, 'error', duration)
}

function warning(message, duration) {
  return showToast(message, 'warning', duration)
}

function info(message, duration) {
  return showToast(message, 'info', duration)
}

export function useToast() {
  // Отдаём toasts как есть (это уже reactive-массив, не нужен toRefs)
  // и функции — без всякой обёртки, прямыми ссылками
  return { toasts, showToast, removeToast, success, error, warning, info }
}