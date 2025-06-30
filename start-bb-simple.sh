#!/bin/bash
# BB-Project シンプル起動スクリプト（文字化け対策版）

echo "BB-Project を起動します..."

# セッション名の定義
SESSION1="bb-md"
SESSION2="bb-cd"
SESSION3="bb-others"

# 既存セッションをクリーンアップ
tmux kill-session -t $SESSION1 2>/dev/null
tmux kill-session -t $SESSION2 2>/dev/null
tmux kill-session -t $SESSION3 2>/dev/null

# Terminal 1: MD専用
echo "Terminal 1: MD起動中..."
tmux new-session -d -s $SESSION1 -n "MD"
tmux send-keys -t $SESSION1:MD "cd $(pwd)" C-m
tmux send-keys -t $SESSION1:MD "clear" C-m
tmux send-keys -t $SESSION1:MD "echo 'MD (Marketing Director)'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo 'Role: Strategy, Persona generation, Final selection'" C-m
tmux send-keys -t $SESSION1:MD "echo 'Note: Does not write scripts (Writer job)'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo 'After authentication, send this message:'" C-m
tmux send-keys -t $SESSION1:MD "echo '私はMD（マーケティングディレクター）です。戦略立案とペルソナ生成、最終選定を担当します。台本は作成しません。'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo 'Then:'" C-m
tmux send-keys -t $SESSION1:MD "echo '1. cd projects/lactron'" C-m
tmux send-keys -t $SESSION1:MD "echo '2. python3 ../../agents/md_agent.py'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Terminal 2: CD専用
echo "Terminal 2: CD起動中..."
tmux new-session -d -s $SESSION2 -n "CD"
tmux send-keys -t $SESSION2:CD "cd $(pwd)" C-m
tmux send-keys -t $SESSION2:CD "clear" C-m
tmux send-keys -t $SESSION2:CD "echo 'CD (Creative Director)'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "echo 'Role declaration will be sent automatically from MD'" C-m
tmux send-keys -t $SESSION2:CD "echo 'Just wait for messages'" C-m
tmux send-keys -t $SESSION2:CD "echo ''" C-m
tmux send-keys -t $SESSION2:CD "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m

# Terminal 3: Others (6分割表示)
echo "Terminal 3: Writers & Personas起動中（6分割）..."
tmux new-session -d -s $SESSION3 -n "All-Agents"

# 6分割レイアウトを作成
tmux split-window -v -t $SESSION3:0
tmux split-window -v -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.2
tmux split-window -h -t $SESSION3:0.4

# 各ペインにシンプルなメッセージ
agents=("Writer1" "Writer2" "Writer3" "Persona1" "Persona2" "Persona3")
for i in {0..5}; do
    tmux send-keys -t $SESSION3:0.$i "cd $(pwd)" C-m
    tmux send-keys -t $SESSION3:0.$i "clear" C-m
    tmux send-keys -t $SESSION3:0.$i "echo '${agents[$i]}'" C-m
    tmux send-keys -t $SESSION3:0.$i "echo 'Role will be sent automatically'" C-m
    tmux send-keys -t $SESSION3:0.$i "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat" C-m
done

# レイアウトを均等に調整
tmux select-layout -t $SESSION3:0 tiled

echo ""
echo "準備完了！"
echo ""
echo "3つの新しいターミナルウィンドウで以下を実行："
echo "  Window 1: tmux attach -t bb-md"
echo "  Window 2: tmux attach -t bb-cd"
echo "  Window 3: tmux attach -t bb-others"
echo ""
echo "MDでの手順:"
echo "1. 認証後、表示されたメッセージを送信"
echo "2. cd projects/lactron"
echo "3. python3 ../../agents/md_agent.py"
echo ""