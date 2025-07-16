# Phase 2: 戦略分析とファイル作成

## 🚨 必須：最初に実行すること
```bash
echo "📖 Phase 2戦略ファイルを読み込み中..."
# この詳細指示ファイルを読み込んだことをTodoWriteで記録してください
# TodoWrite: "Phase 2: phase2_strategy.mdを読み込む" → completed
```

## 📋 このフェーズの概要
商品分析、ターゲット分析を行い、制作に必要な5つの戦略ファイルを作成します。

## タスク一覧
以下の5つのタスクを順番に実行してください：

### タスク1: CSV分析とmarket_analysis.md作成
**詳細指示**: `instructions/md_tasks/phase2_task1_product_analysis.md` を参照
- 売れる台本の要素分析
- 訴求方向性の決定
- WHO-FMT-USP分析

### タスク2: ターゲット分析（target_analysis.md）
**詳細指示**: `instructions/md_tasks/phase2_task2_target_analysis.md` を参照
- ペルソナの深層心理10要素分析
- 認知変化の設計
- キャッチコピーの策定

### タスク3: ライター向け指示書（copywriter_instructions.md）
**詳細指示**: `instructions/md_tasks/phase2_task3_copywriter_instructions.md` を参照
- 3人のライター向け制作方針
- 必須制作要件の明確化
- 品質チェックリスト

### タスク4: ペルソナ評価基準（persona_evaluation_criteria.md）
**詳細指示**: `instructions/md_tasks/phase2_task4_persona_criteria.md` を参照
- 11項目の評価基準設定
- スコアリング方法の定義
- 評価レポートフォーマット

### タスク5: 総合クリエイティブ戦略（creative_strategy.md）
**詳細指示**: `instructions/md_tasks/phase2_task5_creative_strategy.md` を参照
- ブランドポジショニング
- 差別化戦略
- 成功指標の設定

## 実行手順

### 1. タスクファイルの読み込みと実行
各タスクを実行する前に、必ず該当するタスクファイルを読み込んでください：

```bash
# タスク1の実行
echo "📋 Phase 2 タスク1を開始します..."
cat instructions/md_tasks/phase2_task1_product_analysis.md
# 指示に従って実行

# タスク2の実行
echo "📋 Phase 2 タスク2を開始します..."
cat instructions/md_tasks/phase2_task2_target_analysis.md
# 指示に従って実行

# 以下、タスク3〜5も同様に実行
```

### 2. 変数の管理
以下の変数を適切に設定・管理してください：
- `PROJECT_NAME`: CSVファイル名から自動設定
- `PRODUCT_NAME`: Phase 1で収集した商品名
- `PRODUCT_GENRE`: Phase 1で収集した商品ジャンル

### 3. 完了確認
全5タスクの完了後、以下を確認：
```bash
echo "🔍 Phase 2 の完了確認..."
ls -la projects/$PROJECT_NAME/
ls -la projects/$PROJECT_NAME/loop1/

echo "✅ Phase 2: 戦略分析とファイル作成が完了しました"
```

## 重要事項
- **順次実行**: タスク1から順番に実行すること
- **ファイル依存**: 後のタスクは前のタスクの成果物を参照する
- **エラーチェック**: 各タスクの完了確認を必ず行う
- **内容の整合性**: 作成したファイル間で内容が矛盾しないよう注意 