# 🚀 台本作成ワークフロー - クイックスタートガイド

## 📋 概要
商品名を入力するだけで、動画広告台本を自動生成する完全自動化ワークフローです。

## ⚡ 実行手順

### 1. 準備
必要なシークレットが設定されていることを確認：
- `ANTHROPIC_API_KEY`
- `GOOGLE_SHEETS_API_KEY` 
- `GEMINI_API_KEY`
- `GOOGLE_SHEETS_ID`

### 2. ワークフロー実行
```bash
# Phase 1を実行（残りは自動実行）
gh workflow run orchestrator/1-analysis.yml -f product_name="あなたの商品名"
```

または、GitHub UIから：
1. Actionsタブを開く
2. "1. 分析・ペルソナ・ライター生成フェーズ"を選択
3. "Run workflow"をクリック
4. 商品名を入力して実行

### 3. 実行状況確認
- **Phase 1**: 15-30分（分析・ペルソナ・ライター生成）
- **Phase 2**: 5-15分（評価基準最適化、自動ループ）
- **Phase 3**: 20-40分（台本生成・フィルタリング）

### 4. 結果確認
実行完了後、以下のファイルが生成されます：
```
{商品名}/
├── approved_scripts/     # 🎯 承認済み台本（各ライター3本以上）
├── artifacts/           # 📊 分析結果・評価データ
├── personas/            # 👤 ペルソナ定義
└── writers/             # ✍️ ライター定義
```

## 🎯 主要出力

### 承認済み台本
- **ファイル**: `{商品名}/approved_scripts/`
- **内容**: 品質基準をクリアした台本（各ライター3本以上）
- **フォーマット**: 5シーン構成、600文字以上、制作ノート付き

### 分析レポート
- **商品分析**: `{商品名}/artifacts/product_analysis.md`
- **ターゲット分析**: `{商品名}/artifacts/target_analysis_1-3.md`
- **評価レポート**: `{商品名}/artifacts/script_evaluation_report.md`

## 🔧 手動実行（必要時）

通常は自動実行されますが、個別に実行したい場合：

```bash
# Phase 2のみ実行
gh workflow run orchestrator/2-criteria-optimization.yml -f product_name="商品名"

# Phase 3のみ実行
gh workflow run orchestrator/3-script-generation.yml -f product_name="商品名"
```

## ❓ よくある質問

**Q: 実行が途中で止まった場合は？**
A: 各フェーズは独立して実行可能です。止まったフェーズから再実行してください。

**Q: 台本の品質が低い場合は？**
A: Phase 3で自動調整が実行されます。さらに改善が必要な場合は、Phase 2から再実行してください。

**Q: 複数の商品を同時実行できますか？**
A: 可能ですが、API制限があるため、順次実行を推奨します。

**Q: 生成された台本をカスタマイズしたい場合は？**
A: `{商品名}/writers/` のライター定義を編集後、Phase 3を再実行してください。

## 📞 サポート
問題が発生した場合は、GitHub ActionsのログとWORKFLOW_SPECIFICATION.mdのトラブルシューティングセクションを確認してください。
