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
tmux kill-session -t bb-multiagent 2>/dev/null && log_info "bb-multiagentセッション削除完了" || log_info "bb-multiagentセッションは存在しませんでした"

# 完了ファイルクリア
mkdir -p ./tmp
rm -f ./tmp/writer*_done.txt 2>/dev/null && log_info "Writer完了ファイルをクリア" || log_info "Writer完了ファイルは存在しませんでした"
rm -f ./tmp/persona*_done.txt 2>/dev/null && log_info "Persona完了ファイルをクリア" || log_info "Persona完了ファイルは存在しませんでした"

log_success "✅ クリーンアップ完了"
echo ""

# STEP 2: bb-multiagentセッション作成（7ペイン：CD + Writer1-3 + Persona1-3）
log_info "📺 bb-multiagentセッション作成開始 (7ペイン)..."

# 最初のペイン作成
tmux new-session -d -s bb-multiagent -n "agents"

# 7分割レイアウト作成 (2+3+2の配置)
tmux split-window -v -t "bb-multiagent:0"      # 縦分割: 上下2つ
tmux split-window -h -t "bb-multiagent:0.0"    # 上部を左右分割
tmux split-window -h -t "bb-multiagent:0.1"    # 上部右をさらに分割
tmux split-window -h -t "bb-multiagent:0.3"    # 下部を左右分割
tmux split-window -h -t "bb-multiagent:0.4"    # 下部右をさらに分割
tmux split-window -h -t "bb-multiagent:0.5"    # 下部右をさらに分割

# ペインタイトル設定
log_info "ペインタイトル設定中..."
PANE_TITLES=("cd" "writer1" "writer2" "writer3" "persona1" "persona2" "persona3")
PANE_DESCRIPTIONS=("Creative Director" "感情訴求型" "論理訴求型" "カジュアル型" "共感重視型" "合理主義型" "トレンド志向型")

for i in {0..6}; do
    tmux select-pane -t "bb-multiagent:0.$i" -T "${PANE_TITLES[$i]}"
    
    # 作業ディレクトリ設定
    tmux send-keys -t "bb-multiagent:0.$i" "cd $(pwd)" C-m
    
    # カラープロンプト設定
    if [ $i -eq 0 ]; then
        # CD: 赤色
        tmux send-keys -t "bb-multiagent:0.$i" "export PS1='(\[\033[1;31m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    elif [ $i -le 3 ]; then
        # Writers: 青色
        tmux send-keys -t "bb-multiagent:0.$i" "export PS1='(\[\033[1;34m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    else
        # Personas: 紫色
        tmux send-keys -t "bb-multiagent:0.$i" "export PS1='(\[\033[1;35m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    fi
    
    # ウェルカムメッセージ
    tmux send-keys -t "bb-multiagent:0.$i" "echo '=== ${PANE_TITLES[$i]} (${PANE_DESCRIPTIONS[$i]}) ==='" C-m
    tmux send-keys -t "bb-multiagent:0.$i" "echo 'Instructions: @instructions/${PANE_TITLES[$i]}.md'" C-m
done

# レイアウトを調整
tmux select-layout -t bb-multiagent:0 tiled

log_success "✅ bb-multiagentセッション作成完了"
echo ""

# STEP 3: bb-mdセッション作成（1ペイン）
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

# STEP 4: 環境確認・表示
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
echo "  bb-multiagentセッション（7ペイン）:"
echo "    Pane 0: CD        (Creative Director)"
echo "    Pane 1: Writer1   (感情訴求型)"
echo "    Pane 2: Writer2   (論理訴求型)"
echo "    Pane 3: Writer3   (カジュアル型)"
echo "    Pane 4: Persona1  (共感重視型)"
echo "    Pane 5: Persona2  (合理主義型)"
echo "    Pane 6: Persona3  (トレンド志向型)"

echo ""
log_success "🎉 BB-Project Environment セットアップ完了！"
echo ""
echo "📋 次のステップ:"
echo "  1. 🔗 セッションアタッチ:"
echo "     tmux attach-session -t bb-md           # MD確認"
echo "     tmux attach-session -t bb-multiagent   # Multi-Agent確認"
echo ""
echo "  2. 🤖 Claude CLI一括起動:"
echo "     ./start-md.sh         # MD起動"
echo "     ./start-multiagent.sh # 7エージェント一括起動"
echo ""
echo "  3. 📜 指示書確認:"
echo "     MD: instructions/md.md"
echo "     CD: instructions/cd.md"
echo "     Writer1-3: instructions/writer[1-3].md"
echo "     Persona1-3: instructions/persona[1-3].md"
echo "     システム構造: CLAUDE.md"
echo ""
echo "  4. 🎯 実行開始: MDで「あなたはMDです。指示書に従って」と入力" 