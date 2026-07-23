import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  server: {
    host: '0.0.0.0', //"localhost",//
    port: 5173,

    strictPort: true,

    watch: {
      usePolling: true,
    },

    proxy: {
      '/api': {
        target: 'http://backend:8080', //'http://localhost:8000',//,
        changeOrigin: false,//true
      },
    },
  },
})