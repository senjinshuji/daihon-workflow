# Phase 3: CDへの制作指示

## 🚨 必須：最初に実行すること
```bash
echo "📖 Phase 3詳細指示を読み込み中..."
# この詳細指示ファイルを読み込んだことをTodoWriteで記録してください
# TodoWrite: "Phase 3: phase3_cd_instruction.mdを読み込む" → completed
```

## 📋 このフェーズのタスク
Phase 2の全ファイル作成完了後、CDに制作開始を指示します。

## 詳細指示

### ✅ 必須アクション

#### 1. 監督役（supervisor.sh）の起動
```bash
echo "🔥 [MD] Loop1 の監督を開始します。"
echo "🕵️  監督役 (supervisor.sh) をバックグラウンドで起動します..."
# supervisor.sh に現在のループ番号を引数として渡し、バックグラウンドで実行
./supervisor.sh loop1 &
supervisor_pid=$!
echo "✅ 監督役が起動しました (PID: ${supervisor_pid})。これよりCDに指示を出します。"
```

#### 2. CDへの制作指示送信
```bash
echo "📤 CDに制作指示を送信..."

./bb-agent-send.sh cd "Loop1制作開始：プロジェクト準備ファイル作成完了しました。

📋 作成済みファイル:
- market_analysis.md（CSV分析と商品分析）
- target_analysis.md（ペルソナ深層心理分析） 
- copywriter_instructions.md（ライター向け指示書）
- persona_evaluation_criteria.md（評価基準）
- creative_strategy.md（総合戦略）

🎯 次のアクション:
これらのファイルを参照し、writer1-3とpersona1-3の人格ファイルを作成後、
Loop1の15案制作を開始してください。

📊 制作目標:
- Writer1（感情訴求）×5案
- Writer2（論理訴求）×5案 
- Writer3（カジュアル）×5案
合計15案の台本制作

📁 成果物保存先:
projects/$PROJECT_NAME/loop1/[各エージェント名]/"

echo "✅ CDへの制作指示送信完了"
```

### 完了メッセージ表示
```bash
echo "🎉 Phase 1-3 完了！"
echo "✅ 戦略ファイル5つを作成完了"
echo "✅ CDへ制作指示を送信完了"
echo "🚀 15案の台本制作が開始されます"
```

## 重要ポイント
- **監督役の起動**: 必ずsupervisor.shをバックグラウンドで起動する
- **ループ番号の明示**: 現在のループ番号（loop1, loop2等）を明確に伝える
- **ファイル確認**: 作成済みファイルの一覧を正確に伝える
- **保存先の明示**: 成果物の保存先ディレクトリを明確に指定する 