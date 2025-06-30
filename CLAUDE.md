# BB-Project 仕様書

## 🎯 システム概要
BB-Projectは、8体のAIエージェントが協調して動画広告台本を作成するシステムです。

## 👥 エージェント構成（8体）

### 1. **MD (Marketing Director)** - 1体
- **役割**: 戦略立案、ペルソナ生成、最終選定
- **責任**: 
  - CSVデータ分析
  - 戦略ブリーフ作成
  - 全エージェントへの役割宣言自動配信
  - 最終台本選定（80点以上から選定）
- **注意**: 台本は作成しない（Writerの仕事）

### 2. **CD (Creative Director)** - 1体
- **役割**: チーム管理、品質管理、改善指示
- **責任**:
  - MDからの戦略ブリーフ受信
  - Writer1-3への台本制作指示
  - Persona1-3への評価依頼
  - ループごとの改善指示
- **注意**: 台本は作成しない（Writerの仕事）

### 3. **Writer1-3** - 3体
- **Writer1（感情訴求型）**: 感情に訴える台本を3本作成
- **Writer2（論理訴求型）**: データと論理を重視した台本を3本作成
- **Writer3（カジュアル型）**: 親しみやすくテンポの良い台本を3本作成

### 4. **Persona1-3** - 3体
- **Persona1（共感重視型）**: 30-50代主婦層の視点で100点満点評価
- **Persona2（合理主義型）**: 25-45代ビジネスパーソンの視点で100点満点評価
- **Persona3（トレンド志向型）**: 18-30代Z世代の視点で100点満点評価

## 🔄 処理フロー

### 1. **初期化フェーズ**
1. MDが役割宣言を受信
2. MDが全エージェント（CD, Writer1-3, Persona1-3）に役割宣言を自動送信
3. MDがCSVファイルを分析
4. MDが戦略ブリーフとペルソナ設定を作成
5. MDがCDに戦略ブリーフを送信

### 2. **制作ループ（最大3回）**
1. CDがWriter1-3に台本制作を指示
2. 各Writerが3本ずつ台本を作成（合計9本）
3. CDがPersona1-3に評価を依頼
4. 各Personaが100点満点で評価
5. 平均80点以上の台本を承認リストに追加
6. 80点未満の場合、CDが改善指示を出して次のループへ

### 3. **最終選定フェーズ**
1. 承認台本（80点以上）から上位10本を選定
2. MDが最終的に1本を選定
3. 選定結果と理由を記録
4. 🆕**優秀台本5本の詳細レポート自動生成**

## 📁 ファイル構成
```
bb-project/
├── README.md                  # システム説明
├── CLAUDE.md                 # この仕様書
├── agent-send.sh             # エージェント間通信（シンボリックリンク）
├── agents/
│   ├── md_agent.py           # MDエージェント
│   ├── cd_agent.py           # CDエージェント
│   ├── writer_agents.py      # Writer1-3基底クラス
│   ├── persona_agents.py     # Persona1-3基底クラス
│   ├── message_handler.py    # 🤖メッセージ処理基底クラス（NEW）
│   ├── cd_agent_runner.py    # 🤖CD自動化実行（NEW）
│   ├── writer_agent_runner.py # 🤖Writer自動化実行（NEW）
│   └── persona_agent_runner.py # 🤖Persona自動化実行（NEW）
├── messages/                 # 🤖自動化通信ディレクトリ（NEW）
│   ├── cd_inbox.txt         # CD受信メッセージ
│   ├── writer1_inbox.txt    # Writer1受信メッセージ
│   ├── writer2_inbox.txt    # Writer2受信メッセージ
│   ├── writer3_inbox.txt    # Writer3受信メッセージ
│   ├── persona1_inbox.txt   # Persona1受信メッセージ
│   ├── persona2_inbox.txt   # Persona2受信メッセージ
│   └── persona3_inbox.txt   # Persona3受信メッセージ
├── projects/
│   ├── lactron/              # プロジェクトフォルダ例
│   │   ├── *.csv            # 入力CSVファイル
│   │   └── results/         # 成果物フォルダ（自動生成）
│   └── DIO/                 # 別プロジェクト例
├── start-bb-automated.sh     # 🤖完全自動化起動（NEW・推奨）
├── start-bb-stable.sh        # 🧑‍💼手動版（tmux永続化対応）
├── start-bb-simple.sh        # シンプル起動
├── start-bb-smart.sh         # スマート起動
└── start-bb-instant.sh       # 即座起動（認証済み用）
```

## 🚀 起動方法

### 🤖 推奨：完全自動化版（NEW!）
**Writer1,2の台本未提出問題を解決した最新版**
```bash
# 1. プロジェクトディレクトリに移動
cd /Users/shjkt/Downloads/claude_code_folder/Claude-Code-Communication/bb-project

# 2. 自動化システム起動
./start-bb-automated.sh

# 3. 3つのターミナルウィンドウを開く
# ウィンドウ1: tmux attach -t bb-md      (MD - Human Interface)
# ウィンドウ2: tmux attach -t bb-cd      (CD - Automated)
# ウィンドウ3: tmux attach -t bb-others  (Writers & Personas - All Automated)

# 4. MDウィンドウで操作（人間が操作するのはMDのみ）
# 役割宣言: 私はMD（マーケティングディレクター）です。戦略立案とペルソナ生成、最終選定を担当します。台本は作成しません。
# プロジェクト選択: cd projects/lactron （またはDIO）
# システム起動: python3 ../../agents/md_agent.py
```

### 🔄 自動化システムフロー
1. **MDのみ人間操作** - 戦略立案・最終選定
2. **CD〜Persona3まで完全自動** - 台本制作・評価・改善
3. **承認台本80点以上を自動選定**
4. **最終結果をMDに自動報告**

### 🧑‍💼 手動版：安定版起動（tmuxが消えない）
```bash
# 1. プロジェクトディレクトリに移動
cd /Users/shjkt/Downloads/claude_code_folder/Claude-Code-Communication/bb-project

# 2. 安定版起動スクリプト実行
./start-bb-stable.sh

# 3. 3つのターミナルウィンドウを開く
# ウィンドウ1: tmux attach -t bb-md
# ウィンドウ2: tmux attach -t bb-cd
# ウィンドウ3: tmux attach -t bb-others

# 4. MDウィンドウで操作
# 役割宣言: 私はMD（マーケティングディレクター）です。戦略立案とペルソナ生成、最終選定を担当します。台本は作成しません。
# プロジェクト選択: cd projects/lactron （またはDIO）
# システム起動: python3 ../../agents/md_agent.py
```

### その他の起動方法
- `./start-bb-automated.sh`: **🤖完全自動化版（推奨）**
- `./start-bb-stable.sh`: 🧑‍💼手動版（tmux永続化対応）
- `./start-bb-simple.sh`: シンプル版（文字化け対策）
- `./start-bb-smart.sh`: スマート版（詳細表示）
- `./start-bb-instant.sh`: 即座起動（認証済みの場合）

## 🛡️ tmux安定性対策
安定版（start-bb-stable.sh）には以下の対策が含まれています：
- **remain-on-exit**: プロセス終了後もペインを維持
- **bashフォールバック**: Claude CLI終了後もbashシェルに戻る
- **エラー保護**: `|| bash`でエラー時も画面を維持

## 🤖 自動化システム構成（Writer1,2未提出問題の解決）

### 問題の根本原因
- **従来**: 全エージェントがClaude CLI（人間の手動操作が必要）
- **問題**: Writer1,2が台本を作成してもCDに自動提出できない

### 解決策：ハイブリッド自動化
- **MD**: 人間操作（Claude CLI） - 戦略立案・最終判断
- **CD**: 完全自動化（Python Agent） - 調整・管理
- **Writer1-3**: 完全自動化（Python Agent） - 台本制作
- **Persona1-3**: 完全自動化（Python Agent） - 台本評価

### 自動化エージェントの特徴
1. **メッセージ受信**: ファイルベース通信で自動受信
2. **処理実行**: 指示に応じて自動実行
3. **結果送信**: 完了後に自動報告送信
4. **24時間動作**: 人間の介入不要
5. **🆕自動保存**: 台本をCSVと同じディレクトリに自動保存

## 💬 通信仕様

### エージェント間通信
- **通信ツール**: `agent-send.sh`（親ディレクトリへのシンボリックリンク）
- **拡張機能**: BB-projectエージェント向けファイルベース通信追加
- **通信方向**: 
  - MD → CD（戦略ブリーフ）
  - CD → Writer1-3（制作指示）
  - Writer1-3 → CD（台本提出）**← 自動化により解決**
  - CD → Persona1-3（評価依頼）
  - Persona1-3 → CD（評価結果）**← 自動化により解決**
  - CD → MD（ループ結果報告）

### 役割宣言の自動配信
MDが`md_agent.py`を実行すると、自動的に以下が実行されます：
1. 全エージェントに役割宣言メッセージを送信
2. 各エージェントが自分の役割を認識
3. 待機状態に入る

### ファイルベース通信（自動化機能）
各自動化エージェントは以下のメッセージファイルを監視：
- `messages/cd_inbox.txt` - CD用
- `messages/writer1_inbox.txt` - Writer1用
- `messages/writer2_inbox.txt` - Writer2用
- `messages/writer3_inbox.txt` - Writer3用
- `messages/persona1_inbox.txt` - Persona1用
- `messages/persona2_inbox.txt` - Persona2用
- `messages/persona3_inbox.txt` - Persona3用

## 🆕 台本自動保存機能

### 保存仕様
- **保存場所**: CSVファイルと同じプロジェクトディレクトリ
- **ファイル名**: `{writer_id}_台本{番号}_{アプローチ}_loop{ループ数}_{タイムスタンプ}.md`
- **例**: `writer1_台本1_基本アプローチ_loop1_20241230_143022.md`

### 保存内容
- Writer情報（ID、スタイル、ターゲット）
- 制作情報（Loop数、制作日時）
- 台本内容（フル内容）
- BB-Project自動生成マーク

### 自動化レベル
1. **CDからの指示**: 保存場所と形式を自動指定
2. **Writer実行**: 台本制作完了後に自動保存
3. **プロジェクト連携**: MDから現在のプロジェクト情報を自動伝達

## 🏆 優秀台本5本レポート機能

### 自動生成内容
- **評価結果サマリー**: 順位・Writer・スコア・ペルソナ評価の表
- **各台本詳細**: 完全な台本内容とペルソナ別評価
- **成功要因分析**: スコア別の特徴分析（95点以上/90点以上/80点以上）
- **総合分析**: 品質レベル分析・Writer別成果・成功パターン
- **最終評価**: 5段階評価（⭐⭐⭐⭐⭐ 圧倒的成功 〜 ⭐⭐⭐ 成功）

### 生成ファイル
- **ファイル名**: `top5_excellent_scripts_report.md`
- **保存場所**: `results/` ディレクトリ
- **形式**: Markdown形式の読みやすいレポート

### 実用価値
- **クライアント提出用**: そのまま提出可能な高品質レポート
- **分析・改善用**: 成功パターンの把握と今後の改善指針
- **品質保証**: 全台本の内容と評価根拠を完全記録

## 📊 評価基準

### 100点満点の評価項目
- **フックの強さ**: 冒頭3秒の引き込み力
- **論理的な流れ**: ストーリーの一貫性
- **感情的な共感**: ターゲットへの訴求力
- **購買動機**: 行動喚起の強さ
- **信頼性**: ブランド・商品の信頼感

### 承認基準
- **80点以上**: 承認リストに追加
- **80点未満**: 改善指示を出して再制作

## 🎯 成功指標
- **目標**: 平均90点以上の台本を3本以上作成
- **最高目標**: 95点以上の台本を1本作成

## ⚡ 動的改善メカニズム
CDが各ループで以下を実行：
1. 前回の評価結果を分析
2. Writer向けプロンプトを累積的に改善
3. 具体的な改善指示を追加（ファイル書き換えではなく追加指示）

## 🎬 tmuxウィンドウ構成
- **bb-md**: MDエージェント専用
- **bb-cd**: CDエージェント専用
- **bb-others**: 6分割画面
  ```
  ┌─────────┬─────────┬─────────┐
  │Writer1  │Writer2  │Writer3  │
  ├─────────┼─────────┼─────────┤
  │Persona1 │Persona2 │Persona3 │
  └─────────┴─────────┴─────────┘
  ```

## 🚫 禁止事項
- **テストエラーや型エラー解消のための条件緩和**
- **テストのスキップや不適切なモック化**
- **出力やレスポンスのハードコード**
- **エラーメッセージの無視や隠蔽**
- **一時的な修正による問題の先送り**

品質を最優先とし、根本的な解決を図ること。