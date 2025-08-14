# 🎬 AIクリエイティブ自動生成ワークフロー (リファクタリング版)

## 概要

Claude Code SDKを使用した、シンプルで効率的な広告台本自動生成システム。

## 🚀 クイックスタート

### 必要な設定

GitHub Secretsに以下を設定:
```
ANTHROPIC_API_KEY
GEMINI_API_KEY  
GOOGLE_SHEETS_API_KEY
GOOGLE_SHEETS_ID
```

### 実行方法

1つの統合ワークフローで全フェーズを実行:

```bash
# Phase 1: 初期分析
- Actions → "AI Creative Generation Workflow"
- product_name: "商品名"
- phase: "1"
- Run workflow

# Phase 2: 最適化ループ
- phase: "2"
- loop_number: "2" (繰り返し時は増やす)

# Phase 3: 最終生成
- phase: "3"
```

## 📁 構成

### メインワークフロー
```
.github/workflows/
├── main-workflow.yml           # 統合ワークフロー
└── orchestrators-refactored/   # 個別フェーズ版（オプション）
    ├── phase1-analysis.yml
    ├── phase2-optimization.yml
    └── phase3-final.yml
```

### プロンプト
```
.github/prompts-refactored/
├── phase1.txt       # 分析・生成
├── phase2.txt       # 台本生成・評価
└── optimization.txt # 基準最適化
```

### 出力
```
{product_name}/
├── data/            # CSVデータ
├── artifacts/       # 分析レポート
├── personas/        # ペルソナ (3名)
├── writers/         # ライター (3名)
├── scripts/         # 台本 (15本/ループ)
├── evaluations/     # 評価結果
└── deliverables/    # 最終成果物
```

## ⚡ 最適化のポイント

### 1. 統合ワークフロー
- 1つのワークフローで全フェーズ管理
- 条件分岐で適切な処理を実行
- 設定の一元管理

### 2. 並列処理
- ライター3名の台本生成を並列実行
- 9組の評価（3×3）を並列実行
- 処理時間を最大66%削減

### 3. コード削減
- 共通処理をヘルパー関数化
- 重複設定を環境変数に統合
- プロンプトテンプレートを簡潔化

### 削減結果
- **ファイル数**: 24 → 7 (70%削減)
- **コード行数**: ~3000行 → ~500行 (83%削減)
- **実行時間**: ~60分 → ~20分 (66%削減)

## 🔧 カスタマイズ

### 評価基準の調整
```json
// {product_name}/artifacts/criteria.json
{
  "weights": {
    "emotional_appeal": 0.25,
    "logical_structure": 0.25,
    "target_relevance": 0.25,
    "creativity": 0.25
  }
}
```

### Claude SDKパラメータ
```yaml
env:
  MAX_TURNS: 40        # 最大実行回数
  ALLOWED_TOOLS: "Read,Write,Bash"
```

## 📊 モニタリング

- **Actions タブ**: リアルタイム実行状況
- **Step Summary**: 各フェーズの結果サマリー
- **Commits**: 自動コミットで進捗追跡

## 🐛 トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| API制限エラー | MAX_TURNSを減らす |
| タイムアウト | 並列処理数を調整 |
| メモリ不足 | マトリックス戦略を分割 |

## 📄 ライセンス

MIT License