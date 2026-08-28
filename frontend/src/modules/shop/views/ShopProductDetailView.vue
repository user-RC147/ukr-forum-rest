<script setup>
import { ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "@/shared/composables/useToast";
import { useUserStore } from "@/shared/stores/useUserStore";
import { useProductGallery } from "../composables/useProductGallery";
import { getProductDetail, createComplaint } from "../api/shop.js";
import { getProductDescription, getProductTitle } from "../utils/text";
import {
  PhotoIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  DocumentTextIcon,
  PencilSquareIcon,
  TrashIcon,
  FlagIcon,
  ChatBubbleLeftRightIcon,
  LockClosedIcon,
  GlobeAltIcon,
  CalendarDaysIcon,
  UserCircleIcon,
} from "@heroicons/vue/24/outline";

const route = useRoute();
const auth = useUserStore();
const { error: showError, success: showSuccess } = useToast();

const product = ref(null);
const loading = ref(true);
const error = ref(null);

const galleryImages = computed(() => product.value?.files ?? []);
const gallery = useProductGallery(galleryImages);

// Защита от undefined даже при гонке состояний во время навигации
const currentImage = computed(
  () => galleryImages.value[gallery.currentIndex] ?? null,
);

async function loadProduct(pk) {
  loading.value = true;
  error.value = null;
  product.value = null; // важно: сбрасываем, чтобы старые files не "просвечивали"

  try {
    const response = await getProductDetail(pk);
    product.value = response.data;
  } catch {
    error.value = "Не вдалося завантажити товар";
    showError("Помилка завантаження товару");
  } finally {
    loading.value = false;
  }
}

// Аналог повторного вызова get_object() — реагируем на смену :pk в URL,
// а не только на первый "вход" в компонент
watch(
  () => route.params.pk,
  (pk) => {
    if (pk) loadProduct(pk);
  },
  { immediate: true },
);

const isOwner = computed(() => {
  if (!auth.isAuthenticated || !product.value) return false;
  return Number(auth.user?.id) === Number(product.value.owner?.id);
});

const canModerate = computed(() => isOwner.value || auth.user?.is_staff);

// display_name приоритетнее username; если оба пустые — просто ничего не показываем
const sellerName = computed(() => {
  const owner = product.value?.owner;
  return owner?.display_name || owner?.username || "";
});

// TODO: бэкенд пока не отдаёт дату регистрации в owner — как появится поле
// (например owner.date_joined), подставить сюда и убрать v-if="false" ниже
const sellerJoinedDate = computed(() => {
  const raw = product.value?.owner?.date_joined;
  if (!raw) return "";
  return raw.split(" ")[0];
});

const currency = computed(() => {
  const c = product.value?.country;
  return c?.currency_symbol || c?.currency || "";
});

const location = computed(() => {
  const { city, region, country } = product.value || {};
  if (city?.name && region?.name) {
    return `${city.name}, ${region.name}${country?.name ? ", " + country.name : ""}`;
  }
  if (region?.name)
    return `${region.name}${country?.name ? ", " + country.name : ""}`;
  if (country?.name) return country.name;
  return "Адреса не вказана";
});

const safeTitle = computed(() => getProductTitle(product.value?.title));
const safeDescription = computed(() => getProductDescription(product.value?.description));

const formattedDate = computed(() => {
  const raw = product.value?.created_at;
  if (!raw) return "";
  return raw.split(" ")[0]; // "19.06.2026 16:35:41" -> "19.06.2026"
});

const handleComplaint = async () => {
  try {
    await createComplaint(product.value.id);
    showSuccess("Скарга відправлена");
  } catch {
    showError("Помилка при відправці скарги");
  }
};
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-20 text-gray-500">
      Завантаження...
    </div>

    <div
      v-else-if="error"
      class="bg-red-50 border border-red-200 rounded-xl p-4 text-red-600"
    >
      {{ error }}
    </div>

    <div v-else-if="product" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Галерея -->
      <div class="lg:col-span-2">
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6"
        >
          <!-- Фото -->
          <div
            class="relative h-72 sm:h-96 lg:h-[28rem] bg-gray-100 rounded-lg overflow-hidden"
          >
            <Transition
              mode="out-in"
              enter-active-class="transition-opacity duration-300"
              enter-from-class="opacity-0"
              enter-to-class="opacity-100"
              leave-active-class="transition-opacity duration-150"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <img
                v-if="currentImage"
                :key="gallery.currentIndex"
                :src="currentImage.file"
                :alt="safeTitle"
                class="w-full h-full object-cover"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center"
              >
                <PhotoIcon class="w-16 h-16 text-gray-300" />
              </div>
            </Transition>

            <!-- Стрелки навигации -->
            <template v-if="gallery.total > 1">
              <button
                type="button"
                @click="gallery.prev()"
                aria-label="Попереднє фото"
                class="absolute left-3 top-1/2 -translate-y-1/2 cursor-pointer bg-white/80 hover:bg-white text-gray-700 rounded-full p-2 shadow-md transition-colors duration-200"
              >
                <ChevronLeftIcon class="w-5 h-5" />
              </button>
              <button
                type="button"
                @click="gallery.next()"
                aria-label="Наступне фото"
                class="absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer bg-white/80 hover:bg-white text-gray-700 rounded-full p-2 shadow-md transition-colors duration-200"
              >
                <ChevronRightIcon class="w-5 h-5" />
              </button>
            </template>
          </div>

          <!-- Миниатюры (на той же подложке) -->
          <div v-if="gallery.total > 1" class="flex gap-2 flex-wrap mt-4">
            <button
              v-for="(file, idx) in galleryImages"
              :key="file.id ?? idx"
              type="button"
              @click="gallery.show(idx)"
              :class="[
                'h-20 w-20 cursor-pointer rounded-lg border-2 overflow-hidden transition-colors duration-200',
                gallery.isActive(idx)
                  ? 'border-blue-500'
                  : 'border-transparent hover:border-gray-300',
              ]"
            >
              <img
                :src="file.file"
                class="w-full h-full object-cover"
                :alt="`Мініатюра ${idx + 1}`"
              />
            </button>
          </div>
        </div>

        <!-- Описание (своя подложка) -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mt-6"
        >
          <h3
            class="font-semibold text-lg text-gray-900 mb-3 flex items-center gap-2"
          >
            <DocumentTextIcon class="w-5 h-5 text-gray-400" />
            ОПИС
          </h3>
          <p class="text-gray-700 leading-relaxed whitespace-pre-wrap break-words" style="overflow-wrap: anywhere; word-break: break-word;">
            {{ safeDescription }}
          </p>
        </div>
      </div>
      <!-- Информация о товаре -->
      <aside class="flex flex-col gap-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h1 class="text-2xl font-bold text-gray-900 mb-3 leading-tight break-words" style="overflow-wrap: anywhere; word-break: break-word;">
            {{ safeTitle }}
          </h1>
          <p class="text-3xl font-bold text-blue-600 mb-6">
            {{ product.price }} {{ currency }}
          </p>

          <div class="flex flex-col gap-3">
            <template v-if="auth.isAuthenticated && !isOwner">
              <div
                class="w-full bg-blue-50 border border-blue-200 text-blue-600 font-semibold rounded-xl py-3 px-4 flex items-center justify-center gap-2 text-sm"
              >
                <ChatBubbleLeftRightIcon class="w-5 h-5 flex-shrink-0" />
                Натисніть на продавця для отримання контактів
              </div>

              <button
                type="button"
                @click="handleComplaint"
                class="w-full cursor-pointer bg-orange-50 hover:bg-orange-100 text-orange-600 font-medium rounded-xl py-2.5 px-4 text-sm transition-colors duration-200 flex items-center justify-center gap-2"
              >
                <FlagIcon class="w-4 h-4" />
                Подати скаргу
              </button>
            </template>

            <router-link
              v-else-if="!auth.isAuthenticated"
              :to="{ name: 'login', query: { next: route.fullPath } }"
              class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl py-3 px-4 text-center transition-colors duration-200 flex items-center justify-center gap-2"
            >
              <LockClosedIcon class="w-4 h-4" />
              Увійдіть, щоб зв'язатися
            </router-link>

            <template v-if="canModerate">
              <router-link
                :to="{
                  name: 'shop-update-product',
                  params: { pk: product.id },
                }"
                class="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-semibold rounded-xl py-3 px-4 text-center transition-colors duration-200 flex items-center justify-center gap-2"
              >
                <PencilSquareIcon class="w-4 h-4" />
                Редагувати товар
              </router-link>

              <router-link
                :to="{
                  name: 'shop-delete-product',
                  params: { pk: product.id },
                }"
                class="w-full bg-red-500 hover:bg-red-600 text-white font-semibold rounded-xl py-3 px-4 text-center transition-colors duration-200 flex items-center justify-center gap-2"
              >
                <TrashIcon class="w-4 h-4" />
                Видалити товар
              </router-link>
            </template>
          </div>
        </div>

        <div
          v-if="sellerName"
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
        >
          <h3 class="font-semibold text-base text-gray-900 mb-4">
            ПРОДАВЕЦЬ
          </h3>
          <div class="flex items-start gap-3">
            <UserCircleIcon
              class="w-11 h-11 text-gray-300 flex-shrink-0"
            />
            <div class="flex-1 min-w-0">
              <!-- <router-link
                :to="{
                  name: 'users-public-detail',
                  params: { pk: product.owner.id },
                }"
                class="font-medium text-blue-600 hover:text-blue-700 transition-colors duration-200 truncate block"
              >
                {{ sellerName }}
              </router-link> -->
              <!-- Заглушка на будущее: дата регистрации продавца, пока бэкенд её не отдаёт -->
              <p v-if="sellerJoinedDate" class="text-xs text-gray-500 mt-1">
                На сайті з {{ sellerJoinedDate }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-start gap-3">
            <div
              class="flex-shrink-0 w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center"
            >
              <GlobeAltIcon class="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p class="font-medium text-gray-900 mb-1">Місцезнаходження</p>
              <p class="text-sm text-gray-600">{{ location }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-start gap-3">
            <div
              class="flex-shrink-0 w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center"
            >
              <CalendarDaysIcon class="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <p class="font-medium text-gray-900 mb-1">Створено</p>
              <p class="text-sm text-gray-600">{{ formattedDate }}</p>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>