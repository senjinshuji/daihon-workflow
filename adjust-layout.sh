#!/bin/bash

# 🎨 BB-Project tmux レイアウト手動調整スクリプト

echo "🎨 BB-Project レイアウト調整"
echo "=============================="

# セッション確認
if ! tmux has-session -t bb-multiagent 2>/dev/null; then
    echo "❌ bb-multiagentセッションが見つかりません"
    echo "💡 まず './setup-bb.sh' を実行してください"
    exit 1
fi

echo "📋 手動調整手順:"
echo ""
echo "1. セッションにアタッチ:"
echo "   tmux attach -t bb-multiagent"
echo ""
echo "2. レイアウト調整キーボードショートカット:"
echo ""
echo "   Ctrl+B → スペース  : レイアウト切替"
echo "   Ctrl+B → Alt+↑↓←→ : ペインサイズ調整"
echo "   Ctrl+B → 数字      : ペイン選択"
echo ""
echo "3. 理想的なレイアウト:"
echo "┌─────────────┬─────┬─────┬─────┐"
echo "│             │ P1  │ P2  │ P3  │"  
echo "│     CD      ├─────┼─────┼─────┤"
echo "│             │ W1  │ W2  │ W3  │"
echo "└─────────────┴─────┴─────┴─────┘"
echo ""
echo "自動調整を試しますか？ [y/N]:"
read -r answer

if [[ $answer == "y" || $answer == "Y" ]]; then
    echo "🔧 自動調整を実行中..."
    
    # tiledレイアウトで開始
    tmux select-layout -t bb-multiagent tiled
    sleep 0.5
    
    # CDペインを大きめに
    tmux resize-pane -t bb-multiagent:0.0 -x 80
    
    echo "✅ 基本調整完了"
    echo "📊 現在の結果:"
    tmux list-panes -t bb-multiagent -F "#{pane_index}: #{pane_title} #{pane_width}x#{pane_height}"
    echo ""
    echo "💡 完璧な2×3グリッドにするには手動調整が必要です"
else
    echo "📋 手動で調整してください。"
fi
