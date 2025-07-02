# 🤖 BB-Project: AI協調型台本作成システム

## 概要
8体のAIエージェントによる協調型広告台本作成システム。Claude Code Communications設計思想に基づく、mdファイルベースの効率的なAI管理プラットフォームです。

## 🎯 システム特徴

### ✨ 新ワークフロー（2024年12月更新）
- **ループベース改善システム**: 継続的品質向上
- **大量生産体制**: Writer1人×5案 = 計15案制作
- **人格mdファイル**: ループごとの詳細人格定義
- **統合分析**: 3ペルソナ×15案の包括的評価
- **ワンクリック初期化**: チェーン式自動セットアップ

### 🔄 改善ループサイクル
```
Loop1 → 評価・分析 → 指示書更新 → Loop2 → 評価・分析 → Loop3...
```

## 🚀 クイックスタート

### 1. 最速起動（推奨）
```bash
./start-all.sh
```
↓
**1コマンドで完了！**

### 2. 段階的起動
```bash
# 環境構築
./setup-bb.sh

# MD起動
./start-md.sh

# MultiAgent起動
./start-multiagent.sh
```

### 3. システム初期化
MDセッションで以下を実行：
```
あなたはMDです。指示書に従って
```
↓
**全8エージェント自動初期化完了！**

### 4. プロジェクト開始
```
プロジェクト名『[プロジェクト名]』でCSVデータを分析してloop1を開始してください
```

## 🏗️ システム構成

### エージェント構成
```
bb-md セッション:
├── MD (Marketing Director)          # 戦略立案・分析・指示書作成

bb-multiagent セッション:
├── CD (Creative Director)           # 人格形成・制作統括・評価統合
├── Writer1 (感情訴求特化)          # 5案制作
├── Writer2 (論理訴求特化)          # 5案制作
├── Writer3 (カジュアル特化)        # 5案制作
├── Persona1 (30-50代主婦層)       # 15案評価
├── Persona2 (25-45代ビジネス層)   # 15案評価
└── Persona3 (18-30代Z世代)        # 15案評価
```

### ワークフロー詳細

#### 🎯 Phase 1: 戦略立案フェーズ（MD担当）
1. **商品分析**: CSVデータ分析 → `product_analysis.md`
2. **ターゲット分析**: 詳細顧客像策定 → `target_analysis.md`
3. **制作指示書**: ライター向け方針 → `copywriter_instructions.md`
4. **評価基準**: ペルソナ評価軸 → `persona_evaluation_criteria.md`
5. **戦略策定**: 総合方針確定 → `creative_strategy.md`

#### 🎭 Phase 2: 人格形成フェーズ（CD担当）
1. **Writer人格定義**: 各ライターの詳細人格 → `writer[1-3]_loop[N].md`
2. **Persona人格定義**: 各評価者の詳細人格 → `persona[1-3]_loop[N].md`

#### ✍️ Phase 3: 大量制作フェーズ（Writer1-3担当）
- **Writer1**: 感情訴求型5案 → `writer1_台本[1-5]_loop[N].md`
- **Writer2**: 論理訴求型5案 → `writer2_台本[1-5]_loop[N].md`
- **Writer3**: カジュアル型5案 → `writer3_台本[1-5]_loop[N].md`
- **合計**: **15案制作**

#### 📊 Phase 4: 評価フェーズ（Persona1-3担当）
- **Persona1**: 主婦視点で15案評価 → `persona1_evaluation_loop[N].md`
- **Persona2**: ビジネス視点で15案評価 → `persona2_evaluation_loop[N].md`
- **Persona3**: Z世代視点で15案評価 → `persona3_evaluation_loop[N].md`

#### 📈 Phase 5: 統合分析フェーズ（CD担当）
- **統合分析**: 45評価の包括分析 → `integrated_analysis_loop[N].md`
- **改善提案**: 次ループ向け具体的提案

#### 🔄 Phase 6: ループ改善フェーズ（MD担当）
- **指示書更新**: 前回評価を反映した制作方針更新
- **評価基準調整**: より精緻な評価軸への進化
- **戦略修正**: 成功要因を組み込んだ戦略調整

## 📁 ファイル構造

```
projects/[プロジェクト名]/
├── 📊 入力データ
│   └── *.csv                           # CSVデータファイル
├── 📋 戦略ファイル（MD作成）
│   ├── product_analysis.md             # 商品分析結果
│   ├── target_analysis.md              # ターゲット分析詳細書
│   ├── copywriter_instructions.md      # ライター向け指示書
│   ├── persona_evaluation_criteria.md  # ペルソナ評価基準
│   └── creative_strategy.md            # 総合クリエイティブ戦略
├── 📁 Loop1成果物
│   ├── 👥 人格定義ファイル
│   │   ├── writer1_loop1.md           # Writer1人格定義
│   │   ├── writer2_loop1.md           # Writer2人格定義
│   │   ├── writer3_loop1.md           # Writer3人格定義
│   │   ├── persona1_loop1.md          # Persona1人格定義
│   │   ├── persona2_loop1.md          # Persona2人格定義
│   │   └── persona3_loop1.md          # Persona3人格定義
│   ├── 📝 台本ファイル（15案）
│   │   ├── writer1_台本1_loop1.md     # Writer1の5案
│   │   ├── writer1_台本2_loop1.md
│   │   ├── writer1_台本3_loop1.md
│   │   ├── writer1_台本4_loop1.md
│   │   ├── writer1_台本5_loop1.md
│   │   ├── writer2_台本1_loop1.md     # Writer2の5案
│   │   └── ...                        # 全15案
│   ├── 📊 評価ファイル
│   │   ├── persona1_evaluation_loop1.md
│   │   ├── persona2_evaluation_loop1.md
│   │   └── persona3_evaluation_loop1.md
│   └── 📈 統合分析
│       └── integrated_analysis_loop1.md
├── 📁 Loop2成果物
│   └── ...                            # 同様の構造
└── 📁 Loop3成果物
    └── ...                            # 継続的改善
```

## 🛠️ コマンド一覧

### 基本操作
```bash
# 全システム一括起動
./start-all.sh

# MD専用起動
./start-md.sh

# MultiAgent一括起動
./start-multiagent.sh

# 環境セットアップ
./setup-bb.sh

# エージェント間通信
./bb-agent-send.sh [宛先] "[メッセージ]"

# ステータス確認
./bb-agent-send.sh --status

# エージェント一覧
./bb-agent-send.sh --list
```

### プロジェクト操作
```bash
# 新プロジェクト開始
cd projects
mkdir [プロジェクト名]
cd [プロジェクト名]
# CSVファイルを配置

# MD側でプロジェクト開始宣言
プロジェクト名『[プロジェクト名]』でCSVデータを分析してloop1を開始してください
```

## 🎯 活用例

### 小規模案件（Loop1のみ）
```
CSV分析 → 15案制作 → 3視点評価 → 最適案選定
```

### 中規模案件（Loop1-2）
```
Loop1（基本案） → 評価分析 → 指示改善 → Loop2（改善案） → 最終選定
```

### 大規模案件（Loop1-3+）
```
Loop1 → Loop2 → Loop3 → ... → 継続的品質向上 → 最適解到達
```

## 🔧 システム要件

### 必須環境
- **tmux**: セッション管理
- **Claude CLI**: エージェント実行
- **bash**: スクリプト実行環境

### 推奨環境
- **macOS/Linux**: ネイティブサポート
- **ターミナル**: 複数ペイン対応
- **VSCode**: mdファイル編集用

## 📊 性能指標

### 制作能力
- **同時制作**: 15案並列生産
- **評価精度**: 3視点×100点満点
- **改善サイクル**: ループごとの継続向上

### 効率性
- **初期化**: 1コマンド（従来8回 → 1回）
- **起動時間**: 約30秒で全エージェント稼働
- **管理性**: mdファイルベースの透明性

## 🎉 主な改善点（2024年12月）

### Before（旧システム）
- 複雑なPythonベースシステム
- 手動8回初期化
- 3本台本制作（計9本）
- 単発評価・改善なし

### After（新システム）
- シンプルなmdファイルベース
- ワンクリック初期化
- 5本台本制作（計15本）
- ループベース継続改善

## 📝 ログ・履歴管理

```bash
# ログファイル確認
tail -f logs/send_log.txt

# プロジェクト履歴
ls projects/*/loop*/
```

## 🚨 トラブルシューティング

### よくある問題
1. **tmuxセッションエラー**: `./setup-bb.sh` で再構築
2. **エージェント応答なし**: セッション再起動
3. **ファイル保存エラー**: パーミッション確認

### サポート
- 設定ファイル: `instructions/*.md`
- ログファイル: `logs/send_log.txt`
- エージェント状態: `./bb-agent-send.sh --status`

---

## 🎯 次のステップ

1. **クイックスタート実行**: `./start-all.sh`
2. **テストプロジェクト**: 小規模CSVで動作確認
3. **本格運用**: 実案件でループシステム活用
4. **カスタマイズ**: 業界特化型の人格調整

**BB-Project**で、AI協調による革新的な台本作成を体験してください！