#!/bin/bash

# tmuxペインにコマンドを送信するスクリプト

SESSION="bb-multiagent"

# 引数チェック
if [ "$#" -ne 2 ]; then
  echo "使用方法: $0 <ターゲットペイン名> <送信するコマンド>"
  echo "ターゲット: MD/md, CD/cd, Writer1/writer1, Writer2/writer2, Writer3/writer3, Persona1/persona1, Persona2/persona2, Persona3/persona3"
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
  "md")
    # MDは別セッションのため、ここで直接処理
    tmux send-keys -t "bb-md:0.0" "$COMMAND" Enter
    exit 0
    ;;
  "CD") PANE_INDEX=0 ;;
  "cd") PANE_INDEX=0 ;;
  "Writer1") PANE_INDEX=1 ;;
  "writer1") PANE_INDEX=1 ;;
  "Writer2") PANE_INDEX=2 ;;
  "writer2") PANE_INDEX=2 ;;
  "Writer3") PANE_INDEX=3 ;;
  "writer3") PANE_INDEX=3 ;;
  "Persona1") PANE_INDEX=4 ;;
  "persona1") PANE_INDEX=4 ;;
  "Persona2") PANE_INDEX=5 ;;
  "persona2") PANE_INDEX=5 ;;
  "Persona3") PANE_INDEX=6 ;;
  "persona3") PANE_INDEX=6 ;;
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