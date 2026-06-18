import { reactive } from 'vue'

/**
 * Глобальный стейт тостов — не Pinia-store, потому что это
 * чисто UI-состояние без бизнес-логики (как messages framework
 * в Django, только без перезагрузки страницы).
 */
const toasts = reactive([])
let idCounter = 0

const ICONS = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' }
const DURATIONS = { success: 4000, error: 6000, warning: 5000, info: 4000 }

function show(message, type = 'info', duration) {
  const id = ++idCounter
  const ms = duration ?? DURATIONS[type] ?? 4000

  toasts.push({ id, message, type, icon: ICONS[type] ?? ICONS.info })

  if (ms > 0) {
    setTimeout(() => remove(id), ms)
  }
  return id
}

function remove(id) {
  const index = toasts.findIndex((t) => t.id === id)
  if (index !== -1) toasts.splice(index, 1)
}

export function useToast() {
  return {
    toasts,
    success: (msg, ms) => show(msg, 'success', ms),
    error: (msg, ms) => show(msg, 'error', ms),
    warning: (msg, ms) => show(msg, 'warning', ms),
    info: (msg, ms) => show(msg, 'info', ms),
    remove,
  }
}