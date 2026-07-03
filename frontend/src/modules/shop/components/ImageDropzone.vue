<script setup>
import { ref } from 'vue'
import { CloudArrowUpIcon, XMarkIcon, PhotoIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  upload: { type: Object, required: true },
  showExisting: { type: Boolean, default: false },
})

const fileInput = ref(null)

function onFileInputChange(event) {
  props.upload.addFiles(event.target.files)
  event.target.value = ''
}
</script>

<template>
  <div>
    <label class="mb-2 block text-sm font-medium text-gray-700">
      {{ showExisting ? 'Додати нові фотографії' : 'Фотографії' }}
    </label>

    <div
      class="w-full rounded-xl border-2 border-dashed p-8 text-center text-gray-500 transition"
      :class="upload.isDragging ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'"
      @dragover.prevent="upload.isDragging = true"
      @dragleave="upload.isDragging = false"
      @drop.prevent="upload.onDrop($event)"
    >
      <CloudArrowUpIcon class="mx-auto mb-2 h-8 w-8 text-gray-400" />
      Перенесіть фото сюди або
      <button type="button" class="text-blue-600 underline" @click="fileInput.click()">завантажте</button>
      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/jpg,image/png,image/webp,image/gif"
        multiple
        hidden
        @change="onFileInputChange"
      />
      <p class="mt-3 text-xs text-gray-500">
        Формати: JPG, PNG, WEBP, GIF · Макс. 10 MB · До {{ upload.config.MAX_FILES }} фото
        {{ showExisting ? 'загалом' : '' }}
      </p>
    </div>

    <!-- Существующие фото (только режим редактирования) -->
    <div v-if="showExisting && upload.remainingExisting.length" class="mt-4">
      <p class="mb-2 text-sm font-medium text-gray-700">Існуючі фото</p>
      <div class="flex flex-wrap gap-2">
        <div
          v-for="image in upload.remainingExisting"
          :key="image.id"
          class="group relative h-20 w-20"
        >
          <img :src="image.url" class="h-full w-full rounded-lg object-cover shadow" alt="" />
          <button
            type="button"
            class="absolute left-1/2 top-1/2 flex h-10 w-10 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-red-600 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
            @click="upload.removeExistingImage(image.id)"
          >
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Новые фото -->
    <div v-if="upload.newFiles.length" class="mt-4 flex flex-wrap gap-2">
      <div
        v-for="(item, index) in upload.newFiles"
        :key="item.file.name + item.file.lastModified"
        class="group relative h-24 w-24"
      >
        <img :src="item.previewUrl" class="h-full w-full rounded-lg border-2 border-gray-200 object-cover shadow-md" :alt="item.file.name" />
        <button
          type="button"
          class="absolute left-1/2 top-1/2 flex h-10 w-10 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-red-600 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100 hover:bg-red-700"
          @click="upload.removeNewFile(index)"
        >
          <XMarkIcon class="h-5 w-5" />
        </button>
      </div>
    </div>

    <p v-if="!upload.hasAnyImage" class="mt-3 flex items-center gap-1 text-xs text-gray-400">
      <PhotoIcon class="h-4 w-4" /> Фото ще не додано
    </p>
  </div>
</template>