# BB-Agent: AI Creative Agent System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 概要 (Overview)

BB-Agent は、広告台本作成のための革新的なAIエージェントシステムです。8つの専門エージェントが協調して、ペルソナ分析から台本制作、品質評価まで自動化します。

BB-Agent is an innovative AI agent system for advertising script creation. Eight specialized agents collaborate to automate everything from persona analysis to script production and quality evaluation.

## ✨ 主な機能 (Key Features)

### 🎯 8エージェント協調システム
- **MD (Marketing Director)**: 戦略立案・ペルソナ生成・最終選定
- **CD (Creative Director)**: 制作指示・品質管理・チーム統括  
- **Writer1-3**: 台本制作（感情派・論理派・カジュアル派）
- **Persona1-3**: 多角的評価・フィードバック

### 🚀 自動化機能
- **ハイブリッド自動化**: MD手動 + 7エージェント自動実行
- **ファイルベース通信**: メッセージ交換システム
- **自動台本保存**: プロジェクトディレクトリへの自動保存
- **Loop改善システム**: 継続的品質向上

### 📊 データドリブン戦略
- **CSV分析**: 商品・ターゲット・競合分析
- **ペルソナ自動生成**: AIベースペルソナ創出
- **評価システム**: 100点満点評価・改善提案
- **トップ5レポート**: 優秀台本自動選出

## 🛠️ 技術スタック (Tech Stack)

- **Python 3.8+**: コアエンジン
- **Claude AI**: 各エージェントの知能
- **tmux**: セッション管理
- **Bash**: スクリプト自動化
- **Markdown**: レポート生成

## 📦 インストール (Installation)

```bash
# リポジトリクローン
git clone https://github.com/senjinshuji/bb-agent.git
cd bb-agent

# 依存関係インストール
pip install -r requirements.txt

# Claude CLI設定
# https://docs.anthropic.com/claude/docs/cli-installation

# tmuxインストール（macOS）
brew install tmux
```

## 🚀 使用方法 (Usage)

### 基本起動
```bash
# 全自動システム起動（推奨）
./start-bb-automated.sh

# シンプル起動
./start-bb-simple.sh

# 安定版起動
./start-bb-stable.sh
```

### プロジェクト設定
1. `projects/[PROJECT_NAME]/` にCSVファイル配置
2. MD画面でプロジェクト開始
3. 自動でWriter・Persona エージェントが実行
4. 結果は `projects/[PROJECT_NAME]/results/` に保存

### メッセージ送信
```bash
# エージェント間通信
./agent-send.sh [相手] "[メッセージ]"

# 例: CDにメッセージ送信
./agent-send.sh cd "台本制作開始してください"
```

## 📁 ディレクトリ構造 (Directory Structure)

```
bb-agent/
├── agents/                 # エージェントプログラム
│   ├── md_agent.py         # マーケティングディレクター
│   ├── cd_agent_runner.py  # クリエイティブディレクター
│   ├── writer_agent_runner.py # ライターエージェント
│   ├── persona_agent_runner.py # ペルソナエージェント
│   └── message_handler.py  # メッセージハンドリング
├── projects/               # プロジェクトデータ
│   └── [PROJECT_NAME]/
│       ├── [CSV_FILE]      # 商品データ
│       ├── results/        # 台本・評価結果
│       └── md_report/      # 戦略レポート
├── start-bb-*.sh          # 起動スクリプト
├── agent-send.sh           # メッセージ送信
└── CLAUDE.md              # エージェント指示書
```

## 🔄 ワークフロー (Workflow)

1. **MD**: CSV分析 → ペルソナ生成 → 戦略ブリーフ作成
2. **CD**: 戦略受信 → Writer指示 → 品質管理
3. **Writer1-3**: 台本制作（各3本） → 自動保存
4. **Persona1-3**: 台本評価 → フィードバック
5. **CD**: 評価集約 → 改善指示
6. **MD**: 最終選定 → トップ5レポート

## 📈 Loop改善システム (Loop Improvement System)

### Loop2改善対応
- **Writer1**: 母娘絆進化版・友人絆強化版・恋人絆新規版
- **Writer2**: 感情データ融合版・医療温かみ版・論理感情統合版  
- **Writer3**: Z世代トレンド版・SNS映え強化版・コミュニティ版

### 自動改善フロー
1. CD改善指示 → Writer自動検知
2. Loop専用台本制作 → 適切命名保存
3. 完了報告 → 次Loop準備

## 🎯 エージェント特徴 (Agent Characteristics)

| エージェント | 専門性 | 特徴 |
|------------|--------|------|
| **Writer1** | 感情派 | ストーリー性・共感重視 |
| **Writer2** | 論理派 | データ・効果効能重視 |  
| **Writer3** | カジュアル派 | 親しみやすさ・テンポ重視 |
| **Persona1** | 実用主義 | コスパ・効率性重視 |
| **Persona2** | 感情重視 | 共感・安心感重視 |
| **Persona3** | トレンド志向 | 話題性・SNS映え重視 |

## 📊 成果事例 (Success Examples)

- **95点台本達成**: 感情と論理の完璧バランス
- **平均90点超え**: 継続的品質向上システム
- **3倍効率化**: 手動制作比での時間短縮
- **一貫性確保**: エージェント間協調による品質統一

## 🤝 コントリビューション (Contributing)

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 ライセンス (License)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 謝辞 (Acknowledgments)

- [Claude AI](https://www.anthropic.com/claude) - AI エージェントエンジン
- [tmux](https://github.com/tmux/tmux) - セッション管理
- オープンソースコミュニティの皆様

## 📞 サポート (Support)

- **Issues**: [GitHub Issues](https://github.com/senjinshuji/bb-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/senjinshuji/bb-agent/discussions)

---

**BB-Agent** - Revolutionizing AI-Powered Creative Content Generation