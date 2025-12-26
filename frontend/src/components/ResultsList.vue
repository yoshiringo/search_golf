<template>
  <div>
    <h2 class="h6">検索結果（{{ results.length }} 件）</h2>
    <div v-if="!results.length" class="text-muted">結果がありません。</div>
    <ul class="list-group" v-else>
      <li class="list-group-item" v-for="(r, idx) in results" :key="idx">
        <div class="d-flex justify-content-between">
          <div>
            <div><strong>{{ r.courseName }}</strong></div>
            <div class="small text-muted">{{ r.planName }}</div>
            <div class="mt-1">料金: {{ r.price }} 円</div>
            <div>開始時間: {{ r.startTime || '-' }}</div>
            <div>移動時間: {{ r.travelTimeMinutes !== undefined && r.travelTimeMinutes !== null ? r.travelTimeMinutes + ' 分' : '-' }}</div>
            <div>住所: {{ r.address || '-' }}</div>
          </div>
          <div class="text-end">
            <a v-if="r.reservePageUrlPC" :href="r.reservePageUrlPC" target="_blank" rel="noopener" class="btn btn-sm btn-primary">予約ページ</a>
            <a v-else-if="r.reservePageUrlMobile" :href="r.reservePageUrlMobile" target="_blank" rel="noopener" class="btn btn-sm btn-secondary">予約（モバイル）</a>
            <div class="small text-muted mt-2">IC: {{ r.ic || '-' }}</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ResultsList',
  props: {
    results: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.list-group-item { border: 1px solid #e9ecef; border-radius: 6px; margin-bottom: 8px }
</style>
