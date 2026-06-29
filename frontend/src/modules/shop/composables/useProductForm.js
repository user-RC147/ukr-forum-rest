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
  // Поэтому передаём в useCityAutocomplete начальный region из товара,
  // а сам composable обновит regionId/regionName при выборе нового города.
  const cityAutocomplete = useCityAutocomplete(
    {
      id: product?.city?.id ?? '',
      name: product?.city?.name ?? '',
      regionId: product?.region?.id ?? '',
      regionName: product?.region?.name ?? '',
    },
    toRef(countryAutocomplete, 'countryId'),
  )

  const existingImages = (product?.files ?? []).map((img) => ({ id: img.id, url: img.image ?? img.url }))
  const imageUpload = useImageUpload(existingImages)

  // При смене страны зависимый город (а вместе с ним и регион) обязательно сбрасывается —
  // повторяет защиту от рассинхрона из оригинального product_list.js / create_product.js
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

  function validateLocally() {
    if (!name.value.trim()) return 'Вкажіть назву товару'
    if (!description.value.trim()) return 'Вкажіть опис товару'
    if (!categoryId.value) return 'Оберіть категорію'
    if (!price.value || Number(price.value) <= 0) return 'Вкажіть коректну ціну'
    if (!cityAutocomplete.cityId) return 'Оберіть місто зі списку підказок'
    // regionId приходить автоматично разом з містом — якщо його немає,
    // значить місто вибрано "вручну" без кліку по підказці, треба перевибрати
    if (!cityAutocomplete.regionId) return 'Не вдалося визначити регіон — оберіть місто ще раз зі списку'
    return ''
  }

  async function submit() {
    clearErrors()

    if (!isUpdate && !imageUpload.hasAnyImage) {
      showToast('Додайте хоча б одне фото', 'error')
      return
    }

    const countryOk = await countryAutocomplete.ensureSelected()
    if (!countryOk) {
      showToast('Оберіть країну зі списку підказок', 'error')
      return
    }

    const validationError = validateLocally()
    if (validationError) {
      showToast(validationError, 'error')
      return
    }

    const filesValid = await imageUpload.validateAllBeforeSubmit()
    if (!filesValid) return

    const formData = new FormData()
    formData.append('title', name.value)
    formData.append('description', description.value)
    formData.append('category_id', categoryId.value)
    formData.append('price', price.value)
    // formData.append('status', status.value)
    formData.append('country_id', countryAutocomplete.countryId)
    formData.append('city_id', cityAutocomplete.cityId)
    formData.append('region_id', cityAutocomplete.regionId)
    imageUpload.appendToFormData(formData)

    isSubmitting.value = true
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
      isSubmitting.value = false
      if (toastId?.remove) toastId.remove()
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