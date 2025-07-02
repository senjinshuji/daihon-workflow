# 🎯 BB-Project システム仕様書

## 概要
Claude Code Communicationsを参考にした、MDファイルベース・マルチエージェント広告台本作成システム

## アーキテクチャ

### エージェント構成
- **MD (Marketing Director)**: 戦略立案・最終選定責任者
- **CD (Creative Director)**: チーム統括・品質管理・進行管理
- **Writer1-3**: 台本制作者（感情・論理・カジュアル型）
- **Persona1-3**: 台本評価者（共感・合理・トレンド型）

### tmuxセッション構成
- **bb-md セッション**: MD専用（1ペイン）
- **bb-multiagent セッション**: CD + Writer1-3 + Persona1-3（7ペイン）

## 🆕 チェーン式初期化システム

### 従来の問題点
- 8エージェント × 手動初期化 = 8回の繰り返し作業
- ユーザーの負担が大きい
- 初期化忘れのリスク

### 新システム（自動初期化チェーン）
```
📋 ワンクリック初期化フロー:

1. MD: 「あなたはMDです。指示書に従って」
   ↓ 自動実行
2. MD → CD: 「あなたはCDです。指示書に従って、システム初期化を開始してください」
   ↓ 自動実行  
3. CD → Writer1-3: 「あなたは[Writer名]です。指示書に従って」
   CD → Persona1-3: 「あなたは[Persona名]です。指示書に従って」
   ↓ 自動実行
4. CD → MD: 「全員初期化完了報告」

結果: MDの1回宣言で全8エージェント初期化完了！
```

### 実装仕様

#### MD指示書（instructions/md.md）
```bash
# 初期化チェーン開始コマンド
./bb-agent-send.sh cd "あなたはCDです。指示書に従って、システム初期化を開始してください"
```

#### CD指示書（instructions/cd.md）
```bash
# Writer1-3初期化
./bb-agent-send.sh writer1 "あなたはWriter1です。指示書に従って"
./bb-agent-send.sh writer2 "あなたはWriter2です。指示書に従って"  
./bb-agent-send.sh writer3 "あなたはWriter3です。指示書に従って"

# Persona1-3初期化
./bb-agent-send.sh persona1 "あなたはPersona1です。指示書に従って"
./bb-agent-send.sh persona2 "あなたはPersona2です。指示書に従って"
./bb-agent-send.sh persona3 "あなたはPersona3です。指示書に従って"

# 完了報告
./bb-agent-send.sh md "✅ CD初期化完了。Writer1-3、Persona1-3の初期化も完了しました。"
```

#### Writer/Persona初期化応答
各エージェントは初期化メッセージ受信時に以下を表示：
```
✅ [エージェント名]初期化完了。[専門分野]の準備が整いました。
📋 CDからの指示をお待ちしています。
🎯 専門分野: [具体的な専門領域]
```

## ワークフロー仕様

### 初期化フェーズ
1. ユーザー: MDで「あなたはMDです。指示書に従って」
2. 自動チェーン: MD → CD → Writer1-3 & Persona1-3
3. 完了確認: 全エージェント初期化完了

### 実行フェーズ
1. **戦略立案**: MD がCSV分析・戦略ブリーフ作成
2. **制作指示**: MD → CD → Writer1-3 台本制作指示
3. **台本制作**: Writer1-3 が各3本（計9本）制作
4. **評価指示**: CD → Persona1-3 評価指示
5. **品質評価**: Persona1-3 が100点満点評価
6. **承認選定**: CD が80点以上台本を選定
7. **最終選定**: MD が最終台本選定

## 技術仕様

### 通信システム
- **ツール**: `bb-agent-send.sh`
- **ログ**: `logs/send_log.txt`
- **完了管理**: `tmp/[agent]_done.txt`

### ファイル管理
- **指示書**: `instructions/[agent].md`
- **台本**: `projects/[project]/[writer]_script[1-3].md`
- **評価**: `projects/[project]/[persona]_evaluation.md`

### 起動システム
- **一括起動**: `./start-all.sh`
- **環境構築**: `./setup-bb.sh`
- **MD起動**: `./start-md.sh`
- **MultiAgent起動**: `./start-multiagent.sh`

## 品質管理

### 評価基準
- **Persona1**: 共感性・親近感・購買意欲（30-50代主婦層）
- **Persona2**: 論理性・効率性・信頼性（25-45代ビジネス層）
- **Persona3**: トレンド性・SNS映え・話題性（18-30代Z世代）

### 承認基準
- **80点以上**: 承認台本として採用
- **79点以下**: 再制作または不採用

## 設計思想

### Claude Code Communications継承
- **シンプル性**: mdファイルベース管理
- **透明性**: 人間が読める指示書
- **拡張性**: 新エージェント追加容易
- **保守性**: Pythonコード不要

### 改善点
- **ワンクリック初期化**: 手動作業8回 → 1回
- **自動化チェーン**: 指示書ベース自動実行
- **エラー防止**: 初期化忘れリスク削減
- **UX向上**: ユーザー負担大幅軽減

---

🚀 **シンプルで強力、かつユーザーフレンドリーなAI協調システム**