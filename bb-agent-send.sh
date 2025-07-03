#!/bin/bash

# 🚀 BB-Project Agent間メッセージ送信スクリプト

# エージェント→tmuxターゲット マッピング
get_agent_target() {
    case "$1" in
        "md") echo "bb-md" ;;
        "cd") echo "bb-multiagent:0.0" ;;
        "persona1") echo "bb-multiagent:0.1" ;;
        "writer1") echo "bb-multiagent:0.2" ;;
        "persona2") echo "bb-multiagent:0.3" ;;
        "persona3") echo "bb-multiagent:0.4" ;;
        "writer2") echo "bb-multiagent:0.5" ;;
        "writer3") echo "bb-multiagent:0.6" ;;
        *) echo "" ;;
    esac
}

show_usage() {
    cat << EOF
🤖 BB-Project Agent間メッセージ送信

使用方法:
  $0 [エージェント名] [メッセージ]
  $0 --list
  $0 --status

利用可能エージェント:
  md       - Marketing Director (戦略立案・最終選定)
  cd       - Creative Director (チーム統括・品質管理)
  writer1  - 感情訴求型ライター
  writer2  - 論理訴求型ライター
  writer3  - カジュアル型ライター
  persona1 - 共感重視型評価者 (30-50代主婦層)
  persona2 - 合理主義型評価者 (25-45代ビジネス層)
  persona3 - トレンド志向型評価者 (18-30代Z世代)

使用例:
  $0 md "指示書に従って"
  $0 cd "プロジェクト開始：lactronプロジェクトを開始してください"
  $0 writer1 "台本制作開始：感情訴求型で3本作成してください"
  $0 persona1 "台本評価開始：共感性重視で評価してください"
EOF
}

# エージェント一覧表示
show_agents() {
    echo "📋 BB-Project エージェント構成:"
    echo "========================================"
    echo "  md       → bb-md:0           (Marketing Director)"
    echo "  cd       → bb-multiagent:0.0 (Creative Director)"
    echo "  persona1 → bb-multiagent:0.1 (共感重視型評価者)"
    echo "  writer1  → bb-multiagent:0.2 (感情訴求型ライター)"
    echo "  persona2 → bb-multiagent:0.3 (合理主義型評価者)"
    echo "  persona3 → bb-multiagent:0.4 (トレンド志向型評価者)"
    echo "  writer2  → bb-multiagent:0.5 (論理訴求型ライター)"
    echo "  writer3  → bb-multiagent:0.6 (カジュアル型ライター)"
}

# システム状態確認
show_status() {
    echo "🔍 BB-Project システム状態確認:"
    echo "======================================"
    
    # tmuxセッション確認
    if tmux has-session -t bb-md 2>/dev/null; then
        echo "✅ MD Session: Running"
    else
        echo "❌ MD Session: Not found"
    fi
    
    if tmux has-session -t bb-multiagent 2>/dev/null; then
        echo "✅ MultiAgent Session: Running"
        # ペイン数確認
        pane_count=$(tmux list-panes -t bb-multiagent | wc -l)
        echo "   └─ Panes: $pane_count/7 (CD + Writer1-3 + Persona1-3)"
    else
        echo "❌ MultiAgent Session: Not found"
    fi
    
    # 完了ファイル確認
    echo ""
    echo "📁 作業状況確認:"
    if [ -d "./tmp" ]; then
        ls -la ./tmp/writer*_done.txt 2>/dev/null | wc -l | xargs echo "   Writer完了ファイル: " 
        ls -la ./tmp/persona*_done.txt 2>/dev/null | wc -l | xargs echo "   Persona完了ファイル: "
    else
        echo "   tmpディレクトリが見つかりません"
    fi
    
    # ログ確認
    if [ -f "logs/send_log.txt" ]; then
        recent_logs=$(tail -3 logs/send_log.txt)
        echo ""
        echo "📜 最新メッセージログ (直近3件):"
        echo "$recent_logs"
    fi
}

# ログ記録
log_send() {
    local agent="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    mkdir -p logs
    echo "[$timestamp] $agent: SENT - \"$message\"" >> logs/send_log.txt
}

# メッセージ送信
send_message() {
    local target="$1"
    local message="$2"
    
    echo "📤 送信中: $target ← '$message'"
    
    # Claude Codeのプロンプトを一度クリア
    tmux send-keys -t "$target" C-c
    sleep 0.3
    
    # メッセージ送信
    tmux send-keys -t "$target" "$message"
    sleep 0.1
    
    # エンター押下
    tmux send-keys -t "$target" C-m
    sleep 0.5
}

# ターゲット存在確認
check_target() {
    local target="$1"
    local session_name="${target%%:*}"
    
    if ! tmux has-session -t "$session_name" 2>/dev/null; then
        echo "❌ セッション '$session_name' が見つかりません"
        echo "💡 './start-bb-md.sh' でシステムを起動してください"
        return 1
    fi
    
    return 0
}

# メイン処理
main() {
    if [[ $# -eq 0 ]]; then
        show_usage
        exit 1
    fi
    
    # オプション処理
    case "$1" in
        "--list")
            show_agents
            exit 0
            ;;
        "--status")
            show_status
            exit 0
            ;;
        "--help" | "-h")
            show_usage
            exit 0
            ;;
    esac
    
    if [[ $# -lt 2 ]]; then
        show_usage
        exit 1
    fi
    
    local agent_name="$1"
    local message="$2"
    
    # エージェントターゲット取得
    local target
    target=$(get_agent_target "$agent_name")
    
    if [[ -z "$target" ]]; then
        echo "❌ エラー: 不明なエージェント '$agent_name'"
        echo "利用可能エージェント: $0 --list"
        exit 1
    fi
    
    # ターゲット確認
    if ! check_target "$target"; then
        exit 1
    fi
    
    # メッセージ送信
    send_message "$target" "$message"
    
    # ログ記録
    log_send "$agent_name" "$message"
    
    echo "✅ 送信完了: $agent_name に '$message'"
    
    return 0
}

main "$@" 