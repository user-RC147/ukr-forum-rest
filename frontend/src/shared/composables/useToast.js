import { reactive } from 'vue'

// Модульний singleton — стейт створюється один раз при першому імпорті
// і переживає всі виклики useToast() у будь-яких компонентах/composables.
const toasts = reactive([])

let idCounter = 0
const timers = new Map()

function clearTimer(id) {
  const timer = timers.get(id)
  if (timer) {
    clearTimeout(timer)
    timers.delete(id)
  }
}

function scheduleRemoval(id, duration) {
  clearTimer(id)
  if (duration > 0) {
    timers.set(id, setTimeout(() => removeToast(id), duration))
  }
}

function showToast(message, type = 'info', duration = null) {
  const defaultDurations = { success: 4000, error: 8000, warning: 6000, info: 4000, loading: 0 }
  const finalDuration = duration ?? defaultDurations[type] ?? 4000

  // Дедуплікація: однакова помилка (напр. від подвійного кліку, поки триває
  // валідація) не повинна плодити десятки копій одного й того самого тосту —
  // замість цього продовжуємо його показ і рахуємо повтори.
  const existing = toasts.find((t) => t.message === message && t.type === type)
  if (existing) {
    existing.count += 1
    scheduleRemoval(existing.id, finalDuration)
    return { id: existing.id, remove: () => removeToast(existing.id) }
  }

  const id = ++idCounter
  toasts.push({ id, message, type, count: 1 })
  scheduleRemoval(id, finalDuration)

  return { id, remove: () => removeToast(id) }
}

function removeToast(id) {
  clearTimer(id)
  const index = toasts.findIndex((t) => t.id === id)
  if (index !== -1) toasts.splice(index, 1)
}

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
  return { toasts, showToast, removeToast, success, error, warning, info }
}