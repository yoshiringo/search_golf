import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Unified Vite config: polling-based watch (for Docker on Windows) + /api proxy
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 3000,
    watch: {
      usePolling: true,
      interval: 1000
    },
    proxy: {
      // Docker Compose environment: frontend container -> backend service name
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
      },
      // If running frontend locally (not in container), consider: '/api': 'http://localhost:8000'
    }
  }
})
