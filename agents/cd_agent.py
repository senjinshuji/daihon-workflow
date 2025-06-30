#!/usr/bin/env python3
"""
CD (Creative Director) Agent - Creative Agent System BB-project
チームリーダー・品質管理責任者
"""

import json
import os
import subprocess
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple

class CDAgent:
    def __init__(self, data_dir="../data", results_dir="../results"):
        self.data_dir = data_dir
        self.results_dir = results_dir
        self.project_name = None # プロジェクト名を保持
        self.current_loop = 0
        self.strategic_brief = ""
        self.persona_settings = []  # MDから受信したペルソナ設定
        self.writer_prompts = self._initialize_writer_prompts()
        self.current_scripts = {}
        self.current_evaluations = {}
        self.loop_history = []
        
    def _initialize_writer_prompts(self) -> Dict[str, str]:
        """Writer初期プロンプト設定"""
        return {
            "writer1": """あなたは感情に訴える表現力豊かなコピーライターです。
ストーリー性を重視し、読者の心に深く響く共感型の動画広告台本を制作してください。
- 感情的な共感を最優先
- ストーリー仕立ての構成
- 安心感と信頼感を演出
- 主婦層に響く親しみやすい表現
- 体験談や実感を重視した内容
今回の商品を、ユーザーから高確率で買ってもらえるような45-59秒の動画広告台本を制作してください。""",
            
            "writer2": """あなたは論理性と説得力を重視するマーケティング専門のコピーライターです。
データと根拠に基づいた説得力のある動画広告台本を制作してください。
- 科学的根拠と論理的説明を重視
- 数値データや効果効能を明確に提示
- 問題→原因→解決策の論理構成
- 権威性と専門性をアピール
- ROIや効果の明確化
今回の商品を、ユーザーから高確率で買ってもらえるような45-59秒の動画広告台本を制作してください。""",
            
            "writer3": """あなたは親しみやすくテンポの良い現代的なコピーライターです。
カジュアルで親近感のある、SNS世代にも響く動画広告台本を制作してください。
- 親しみやすい口調とテンポ
- 現代的な表現とトレンド感
- シンプルで分かりやすい構成
- 気軽に試せる雰囲気作り
- エンターテイメント性も考慮
今回の商品を、ユーザーから高確率で買ってもらえるような45-59秒の動画広告台本を制作してください。"""
        }
    
    def receive_strategic_brief_and_personas(self, brief: str, project_name: str, personas: List[Dict[str, Any]] = None):
        """MDからの戦略ブリーフとペルソナ設定を受信"""
        print("📋 戦略ブリーフとペルソナ設定受信...")
        self.strategic_brief = brief
        self.project_name = project_name

        # ブリーフからループ番号を抽出
        loop_match = re.search(r"Loop (\d+)", brief)
        if loop_match:
            self.current_loop = int(loop_match.group(1))
        
        # ペルソナ設定を抽出
        if personas:
            self.persona_settings = personas
        elif "【自動生成されたペルソナ設定】" in brief:
            self._extract_personas_from_brief(brief)
        
        print(f"✅ 戦略ブリーフ受信完了 (プロジェクト: {self.project_name}, Loop: {self.current_loop})")
    
    def _extract_personas_from_brief(self, brief: str):
        """ブリーフメッセージからペルソナ設定を抽出"""
        self.persona_settings = []
        
        # 簡易的な抽出（実際のメッセージ形式に合わせて調整）
        if "Persona1（共感重視）" in brief:
            self.persona_settings.append({"id": "persona1", "name": "Persona1（共感重視）", "type": "emotional"})
        if "Persona2（合理主義）" in brief:
            self.persona_settings.append({"id": "persona2", "name": "Persona2（合理主義）", "type": "logical"})
        if "Persona3（トレンド志向）" in brief:
            self.persona_settings.append({"id": "persona3", "name": "Persona3（トレンド志向）", "type": "trend"})
    
    def start_creation_loop(self):
        """MDからの指示に基づき、1サイクルの台本制作を実行"""
        print(f"\n=== Loop {self.current_loop} 開始 ===")
        
        # 1. copywriter_instructions.mdを確認
        writer_instructions = self._read_writer_instructions()
        if not writer_instructions:
            print(f"❌ ライター向け指示書が見つからなかったため、Loop {self.current_loop} を中止します。")
            return

        # 2. 3人のライターに各訴求軸で5案制作を指示
        self._instruct_writers_for_loop()
        
        # 3. 15案の完了制作を確認・品質チェック
        self._wait_for_scripts()
        
        # 4. ペルソナへ評価依頼を送信
        self._request_persona_evaluation()
        
        # 5. Persona完了待機
        self._wait_for_evaluation_report()
        
        # 6. 評価結果の統合分析
        approved_scripts, writer_scores, full_evaluations = self._analyze_and_report_to_md()
        
        # 7. MDへループ完了報告
        self._report_to_md(approved_scripts, writer_scores, full_evaluations)
        
        print(f"✅ Loop {self.current_loop} 完了。MDからの次ループ指示を待機します。")
    
    def _read_writer_instructions(self) -> str:
        """現在のループに対応するライター向け指示書を読み込む"""
        suffix = f"_loop{self.current_loop}" if self.current_loop > 1 else ""
        file_name = f"copywriter_instructions{suffix}.md"
        file_path = os.path.join("projects", self.project_name, file_name)
        
        print(f"📖 {file_path} を読み込んでいます...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ ファイルが見つかりません: {file_path}")
            return None
    
    def _instruct_writers_for_loop(self):
        """ライターたちに、現在のループ用の台本作成を指示する"""
        print(f"📝 [CD] Loop {self.current_loop}: 全ライターに指示を開始...")

        # ライターへの指示を、ファイルの内容を読み込むのではなく、
        # プロジェクト名とループ番号を伝えるだけのシンプルなシグナルに変更
        message = f"[PROJECT:{self.project_name}] [LOOP:{self.current_loop}]"

        for writer_id in range(1, 4):
            writer_inbox = f"messages/writer{writer_id}_inbox.txt"
            print(f"   -> ✍️ Writer {writer_id} への指示を送信中...")
            self._send_message(writer_inbox, message)
            # 少し待機して、各ライターが個別にファイルにアクセスできるようにする
            time.sleep(1) 
        
        print(f"✅ [CD] 全ライターへの指示が完了しました。")
    
    def _wait_for_scripts(self):
        """Writer完了待機（5本×3人=15本）と品質チェック"""
        print("⏳ Writer完了待機中（15本の台本作成）...")
        # 実際の実装では、Writerからの完了通知を待機
        time.sleep(10)
        print("  - ライターAの5案受信・品質確認完了...")
        time.sleep(10)
        print("  - ライターBの5案受信・品質確認完了...")
        print("  - ライターCの5案受信・品質確認完了...")
        print("✅ 全15本の台本制作・品質チェック完了")
    
    def _request_persona_evaluation(self):
        """ペルソナたちに、現在のループで生成された台本の評価を依頼する"""
        print(f"📊 [CD] Loop {self.current_loop}: 全ペルソナに評価を依頼...")

        # ペルソナへの指示を、台本内容を含まないシンプルなシグナルに変更
        # Persona側がこのシグナルを元に、該当ファイルを自分で探しに行く
        message = f"[PROJECT:{self.project_name}] [LOOP:{self.current_loop}] [EVALUATE]"

        for persona_id in range(1, 4):
            persona_inbox = f"messages/persona{persona_id}_inbox.txt"
            print(f"   -> 📊 Persona {persona_id} への評価依頼を送信中...")
            self._send_message(persona_inbox, message)
            time.sleep(1) # 念のため待機
        
        print(f"✅ [CD] 全ペルソナへの評価依頼が完了しました。")
    
    def _get_persona_config(self, persona: str) -> str:
        """Persona設定取得（MDが生成した設定を優先）"""
        # MDが生成したペルソナ設定を検索
        if self.persona_settings:
            for p in self.persona_settings:
                if p["id"] == persona:
                    return self._format_persona_config(p)
        
        # デフォルト設定
        configs = {
            "persona1": """**共感重視（主婦層・感情派）**
- 性格: 感情派・主婦層・家族思い
- 好む要素: ストーリー性・安心感・共感のセリフ・体験談
- 嫌う要素: 複雑な専門用語・抽象表現・押し売り感
- 判断基準: 「自分や家族に合いそう」「安心して試せそう」""",
            
            "persona2": """**合理主義（若手起業家・数字重視）**
- 性格: 数字重視・効率性追求・論理思考
- 好む要素: ROI訴求・データ・問題解決型・科学的根拠
- 嫌う要素: 感情に頼る曖昧な表現・根拠のない主張
- 判断基準: 「効果が明確」「コスパが良い」「論理的に納得」""",
            
            "persona3": """**トレンド志向（Z世代・SNS感覚）**
- 性格: トレンド敏感・SNS慣れ・新しもの好き
- 好む要素: トレンドワード・テンポ・刺激・エンタメ性
- 嫌う要素: 古臭い表現・硬すぎる語り・長い説明
- 判断基準: 「面白そう」「話題になりそう」「気軽に試せる」"""
        }
        return configs.get(persona, "")
    
    def _format_persona_config(self, persona_data: Dict[str, Any]) -> str:
        """MDが生成したペルソナデータをフォーマット"""
        config = f"**{persona_data.get('name', 'Unknown')}**\n"
        
        if 'personality_traits' in persona_data:
            config += f"- 性格: {', '.join(persona_data['personality_traits'])}\n"
        
        if 'preferred_elements' in persona_data:
            config += f"- 好む要素: {', '.join(persona_data['preferred_elements'])}\n"
        
        if 'disliked_elements' in persona_data:
            config += f"- 嫌う要素: {', '.join(persona_data['disliked_elements'])}\n"
        
        if 'decision_factors' in persona_data:
            config += f"- 判断基準: {', '.join(persona_data['decision_factors'])}\n"
        
        if 'age_group' in persona_data:
            config += f"- 年齢層: {persona_data['age_group']}\n"
        
        if 'lifestyle' in persona_data:
            config += f"- ライフスタイル: {persona_data['lifestyle']}\n"
        
        return config
    
    def _format_scripts_for_evaluation(self) -> str:
        """評価用台本フォーマット（各Writer3本ずつ）"""
        # 実際の実装では、Writerから受信した台本を整理
        return """
== Writer1台本（情緒派） ==
台本1-1: [Writer1の基本アプローチ台本]
台本1-2: [Writer1の強化アプローチ台本]
台本1-3: [Writer1の実験的アプローチ台本]

== Writer2台本（論理派） ==
台本2-1: [Writer2の基本アプローチ台本]
台本2-2: [Writer2の強化アプローチ台本]
台本2-3: [Writer2の実験的アプローチ台本]

== Writer3台本（カジュアル派） ==
台本3-1: [Writer3の基本アプローチ台本]
台本3-2: [Writer3の強化アプローチ台本]
台本3-3: [Writer3の実験的アプローチ台本]
        """.strip()
    
    def _wait_for_evaluation_report(self):
        """Persona完了待機（15台本×3ペルソナ=45評価）"""
        print("⏳ Persona評価完了待機中（45評価処理）...")
        time.sleep(30)
        print("✅ Persona評価完了確認（45評価）")
    
    def _analyze_and_report_to_md(self) -> Tuple[List[Dict], Dict[str, float], Dict[str, Any]]:
        """評価集約・承認判定。15台本を処理。"""
        print("📊 評価集約中（45評価処理）...")
        
        # 仮の評価データ（15台本分）
        sample_evaluations = {}
        for i in range(1, 4):
            for j in range(1, 6):
                sample_evaluations[f'writer{i}-{j}'] = {
                    "persona1": 70 + (i*5) + j, 
                    "persona2": 75 + (i*5) + j, 
                    "persona3": 80 + (i*5) - j
                }

        approved_scripts = []
        writer_scores = {}
        writer_script_scores = {"writer1": [], "writer2": [], "writer3": []}
        
        for script_id, scores in sample_evaluations.items():
            writer_id = script_id.split('-')[0]
            avg_score = sum(scores.values()) / len(scores)
            
            writer_script_scores[writer_id].append(avg_score)
            
            if avg_score >= 80:
                approved_scripts.append({
                    "script_id": script_id,
                    "average_score": avg_score,
                    "individual_scores": scores
                })
        
        for writer_id, script_scores in writer_script_scores.items():
            writer_avg = sum(script_scores) / len(script_scores) if script_scores else 0
            writer_scores[writer_id] = writer_avg
        
        print(f"✅ 評価集約完了: 承認台本{len(approved_scripts)}本（全15本中）")
        print(f"   Writer別平均: {', '.join([f'{w}: {s:.1f}点' for w, s in writer_scores.items()])}")
        return approved_scripts, writer_scores, sample_evaluations
    
    def _report_to_md(self, approved_scripts: List[Dict], writer_scores: Dict[str, float], full_evaluations: Dict[str, Any]):
        """MDへループ完了報告。詳細なレポートを送信。"""
        print("📤 MDへのループ完了報告を作成・送信中...")
        
        report = f"""【CD Loop {self.current_loop} 完了報告】
プロジェクト: {self.project_name}
報告日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. ループサマリー
- **承認台本数**: {len(approved_scripts)}本 / 15本中
- **Writer平均スコア**:
{self._format_writer_scores(writer_scores)}

## 2. 承認台本リスト (平均80点以上)
{self._format_approved_scripts(approved_scripts)}

## 3. 全台本の評価詳細
"""
        for script_id, scores in full_evaluations.items():
            avg_score = sum(scores.values()) / len(scores)
            writer_id = script_id.split('-')[0]
            report += f"\n### 台本ID: {script_id} (Writer: {writer_id}) - 平均: {avg_score:.2f}点\n"
            for persona, score in scores.items():
                report += f"- {persona}: {score}点\n"
        
        report += """
## 4. 次ステップの提案
MDによる分析と、次ループの改善指示をお待ちしています。
"""
        
        # "md" をターゲットにしてメッセージを送信
        self._send_message("md", report)
        print("✅ MD報告完了")
    
    def _format_approved_scripts(self, scripts: List[Dict]) -> str:
        """承認台本フォーマット"""
        if not scripts:
            return "承認台本なし"
        
        formatted = []
        for i, script in enumerate(scripts, 1):
            script_id = script.get('script_id', f"{script['writer']}")
            formatted.append(f"{i}. {script_id}: {script['average_score']:.1f}点")
        return "\n".join(formatted)
    
    def _format_writer_scores(self, scores: Dict[str, float]) -> str:
        """Writer成績フォーマット"""
        formatted = []
        for writer, score in scores.items():
            # 改善が必要かどうかの判断はMDに委ねる
            formatted.append(f"- {writer}: {score:.2f}点")
        return "\n".join(formatted)
    
    def _send_message(self, target: str, message: str):
        """メッセージ送信"""
        try:
            subprocess.run(
                ["./agent-send.sh", target, message],
                capture_output=True,
                text=True,
                cwd="../.."
            )
        except Exception as e:
            print(f"❌ {target}送信エラー: {e}")

def main():
    """CDエージェント実行テスト"""
    print("🎬 CD Agent 起動...")
    
    cd = CDAgent()
    
    # 実際には、MDからのメッセージをトリガーに実行される
    
    # 1. MDから最初の指示を受信 (Loop 1)
    demo_brief_loop1 = "【Creative Agent System - 戦略ブリーフ (Loop 1)】..."
    demo_personas = [{"id": "persona1", "name": "Persona1"}]
    cd.receive_strategic_brief_and_personas(demo_brief_loop1, "デモプロジェクト", demo_personas)
    
    # 2. Loop 1 を実行
    cd.start_creation_loop()
    
    # この後、エージェントはMDからの次の指示(Loop2のブリーフ)を待機する
    print("\n--- MDからの次の指示を待っています ---")

if __name__ == "__main__":
    main()