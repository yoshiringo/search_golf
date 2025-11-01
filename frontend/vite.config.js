import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 3000,
    proxy: {
      // Docker Compose 環境: frontend コンテナ -> backend サービス名で到達
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
      },
      // ローカルでフロントをホスト上で動かしている場合は代わりに以下を使う:
      // '/api': 'http://localhost:8000'
    }
  }
})
