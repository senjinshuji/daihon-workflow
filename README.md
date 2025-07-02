# 🎯 BB-Project: MDファイルベース・マルチエージェント広告台本作成システム

Claude Code Communicationsを参考にした、シンプルで強力なMDファイル管理ベースの8体AIエージェント協調システム

## 🎯 システム概要

**MD → CD → Writers & Personas** の階層型指示システムで高品質な広告台本を自動作成

### 👥 エージェント構成

```
📊 bb-md セッション (1ペイン)
└── MD: Marketing Director (戦略立案・最終選定責任者)

📊 bb-multiagent セッション (7ペイン)  
├── CD: Creative Director (チーム統括・品質管理)
├── Writer1: 感情訴求型 (3本台本制作)
├── Writer2: 論理訴求型 (3本台本制作)  
├── Writer3: カジュアル型 (3本台本制作)
├── Persona1: 共感重視型評価者 (30-50代主婦層視点)
├── Persona2: 合理主義型評価者 (25-45代ビジネス層視点)
└── Persona3: トレンド志向型評価者 (18-30代Z世代視点)
```

## 🚀 クイックスタート（超簡単版）

### 最速起動（1コマンド）

```bash
./start-all.sh
```

これだけで全エージェントの環境構築 + Claude CLI起動まで完了！

### 分割起動（3コマンド）

```bash
# 1. 環境構築
./setup-bb.sh

# 2. MD起動
./start-md.sh

# 3. MultiAgent一括起動  
./start-multiagent.sh
```

## 🎬 使用手順

### 1. セッションアタッチ

```bash
# MDセッション（別ターミナル）
tmux attach -t bb-md

# MultiAgentセッション（別ターミナル）
tmux attach -t bb-multiagent
```

### 2. ワンクリック全エージェント初期化 🆕

**MDだけで全システム初期化！**

MDエージェントで Claude CLI認証完了後、たった1回の入力で全エージェントが自動初期化：

```
あなたはMDです。指示書に従って
```

**自動初期化チェーン:**
1. **MD**: 宣言と同時にCDに初期化指示を送信
2. **CD**: Writer1-3、Persona1-3に初期化指示を一括送信
3. **Writer1-3 & Persona1-3**: 各々が自動初期化完了
4. **CD**: MDに全員初期化完了を報告

もう8回の手動入力は不要！MDの1回だけで完了します。

### 3. プロジェクト実行

MDエージェントでプロジェクトを開始：
```
プロジェクト名「XXXX」でCSVデータを分析して台本作成を開始してください
```

## 📜 エージェント指示書

各エージェントの詳細な役割と実行手順：

- **MD**: `instructions/md.md` - 戦略立案・ペルソナ分析・最終選定
- **CD**: `instructions/cd.md` - チーム統括・品質管理・進行管理
- **Writer1**: `instructions/writer1.md` - 感情訴求型台本作成（3本）
- **Writer2**: `instructions/writer2.md` - 論理訴求型台本作成（3本）
- **Writer3**: `instructions/writer3.md` - カジュアル型台本作成（3本）
- **Persona1**: `instructions/persona1.md` - 共感重視型評価（30-50代主婦層）
- **Persona2**: `instructions/persona2.md` - 合理主義型評価（25-45代ビジネス層）
- **Persona3**: `instructions/persona3.md` - トレンド志向型評価（18-30代Z世代）

**システム構造**: `CLAUDE.md` で全体仕様を確認

## 🎯 期待される動作フロー

```
🔄 初期化フェーズ:
1. MD: 「あなたはMDです。指示書に従って」→ 自動初期化チェーン開始
2. CD: Writer1-3、Persona1-3を一括初期化 → MD完了報告

🎯 実行フェーズ:
1. MD: CSV分析 → 戦略ブリーフ → CDに指示送信
2. CD: Writer1-3に台本制作指示 → 完了確認 → Persona1-3に評価指示  
3. Writer1-3: 各3本台本制作 → 完了ファイル作成
4. CD: 評価集約 → 承認台本選定 → MDに報告
5. MD: 最終台本選定 → プロジェクト完了
```

## 🔧 エージェント間通信

### bb-agent-send.sh を使った送信

```bash
# 基本送信
./bb-agent-send.sh [エージェント名] [メッセージ]

# 例
./bb-agent-send.sh cd "Writer1-3に台本制作を開始してください"
./bb-agent-send.sh md "全台本評価が完了しました"

# エージェント一覧確認
./bb-agent-send.sh --list

# 状況確認
./bb-agent-send.sh --status
```

## 🧪 確認・デバッグ

### ログ確認

```bash
# 送信ログ確認
cat logs/send_log.txt

# 特定エージェントのログ
grep "writer1" logs/bb-project/send_log.txt

# 完了ファイル確認
ls -la ./tmp/writer*_done.txt ./tmp/persona*_done.txt
```

### セッション状態確認

```bash
# セッション一覧
tmux list-sessions

# ペイン一覧
tmux list-panes -t bb-md
tmux list-panes -t bb-multiagent
```

## 🔄 環境リセット

```bash
# セッション削除
tmux kill-session -t bb-md
tmux kill-session -t bb-multiagent

# 完了ファイル削除
rm -f ./tmp/writer*_done.txt ./tmp/persona*_done.txt

# 再構築（自動クリア付き）
./setup-bb.sh
```

## 📁 プロジェクト構造

```
bb-project/
├── setup-bb.sh              # 環境構築（tmuxセッション作成）
├── start-all.sh             # 全エージェント一括起動
├── start-md.sh              # MD専用起動
├── start-multiagent.sh      # MultiAgent一括起動
├── bb-agent-send.sh         # エージェント間通信
├── instructions/            # エージェント指示書
│   ├── md.md
│   ├── cd.md
│   ├── writer1.md
│   ├── writer2.md
│   ├── writer3.md
│   ├── persona1.md
│   ├── persona2.md
│   └── persona3.md
├── projects/                # プロジェクト成果物
├── logs/                    # 通信ログ
└── tmp/                     # 作業ファイル
```

## 🎯 特徴

- **ワンクリック初期化**: MDの1回宣言で全8エージェント自動初期化 🆕
- **シンプルな起動**: 1コマンドで全環境構築 + Claude CLI起動
- **mdファイルベース**: 複雑なPythonコード不要、純粋なmdファイル管理
- **Claude Code Communicationsライク**: 実証済みのシンプル設計を採用
- **自動化フロー**: エージェント間の協調による高品質な台本作成
- **柔軟な評価**: 3つの異なる視点での多角的評価

---

🚀 **Claude Code Communicationsの理念を受け継いだ、ワンクリック初期化対応のシンプルで強力な広告台本作成システム！** 🤖✨