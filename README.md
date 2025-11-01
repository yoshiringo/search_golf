# search_golf

開発用の最小構成を用意しました。バックエンド（Django）、フロントエンド（Vite + Vue）、nginx リバースプロキシを Docker Compose で起動できます。

目的:
- ローカルでの開発環境の初期化
- コンテナでバックエンドとフロントエンドを分離して実行

ファイル一覧（新規追加）:
- `docker-compose.yml` - backend/frontend/nginx を定義
- `backend/Dockerfile`, `backend/requirements.txt`
- `frontend/Dockerfile`, `frontend/package.json`
- `infra/nginx/nginx.conf`, `infra/nginx/Dockerfile`
- `.env.example`, `.gitignore`

使い方（Windows + Docker Desktop）:

1. `.env` をルートに作成し、`.env.example` を参考に必要な環境変数を設定します。
2. 初回のみ依存をローカルで追加したい場合、コンテナを利用して生成するかローカルで `npm install` / `pip install -r backend/requirements.txt` を実行してください。
3. コンテナを起動します。

```powershell
docker compose up --build
```

注意:
- このリポジトリにはまだ Django プロジェクトや Vue コンポーネントは含まれていません。`backend/` 内で `django-admin startproject`、`frontend/` 内で `npm init @vitejs/app` などを実行して初期化してください。

次のステップ:
- `backend` に Django プロジェクト初期化
- `frontend` に Vite + Vue のプロジェクト初期化
