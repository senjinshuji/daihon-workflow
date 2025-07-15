# Phase 1: プロジェクト初期設定

## 🚨 必須：最初に実行すること
```bash
echo "📖 Phase 1詳細指示を読み込み中..."
# この詳細指示ファイルを読み込んだことをTodoWriteで記録してください
# TodoWrite: "Phase 1: phase1_setup.mdを読み込む" → completed
```

## 📋 このフェーズのタスク一覧
1. プロジェクトディレクトリの作成
2. 商品情報の対話的収集

## 詳細指示

### ✅ タスク1: プロジェクトディレクトリ作成

CSVファイル名に基づいたプロジェクト構造を作成します。

```bash
# CSVファイル名からプロジェクト名を自動設定（例：sales_data.csv → sales_data）
PROJECT_NAME="[CSVファイル名から拡張子を除いた名前]"
mkdir -p projects/$PROJECT_NAME/loop1
cd projects/$PROJECT_NAME

# プロジェクト直下に作成するファイル（loop共通で使用）
touch product_analysis.yaml
touch target_analysis.yaml

# loop1ディレクトリに移動
cd loop1

# loop1直下に作成するファイル（loop固有）
touch copywriter_instructions.md
touch persona_evaluation_criteria.yaml
touch creative_strategy.md

# 各エージェントの成果物用ディレクトリ
mkdir -p writer1 writer2 writer3
mkdir -p persona1 persona2 persona3

echo "🚀 プロジェクト '$PROJECT_NAME' のディレクトリ構造を作成しました。"
```

### ✅ タスク2: 商品情報の収集（対話形式）

**ユーザーとの対話を通じて以下の情報を収集します：**

1. 「商品名を教えてください」と質問
2. ユーザーの回答を待つ
3. 「商品ジャンルを教えてください」と質問
4. ユーザーの回答を待つ
5. 収集した情報を確認表示してから次へ進む

### 完了確認
```bash
echo "✅ Phase 1: プロジェクト初期設定が完了しました。"
echo "📁 作成されたディレクトリ: projects/$PROJECT_NAME"
echo "📝 収集した情報: 商品名=$PRODUCT_NAME, ジャンル=$PRODUCT_GENRE"
``` 