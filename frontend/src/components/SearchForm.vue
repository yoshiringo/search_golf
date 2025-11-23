<template>
  <div class="card p-3 mb-3">
    <h2 class="h5">ゴルフ場検索</h2>

    <div class="mb-2">
      <label class="form-label">エリア（必須）</label>
      <select class="form-select" v-model.number="form.areaCode">
        <option v-for="opt in areas" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>

    <div class="mb-2">
      <label class="form-label">プレー日（必須）</label>
      <input type="date" class="form-control" v-model="form.playDate" />
    </div>

    <div class="row mb-2">
      <div class="col">
        <label class="form-label">最小価格</label>
        <input type="number" class="form-control" v-model.number="form.minPrice" min="0" />
      </div>
      <div class="col">
        <label class="form-label">最大価格</label>
        <input type="number" class="form-control" v-model.number="form.maxPrice" min="0" />
      </div>
    </div>

    <div class="mb-2">
      <label class="form-label">時間帯（任意・複数選択可）</label>
      <div class="d-flex flex-wrap">
        <div v-for="tz in timeZones" :key="tz.value" class="form-check me-3">
          <input class="form-check-input" type="checkbox" :id="`tz-${tz.value}`" :value="tz.value" v-model.number="form.startTimeZones" />
          <label class="form-check-label" :for="`tz-${tz.value}`">{{ tz.label }}</label>
        </div>
      </div>
      <div class="form-text">複数選択時は先頭の値をAPIパラメータ `startTimeZone` に渡します（実装で拡張予定）。</div>
    </div>

    <div class="mb-2">
      <label class="form-label">出発地住所（任意）</label>
      <input type="text" class="form-control" v-model="form.originAddress" placeholder="東京都渋谷区 など" />
    </div>

    <div class="mb-3">
      <label class="form-label">移動時間上限（分・任意）</label>
      <input type="number" class="form-control" v-model.number="form.maxTravelTime" min="0" />
    </div>

    <div class="d-flex gap-2">
      <button class="btn btn-primary" @click="onSearch">検索</button>
      <button class="btn btn-secondary" @click="onClear">クリア</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchForm',
  emits: ['search'],
  data() {
    return {
      // Default form values
      form: {
        areaCode: 13,
        playDate: '',
        minPrice: null,
        maxPrice: null,
        startTimeZones: [],
        originAddress: '',
        maxTravelTime: null
      },
      areas: [
        { label: '北海道', value: 1 },
        { label: '青森県', value: 2 },
        { label: '岩手県', value: 3 },
        { label: '宮城県', value: 4 },
        { label: '秋田県', value: 5 },
        { label: '山形県', value: 6 },
        { label: '福島県', value: 7 },
        { label: '茨城県', value: 8 },
        { label: '栃木県', value: 9 },
        { label: '群馬県', value: 10 },
        { label: '埼玉県', value: 11 },
        { label: '千葉県', value: 12 },
        { label: '東京都', value: 13 },
        { label: '神奈川県', value: 14 },
        { label: '新潟県', value: 15 },
        { label: '富山県', value: 16 },
        { label: '石川県', value: 17 },
        { label: '福井県', value: 18 },
        { label: '山梨県', value: 19 },
        { label: '長野県', value: 20 },
        { label: '静岡県', value: 22 },
        { label: '岐阜県', value: 21 },
        { label: '愛知県', value: 23 },
        { label: '三重県', value: 24 },
        { label: '滋賀県', value: 25 },
        { label: '京都府', value: 26 },
        { label: '大阪府', value: 27 },
        { label: '兵庫県', value: 28 },
        { label: '奈良県', value: 29 },
        { label: '和歌山県', value: 30 },
        { label: '鳥取県', value: 31 },
        { label: '島根県', value: 32 },
        { label: '岡山県', value: 33 },
        { label: '広島県', value: 34 },
        { label: '山口県', value: 35 },
        { label: '徳島県', value: 36 },
        { label: '香川県', value: 37 },
        { label: '愛媛県', value: 38 },
        { label: '高知県', value: 39 },
        { label: '福岡県', value: 40 },
        { label: '佐賀県', value: 41 },
        { label: '長崎県', value: 42 },
        { label: '熊本県', value: 43 },
        { label: '大分県', value: 44 },
        { label: '宮崎県', value: 45 },
        { label: '鹿児島県', value: 46 },
        { label: '沖縄県', value: 47 }
      ],
      timeZones: [
        { value: 4, label: '4時台' },
        { value: 5, label: '5時台' },
        { value: 6, label: '6時台' },
        { value: 7, label: '7時台' },
        { value: 8, label: '8時台' },
        { value: 9, label: '9時台' },
        { value: 10, label: '10時台' },
        { value: 11, label: '11時台' },
        { value: 12, label: '12時台' },
        { value: 13, label: '13時台' },
        { value: 14, label: '14時台' },
        { value: 15, label: '15時台以降' }
      ]
    }
  },
  methods: {
    buildPayload() {
      return {
        areaCode: this.form.areaCode,
        playDate: this.form.playDate,
        minPrice: this.form.minPrice === '' ? null : this.form.minPrice,
        maxPrice: this.form.maxPrice === '' ? null : this.form.maxPrice,
        // API currently expects single startTimeZone; take first selected if any
        startTimeZone: this.form.startTimeZones.length ? this.form.startTimeZones[0] : null,
        // Send empty string for optional text fields instead of null to satisfy serializer
        originAddress: this.form.originAddress || '',
        maxTravelTime: this.form.maxTravelTime === '' ? null : this.form.maxTravelTime
      }
    },
    onSearch() {
      // Basic validation for required fields
      if (!this.form.playDate || !this.form.areaCode) {
        alert('エリアとプレー日は必須です。')
        return
      }

      const payload = this.buildPayload()
      // Emit payload to parent — actual search implementation is out of scope for now
      this.$emit('search', payload)
    },
    onClear() {
      if (!confirm('値をクリアしてよろしいですか？')) return
      this.form = {
        areaCode: 13,
        playDate: '',
        minPrice: null,
        maxPrice: null,
        startTimeZones: [],
        originAddress: '',
        maxTravelTime: null
      }
    }
  }
}
</script>

<style scoped>
.card { border: 1px solid #e3e3e3; border-radius: 6px }
</style>
