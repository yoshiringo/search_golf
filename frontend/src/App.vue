<template>
  <div class="container">
    <h1>Search Golf (dev)</h1>
    <p>This is a minimal Vite + Vue scaffold.</p>
    <button @click="check">Check API (POST /api/golf-search/)</button>
    <pre v-if="res">{{ res }}</pre>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { res: null }
  },
  methods: {
    async check() {
      try {
        // サンプルペイロード — 必要に応じて変更してください
        const payload = {
          areaCode: 1,
          playDate: '2025-11-03',
          minPrice: null,
          maxPrice: null,
          startTimeZone: null,
          originAddress: '東京都渋谷区',
          maxTravelTime: 120
        }
        const r = await axios.post('/api/golf-search/', payload)
        this.res = JSON.stringify(r.data, null, 2)
      } catch (e) {
        this.res = String(e)
      }
    }
  }
}
</script>

<style>
body { font-family: system-ui, sans-serif; padding: 1rem }
.container { max-width: 800px }
</style>
