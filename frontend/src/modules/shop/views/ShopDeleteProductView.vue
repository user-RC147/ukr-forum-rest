<script setup>
import { ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "@/shared/composables/useToast";
import { getProductDetail, deleteProduct } from "../api/shop.js";
import { TrashIcon, ArrowUturnLeftIcon, CalendarDaysIcon } from "@heroicons/vue/24/outline";

const route = useRoute();
const router = useRouter();
const { error: showError, success: showSuccess } = useToast();

const product = ref(null);
const loading = ref(true);
const deleting = ref(false);
const error = ref(null);

async function loadProduct(pk) {
  loading.value = true;
  error.value = null;
  product.value = null;

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

// Аналог повторного get_object() при смене :pk в URL без полного размонтирования компонента
watch(
  () => route.params.pk,
  (pk) => {
    if (pk) loadProduct(pk);
  },
  { immediate: true },
);

const previewImage = computed(() => product.value?.files?.[0]?.file ?? null);

const formattedDate = computed(() => {
  const raw = product.value?.created_at;
  if (!raw) return "";
  return raw.split(" ")[0]; // "28.06.2026 21:36:33" -> "28.06.2026"
});

function goBack() {
  router.push({
    name: "shop-product",
    params: { pk: product.value.id, productSlug: product.value.slug },
  });
}

async function confirmDelete() {
  deleting.value = true;
  try {
    await deleteProduct(product.value.id);
    showSuccess("Товар видалено");
    router.push({ name: "shop-index" });
  } catch {
    showError("Помилка при видаленні товару");
  } finally {
    deleting.value = false;
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-20 text-gray-500">
      Завантаження...
    </div>

    <div
      v-else-if="error"
      class="bg-red-50 border border-red-200 rounded-xl p-4 text-red-600"
    >
      {{ error }}
    </div>

    <div
      v-else-if="product"
      class="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
    >
      <h2 class="text-xl font-semibold text-gray-900 mb-6">
        Підтвердження видалення товару
      </h2>

      <!-- Превью товара -->
      <div
        class="flex flex-col sm:flex-row items-center gap-6 border border-gray-100 rounded-xl p-4 mb-6"
      >
        <img
          v-if="previewImage"
          :src="previewImage"
          :alt="product.title"
          class="w-48 h-32 object-cover rounded-lg shadow-sm flex-shrink-0"
        />
        <div
          v-else
          class="w-48 h-32 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0"
        >
          <TrashIcon class="w-10 h-10 text-gray-300" />
        </div>

        <div class="min-w-0">
          <h3 class="text-lg font-semibold text-gray-900 truncate">
            {{ product.title }}
          </h3>
          <p class="text-sm text-gray-500 mt-1 flex items-center gap-1.5">
            <CalendarDaysIcon class="w-4 h-4" />
            Дата створення: {{ formattedDate }}
          </p>
        </div>
      </div>

      <!-- Подтверждение -->
      <div class="flex flex-col sm:flex-row gap-3">
        <button
          type="button"
          :disabled="deleting"
          @click="confirmDelete"
          class="flex-1 cursor-pointer bg-red-600 hover:bg-red-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold rounded-xl py-2.5 px-4 transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <TrashIcon class="w-4 h-4" />
          {{ deleting ? "Видалення..." : "Так, видалити" }}
        </button>

        <button
          type="button"
          :disabled="deleting"
          @click="goBack"
          class="flex-1 cursor-pointer bg-gray-100 hover:bg-gray-200 disabled:opacity-60 disabled:cursor-not-allowed text-gray-800 font-semibold rounded-xl py-2.5 px-4 transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <ArrowUturnLeftIcon class="w-4 h-4" />
          Ні, назад
        </button>
      </div>
    </div>
  </div>
</template>