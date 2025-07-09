#!/bin/bash

# tmuxペインにコマンドを送信するスクリプト

SESSION="bb-multiagent"

# 引数チェック
if [ "$#" -ne 2 ]; then
  echo "使用方法: $0 <ターゲットペイン名> <送信するコマンド>"
  echo "ターゲット: MD, CD, Writer1, Writer2, Writer3, Persona1, Persona2, Persona3"
  exit 1
fi

TARGET_NAME=$1
COMMAND=$2
PANE_INDEX=-1

# ターゲット名からペイン番号を特定
case "$TARGET_NAME" in
  "MD")
    # MDは別セッションのため、ここで直接処理
    tmux send-keys -t "bb-md:0.0" "$COMMAND" Enter
    exit 0
    ;;
  "CD") PANE_INDEX=0 ;;
  "Writer1") PANE_INDEX=2 ;;
  "Writer2") PANE_INDEX=5 ;;
  "Writer3") PANE_INDEX=6 ;;
  "Persona1") PANE_INDEX=1 ;;
  "Persona2") PANE_INDEX=3 ;;
  "Persona3") PANE_INDEX=4 ;;
  *)
    echo "エラー: 不明なターゲットペイン名です: $TARGET_NAME"
    exit 1
    ;;
esac

# コマンド送信
TARGET_PANE="$SESSION:0.$PANE_INDEX"

# Claude Codeのプロンプトを一度クリア
tmux send-keys -t "$TARGET_PANE" C-c
sleep 0.3

# メッセージ送信
tmux send-keys -t "$TARGET_PANE" "$COMMAND"
sleep 0.1

# エンター押下
tmux send-keys -t "$TARGET_PANE" C-m
sleep 0.5

echo "コマンドをペイン $TARGET_NAME (PANE: $TARGET_PANE) に送信しました。" 