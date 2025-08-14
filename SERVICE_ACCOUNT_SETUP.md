# サービスアカウント認証の設定

## 📋 概要
Google Sheets APIへのアクセスには、サービスアカウント認証を使用します。これはAPIキーよりも安全で、細かい権限管理が可能です。

## 🔐 サービスアカウント情報

- **プロジェクトID**: `daihon-api`
- **サービスアカウントメール**: `daihon@daihon-api.iam.gserviceaccount.com`
- **クライアントID**: `110530229580380349302`

## 🚀 セットアップ手順

### 1. Google Sheetsへのアクセス権限付与

対象のGoogle Sheetsに、サービスアカウントのメールアドレスを共有設定で追加してください：

1. Google Sheetsを開く（ID: `1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo`）
2. 右上の「共有」ボタンをクリック
3. メールアドレス欄に以下を入力：
   ```
   daihon@daihon-api.iam.gserviceaccount.com
   ```
4. 権限を「閲覧者」または「編集者」に設定
5. 「送信」をクリック

#### 📄 必要なシート名
スプレッドシートには以下のシートが必要です：
- `レジェンド台本` - 市場ベストセラーデータ
- `【配信結果】上位` - 高パフォーマンス台本
- `【配信結果】中位` - 中パフォーマンス台本
- `【配信結果】下位` - 低パフォーマンス台本

詳細は[SHEET_MAPPING.md](./SHEET_MAPPING.md)を参照してください。

### 2. GitHub Secretsの設定

#### 方法1: JSON全体を1つのSecretとして設定（推奨）

1. GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. 設定内容：
   - **Name**: `GOOGLE_SERVICE_ACCOUNT_JSON`
   - **Secret**: JSONファイルの内容全体をコピー＆ペースト
4. 「Add secret」をクリック

#### 方法2: 個別のSecretとして設定

以下の値を個別にGitHub Secretsに追加：

| Secret名 | 値 |
|----------|-----|
| `GOOGLE_PROJECT_ID` | `daihon-api` |
| `GOOGLE_PRIVATE_KEY_ID` | `802db2b19b046070a9c4ec0a65b06bae6fa6ec6d` |
| `GOOGLE_PRIVATE_KEY` | （private_keyの値全体、改行含む） |
| `GOOGLE_CLIENT_EMAIL` | `daihon@daihon-api.iam.gserviceaccount.com` |
| `GOOGLE_CLIENT_ID` | `110530229580380349302` |

### 3. ワークフローでの使用方法

```yaml
- name: Setup Service Account
  run: |
    echo '${{ secrets.GOOGLE_SERVICE_ACCOUNT_JSON }}' > service-account.json
    
- name: Fetch from Google Sheets
  env:
    GOOGLE_APPLICATION_CREDENTIALS: service-account.json
  run: |
    python fetch_sheets_data.py
```

## 📝 Pythonコードでの使用例

```python
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# サービスアカウント認証
credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

# Sheets APIクライアントの作成
service = build('sheets', 'v4', credentials=credentials)

# データ取得
SPREADSHEET_ID = '1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo'
RANGE_NAME = 'Sheet1!A1:Z1000'

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME
).execute()

values = result.get('values', [])
```

## 🔒 セキュリティ注意事項

1. **JSONファイルは絶対にGitにコミットしない**
2. **サービスアカウントには最小限の権限のみ付与**
3. **定期的にキーをローテーション**（推奨：6ヶ月ごと）
4. **不要になったサービスアカウントは削除**

## 🚨 トラブルシューティング

### エラー: "Permission denied"
- Google Sheetsの共有設定を確認
- サービスアカウントのメールアドレスが正しく追加されているか確認

### エラー: "Invalid credentials"
- JSONファイルが正しくGitHub Secretsに設定されているか確認
- 改行やエスケープ文字が正しく保持されているか確認

## 📚 参考リンク

- [Google Cloud サービスアカウント](https://cloud.google.com/iam/docs/service-accounts)
- [Google Sheets API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)