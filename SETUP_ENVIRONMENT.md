# 環境設定ガイド - 台本作成ワークフロー (CCSDK)

## 📋 概要

このワークフローを実行するために必要なAPIキーと環境変数の設定方法を説明します。

## 🔑 必要なAPIキー

### 1. Claude API Key (Anthropic)
- **用途**: AI台本生成・分析エンジン
- **取得方法**: [Anthropic Console](https://console.anthropic.com/) でアカウント作成
- **形式**: `sk-ant-api03-...`

### 2. GitHub Personal Access Token
- **用途**: ワークフロー間の連携・自動実行
- **取得方法**: GitHub Settings > Developer settings > Personal access tokens
- **必要な権限**: `workflow`, `repo`
- **形式**: `ghp_...`

### 3. Google Gemini API Key
- **用途**: Web検索・市場調査
- **取得方法**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **形式**: `AIzaSy...`

### 4. Google Sheets API Key (オプション)
- **用途**: データ取得
- **取得方法**: [Google Cloud Console](https://console.cloud.google.com/)
- **対象シート**: [DIOデータ](https://docs.google.com/spreadsheets/d/1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo/edit?gid=372030184#gid=372030184)
- **データ構造**: 売れている動画広告台本例を含むマーケティングデータ
- **使用タブ**: 
  - `ローデータ`
  - `【配信結果】上位`
  - `【配信結果】中位`
  - `【配信結果】下位`
  - `レジェンド台本`

## ⚙️ GitHub Actions Secrets設定

### 設定手順

1. **GitHubリポジトリの設定画面を開く**
   ```
   リポジトリ > Settings > Secrets and variables > Actions
   ```

2. **Repository secretsに以下を追加**

   | Secret名 | 値 |
   |----------|-----|
   | `ANTHROPIC_API_KEY` | Anthropic APIキー（sk-ant-で始まる） |
   | `GITHUB_TOKEN` | GitHub Personal Access Token（ghp_で始まる） |
   | `GEMINI_API_KEY` | Google Gemini APIキー |
   | `GOOGLE_SHEETS_API_KEY` | (必要に応じて設定) |
   | `GOOGLE_SHEETS_ID` | `1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo` |

### 設定確認

設定が完了したら、以下のコマンドでワークフローを実行できます：

```bash
# Phase 1: 分析・ペルソナ・ライター生成
gh workflow run 1-analysis.yml -f product_name="テスト商品"

# Phase 2: 評価基準最適化ループ  
gh workflow run 2-criteria-optimization.yml -f product_name="テスト商品"

# Phase 3: 台本生成とフィルタリング
gh workflow run 3-script-generation.yml -f product_name="テスト商品"
```

## 🔒 セキュリティ注意事項

### ⚠️ 重要な注意点

1. **APIキーの取り扱い**
   - APIキーは絶対にコードにハードコーディングしない
   - `.env`ファイルは`.gitignore`に追加済み
   - GitHub Secretsのみを使用する

2. **権限管理**
   - GitHub Personal Access Tokenは最小限の権限のみ付与
   - 定期的にトークンをローテーション

3. **監査**
   - API使用量を定期的に確認
   - 不審なアクティビティがないかチェック

## 🛠️ ローカル開発環境

ローカルでテストする場合：

1. **環境ファイルの作成**
   ```bash
   cp env.example .env
   ```

2. **APIキーの設定**
   `.env`ファイルを編集して実際のAPIキーを設定
   
   **重要**: `GOOGLE_SHEETS_ID`を以下の値に設定してください：
   ```bash
   GOOGLE_SHEETS_ID=1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo
   ```

3. **環境変数の読み込み**
   ```bash
   # Bashの場合
   source .env
   
   # または
   export $(cat .env | xargs)
   ```

## 📞 トラブルシューティング

### よくある問題

1. **API Key Invalid エラー**
   - キーが正しく設定されているか確認
   - キーの有効期限をチェック
   - 権限が適切に設定されているか確認

2. **Workflow Permission エラー**
   - GitHub Tokenの権限を確認
   - リポジトリのActions設定を確認

3. **Rate Limit エラー**
   - API使用量制限に達している可能性
   - 実行間隔を調整

### サポート

問題が解決しない場合は、以下を確認してください：
- GitHub Actions実行ログ
- API提供者のステータスページ
- 各APIの使用量ダッシュボード

---

**最終更新**: 2024年12月
**バージョン**: 1.4.0
