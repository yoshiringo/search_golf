# 要件定義書

## 概要

楽天GoraAPIとGoogle Maps Distance Matrix APIを統合したゴルフ場検索システム。従来のゴルフ場検索条件に加えて、指定した出発地からの車での移動時間を検索条件として追加できるWebアプリケーション。

## 用語集

- **Golf_Search_System**: 楽天GoraAPIとGoogle Maps APIを統合したゴルフ場検索システム
- **Rakuten_Gora_API**: 楽天が提供するゴルフ場検索API
- **Google_Distance_Matrix_API**: Googleが提供する距離・移動時間計算API
- **Golf_Course**: ゴルフ場
- **Golf_Plan**: ゴルフ場のプレープラン
- **Travel_Time**: 出発地からゴルフ場までの車での移動時間
- **Search_Criteria**: ゴルフ場検索の条件（日付、エリア、価格等）
- **Origin_Address**: ユーザーが指定する出発地住所
- **Max_Travel_Time**: ユーザーが指定する移動時間の上限

## 要件

### 要件1

**ユーザーストーリー:** ゴルフプレイヤーとして、基本的なゴルフ場検索条件を入力できるようにしたい。これにより、希望する条件に合うゴルフ場を見つけることができる。

#### 受入基準

1. THE Golf_Search_System SHALL エリアコード入力フィールドを提供する（必須）
2. THE Golf_Search_System SHALL プレー日入力フィールドを提供する（YYYY-MM-DD形式）（必須）
3. THE Golf_Search_System SHALL 最小価格入力フィールドを提供する
4. THE Golf_Search_System SHALL 最大価格入力フィールドを提供する
5. THE Golf_Search_System SHALL 時間帯指定入力フィールドを提供する

### 要件2

**ユーザーストーリー:** ゴルフプレイヤーとして、出発地からの移動時間を検索条件に含めたい。これにより、アクセスしやすいゴルフ場のみを検索結果として得ることができる。

#### 受入基準

1. THE Golf_Search_System SHALL 出発地住所入力フィールドを提供する
2. THE Golf_Search_System SHALL 移動時間上限入力フィールドを提供する
3. WHEN ユーザーが出発地住所を入力する時、THE Golf_Search_System SHALL 住所の妥当性を検証する
4. WHEN ユーザーが移動時間上限を入力する時、THE Golf_Search_System SHALL 数値の妥当性を検証する

### 要件3

**ユーザーストーリー:** ゴルフプレイヤーとして、検索ボタンを押すことで条件に合うゴルフ場を検索したい。これにより、効率的にゴルフ場を見つけることができる。

#### 受入基準

1. THE Golf_Search_System SHALL 検索実行ボタンを提供する
2. WHEN ユーザーが検索ボタンを押下する時、THE Golf_Search_System SHALL 入力された条件の妥当性を検証する
3. WHEN 条件が妥当でない場合、THE Golf_Search_System SHALL エラーメッセージを表示する
4. WHEN 条件が妥当な場合、THE Golf_Search_System SHALL 検索処理を開始する

### 要件4

**ユーザーストーリー:** システム管理者として、楽天GoraAPIから条件に合うゴルフ場データを取得したい。これにより、ユーザーに最新のゴルフ場情報を提供できる。

#### 受入基準

1. WHEN 検索処理が開始される時、THE Golf_Search_System SHALL Rakuten_Gora_APIにリクエストを送信する
2. THE Golf_Search_System SHALL APIリクエストにエリアコード、プレー日、価格範囲、時間帯、予約URLを含める
3. WHEN APIからレスポンスを受信する時、THE Golf_Search_System SHALL レスポンスデータを解析する
	- レスポンス中の `highwayCode`（最寄ICを示すコード）を抽出して後続処理に利用できるようにする
4. IF APIエラーが発生した場合、THEN THE Golf_Search_System SHALL エラーハンドリングを実行する

### 要件5

**ユーザーストーリー:** システム管理者として、各ゴルフ場への移動時間を計算したい。これにより、ユーザーの移動時間条件に基づいてフィルタリングできる。

#### 受入基準

1. WHEN ゴルフ場データを取得した後、THE Golf_Search_System SHALL 各Golf_Courseの住所を抽出する
2. THE Golf_Search_System SHALL Origin_Addressから各Golf_Courseへの移動時間をGoogle_Distance_Matrix_APIで取得する
3. THE Golf_Search_System SHALL 車での移動時間を計算条件として指定する
4. WHEN APIから移動時間データを受信する時、THE Golf_Search_System SHALL データを解析して移動時間を抽出する
5. IF Distance Matrix APIエラーが発生した場合、THEN THE Golf_Search_System SHALL エラーハンドリングを実行する

### 要件6

**ユーザーストーリー:** ゴルフプレイヤーとして、移動時間条件を満たすゴルフ場のみを検索結果として見たい。これにより、アクセス可能な範囲内のゴルフ場のみを確認できる。

#### 受入基準

1. WHEN 移動時間データを取得した後、THE Golf_Search_System SHALL 各Golf_PlanのTravel_TimeをMax_Travel_Timeと比較する
2. THE Golf_Search_System SHALL Travel_TimeがMax_Travel_Time以下のGolf_Planのみを結果に含める
3. THE Golf_Search_System SHALL フィルタリングされた結果をユーザーに表示する
4. THE Golf_Search_System SHALL 各結果に移動時間情報を含める

### 要件7

**ユーザーストーリー:** ゴルフプレイヤーとして、検索結果を見やすい形式で確認したい。これにより、ゴルフ場の詳細情報と移動時間を効率的に比較検討できる。

#### 受入基準

1. THE Golf_Search_System SHALL ゴルフ場名、プラン詳細、価格、移動時間、予約URLを表示する
2. THE Golf_Search_System SHALL 検索結果を一覧形式で表示する
3. THE Golf_Search_System SHALL 移動時間順での並び替え機能を提供する
4. WHEN 検索結果が0件の場合、THE Golf_Search_System SHALL 適切なメッセージを表示する

### 要件8

**ユーザーストーリー:** システム利用者として、レスポンシブなWebインターフェースを使用したい。これにより、様々なデバイスから快適にシステムを利用できる。

#### 受入基準

1. THE Golf_Search_System SHALL HTML、CSS、Vueを使用したフロントエンドを提供する
2. THE Golf_Search_System SHALL モバイルデバイスでも使用可能なレスポンシブデザインを実装する
3. THE Golf_Search_System SHALL 直感的なユーザーインターフェースを提供する
4. THE Golf_Search_System SHALL 検索処理中のローディング表示を提供する