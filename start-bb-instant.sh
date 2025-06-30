#!/bin/bash
# BB-Project 即座起動スクリプト（認証済み前提）
# Claude CLI認証済みの場合、全エージェントの役割宣言を自動実行

echo "🚀 BB-Project 即座起動中（認証済み前提）..."

# Claude CLIのフルパス
CLAUDE_CLI="/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude"

# セッション名の定義
SESSION1="bb-md"
SESSION2="bb-cd"
SESSION3="bb-others"

# 認証状態を確認する関数
check_auth() {
    echo "🔍 Claude CLI認証状態を確認中..."
    if timeout 10s $CLAUDE_CLI auth status >/dev/null 2>&1; then
        echo "✅ Claude CLI認証済み - 即座起動を継続"
        return 0
    else
        echo "❌ Claude CLI未認証 - 手動認証が必要"
        return 1
    fi
}

# 非対話モードで役割宣言を送信する関数
send_role_declaration() {
    local session=$1
    local pane=$2
    local role_message="$3"
    local agent_name="$4"
    
    echo "📤 $agent_name に役割宣言送信中..."
    
    # 役割宣言をechoしてclaude chatにパイプ
    if [ -z "$pane" ]; then
        # セッション全体の場合
        tmux send-keys -t $session "echo '$role_message' | $CLAUDE_CLI --dangerously-skip-permissions chat" C-m
    else
        # 特定のペインの場合
        tmux send-keys -t $session:$pane "echo '$role_message' | $CLAUDE_CLI --dangerously-skip-permissions chat" C-m
    fi
}

# 認証状態をチェック
if ! check_auth; then
    echo ""
    echo "⚠️  Claude CLIが未認証です。手動認証が必要です。"
    echo "    通常の起動スクリプトを使用してください:"
    echo "    ./start-bb-smart.sh"
    echo ""
    exit 1
fi

# 既存セッションをクリーンアップ
tmux kill-session -t $SESSION1 2>/dev/null
tmux kill-session -t $SESSION2 2>/dev/null
tmux kill-session -t $SESSION3 2>/dev/null

echo "🎯 全エージェントを起動し、役割宣言を自動送信します..."

# Terminal 1: MD専用
echo "📊 Terminal 1: MD起動中..."
tmux new-session -d -s $SESSION1 -n "MD"
tmux send-keys -t $SESSION1:MD "cd $(pwd)" C-m
tmux send-keys -t $SESSION1:MD "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION1:MD "clear" C-m
tmux send-keys -t $SESSION1:MD "echo '🎯 MD (Marketing Director) - 自動役割宣言実行中...'" C-m

# MD役割宣言を自動送信
send_role_declaration "$SESSION1:MD" "" "私はMD（マーケティングディレクター）です。戦略立案とペルソナ生成、最終選定を担当します。台本は作成しません。プロジェクトを開始する準備ができました。" "MD"

sleep 2
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '📁 利用可能なプロジェクト:'" C-m
tmux send-keys -t $SESSION1:MD "ls -la projects/" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo '🚀 プロジェクト開始手順:'" C-m
tmux send-keys -t $SESSION1:MD "echo '1. cd projects/[プロジェクト名]'" C-m
tmux send-keys -t $SESSION1:MD "echo '2. python3 ../../agents/md_agent.py'" C-m

# Terminal 2: CD専用
echo "🎬 Terminal 2: CD起動中..."
tmux new-session -d -s $SESSION2 -n "CD"
tmux send-keys -t $SESSION2:CD "cd $(pwd)" C-m
tmux send-keys -t $SESSION2:CD "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
tmux send-keys -t $SESSION2:CD "clear" C-m
tmux send-keys -t $SESSION2:CD "echo '🎬 CD (Creative Director) - 自動役割宣言実行中...'" C-m

# CD役割宣言を自動送信
send_role_declaration "$SESSION2:CD" "" "私はCD（クリエイティブディレクター）です。MDからの戦略ブリーフを受信し、Writerへの指示とPersonaへの評価依頼を行います。台本は作成しません。agent-send.shで送られてくるメッセージを待機します。" "CD"

sleep 2
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo '📨 MDからのメッセージ待機中...'" C-m

# Terminal 3: Others (6分割表示)
echo "✍️ Terminal 3: Writers & Personas起動中（6分割）..."

# 単一ウィンドウで6ペイン作成
tmux new-session -d -s $SESSION3 -n "All-Agents"
tmux split-window -v -t $SESSION3:0
tmux split-window -v -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.2
tmux split-window -h -t $SESSION3:0.4

# 各エージェントの設定と役割宣言
agents=(
    "0.0:Writer1:私はwriter1（感情訴求型）です。CDからの指示を待ちます。感情に訴える台本を3本作成する準備ができています。"
    "0.1:Writer2:私はwriter2（論理訴求型）です。CDからの指示を待ちます。データと論理を重視した台本を3本作成する準備ができています。"
    "0.2:Writer3:私はwriter3（カジュアル型）です。CDからの指示を待ちます。親しみやすくテンポの良い台本を3本作成する準備ができています。"
    "0.3:Persona1:私はpersona1（共感重視型）です。CDからの評価依頼を待ちます。30-50代主婦層の視点で100点満点評価をする準備ができています。"
    "0.4:Persona2:私はpersona2（合理主義型）です。CDからの評価依頼を待ちます。25-45代ビジネスパーソンの視点で100点満点評価をする準備ができています。"
    "0.5:Persona3:私はpersona3（トレンド志向型）です。CDからの評価依頼を待ちます。18-30代Z世代の視点で100点満点評価をする準備ができています。"
)

for agent_info in "${agents[@]}"; do
    IFS=':' read -r pane_id agent_name role_message <<< "$agent_info"
    
    echo "🤖 $agent_name 起動中..."
    
    # 基本設定
    tmux send-keys -t $SESSION3:$pane_id "cd $(pwd)" C-m
    tmux send-keys -t $SESSION3:$pane_id "export PATH=/Users/shjkt/.nvm/versions/node/v24.1.0/bin:\$PATH" C-m
    tmux send-keys -t $SESSION3:$pane_id "clear" C-m
    tmux send-keys -t $SESSION3:$pane_id "echo '🤖 $agent_name - 自動役割宣言実行中...'" C-m
    
    # 役割宣言を自動送信
    send_role_declaration "$SESSION3" "$pane_id" "$role_message" "$agent_name"
    
    sleep 1
    tmux send-keys -t $SESSION3:$pane_id "echo '✅ $agent_name 準備完了 - 指示待機中'" C-m
done

# レイアウトを均等に調整
tmux select-layout -t $SESSION3:0 tiled

echo ""
echo "✅ 全エージェント即座起動完了！"
echo ""
echo "🎯 全8体のエージェントが役割を認識し、待機状態になりました"
echo ""
echo "📌 各ウィンドウにアクセス:"
echo "  tmux attach -t bb-md     # MDウィンドウ"
echo "  tmux attach -t bb-cd     # CDウィンドウ" 
echo "  tmux attach -t bb-others # Others（6分割）"
echo ""
echo "🚀 システム開始手順:"
echo "  1. tmux attach -t bb-md"
echo "  2. cd projects/[プロジェクト名] (例: cd projects/lactron)"
echo "  3. python3 ../../agents/md_agent.py"
echo ""
echo "🎯 エージェント配置:"
echo "  ┌─────────┬─────────┬─────────┐"
echo "  │Writer1  │Writer2  │Writer3  │"
echo "  ├─────────┼─────────┼─────────┤"
echo "  │Persona1 │Persona2 │Persona3 │"
echo "  └─────────┴─────────┴─────────┘"
echo ""
echo "💡 認証エラーが発生した場合は ./start-bb-smart.sh を使用してください"
echo ""