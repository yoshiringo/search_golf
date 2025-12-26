<template>
  <div>
    <div class="container">
      <h1>Search Golf (dev)</h1>

      <SearchForm @search="onSearch" :loading="loading" />

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

    <div v-if="loading" class="loading-overlay" role="status" aria-live="polite">
      <div class="loading-box text-center">
        <div class="spinner-border text-primary" role="status" style="width:3rem;height:3rem">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div class="mt-3">検索中です。しばらくお待ちください…</div>
      </div>
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
    return { res: null, lastPayload: null, results: [], loading: false }
  },
  methods: {
    async onSearch(payload) {
      // Send payload to backend and display response; also log golfCourseName for verification
      this.lastPayload = JSON.stringify(payload, null, 2)
      this.loading = true
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
      } finally {
        this.loading = false
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

.loading-overlay {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background: rgba(255,255,255,0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.loading-box {
  padding: 1.5rem 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
</style>
