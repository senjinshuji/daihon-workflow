#!/bin/bash

# 🎯 BB-Project Environment Setup
# Claude Code Communications参考版

set -e  # エラー時に停止

# 色付きログ関数
log_info() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[1;34m[SUCCESS]\033[0m $1"
}

echo "🎯 BB-Project Environment Setup"
echo "==============================="
echo ""

# STEP 1: 既存セッションクリーンアップ
log_info "🧹 既存セッションクリーンアップ開始..."

tmux kill-session -t bb-md 2>/dev/null && log_info "bb-mdセッション削除完了" || log_info "bb-mdセッションは存在しませんでした"
tmux kill-session -t bb-cd 2>/dev/null && log_info "bb-cdセッション削除完了" || log_info "bb-cdセッションは存在しませんでした"
tmux kill-session -t bb-agents 2>/dev/null && log_info "bb-agentsセッション削除完了" || log_info "bb-agentsセッションは存在しませんでした"

# 完了ファイルクリア
mkdir -p ./tmp
rm -f ./tmp/writer*_done.txt 2>/dev/null && log_info "Writer完了ファイルをクリア" || log_info "Writer完了ファイルは存在しませんでした"
rm -f ./tmp/persona*_done.txt 2>/dev/null && log_info "Persona完了ファイルをクリア" || log_info "Persona完了ファイルは存在しませんでした"

log_success "✅ クリーンアップ完了"
echo ""

# STEP 2: bb-cdセッション作成（1ペイン：CD専用）
log_info "🤖 bb-cdセッション作成開始..."

tmux new-session -d -s bb-cd -n "cd"
tmux send-keys -t bb-cd "cd $(pwd)" C-m
tmux send-keys -t bb-cd "export PS1='(\[\033[1;31m\]CD\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
tmux send-keys -t bb-cd "echo '=== CD (Creative Director) ==='" C-m
tmux send-keys -t bb-cd "echo '人格形成・制作統括・品質管理・評価統合・ループ管理責任者'" C-m
tmux send-keys -t bb-cd "echo 'Instructions: @instructions/cd.md'" C-m
tmux send-keys -t bb-cd "echo '=============================='" C-m

log_success "✅ bb-cdセッション作成完了"

# STEP 3: bb-agentsセッション作成（6ペイン：Writer1-3 + Persona1-3）
log_info "📺 bb-agentsセッション作成開始 (6ペイン)..."

# 最初のペイン作成
tmux new-session -d -s bb-agents -n "agents"

# 6分割レイアウト作成（2×3グリッド）
# 1. 上下分割
tmux split-window -v -t "bb-agents:0"

# 2. 上段を3分割（persona1-3）
tmux split-window -h -t "bb-agents:0.0"
tmux split-window -h -t "bb-agents:0.1"

# 3. 下段を3分割（writer1-3）
tmux split-window -h -t "bb-agents:0.3"
tmux split-window -h -t "bb-agents:0.4"

# ペインタイトル設定
log_info "ペインタイトル設定中..."
PANE_TITLES=("persona1" "persona2" "persona3" "writer1" "writer2" "writer3")
PANE_DESCRIPTIONS=("共感重視型" "合理主義型" "トレンド志向型" "感情訴求型" "論理訴求型" "カジュアル型")

for i in {0..5}; do
    tmux select-pane -t "bb-agents:0.$i" -T "${PANE_TITLES[$i]}"
    
    # 作業ディレクトリ設定
    tmux send-keys -t "bb-agents:0.$i" "cd $(pwd)" C-m
    
    # カラープロンプト設定
    if [ $i -le 2 ]; then
        # Personas: 紫色
        tmux send-keys -t "bb-agents:0.$i" "export PS1='(\[\033[1;35m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    else
        # Writers: 青色
        tmux send-keys -t "bb-agents:0.$i" "export PS1='(\[\033[1;34m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    fi
    
    # ウェルカムメッセージ
    tmux send-keys -t "bb-agents:0.$i" "echo '=== ${PANE_TITLES[$i]} (${PANE_DESCRIPTIONS[$i]}) ==='" C-m
    tmux send-keys -t "bb-agents:0.$i" "echo 'Instructions: @instructions/${PANE_TITLES[$i]}.md'" C-m
done

# 2×3グリッドレイアウト適用
tmux select-layout -t bb-agents:0 tiled

log_success "✅ bb-agentsセッション作成完了"
echo ""

# STEP 4: bb-mdセッション作成（1ペイン）
log_info "🎯 bb-mdセッション作成開始..."

tmux new-session -d -s bb-md -n "md"
tmux send-keys -t bb-md "cd $(pwd)" C-m
tmux send-keys -t bb-md "export PS1='(\[\033[1;33m\]MD\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
tmux send-keys -t bb-md "echo '=== MD (Marketing Director) ==='" C-m
tmux send-keys -t bb-md "echo '戦略立案・ペルソナ分析・最終選定責任者'" C-m
tmux send-keys -t bb-md "echo 'Instructions: @instructions/md.md'" C-m
tmux send-keys -t bb-md "echo '=============================='" C-m

log_success "✅ bb-mdセッション作成完了"
echo ""

# STEP 5: 環境確認・表示
log_info "🔍 環境確認中..."

echo ""
echo "📊 セットアップ結果:"
echo "==================="

# tmuxセッション確認
echo "📺 Tmux Sessions:"
tmux list-sessions
echo ""

# ペイン構成表示
echo "📋 ペイン構成:"
echo "  bb-mdセッション（1ペイン）:"
echo "    Pane 0: MD        (Marketing Director)"
echo ""
echo "  bb-cdセッション（1ペイン）:"
echo "    Pane 0: CD        (Creative Director)"
echo ""
echo "  bb-agentsセッション（6ペイン - 2×3グリッド）:"
echo "    Pane 0: Persona1  (共感重視型)            ← 上左"
echo "    Pane 1: Persona2  (合理主義型)            ← 上中"
echo "    Pane 2: Persona3  (トレンド志向型)        ← 上右"
echo "    Pane 3: Writer1   (感情訴求型)            ← 下左"
echo "    Pane 4: Writer2   (論理訴求型)            ← 下中"
echo "    Pane 5: Writer3   (カジュアル型)          ← 下右"

echo ""
log_success "🎉 BB-Project Environment セットアップ完了！"
echo ""
echo "📋 次のステップ:"
echo "  1. 🔗 セッションアタッチ:"
echo "     tmux attach-session -t bb-md        # MD確認"
echo "     tmux attach-session -t bb-cd        # CD確認"
echo "     tmux attach-session -t bb-agents    # 6エージェント確認"
echo ""
echo "  2. 🤖 Claude CLI一括起動:"
echo "     ./start-md.sh         # MD起動"
echo "     ./start-cd.sh         # CD起動"
echo "     ./start-agents.sh     # 6エージェント一括起動"
echo ""
echo "  3. 📜 指示書確認:"
echo "     MD: instructions/md.md"
echo "     CD: instructions/cd.md"
echo "     Writer1-3: instructions/writer[1-3].md"
echo "     Persona1-3: instructions/persona[1-3].md"
echo "     システム構造: CLAUDE.md"
echo ""
echo "  4. 🎯 実行開始: MDで「あなたはMDです。指示書に従って」と入力" 