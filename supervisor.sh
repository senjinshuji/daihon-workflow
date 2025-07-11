#!/bin/bash

# supervisor.sh - エージェントのタスク完了を監視し、プロセス間連携を行う監督役スクリプト

# --- 設定 ---
# タイムアウト時間（秒）。この時間を超えてもファイルが揃わない場合、異常とみなす。
TIMEOUT=1800 # 30分

# --- 関数定義 ---

# 指定されたファイルがすべて存在するまで待機する関数
# 使用法: wait_for_files <ファイルプレフィックス> <ファイル数> <説明>
# 例: wait_for_files "tmp/writer" 3 "ライター"
wait_for_files() {
    local prefix=$1
    local count=$2
    local description=$3
    
    local start_time=$(date +%s)
    echo "🕵️  [監督役] ${description}の完了を監視中（最大${TIMEOUT}秒）..."

    while true; do
        # 完了ファイルの数をチェック
        local done_files=(${prefix}*_done.txt)
        local done_count=${#done_files[@]}

        if [ -f "${prefix}1_done.txt" ] && [ -f "${prefix}2_done.txt" ] && [ -f "${prefix}3_done.txt" ]; then
             echo "✅ [監督役] 全${count}名の${description}の完了を確認しました。"
             break
        fi

        # タイムアウトチェック
        local current_time=$(date +%s)
        local elapsed_time=$((current_time - start_time))
        if [ ${elapsed_time} -ge ${TIMEOUT} ]; then
            echo "❌ [監督役] エラー: ${TIMEOUT}秒以内に${description}の完了を確認できませんでした。プロセスが停止した可能性があります。"
            exit 1
        fi

        # 待機
        sleep 10
    done
}

# クリエイティブディレクター（CD）に通知を送る関数
# 使用法: notify_cd <メッセージ>
notify_cd() {
    local message=$1
    echo "📤 [監督役] CDに通知を送信します: '$message'"
    ./bb-agent-send.sh cd "$message"
}

# --- メインロジック ---

# 引数チェック
if [ -z "$1" ]; then
    echo "❌ [監督役] エラー: ループ番号が引数として指定されていません。（例: ./supervisor.sh loop1）"
    exit 1
fi
CURRENT_LOOP=$1
echo "🔥 [監督役] ループ '${CURRENT_LOOP}' の監視を開始します。"

# 1. 初期化
echo "🧹 [監督役] tmpディレクトリ内の既存の状態ファイルをクリーンアップします..."
rm -f tmp/writer*_done.txt tmp/persona*_done.txt

# 2. ライターフェーズの監視と連携
wait_for_files "tmp/writer" 3 "ライター"
notify_cd "全ライターの制作が完了しました。${CURRENT_LOOP}の評価フェーズを開始してください。"
rm -f tmp/writer*_done.txt
echo "🧹 [監督役] ライターの完了ファイルをクリーンアップしました。"

# 3. ペルソナ評価フェーズの監視と連携
wait_for_files "tmp/persona" 3 "ペルソナ"
notify_cd "全ペルソナの評価が完了しました。${CURRENT_LOOP}の最終報告をMDに提出してください。"
rm -f tmp/persona*_done.txt
echo "🧹 [監督役] ペルソナの完了ファイルをクリーンアップしました。"

# 4. 正常終了
echo "🎉 [監督役] ループ '${CURRENT_LOOP}' の全工程の監視が正常に完了しました。自身を終了します。"
exit 0 