#!/bin/bash
# BB-Project スマート起動スクリプト
# tmux起動時に役割を明確表示し、Claude認証後すぐに作業開始できるようにします

echo "🚀 BB-Project スマート起動中..."

# セッション名の定義
SESSION1="bb-md"
SESSION2="bb-cd"
SESSION3="bb-others"

# 既存セッションをクリーンアップ
tmux kill-session -t $SESSION1 2>/dev/null
tmux kill-session -t $SESSION2 2>/dev/null
tmux kill-session -t $SESSION3 2>/dev/null

# Terminal 1: MD専用
echo "📊 Terminal 1: MD起動中..."
tmux new-session -d -s $SESSION1 -n "MD"
tmux send-keys -t $SESSION1:MD "cd $(pwd)" C-m
tmux send-keys -t $SESSION1:MD "clear" C-m

# 環境変数とPATHを設定
tmux send-keys -t $SESSION1:MD "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION1:MD "export NVM_DIR=\"/Users/shjkt/.nvm\"" C-m

tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '🎯 あなたは MD (Marketing Director) です'" C-m
tmux send-keys -t $SESSION1:MD "echo '役割: 戦略立案・ペルソナ生成・最終選定'" C-m
tmux send-keys -t $SESSION1:MD "echo '注意: 台本は作成しません（Writerの仕事）'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '📁 利用可能なプロジェクト:'" C-m
tmux send-keys -t $SESSION1:MD "ls -la projects/" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m

# Claude CLIの確認
tmux send-keys -t $SESSION1:MD "echo '🔍 Claude CLI確認中...'" C-m
tmux send-keys -t $SESSION1:MD "which claude" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m

tmux send-keys -t $SESSION1:MD "echo '🚀 Claude認証後の次のフロー:'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '【STEP 1】以下のメッセージをコピー＆ペーストして送信:'" C-m
tmux send-keys -t $SESSION1:MD "echo '（送信後、全エージェントに役割宣言が自動配信されます）'" C-m
tmux send-keys -t $SESSION1:MD "echo '┌─────────────────────────────────────────────────────────────┐'" C-m
tmux send-keys -t $SESSION1:MD "echo '│ 私はMD（マーケティングディレクター）です。                 │'" C-m
tmux send-keys -t $SESSION1:MD "echo '│ 戦略立案とペルソナ生成、最終選定を担当します。             │'" C-m
tmux send-keys -t $SESSION1:MD "echo '│ 台本は作成しません。                                       │'" C-m
tmux send-keys -t $SESSION1:MD "echo '└─────────────────────────────────────────────────────────────┘'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '【STEP 2】プロジェクト選択:'" C-m
tmux send-keys -t $SESSION1:MD "echo '  cd projects/lactron  (または他のプロジェクト名)'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '【STEP 3】MDシステム起動:'" C-m
tmux send-keys -t $SESSION1:MD "echo '  python3 ../../agents/md_agent.py'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '⚠️  Claude CLIが起動しない場合は手動で以下を実行:'" C-m
tmux send-keys -t $SESSION1:MD "echo '/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m

# Claude CLIを実行
tmux send-keys -t $SESSION1:MD "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Terminal 2: CD専用
echo "🎬 Terminal 2: CD起動中..."
tmux new-session -d -s $SESSION2 -n "CD"
tmux send-keys -t $SESSION2:CD "cd $(pwd)" C-m
tmux send-keys -t $SESSION2:CD "clear" C-m

# 環境変数とPATHを設定
tmux send-keys -t $SESSION2:CD "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION2:CD "export NVM_DIR=\"/Users/shjkt/.nvm\"" C-m

tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo '🎬 あなたは CD (Creative Director) です'" C-m
tmux send-keys -t $SESSION2:CD "echo '役割: チーム管理・品質管理・改善指示'" C-m
tmux send-keys -t $SESSION2:CD "echo '注意: 台本は作成しません（Writerの仕事）'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo '🚀 Claude認証後の次のフロー:'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo '【役割宣言は自動配信されます】'" C-m
tmux send-keys -t $SESSION2:CD "echo 'MDがシステムを起動すると、以下が自動実行されます:'" C-m
tmux send-keys -t $SESSION2:CD "echo '1. あなたの役割宣言が自動送信されます'" C-m
tmux send-keys -t $SESSION2:CD "echo '2. 戦略ブリーフが自動送信されます'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo '手動で役割宣言したい場合のメッセージ:'" C-m
tmux send-keys -t $SESSION2:CD "echo '┌─────────────────────────────────────────────────────────────┐'" C-m
tmux send-keys -t $SESSION2:CD "echo '│ 私はCD（クリエイティブディレクター）です。                │'" C-m
tmux send-keys -t $SESSION2:CD "echo '│ MDからの戦略ブリーフを受信し、Writerへの指示と            │'" C-m
tmux send-keys -t $SESSION2:CD "echo '│ Personaへの評価依頼を行います。台本は作成しません。       │'" C-m
tmux send-keys -t $SESSION2:CD "echo '└─────────────────────────────────────────────────────────────┘'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo '📨 MDからのメッセージ待機中...'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Terminal 3: Others (6分割表示)
echo "✍️ Terminal 3: Writers & Personas起動中（6分割）..."

# 単一ウィンドウで6ペイン作成
tmux new-session -d -s $SESSION3 -n "All-Agents"

# 2x3グリッドレイアウトを作成
tmux split-window -v -t $SESSION3:0
tmux split-window -v -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.2
tmux split-window -h -t $SESSION3:0.4

# Writer1
tmux send-keys -t $SESSION3:0.0 "cd $(pwd)" C-m
tmux send-keys -t $SESSION3:0.0 "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION3:0.0 "clear" C-m
tmux send-keys -t $SESSION3:0.0 "echo '✍️ Writer1 (感情訴求型)'" C-m
tmux send-keys -t $SESSION3:0.0 "echo '役割宣言は自動配信されます'" C-m
tmux send-keys -t $SESSION3:0.0 "echo 'CDからの指示を待ちます'" C-m
tmux send-keys -t $SESSION3:0.0 "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Writer2
tmux send-keys -t $SESSION3:0.1 "cd $(pwd)" C-m
tmux send-keys -t $SESSION3:0.1 "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION3:0.1 "clear" C-m
tmux send-keys -t $SESSION3:0.1 "echo '✍️ Writer2 (論理訴求型)'" C-m
tmux send-keys -t $SESSION3:0.1 "echo '役割宣言は自動配信されます'" C-m
tmux send-keys -t $SESSION3:0.1 "echo 'CDからの指示を待ちます'" C-m
tmux send-keys -t $SESSION3:0.1 "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Writer3
tmux send-keys -t $SESSION3:0.2 "cd $(pwd)" C-m
tmux send-keys -t $SESSION3:0.2 "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION3:0.2 "clear" C-m
tmux send-keys -t $SESSION3:0.2 "echo '✍️ Writer3 (カジュアル型)'" C-m
tmux send-keys -t $SESSION3:0.2 "echo '役割宣言は自動配信されます'" C-m
tmux send-keys -t $SESSION3:0.2 "echo 'CDからの指示を待ちます'" C-m
tmux send-keys -t $SESSION3:0.2 "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Persona1
tmux send-keys -t $SESSION3:0.3 "cd $(pwd)" C-m
tmux send-keys -t $SESSION3:0.3 "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION3:0.3 "clear" C-m
tmux send-keys -t $SESSION3:0.3 "echo '👤 Persona1 (共感重視型)'" C-m
tmux send-keys -t $SESSION3:0.3 "echo '役割宣言は自動配信されます'" C-m
tmux send-keys -t $SESSION3:0.3 "echo 'CDからの評価依頼を待ちます'" C-m
tmux send-keys -t $SESSION3:0.3 "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Persona2
tmux send-keys -t $SESSION3:0.4 "cd $(pwd)" C-m
tmux send-keys -t $SESSION3:0.4 "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION3:0.4 "clear" C-m
tmux send-keys -t $SESSION3:0.4 "echo '👤 Persona2 (合理主義型)'" C-m
tmux send-keys -t $SESSION3:0.4 "echo '役割宣言は自動配信されます'" C-m
tmux send-keys -t $SESSION3:0.4 "echo 'CDからの評価依頼を待ちます'" C-m
tmux send-keys -t $SESSION3:0.4 "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Persona3
tmux send-keys -t $SESSION3:0.5 "cd $(pwd)" C-m
tmux send-keys -t $SESSION3:0.5 "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION3:0.5 "clear" C-m
tmux send-keys -t $SESSION3:0.5 "echo '👤 Persona3 (トレンド志向型)'" C-m
tmux send-keys -t $SESSION3:0.5 "echo '役割宣言は自動配信されます'" C-m
tmux send-keys -t $SESSION3:0.5 "echo 'CDからの評価依頼を待ちます'" C-m
tmux send-keys -t $SESSION3:0.5 "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# レイアウトを均等に調整
tmux select-layout -t $SESSION3:0 tiled

echo ""
echo "✅ 全エージェントが Claude認証待機中です！"
echo ""
echo "📌 各ウィンドウにアクセス:"
echo "  tmux attach -t bb-md     # MDウィンドウ"
echo "  tmux attach -t bb-cd     # CDウィンドウ"
echo "  tmux attach -t bb-others # Others（6分割）"
echo ""
echo "🎯 各エージェントで認証後、表示されているメッセージをすぐに送信してください"
echo ""
echo "🚀 システム開始手順:"
echo "  1. 全エージェントで Claude認証完了"
echo "  2. 各エージェントで表示されているメッセージを送信"
echo "  3. MD で cd projects/[プロジェクト名]"
echo "  4. MD で python3 ../../agents/md_agent.py"
echo ""
echo "🎯 エージェント配置:"
echo "  ┌─────────┬─────────┬─────────┐"
echo "  │Writer1  │Writer2  │Writer3  │"
echo "  ├─────────┼─────────┼─────────┤"
echo "  │Persona1 │Persona2 │Persona3 │"
echo "  └─────────┴─────────┴─────────┘"
echo ""