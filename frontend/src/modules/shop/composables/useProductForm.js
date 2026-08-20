// modules/shop/composables/useProductForm.js
import { ref, reactive, onMounted, toRef } from 'vue'
import { useRouter } from 'vue-router'
import { getCategories, createProduct, updateProduct } from '@/modules/shop/api/shop'
import { useCountryAutocomplete } from './useCountryAutocomplete'
import { useCityAutocomplete } from './useCityAutocomplete'
import { useImageUpload } from './useImageUpload'
import { useToast } from '@/shared/composables/useToast'

// Те самі варіанти, що використовуються у фільтрі стану товару на search.html
export const STATUS_OPTIONS = [
  { value: 'new', label: 'Нові' },
  { value: 'used', label: 'Вживані' },
]

/**
 * @param {object} options
 * @param {'create'|'update'} options.mode
 * @param {object|null} options.product — заповнений товар у режимі редагування (з API)
 */
export function useProductForm({ mode, product = null }) {
  const router = useRouter()
  const { showToast } = useToast()

  const isUpdate = mode === 'update'

  const name = ref(product?.title ?? '')
  const description = ref(product?.description ?? '')
  const categoryId = ref(product?.category?.id ?? '')
  const price = ref(product?.price ?? '')
  const status = ref(product?.status ?? 'new')

  const categories = ref([])
  const isSubmitting = ref(false)
  const fieldErrors = reactive({})
  const nonFieldError = ref('')

  const countryAutocomplete = useCountryAutocomplete({
    id: product?.country?.id ?? '',
    name: product?.country?.name ?? '',
    currency: product?.country?.currency ?? '',
  })

  // region_id больше не выбирается отдельно — он "приклеен" к городу
  // и приходит вместе с ним из /api/geo/cities/search/ (поле region).
  const cityAutocomplete = useCityAutocomplete(
    {
      id: product?.city?.id ?? '',
      name: product?.city?.name ?? '',
      regionId: product?.region?.id ?? '',
      regionName: product?.region?.name ?? '',
    },
    toRef(countryAutocomplete, 'countryId'),
  )

  const existingImages = (product?.files ?? []).map((img) => ({ id: img.id, url: img.file }))
  const imageUpload = useImageUpload(existingImages, mode)

  function onCountrySelect() {
    cityAutocomplete.reset()
  }

  async function loadCategories() {
    try {
      categories.value = await getCategories()
    } catch {
      showToast('Не вдалося завантажити список категорій', 'error')
    }
  }

  function clearErrors() {
    Object.keys(fieldErrors).forEach((key) => delete fieldErrors[key])
    nonFieldError.value = ''
  }

  function applyServerErrors(responseData) {
    clearErrors()
    if (!responseData) return
    Object.entries(responseData).forEach(([key, value]) => {
      const message = Array.isArray(value) ? value.join(' ') : String(value)
      if (key === 'non_field_errors' || key === 'detail') nonFieldError.value = message
      else fieldErrors[key] = message
    })
  }

  /**
   * Повертає об'єкт помилок по кожному полю окремо (а не першу-ліпшу),
   * щоб можна було підсвітити ВСІ проблемні поля одразу, а не змушувати
   * користувача виправляти форму по одній помилці за раз.
   */
  function validateLocally() {
    const errors = {}

    if (!name.value.trim()) errors.name = 'Вкажіть назву товару'
    if (!description.value.trim()) errors.description = 'Вкажіть опис товару'
    if (!categoryId.value) errors.category = 'Оберіть категорію'
    const numericPrice = Number(price.value)
    if (!price.value || !Number.isInteger(numericPrice) || numericPrice <= 0) {
      errors.price = 'Вкажіть коректну ціну цілим числом'
    }

    if (!cityAutocomplete.cityId) {
      errors.city_id = 'Оберіть місто зі списку підказок'
    } else if (!cityAutocomplete.regionId) {
      // regionId приходить автоматично разом із містом — якщо його немає,
      // значить місто вибрано без кліку по підказці, треба перевибрати
      errors.city_id = 'Не вдалося визначити регіон — оберіть місто ще раз зі списку'
    }

    return errors
  }

  async function submit() {
    // Захист від повторних кліків: без цього кожен клік по кнопці, поки
    // ще триває перевірка чи запит, породжував ще одну спробу і ще один
    // toast — як подвійний POST без блокування кнопки в Django-admin.
    if (isSubmitting.value || imageUpload.isValidating) return
    isSubmitting.value = true
    clearErrors()

    try {
      if (!isUpdate && !imageUpload.hasAnyImage) {
        showToast('Додайте хоча б одне фото', 'error')
        return
      }

      const countryOk = await countryAutocomplete.ensureSelected()
      if (!countryOk) {
        fieldErrors.country = 'Оберіть країну зі списку підказок'
        showToast('Перевірте позначені поля форми', 'error')
        return
      }

      const localErrors = validateLocally()
      if (Object.keys(localErrors).length > 0) {
        Object.assign(fieldErrors, localErrors)
        showToast('Перевірте позначені поля форми', 'error')
        return
      }

      const filesValid = await imageUpload.validateAllBeforeSubmit()
      if (!filesValid) return

      const formData = new FormData()
      formData.append('title', name.value)
      formData.append('description', description.value)
      formData.append('category_id', categoryId.value)
      formData.append('price', price.value)
      formData.append('status', status.value)
      formData.append('country_id', countryAutocomplete.countryId)
      formData.append('city_id', cityAutocomplete.cityId)
      formData.append('region_id', cityAutocomplete.regionId)
      imageUpload.appendToFormData(formData)

      const loadingMessage = isUpdate ? 'Збереження змін...' : 'Відправка на сервер...'
      const toastId = showToast(loadingMessage, 'loading')

      try {
        if (isUpdate) {
          await updateProduct(product.id, formData)
          showToast('✓ Зміни успішно збережено!', 'success')
        } else {
          await createProduct(formData)
          showToast('✓ Товар успішно додано!', 'success')
        }
        router.push({ name: 'shop-index' })
      } catch (error) {
        applyServerErrors(error.response?.data)
        showToast('Перевірте дані форми та спробуйте ще раз', 'error')
      } finally {
        if (toastId?.remove) toastId.remove()
      }
    } finally {
      isSubmitting.value = false
    }
  }

  onMounted(loadCategories)

  return reactive({
    name,
    description,
    categoryId,
    price,
    status,
    categories,
    statusOptions: STATUS_OPTIONS,
    isSubmitting,
    fieldErrors,
    nonFieldError,
    countryAutocomplete,
    cityAutocomplete,
    imageUpload,
    onCountrySelect,
    submit,
  })
}