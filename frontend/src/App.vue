<template>
  <div class="container">
    <h1>Search Golf (dev)</h1>
    <p>This is a minimal Vite + Vue scaffold.</p>
    <button @click="check">Check API</button>
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
        const r = await axios.get('/api/health/')
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
