# Google Sheets API キーの取得方法

## 📋 概要
このドキュメントでは、Google Sheets APIを使用するために必要なAPIキーの取得方法を説明します。

## 🔧 セットアップ手順

### 1. Google Cloud Consoleにアクセス
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. Googleアカウントでログイン

### 2. プロジェクトの作成または選択
1. 上部のプロジェクトセレクターをクリック
2. 「新しいプロジェクト」を選択（既存プロジェクトがある場合はそれを使用可能）
3. プロジェクト名を入力（例：`daihon-workflow`）
4. 「作成」をクリック

### 3. Google Sheets APIの有効化
1. 左側メニューから「APIとサービス」→「ライブラリ」を選択
2. 検索バーに「Google Sheets API」と入力
3. 「Google Sheets API」をクリック
4. 「有効にする」ボタンをクリック

### 4. APIキーの作成
1. 左側メニューから「APIとサービス」→「認証情報」を選択
2. 上部の「+ 認証情報を作成」をクリック
3. 「APIキー」を選択
4. APIキーが生成されます

### 5. APIキーの制限（推奨）
セキュリティのため、APIキーに制限を設定することを強く推奨します：

1. 作成されたAPIキーの「編集」ボタンをクリック
2. **アプリケーションの制限**：
   - 「HTTPリファラー」を選択（Webアプリの場合）
   - 「IPアドレス」を選択（サーバーアプリの場合）
   - GitHub Actionsの場合は「なし」でも可（ただしセキュリティリスクあり）

3. **APIの制限**：
   - 「キーを制限」を選択
   - 「Google Sheets API」のみを選択
   - 「保存」をクリック

### 6. APIキーをGitHub Secretsに追加
1. GitHubリポジトリの「Settings」タブを開く
2. 左側メニューから「Secrets and variables」→「Actions」を選択
3. 「New repository secret」をクリック
4. Name: `GOOGLE_SHEETS_API_KEY`
5. Secret: 取得したAPIキーを貼り付け
6. 「Add secret」をクリック

## 🔐 セキュリティベストプラクティス

### APIキーの取り扱い
- **絶対にコードにハードコーディングしない**
- **公開リポジトリにコミットしない**
- **定期的にローテーション**（3-6ヶ月ごと）

### 代替認証方法（より安全）
APIキーの代わりに、サービスアカウントを使用する方法もあります：

1. **サービスアカウントの作成**
   - 「認証情報」→「+ 認証情報を作成」→「サービスアカウント」
   - 必要事項を入力して作成
   - JSONキーをダウンロード

2. **Google Sheetsへのアクセス権限付与**
   - サービスアカウントのメールアドレスをコピー
   - 対象のGoogle Sheetsを開く
   - 「共有」からサービスアカウントのメールを追加（閲覧者権限）

3. **GitHub Secretsへの追加**
   - JSONキーの内容全体を`GOOGLE_SHEETS_SERVICE_ACCOUNT`として追加

## 📊 使用するGoogle Sheets ID

プロジェクトで使用するGoogle Sheets IDは以下の通りです：

```
1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo
```

このIDは、Google SheetsのURLから取得できます：
```
https://docs.google.com/spreadsheets/d/[SHEETS_ID]/edit
```

## 🚨 トラブルシューティング

### よくあるエラーと対処法

1. **「API key not valid」エラー**
   - APIキーが正しくコピーされているか確認
   - APIが有効化されているか確認
   - APIキーの制限が適切か確認

2. **「Insufficient permissions」エラー**
   - Google Sheetsの共有設定を確認
   - 「リンクを知っている全員」に閲覧権限があるか確認

3. **「Quota exceeded」エラー**
   - Google Cloud ConsoleでAPIの使用量を確認
   - 必要に応じてクォータの引き上げをリクエスト

## 📝 ワークフローでの使用例

```yaml
- name: Fetch data from Google Sheets
  env:
    GOOGLE_SHEETS_API_KEY: ${{ secrets.GOOGLE_SHEETS_API_KEY }}
    GOOGLE_SHEETS_ID: ${{ secrets.GOOGLE_SHEETS_ID }}
  run: |
    # APIキーを使用してGoogle Sheetsからデータを取得
    python fetch_sheets_data.py
```

## 🔗 参考リンク

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API キーの使用に関するベストプラクティス](https://cloud.google.com/docs/authentication/api-keys)