// modules/shop/composables/useImageUpload.js
import { ref, reactive, computed } from 'vue'
import { useToast } from '@/shared/composables/useToast'

export const IMAGE_CONFIG = {
  MAX_FILES: 10,
  MAX_SIZE_BYTES: 10 * 1024 * 1024,
  MIN_SIZE_BYTES: 100,
  ALLOWED_MIME_TYPES: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'],
  ALLOWED_EXTENSIONS: ['.jpg', '.jpeg', '.png', '.webp', '.gif'],
  MAX_DIMENSION: 8000,
  MIN_DIMENSION: 100,
  MAX_ASPECT_RATIO: 20,
}

function getPluralForm(num, one, few, many) {
  const n = Math.abs(num) % 100
  const n1 = n % 10
  if (n > 10 && n < 20) return many
  if (n1 > 1 && n1 < 5) return few
  if (n1 === 1) return one
  return many
}

function validateExtensionAndName(filename) {
  if (filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
    return { valid: false, error: 'Заборонені символи в імені файлу' }
  }
  if (filename.length > 255) return { valid: false, error: "Ім'я файлу занадто довге" }
  const lower = filename.toLowerCase()
  const hasValidExt = IMAGE_CONFIG.ALLOWED_EXTENSIONS.some((ext) => lower.endsWith(ext))
  if (!hasValidExt) {
    return { valid: false, error: `Дозволені формати: ${IMAGE_CONFIG.ALLOWED_EXTENSIONS.join(', ')}` }
  }
  return { valid: true }
}

function validateMime(file) {
  if (!file.type || !IMAGE_CONFIG.ALLOWED_MIME_TYPES.includes(file.type)) {
    return { valid: false, error: `Недозволений тип файлу: ${file.type || 'невідомий'}` }
  }
  return { valid: true }
}

function validateSize(file) {
  if (file.size === 0) return { valid: false, error: 'Файл порожній' }
  if (file.size < IMAGE_CONFIG.MIN_SIZE_BYTES) return { valid: false, error: 'Файл занадто малий' }
  if (file.size > IMAGE_CONFIG.MAX_SIZE_BYTES) {
    const sizeMB = (file.size / 1024 / 1024).toFixed(2)
    return { valid: false, error: `Розмір ${sizeMB} MB перевищує максимум 10 MB` }
  }
  return { valid: true }
}

function validateDimensions(file) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onerror = () => resolve({ valid: false, error: 'Помилка читання файлу' })
    reader.onload = (e) => {
      const img = new Image()
      img.onerror = () => resolve({ valid: false, error: 'Файл не є зображенням' })
      img.onload = () => {
        const { width, height } = img
        if (width > IMAGE_CONFIG.MAX_DIMENSION || height > IMAGE_CONFIG.MAX_DIMENSION) {
          return resolve({ valid: false, error: `${width}x${height}px перевищує максимум` })
        }
        if (width < IMAGE_CONFIG.MIN_DIMENSION || height < IMAGE_CONFIG.MIN_DIMENSION) {
          return resolve({ valid: false, error: `${width}x${height}px менше мінімуму` })
        }
        if (Math.max(width, height) / Math.min(width, height) > IMAGE_CONFIG.MAX_ASPECT_RATIO) {
          return resolve({ valid: false, error: 'Некоректні пропорції зображення' })
        }
        resolve({ valid: true })
      }
      img.src = e.target.result
    }
    reader.readAsDataURL(file)
  })
}

async function validateImageFile(file) {
  const checks = [validateExtensionAndName(file.name), validateMime(file), validateSize(file)]
  const failed = checks.find((c) => !c.valid)
  if (failed) return failed
  return validateDimensions(file)
}

function readAsDataUrl(file) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.readAsDataURL(file)
  })
}

/**
 * @param {Array<{id: number|string, url: string}>} existingImages — тільки для режиму update
 * @param {'create'|'update'} mode
 *
 * UI не змінюється: як і раніше — один хрестик на існуючому фото = "прибрати".
 * А от ЩО це означає для бекенду (пряме видалення чи заміна вмісту при
 * збереженому id) фронт вирішує сам, автоматично, у appendToFormData:
 * "видалене старе" + "щойно додане нове" паруються в update_files[id],
 * поки вистачає або тих, або тих. Клієнту думати про це не потрібно.
 */
export function useImageUpload(existingImages = [], mode = 'create') {
  const { showToast, showToastList } = useToast()

  const newFiles = ref([]) // [{ file: File, previewUrl: string }]
  const remainingExisting = ref([...existingImages]) // [{ id, url }] — те, що лишилось видимим у галереї
  const deletedImageIds = ref([]) // id фото, які користувач прибрав хрестиком

  const isDragging = ref(false)
  const isValidating = ref(false)

  const totalCount = computed(() => newFiles.value.length + remainingExisting.value.length)
  const slotsLeft = computed(() => IMAGE_CONFIG.MAX_FILES - totalCount.value)
  const hasAnyImage = computed(() => totalCount.value > 0)

  async function addFiles(fileList) {
    const incoming = Array.from(fileList || [])
    if (!incoming.length) return

    isValidating.value = true
    incoming.sort((a, b) => a.lastModified - b.lastModified)

    const errors = []
    let addedCount = 0

    for (const file of incoming) {
      if (totalCount.value + addedCount >= IMAGE_CONFIG.MAX_FILES) {
        errors.push(`Ліміт ${IMAGE_CONFIG.MAX_FILES} фото загалом досягнуто`)
        break
      }
      const isDuplicate = newFiles.value.some(
        (f) => f.file.name === file.name && f.file.size === file.size && f.file.lastModified === file.lastModified,
      )
      if (isDuplicate) {
        errors.push(`«${file.name}» вже додано`)
        continue
      }
      const validation = await validateImageFile(file)
      if (!validation.valid) {
        errors.push(`${file.name}: ${validation.error}`)
        continue
      }
      const previewUrl = await readAsDataUrl(file)
      newFiles.value.push({ file, previewUrl })
      addedCount++
    }

    isValidating.value = false

    if (addedCount > 0) {
      showToast(`✓ Додано ${addedCount} ${getPluralForm(addedCount, 'файл', 'файли', 'файлів')}`, 'success')
    }
    if (errors.length) showToastList('Помилки завантаження', errors, 'error')
  }

  function removeNewFile(index) {
    const [removed] = newFiles.value.splice(index, 1)
    if (removed) showToast(`Видалено: ${removed.file.name}`, 'info', 2500)
  }

  /** Той самий хрестик, що й раніше. Що з цим станеться на бекенді — вирішується пізніше, автоматично. */
  function removeExistingImage(imageId) {
    remainingExisting.value = remainingExisting.value.filter((img) => img.id !== imageId)
    deletedImageIds.value.push(imageId)
    showToast('Фото буде видалено після збереження', 'info', 3500)
  }

  async function onDrop(event) {
    isDragging.value = false
    await addFiles(event.dataTransfer.files)
  }

  async function validateAllBeforeSubmit() {
    for (const { file } of newFiles.value) {
      const result = await validateImageFile(file)
      if (!result.valid) {
        showToast(`Помилка у файлі «${file.name}»: ${result.error}`, 'error')
        return false
      }
    }
    return true
  }

  /**
   * Авто-парування delete+create → update_files[id].
   * Не міняє поведінку для користувача, лише оптимізує запит до бекенду:
   * замість "видалити стару картку + створити нову" (втрата id/позиції),
   * там де можливо — "оновити вміст картки за тим самим id".
   */
  function appendToFormData(formData) {
    if (mode === 'update') {
      const pendingNewFiles = [...newFiles.value]
      const pendingDeletedIds = [...deletedImageIds.value]

      const pairCount = Math.min(pendingNewFiles.length, pendingDeletedIds.length)
      for (let i = 0; i < pairCount; i++) {
        const { file } = pendingNewFiles.shift()
        const id = pendingDeletedIds.shift()
        formData.append(`update_files[${id}]`, file)
      }

      // Залишок нових файлів (якщо додали більше, ніж видалили) — справді нові фото
      pendingNewFiles.forEach(({ file }) => formData.append('create_files', file))

      // Залишок видалених id без пари (якщо видалили більше, ніж додали) —
      // нікуди не потрапляє: бек видалить їх сам, бо їх немає ні в keep, ні в update

      remainingExisting.value.forEach((img) => formData.append('keep_files_ids', img.id))
    } else {
      newFiles.value.forEach(({ file }) => formData.append('files', file))
    }
  }

  return reactive({
    newFiles,
    remainingExisting,
    deletedImageIds,
    isDragging,
    isValidating,
    totalCount,
    slotsLeft,
    hasAnyImage,
    addFiles,
    removeNewFile,
    removeExistingImage,
    onDrop,
    validateAllBeforeSubmit,
    appendToFormData,
    config: IMAGE_CONFIG,
  })
}