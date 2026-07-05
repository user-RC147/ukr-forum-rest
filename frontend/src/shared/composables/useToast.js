import { reactive } from 'vue'

// Модульний singleton — стейт створюється один раз при першому імпорті
// і переживає всі виклики useToast() у будь-яких компонентах/composables.
const toasts = reactive([])

let idCounter = 0
const timers = new Map()

// Заголовок автоматично підбирається за типом тосту — виклики на кшталт
// showToast('Товар успішно додано!', 'success') не потребують зміни
// сигнатури по всьому проєкту, просто отримують гарний title "з коробки".
const TITLES = {
  success: 'Успіх',
  error: 'Помилка',
  warning: 'Увага',
  info: 'Інформація',
  loading: 'Зачекайте',
}

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
  const defaultDurations = { success: 4000, error: 6000, warning: 5000, info: 4000, loading: 0 }
  const finalDuration = duration ?? defaultDurations[type] ?? 4000
  const title = TITLES[type] ?? TITLES.info

  // Дедуплікація: однакова помилка (напр. кілька невдалих спроб сабміту
  // поспіль) не створює нову картку, а продовжує показ існуючої — інакше
  // екран за секунди перетворюється на стіну однакових банерів.
  const existing = toasts.find((t) => t.message === message && t.type === type)
  if (existing) {
    existing.count += 1
    existing.duration = finalDuration
    existing.resetKey += 1 // сигнал для ToastItem перезапустити прогрес-бар
    scheduleRemoval(existing.id, finalDuration)
    return { id: existing.id, remove: () => removeToast(existing.id) }
  }

  const id = ++idCounter
  toasts.push({ id, title, message, type, duration: finalDuration, count: 1, resetKey: 0 })
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