#!/bin/bash

# 🤖 BB-Project CD Launcher

echo "🤖 CD (Creative Director) Agent 起動中..."

# セッション存在確認
if ! tmux has-session -t bb-cd 2>/dev/null; then
    echo "❌ エラー: bb-cdセッションが見つかりません"
    echo "💡 まず './setup-bb.sh' を実行してください"
    exit 1
fi

# Claude CLI起動
echo "📤 Claude CLI起動中..."
tmux send-keys -t bb-cd "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions" C-m

echo "✅ CD Agent起動完了！"
echo ""
echo "📋 次のステップ:"
echo "  1. tmux attach -t bb-cd でセッションにアタッチ"
echo "  2. Claude CLI認証完了後、以下を入力:"
echo "     あなたはCDです。指示書に従って"
echo ""
echo "📜 CD指示書: instructions/cd.md" 