#!/bin/bash

# 🚀 BB-Project Agent間メッセージ送信スクリプト (Hooks対応版)

# 🔧 設定ファイル
PROGRESS_FILE="progress_status.md"
HOOKS_LOG="logs/hooks_log.txt"

# 🎯 Hooks設定
HOOKS_ENABLED=true
AUTO_PROGRESS=true

# ===================================
# 📊 状態管理システム
# ===================================

# 進行状況ファイル初期化
init_progress_file() {
    if [ ! -f "$PROGRESS_FILE" ]; then
        echo "🔄 進行状況ファイルを初期化..."
        touch "$PROGRESS_FILE"
    fi
}

# 状態更新
update_status() {
    local agent="$1"
    local status="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    init_progress_file
    
    # 簡易的な状態更新（実際のYAMLパーサーの代わり）
    if grep -q "${agent}_status:" "$PROGRESS_FILE"; then
        sed -i.bak "s/${agent}_status: .*/${agent}_status: $status/" "$PROGRESS_FILE"
    else
        echo "${agent}_status: $status" >> "$PROGRESS_FILE"
    fi
    
    # タイムスタンプ更新
    sed -i.bak "s/updated_at: .*/updated_at: \"$timestamp\"/" "$PROGRESS_FILE"
    
    log_hooks "STATUS_UPDATE" "$agent → $status"
}

# 完了カウンター更新
update_completion_count() {
    local agent="$1"
    local count="$2"
    
    init_progress_file
    
    if grep -q "${agent}_completed_count:" "$PROGRESS_FILE"; then
        sed -i.bak "s/${agent}_completed_count: .*/${agent}_completed_count: $count/" "$PROGRESS_FILE"
    else
        echo "${agent}_completed_count: $count" >> "$PROGRESS_FILE"
    fi
    
    log_hooks "COUNT_UPDATE" "$agent → $count"
}

# フェーズ更新
update_phase() {
    local new_phase="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    init_progress_file
    
    if grep -q "phase_current:" "$PROGRESS_FILE"; then
        sed -i.bak "s/phase_current: .*/phase_current: $new_phase/" "$PROGRESS_FILE"
    else
        echo "phase_current: $new_phase" >> "$PROGRESS_FILE"
    fi
    
    # フェーズ開始時刻更新
    sed -i.bak "s/phase_started_at: .*/phase_started_at: \"$timestamp\"/" "$PROGRESS_FILE"
    
    log_hooks "PHASE_UPDATE" "新フェーズ: $new_phase"
}

# ===================================
# 🎯 Hooks システム
# ===================================

# Hooks ログ記録
log_hooks() {
    local hook_type="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    mkdir -p logs
    echo "[$timestamp] HOOK:$hook_type - $message" >> "$HOOKS_LOG"
}

# 完了通知パターンマッチング
detect_completion_pattern() {
    local agent="$1"
    local message="$2"
    
    # Writer完了パターン
    if [[ "$message" =~ Writer[1-3]制作完了 ]]; then
        local writer_num=$(echo "$message" | sed -n 's/.*Writer\([1-3]\)制作完了.*/\1/p')
        handle_writer_completion "writer$writer_num" "$message"
        return 0
    fi
    
    # Persona完了パターン
    if [[ "$message" =~ Persona[1-3]評価完了 ]]; then
        local persona_num=$(echo "$message" | sed -n 's/.*Persona\([1-3]\)評価完了.*/\1/p')
        handle_persona_completion "persona$persona_num" "$message"
        return 0
    fi
    
    # Loop完了パターン
    if [[ "$message" =~ Loop[0-9]+完了報告 ]]; then
        local loop_num=$(echo "$message" | sed -n 's/.*Loop\([0-9]\+\)完了報告.*/\1/p')
        handle_loop_completion "$loop_num" "$message"
        return 0
    fi
    
    # MD分析完了パターン
    if [[ "$message" =~ 分析完了 ]] && [[ "$agent" == "md" ]]; then
        handle_md_analysis_completion "$message"
        return 0
    fi
    
    return 1
}

# Writer完了処理
handle_writer_completion() {
    local writer="$1"
    local message="$2"
    
    log_hooks "WRITER_COMPLETION" "$writer完了検出"
    
    # ファイル数確認
    local loop_num=$(get_current_loop)
    local completed_files=$(ls loop${loop_num}/${writer}_台本*_loop${loop_num}.md 2>/dev/null | wc -l)
    
    # 状態更新
    update_status "$writer" "completed"
    update_completion_count "$writer" "$completed_files"
    
    # 全Writer完了確認
    if check_all_writers_completed; then
        log_hooks "ALL_WRITERS_COMPLETED" "全Writer完了 → 評価フェーズ開始"
        trigger_evaluation_phase
    fi
}

# Persona完了処理
handle_persona_completion() {
    local persona="$1"
    local message="$2"
    
    log_hooks "PERSONA_COMPLETION" "$persona完了検出"
    
    # 状態更新
    update_status "$persona" "completed"
    
    # 完了フラグ設定
    if grep -q "${persona}_completed:" "$PROGRESS_FILE"; then
        sed -i.bak "s/${persona}_completed: .*/${persona}_completed: true/" "$PROGRESS_FILE"
    else
        echo "${persona}_completed: true" >> "$PROGRESS_FILE"
    fi
    
    # 全Persona完了確認
    if check_all_personas_completed; then
        log_hooks "ALL_PERSONAS_COMPLETED" "全Persona完了 → 統合分析フェーズ開始"
        trigger_analysis_phase
    fi
}

# Loop完了処理
handle_loop_completion() {
    local loop_num="$1"
    local message="$2"
    
    log_hooks "LOOP_COMPLETION" "Loop$loop_num完了検出"
    
    # 状態更新
    update_phase "completed"
    
    # 次ループ準備
    if [[ "$AUTO_PROGRESS" == true ]]; then
        log_hooks "AUTO_NEXT_LOOP" "次ループ準備中..."
        # 次ループ指示をMDに送信
        sleep 2
        send_message_internal "md" "前回ループ完了確認。次ループ準備を開始してください。"
    fi
}

# MD分析完了処理
handle_md_analysis_completion() {
    local message="$1"
    
    log_hooks "MD_ANALYSIS_COMPLETION" "MD分析完了 → CD制作指示"
    
    # 状態更新
    update_phase "creating"
    
    # CDに制作指示送信
    if [[ "$AUTO_PROGRESS" == true ]]; then
        sleep 1
        send_message_internal "cd" "MD分析完了確認。制作フェーズを開始してください。"
    fi
}

# ===================================
# 🔍 完了状態確認
# ===================================

# 現在のループ番号取得
get_current_loop() {
    if grep -q "現在のループ:" "$PROGRESS_FILE"; then
        grep "現在のループ:" "$PROGRESS_FILE" | sed 's/.*: *//'
    else
        echo "1"
    fi
}

# 全Writer完了確認
check_all_writers_completed() {
    local loop_num=$(get_current_loop)
    local writer1_count=$(ls loop${loop_num}/writer1_台本*_loop${loop_num}.md 2>/dev/null | wc -l)
    local writer2_count=$(ls loop${loop_num}/writer2_台本*_loop${loop_num}.md 2>/dev/null | wc -l)
    local writer3_count=$(ls loop${loop_num}/writer3_台本*_loop${loop_num}.md 2>/dev/null | wc -l)
    
    [[ $writer1_count -eq 5 ]] && [[ $writer2_count -eq 5 ]] && [[ $writer3_count -eq 5 ]]
}

# 全Persona完了確認
check_all_personas_completed() {
    local loop_num=$(get_current_loop)
    
    [[ -f "loop${loop_num}/persona1_evaluation_loop${loop_num}.md" ]] && \
    [[ -f "loop${loop_num}/persona2_evaluation_loop${loop_num}.md" ]] && \
    [[ -f "loop${loop_num}/persona3_evaluation_loop${loop_num}.md" ]]
}

# ===================================
# 🚀 自動進行トリガー
# ===================================

# 評価フェーズ開始
trigger_evaluation_phase() {
    if [[ "$AUTO_PROGRESS" != true ]]; then
        return
    fi
    
    log_hooks "TRIGGER_EVALUATION" "評価フェーズ自動開始"
    
    # フェーズ更新
    update_phase "evaluating"
    
    # CDに評価指示送信
    sleep 1
    send_message_internal "cd" "Writer制作完了確認。評価フェーズを開始してください。"
}

# 統合分析フェーズ開始
trigger_analysis_phase() {
    if [[ "$AUTO_PROGRESS" != true ]]; then
        return
    fi
    
    log_hooks "TRIGGER_ANALYSIS" "統合分析フェーズ自動開始"
    
    # フェーズ更新
    update_phase "analyzing"
    
    # CDに統合分析指示送信
    sleep 1
    send_message_internal "cd" "Persona評価完了確認。統合分析フェーズを開始してください。"
}

# ===================================
# 📤 内部メッセージ送信
# ===================================

# 内部メッセージ送信（Hooks用）
send_message_internal() {
    local agent="$1"
    local message="$2"
    
    local target=$(get_agent_target "$agent")
    
    if [[ -n "$target" ]] && check_target "$target"; then
        log_hooks "AUTO_SEND" "$agent ← '$message'"
        send_message "$target" "$message"
    fi
}

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
🤖 BB-Project Agent間メッセージ送信 (Hooks対応版)

使用方法:
  $0 [エージェント名] [メッセージ]
  $0 --list
  $0 --status
  $0 --hooks-status
  $0 --reset-progress

利用可能エージェント:
  md       - Marketing Director (戦略立案・最終選定)
  cd       - Creative Director (チーム統括・品質管理)
  writer1  - 感情訴求型ライター
  writer2  - 論理訴求型ライター
  writer3  - カジュアル型ライター
  persona1 - 共感重視型評価者 (30-50代主婦層)
  persona2 - 合理主義型評価者 (25-45代ビジネス層)
  persona3 - トレンド志向型評価者 (18-30代Z世代)

🎯 Hooks機能:
  - 完了通知自動検出
  - 自動フェーズ移行
  - 状態管理システム
  - 進行状況可視化

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

# Hooks状態表示
show_hooks_status() {
    echo "🎯 Hooks システム状態:"
    echo "======================================"
    echo "  Hooks有効: $HOOKS_ENABLED"
    echo "  自動進行: $AUTO_PROGRESS"
    echo "  進行状況ファイル: $PROGRESS_FILE"
    echo "  Hooksログ: $HOOKS_LOG"
    echo ""
    
    if [ -f "$PROGRESS_FILE" ]; then
        echo "📊 現在の進行状況:"
        echo "------------------------------------"
        grep -E "(phase_current|現在のループ|_status|_completed)" "$PROGRESS_FILE" | head -10
        echo ""
    fi
    
    if [ -f "$HOOKS_LOG" ]; then
        echo "📜 最新Hooksログ (直近5件):"
        echo "------------------------------------"
        tail -5 "$HOOKS_LOG"
    fi
}

# 進行状況リセット
reset_progress() {
    echo "🔄 進行状況をリセット中..."
    
    if [ -f "$PROGRESS_FILE" ]; then
        cp "$PROGRESS_FILE" "${PROGRESS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        echo "📁 バックアップ作成: ${PROGRESS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # 進行状況を初期化
    cat > "$PROGRESS_FILE" << EOF
phase_current: waiting
現在のループ: 1
md_status: waiting
cd_status: waiting
writer1_status: waiting
writer2_status: waiting
writer3_status: waiting
persona1_status: waiting
persona2_status: waiting
persona3_status: waiting
writer1_completed_count: 0
writer2_completed_count: 0
writer3_completed_count: 0
persona1_completed: false
persona2_completed: false
persona3_completed: false
updated_at: "$(date '+%Y-%m-%d %H:%M:%S')"
EOF
    
    echo "✅ 進行状況リセット完了"
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
        echo "💡 './start-all.sh' でシステムを起動してください"
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
        "--hooks-status")
            show_hooks_status
            exit 0
            ;;
        "--reset-progress")
            reset_progress
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
    
    # 🎯 Hooks処理: 完了通知検出
    if [[ "$HOOKS_ENABLED" == true ]]; then
        if detect_completion_pattern "$agent_name" "$message"; then
            log_hooks "PATTERN_DETECTED" "$agent_name: $message"
        fi
    fi
    
    # メッセージ送信
    send_message "$target" "$message"
    
    # ログ記録
    log_send "$agent_name" "$message"
    
    echo "✅ 送信完了: $agent_name に '$message'"
    
    return 0
}

main "$@" 