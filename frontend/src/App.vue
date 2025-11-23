<template>
  <div class="container">
    <h1>Search Golf (dev)</h1>
    <p>This is a minimal Vite + Vue scaffold.</p>

    <SearchForm @search="onSearch" />

    <div class="mt-3">
      <h2 class="h6">Last Search Payload</h2>
      <pre v-if="lastPayload">{{ lastPayload }}</pre>
      <div v-else class="text-muted">フォームで検索を実行するとここにペイロードが表示されます。</div>
    </div>

    <div class="mt-3">
      <button class="btn btn-outline-primary" @click="check">Check API (POST /api/golf-search/)</button>
    </div>
    <div class="mt-4">
      <ResultsList :results="results" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SearchForm from './components/SearchForm.vue'
import ResultsList from './components/ResultsList.vue'

export default {
  components: { SearchForm, ResultsList },
  data() {
    return { res: null, lastPayload: null, results: [] }
  },
  methods: {
    async onSearch(payload) {
      // Send payload to backend and display response; also log golfCourseName for verification
      this.lastPayload = JSON.stringify(payload, null, 2)
      try {
        this.res = null
        const r = await axios.post('/api/golf-search/', payload)
        this.res = JSON.stringify(r.data, null, 2)
        this.results = Array.isArray(r.data && r.data.results) ? r.data.results : []
      } catch (e) {
        console.error('Search API error', e)
        // If server returned validation errors, show them to the user for diagnosis
        const serverData = e.response && e.response.data ? e.response.data : null
        if (serverData) {
          console.error('Server response:', serverData)
          // Try to show a useful message
          const msg = serverData.detail || serverData.error || JSON.stringify(serverData)
          alert('検索中にエラーが発生しました: ' + msg)
        } else {
          alert('検索中にエラーが発生しました。コンソールを確認してください。')
        }
      }
    },
    async check() {
      try {
        const future = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
        const yyyy = future.getFullYear()
        const mm = String(future.getMonth() + 1).padStart(2, '0')
        const dd = String(future.getDate()).padStart(2, '0')
        const payload = {
          areaCode: 1,
          playDate: `${yyyy}-${mm}-${dd}`,
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
