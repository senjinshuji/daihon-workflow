# Phase 4: 改善ループ

## 🚨 必須：最初に実行すること
```bash
echo "📖 Phase 4詳細指示を読み込み中..."
# この詳細指示ファイルを読み込んだことをTodoWriteで記録してください
# TodoWrite: "Phase 4: phase4_improvement_loop.mdを読み込む" → completed
```

## 📋 このフェーズのタスク
CDから統合分析レポートを受領後、次のループに向けた改善を実施します。

## 実行条件
CDから `integrated_analysis_loop[N].md` を受け取った時に実行

## 詳細指示

### ✅ タスク1: 統合分析レポートの分析と評価モード決定

#### 1-1: 平均点の確認と評価モード選択
```bash
# 統合分析レポートから全体平均点を確認
# integrated_analysis_loop[N].md の「全体平均スコア」を参照

# 評価モードの自動決定
if [ "$CURRENT_LOOP_NUM" -eq 1 ]; then
    EVAL_MODE="standard"
elif [ "$AVERAGE_SCORE" -lt 70 ]; then
    EVAL_MODE="standard"
elif [ "$AVERAGE_SCORE" -lt 85 ]; then
    EVAL_MODE="strict"
else
    EVAL_MODE="critical"
fi

echo "📊 前回平均点: ${AVERAGE_SCORE}点"
echo "🎯 次回評価モード: ${EVAL_MODE}"
```

#### 1-2: 改善点の抽出
以下の観点で分析し、改善点を抽出：
- **高評価台本の成功要因**
- **低評価台本の改善点**
- **ペルソナ別の反応傾向**
- **新たに発見されたインサイト**

### ✅ タスク2: 次ループ用ディレクトリの作成

```bash
# ループ番号を設定（例：loop2）
CURRENT_LOOP_NUM=[現在のループ番号]  # 例: 1
NEXT_LOOP_NUM=$((CURRENT_LOOP_NUM + 1))
NEXT_LOOP="loop${NEXT_LOOP_NUM}"

# 次ループ用ディレクトリを作成
mkdir -p projects/$PROJECT_NAME/$NEXT_LOOP

# 各エージェントの成果物用ディレクトリを作成
cd projects/$PROJECT_NAME/$NEXT_LOOP
mkdir -p writer1 writer2 writer3
mkdir -p persona1 persona2 persona3

echo "📁 次ループ用ディレクトリを作成: projects/$PROJECT_NAME/$NEXT_LOOP"
echo "📁 各エージェント用サブディレクトリを作成: writer1-3, persona1-3"

# プロジェクトディレクトリに戻る
cd ../../..
```

### ✅ タスク3: 改善版ファイルの作成

統合分析レポートに基づいて、以下のファイルを更新：

#### 3-1: ライター向け指示書の更新
```bash
# 前回の成功要因を反映した新しい指示書を作成
cat > projects/$PROJECT_NAME/$NEXT_LOOP/copywriter_instructions.md << 'EOF'
# ライター向け制作指示書（${NEXT_LOOP}版）

## 前回ループからの学習事項
[統合分析から抽出した成功要因を記載]

## 改善された基本方針
[更新された方針を記載]

## 強化された訴求ポイント
[より効果的な訴求方法を記載]
EOF
```

#### 3-2: 評価基準の更新（評価モード付き）
```bash
# より精緻化された評価基準を作成
cat > projects/$PROJECT_NAME/$NEXT_LOOP/persona_evaluation_criteria.md << 'EOF'
# ペルソナ評価基準

## 評価モード: ${EVAL_MODE}
※前回平均${AVERAGE_SCORE}点に基づいて自動選択

## タスク
動画広告台本の評価 - 提供された台本を以下の基準で評価し、改善点を提案する

[評価モードに応じた基準を記載]
EOF
```

#### 3-3: クリエイティブ戦略の更新
```bash
# 戦略の改善版を作成
cat > projects/$PROJECT_NAME/$NEXT_LOOP/creative_strategy.md << 'EOF'
# 総合クリエイティブ戦略（${NEXT_LOOP}版）

## 前回ループの成果
[具体的な成果と学習事項]

## 改善された戦略
[新しい戦略方針]
EOF
```

### ✅ タスク4: 監督役の起動とCDへの次ループ開始指示

```bash
# 監督役を起動
echo "🔥 [MD] ${NEXT_LOOP} の監督を開始します。"
./supervisor.sh $NEXT_LOOP &
supervisor_pid=$!
echo "✅ 監督役が起動しました (PID: ${supervisor_pid})"

# CDへ次ループ開始を指示
./bb-agent-send.sh cd "${NEXT_LOOP}制作開始：
前回の統合分析に基づき、戦略ファイルを更新しました。

📊 前回平均: ${AVERAGE_SCORE}点
🎯 評価モード: ${EVAL_MODE}

📈 主な改善点：
[具体的な改善内容を箇条書き]

📁 更新ファイル：
- copywriter_instructions.md
- persona_evaluation_criteria.md（${EVAL_MODE}モード）
- creative_strategy.md

🚨 重要：評価基準が${EVAL_MODE}モードに設定されました。
より厳格な評価となりますが、台本品質の向上を目指してください。

🎯 これらの新指示書で${NEXT_LOOP}の制作を開始してください。"
```

### 完了確認
```bash
echo "✅ Phase 4: 改善ループ処理が完了しました。"
echo "🔄 ${NEXT_LOOP}の制作が開始されます。"
```

## 重要ポイント
- **分析の深度**: 統合分析レポートを詳細に分析し、具体的な改善点を抽出
- **評価モード管理**: 前回平均点に基づいて適切な評価モードを自動選択
- **継続的改善**: 各ループで着実に品質を向上させる
- **明確な指示**: CDへの指示は具体的かつ実行可能な内容にする
- **ループ番号管理**: 現在のループ番号を正確に把握し、次のループ番号を適切に設定

## 評価モード別の期待効果
- **standard (70-80点目標)**: 基本的な品質確保
- **strict (60-70点目標)**: より客観的な評価で改善点を明確化
- **critical (50-65点目標)**: 業界最高水準を目指す厳格評価 