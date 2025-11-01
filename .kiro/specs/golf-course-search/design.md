# 設計書

## 概要

楽天GoraAPIとGoogle Maps Distance Matrix APIを統合したゴルフ場検索システムの詳細設計。DjangoをバックエンドフレームワークとしてRESTful APIを構築し、Vue.jsを使用したSPAフロントエンドで直感的なユーザーインターフェースを提供する。

## アーキテクチャ

### システム構成

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │  External APIs  │
│   (Vue.js)      │◄──►│   (Django)      │◄──►│  Rakuten Gora   │
│                 │    │                 │    │  Google Maps    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 技術スタック

**バックエンド:**
- Django 5.2 (Webフレームワーク)
- Django REST Framework (API構築)
- Python 3.14
- Requests (HTTP クライアント)

**フロントエンド:**
- Vue.js 3.5.22 (フロントエンドフレームワーク)
- Axios (HTTP クライアント)
- HTML5/CSS3
- Bootstrap (UIフレームワーク)

**開発環境:**
- Docker & Docker Compose (開発環境構築)
- データベース不要（ステートレスAPI）

**デプロイメント:**
- Heroku (無料プランでの低コストデプロイ)
- データベース不要（ステートレスAPI）

## コンポーネントとインターフェース

### バックエンドコンポーネント

#### 1. APIビュー層
- `GolfSearchView`: メインの検索エンドポイント
- `HealthCheckView`: システムヘルスチェック

#### 2. サービス層
- `RakutenGoraService`: 楽天GoraAPI連携サービス
- `GoogleMapsService`: Google Maps API連携サービス
- `GolfSearchService`: 検索ロジック統合サービス

#### 3. データクラス層
- `SearchRequest`: 検索リクエストデータクラス
- `GolfCourse`: ゴルフ場データクラス
- `SearchResult`: 検索結果データクラス

### フロントエンドコンポーネント

#### 1. ページコンポーネント
- `SearchPage`: メイン検索ページ
- `ResultsPage`: 検索結果表示ページ

#### 2. UIコンポーネント
- `SearchForm`: 検索条件入力フォーム
- `ResultsList`: 検索結果一覧表示
- `LoadingSpinner`: ローディング表示
- `ErrorMessage`: エラーメッセージ表示

### API設計

#### エンドポイント

```
POST /api/golf-search/
```

**リクエスト:**
```json
{
  "areaCode": 1,
  "playDate": "2024-12-01",
  "minPrice": 5000,
  "maxPrice": 15000,
  "startTimeZone": 1,
  "originAddress": "東京都渋谷区",
  "maxTravelTime": 120
}
```

**レスポンス:**
```json
{
  "results": [
    {
      "golfCourseName": "○○ゴルフクラブ",
      "planName": "平日プラン",
      "price": 8000,
      "address": "千葉県○○市",
      "travelTime": 90,
      "playDate": "2024-12-01",
      "startTime": "08:00"
    }
  ],
  "totalCount": 1,
  "searchTime": "2024-11-01T10:00:00Z"
}
```

## データクラス

### SearchRequest
```python
@dataclass
class SearchRequest:
    area_code: int
    play_date: str  # YYYY-MM-DD
    origin_address: str
    max_travel_time: int  # minutes
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    start_time_zone: Optional[int] = None
```

### GolfCourse
```python
@dataclass
class GolfCourse:
    course_id: str
    course_name: str
    plan_name: str
    price: int
    address: str
    play_date: str
    start_time: str
    travel_time: Optional[int] = None  # minutes
```

### SearchResult
```python
@dataclass
class SearchResult:
    results: List[GolfCourse]
    total_count: int
    search_time: datetime
    errors: Optional[List[str]] = None
```

## 外部API統合

### 楽天GoraAPI統合

**エンドポイント:**
```
https://app.rakuten.co.jp/services/api/Gora/GoraPlanSearch/20170623
```

**パラメータマッピング:**
- `areaCode` → `areaCode`
- `playDate` → `playDate`
- `minPrice` → `minPrice`
- `maxPrice` → `maxPrice`
- `startTimeZone` → `startTimeZone`
- `applicationId` → 固定値（環境変数から取得）

### Google Distance Matrix API統合

**エンドポイント:**
```
https://maps.googleapis.com/maps/api/distancematrix/json
```

**パラメータ:**
- `origins`: ユーザー指定の出発地住所
- `destinations`: ゴルフ場住所（複数）
- `mode`: driving（車での移動）
- `units`: metric（メートル法）
- `key`: APIキー（環境変数から取得）

## エラーハンドリング

### エラータイプ

1. **バリデーションエラー**
   - 必須フィールド未入力
   - 日付形式不正
   - 数値範囲外

2. **外部APIエラー**
   - 楽天GoraAPI接続エラー
   - Google Maps API接続エラー
   - APIレート制限エラー

3. **システムエラー**
   - サーバー内部エラー
   - タイムアウトエラー

### エラーレスポンス形式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力データに不正があります",
    "details": [
      {
        "field": "playDate",
        "message": "日付形式が正しくありません"
      }
    ]
  }
}
```

## パフォーマンス最適化

### キャッシュ戦略
- Google Maps APIレスポンスの一時キャッシュ（同一住所ペア）
- 楽天GoraAPIレスポンスの短期キャッシュ

### 非同期処理
- 複数ゴルフ場への距離計算の並列実行
- フロントエンドでの非同期API呼び出し

### レート制限対応
- Google Maps APIの呼び出し頻度制限
- 楽天GoraAPIの呼び出し制限遵守

## セキュリティ

### API キー管理
- 環境変数でのAPIキー管理
- 本番環境でのシークレット管理

### CORS設定
- フロントエンドドメインからのアクセス許可
- 適切なCORSヘッダー設定

### 入力検証
- XSS攻撃対策
- CSRFトークン使用
- 入力データサニタイゼーション

## テスト戦略

### バックエンドテスト
- 単体テスト: 各サービスクラスのテスト
- 統合テスト: API エンドポイントのテスト
- 外部APIモックテスト

### フロントエンドテスト
- コンポーネント単体テスト
- E2Eテスト（主要フロー）

### テストデータ
- 楽天GoraAPIのモックレスポンス
- Google Maps APIのモックレスポンス

## 開発環境設計

### Docker構成

**開発環境構成:**
- Django バックエンドコンテナ
- Vue.js フロントエンド開発サーバーコンテナ
- Nginx リバースプロキシ（本番用）

**Docker Compose サービス:**
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - RAKUTEN_APPLICATION_ID
      - GOOGLE_MAPS_API_KEY
      - DJANGO_SECRET_KEY
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## デプロイメント設計

### Heroku デプロイ構成

**アプリケーション構成:**
- Web dyno: Django アプリケーション
- 静的ファイル: WhiteNoise での配信
- データベース不要（ステートレス設計）

**環境変数:**
```
RAKUTEN_APPLICATION_ID=your_rakuten_app_id
GOOGLE_MAPS_API_KEY=your_google_maps_key
DJANGO_SECRET_KEY=your_secret_key
```

**デプロイフロー:**
1. GitHub リポジトリ連携
2. 自動デプロイ設定
3. 環境変数設定
4. 静的ファイル収集

### 費用最適化
- Heroku 無料プラン使用
- 静的ファイルのCDN不使用（WhiteNoise使用）
- データベース不要（コスト削減）
- APIキー使用量監視

## 運用・監視

### ログ管理
- Django ログ設定
- 外部API呼び出しログ
- エラーログ収集

### 監視項目
- API レスポンス時間
- 外部API呼び出し成功率
- エラー発生率

### アラート設定
- 外部API接続エラー
- システムエラー増加
- レスポンス時間劣化