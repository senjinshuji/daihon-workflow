#!/bin/bash

# GitHub Actions Secrets設定スクリプト
# 台本作成ワークフロー (CCSDK)

set -e

echo "🔑 GitHub Actions Secrets設定スクリプト"
echo "========================================"

# 環境変数の確認
if [ ! -f ".env" ]; then
    echo "❌ .envファイルが見つかりません"
    echo "   env.exampleをコピーして.envを作成してください:"
    echo "   cp env.example .env"
    exit 1
fi

# .envファイルから環境変数を読み込み
source .env

echo "📋 設定するSecrets:"
echo "- ANTHROPIC_API_KEY"
echo "- GITHUB_TOKEN" 
echo "- GEMINI_API_KEY"
echo "- GOOGLE_SHEETS_API_KEY"
echo "- GOOGLE_SHEETS_ID"
echo ""

# GitHub CLIの確認
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLIがインストールされていません"
    echo "   インストール方法: https://cli.github.com/"
    exit 1
fi

# 認証確認
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLIで認証されていません"
    echo "   認証してください: gh auth login"
    exit 1
fi

echo "🚀 Secretsを設定中..."

# Secretsの設定
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "$ANTHROPIC_API_KEY" | gh secret set ANTHROPIC_API_KEY
    echo "✅ ANTHROPIC_API_KEY を設定しました"
else
    echo "⚠️  ANTHROPIC_API_KEY が空です"
fi

if [ -n "$GITHUB_TOKEN" ]; then
    echo "$GITHUB_TOKEN" | gh secret set GITHUB_TOKEN
    echo "✅ GITHUB_TOKEN を設定しました"
else
    echo "⚠️  GITHUB_TOKEN が空です"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "$GEMINI_API_KEY" | gh secret set GEMINI_API_KEY
    echo "✅ GEMINI_API_KEY を設定しました"
else
    echo "⚠️  GEMINI_API_KEY が空です"
fi

if [ -n "$GOOGLE_SHEETS_API_KEY" ]; then
    echo "$GOOGLE_SHEETS_API_KEY" | gh secret set GOOGLE_SHEETS_API_KEY
    echo "✅ GOOGLE_SHEETS_API_KEY を設定しました"
else
    echo "ℹ️  GOOGLE_SHEETS_API_KEY は空です（オプション）"
fi

# Google Sheets IDを設定（DIOデータ）
SHEETS_ID="1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo"
echo "$SHEETS_ID" | gh secret set GOOGLE_SHEETS_ID
echo "✅ GOOGLE_SHEETS_ID を設定しました (DIOデータ)"

echo ""
echo "🎉 Secrets設定完了！"
echo ""
echo "📋 設定確認:"
gh secret list

echo ""
echo "🚀 ワークフロー実行例:"
echo "gh workflow run 1-analysis.yml -f product_name=\"テスト商品\""
echo "gh workflow run 2-criteria-optimization.yml -f product_name=\"テスト商品\""
echo "gh workflow run 3-script-generation.yml -f product_name=\"テスト商品\""
