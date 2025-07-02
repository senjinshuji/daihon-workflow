#!/bin/bash

# 🚀 BB-Project All Agents Launcher (超簡単版)

echo "🚀 BB-Project 全エージェント一括起動中..."

# 環境セットアップ
echo "🔧 環境セットアップ中..."
./setup-bb.sh

echo ""
echo "⏳ 3秒待機中..."
sleep 3

# MD起動
echo "🎯 MD Agent起動中..."
./start-md.sh

echo ""
echo "⏳ 2秒待機中..."
sleep 2

# MultiAgent起動
echo "🤖 MultiAgent 一括起動中..."
./start-multiagent.sh

echo ""
echo "🎉 全エージェント起動完了！"
echo ""
echo "📋 セッションアタッチ方法:"
echo "  tmux attach -t bb-md           # MDセッション"
echo "  tmux attach -t bb-multiagent   # MultiAgentセッション"
echo ""
echo "🎯 使用開始手順:"
echo "  1. 各セッションにアタッチ"
echo "  2. Claude CLI認証"  
echo "  3. 各エージェントで役割宣言:"
echo "     MD: 「あなたはMDです。指示書に従って」"
echo "     その他: 「あなたは[エージェント名]です。指示書に従って」" 