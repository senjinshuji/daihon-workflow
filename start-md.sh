#!/bin/bash

# 🎯 BB-Project MD Agent Launcher

echo "🎯 MD (Marketing Director) Agent 起動中..."

# セッション存在確認
if ! tmux has-session -t bb-md 2>/dev/null; then
    echo "❌ エラー: bb-mdセッションが見つかりません"
    echo "💡 まず './setup-bb.sh' を実行してください"
    exit 1
fi

# Claude CLI起動
echo "📤 Claude CLI起動中..."
tmux send-keys -t bb-md "/Users/shjkt/.nvm/versions/node/v24.1.0/bin/claude --dangerously-skip-permissions" C-m

echo "✅ MD Agent起動完了！"
echo ""
echo "📋 次のステップ:"
echo "  1. tmux attach -t bb-md でセッションにアタッチ"
echo "  2. Claude CLI認証完了後、以下を入力:"
echo "     あなたはMDです。指示書に従って"
echo ""
echo "📜 MD指示書: instructions/md.md" 