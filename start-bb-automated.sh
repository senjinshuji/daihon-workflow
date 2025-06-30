#!/bin/bash
# BB-Project 自動化起動スクリプト（Python Agent版）

echo "🤖 BB-Project 自動化システム起動開始..."

# セッション名の定義
SESSION1="bb-md"
SESSION2="bb-cd" 
SESSION3="bb-others"

# 既存セッションをクリーンアップ
tmux kill-session -t $SESSION1 2>/dev/null
tmux kill-session -t $SESSION2 2>/dev/null
tmux kill-session -t $SESSION3 2>/dev/null

# メッセージディレクトリ作成
mkdir -p messages
echo "📁 メッセージディレクトリ作成完了"

echo ""
echo "🚀 自動化エージェント起動中..."

# Terminal 1: MD Agent (Human-Operated)
echo "Terminal 1: MD Agent起動中..."
tmux new-session -d -s $SESSION1 -n "MD"
tmux set-option -t $SESSION1 remain-on-exit on
tmux send-keys -t $SESSION1:MD "cd $(pwd)" C-m
tmux send-keys -t $SESSION1:MD "clear" C-m
tmux send-keys -t $SESSION1:MD "echo '🎯 MD (Marketing Director) - Human Interface'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo 'Role: 戦略立案・ペルソナ生成・最終選定'" C-m
tmux send-keys -t $SESSION1:MD "echo 'Mode: Human operated (Claude CLI)'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo 'After authentication:'" C-m
tmux send-keys -t $SESSION1:MD "echo '1. Send role declaration message'" C-m
tmux send-keys -t $SESSION1:MD "echo '2. cd projects/lactron'" C-m
tmux send-keys -t $SESSION1:MD "echo '3. python3 ../../agents/md_agent.py'" C-m
tmux send-keys -t $SESSION1:MD "echo ''" C-m
tmux send-keys -t $SESSION1:MD "echo 'Starting Claude CLI...'" C-m
tmux send-keys -t $SESSION1:MD "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions chat || bash" C-m

# Terminal 2: CD Agent (Automated)
echo "Terminal 2: CD Agent自動化起動中..."
tmux new-session -d -s $SESSION2 -n "CD-Auto"
tmux set-option -t $SESSION2 remain-on-exit on
tmux send-keys -t $SESSION2:CD-Auto "cd $(pwd)" C-m
tmux send-keys -t $SESSION2:CD-Auto "clear" C-m
tmux send-keys -t $SESSION2:CD-Auto "echo '🎬 CD (Creative Director) - Automated Agent'" C-m
tmux send-keys -t $SESSION2:CD-Auto "echo ''" C-m
tmux send-keys -t $SESSION2:CD-Auto "echo 'Role: Writer調整・Persona評価管理・ループ制御'" C-m
tmux send-keys -t $SESSION2:CD-Auto "echo 'Mode: Fully automated (Python process)'" C-m
tmux send-keys -t $SESSION2:CD-Auto "echo ''" C-m
tmux send-keys -t $SESSION2:CD-Auto "echo 'Starting CD Agent...'" C-m
tmux send-keys -t $SESSION2:CD-Auto "python3 agents/cd_agent_runner.py" C-m

# Terminal 3: Writers & Personas (6分割 - All Automated)
echo "Terminal 3: Writers & Personas自動化起動中（6分割）..."
tmux new-session -d -s $SESSION3 -n "Automated-Agents"
tmux set-option -t $SESSION3 remain-on-exit on

# 6分割レイアウトを作成
tmux split-window -v -t $SESSION3:0
tmux split-window -v -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.0
tmux split-window -h -t $SESSION3:0.2
tmux split-window -h -t $SESSION3:0.4

# 各ペインに自動化エージェントを配置
agents=("writer1" "writer2" "writer3" "persona1" "persona2" "persona3")
descriptions=("Writer1 (感情派)" "Writer2 (論理派)" "Writer3 (カジュアル派)" "Persona1 (共感重視)" "Persona2 (合理主義)" "Persona3 (トレンド志向)")

for i in {0..5}; do
    agent_id=${agents[$i]}
    description=${descriptions[$i]}
    
    tmux send-keys -t $SESSION3:0.$i "cd $(pwd)" C-m
    tmux send-keys -t $SESSION3:0.$i "clear" C-m
    tmux send-keys -t $SESSION3:0.$i "echo '🤖 $description - Automated Agent'" C-m
    tmux send-keys -t $SESSION3:0.$i "echo ''" C-m
    tmux send-keys -t $SESSION3:0.$i "echo 'Mode: Fully automated (Python process)'" C-m
    tmux send-keys -t $SESSION3:0.$i "echo 'Status: Starting agent...'" C-m
    tmux send-keys -t $SESSION3:0.$i "echo ''" C-m
    
    # Start appropriate agent
    if [[ "$agent_id" =~ ^writer ]]; then
        tmux send-keys -t $SESSION3:0.$i "python3 agents/writer_agent_runner.py $agent_id" C-m
    else
        tmux send-keys -t $SESSION3:0.$i "python3 agents/persona_agent_runner.py $agent_id" C-m
    fi
done

# レイアウトを均等に調整
tmux select-layout -t $SESSION3:0 tiled

# 起動確認のための待機
echo ""
echo "⏳ エージェント起動中... (5秒)"
sleep 5

echo ""
echo "✅ BB-Project 自動化システム起動完了！"
echo ""
echo "📌 3つの新しいターミナルウィンドウで以下を実行："
echo "  Window 1: tmux attach -t bb-md      (MD - Human Interface)"
echo "  Window 2: tmux attach -t bb-cd      (CD - Automated)"
echo "  Window 3: tmux attach -t bb-others  (Writers & Personas - All Automated)"
echo ""
echo "🤖 自動化システム構成:"
echo "  ✅ MD Agent:      Human-operated (戦略立案・ペルソナ生成)"
echo "  ✅ CD Agent:      Automated (Writer調整・評価管理)" 
echo "  ✅ Writer1-3:     Automated (台本制作)"
echo "  ✅ Persona1-3:    Automated (台本評価)"
echo ""
echo "🔄 実行フロー:"
echo "1. MDでClaude CLI認証後、台本制作指示を送信"
echo "2. 全8エージェントが自動で協調動作"
echo "3. 承認台本（80点以上）を自動選定"
echo "4. 最終結果をMDに自動報告"
echo ""
echo "🎯 MDでの開始手順:"
echo "1. tmux attach -t bb-md"
echo "2. Claude CLI認証"
echo "3. 役割宣言メッセージ送信"
echo "4. cd projects/lactron"
echo "5. python3 ../../agents/md_agent.py"
echo ""
echo "📊 システム状態確認: ./agent-send.sh --status"
echo ""