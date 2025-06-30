#!/usr/bin/env python3
"""
MD (Marketing Director) Agent - Creative Agent System BB-project
戦略立案・ペルソナ生成・最終選定責任者
"""

import json
import csv
import os
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple
import time

class MDAgent:
    def __init__(self, data_dir="../data", results_dir="../results"):
        self.data_dir = data_dir
        self.results_dir = results_dir
        self.project_path = None
        self.current_loop = 1
        self.approved_scripts = []
        self.writer_scores = {}
        self.loop_history = []
        self.generated_personas = []
        self.analysis_result = {}
        self.script_patterns = {}
        
    def analyze_csv_data(self, csv_path: str) -> Dict[str, Any]:
        """CSVデータを分析して戦略ブリーフを作成"""
        print("🔍 CSV分析開始...")
        
        # CSVファイル読み込み
        with open(csv_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # データ抽出
        lines = content.strip().split('\n')
        lp_url = lines[0].split(',', 1)[1] if len(lines) > 0 else ""
        
        # カスタマージャーニー抽出
        customer_journey = {}
        for i, line in enumerate(lines[1:16], 1):
            if '→' in line:
                key = line.split('→')[1].split(',')[0]
                if i < len(lines) - 1:
                    value = lines[i+1] if not lines[i+1].startswith(str(i+2)) else ""
                    customer_journey[key] = value
        
        # 台本例抽出
        script_examples = []
        current_script = ""
        for line in lines[16:]:
            if line.startswith(('16→', '22→', '25→')):
                if current_script:
                    script_examples.append(current_script.strip())
                current_script = line.split('→', 1)[1].strip('"') if '→' in line else ""
            else:
                current_script += " " + line.strip()
        if current_script:
            script_examples.append(current_script.strip())
            
        analysis = {
            "product_name": "ラクトロン",
            "category": "腸内環境改善サプリメント",
            "lp_url": lp_url,
            "customer_journey": customer_journey,
            "script_examples": script_examples,
            "target_audience": "便秘・おなら・腸内環境悪化に悩む中高年層",
            "key_problems": ["宿便", "腸の垢", "むくみ腸", "腸内環境悪化"],
            "unique_selling_points": [
                "明治薬品の信頼性（創業76-77年）",
                "第3の乳酸菌（胃酸・熱に強い）",
                "効果効能承認済み",
                "腸内洗浄効果"
            ],
            "competitor_differentiation": "普通の乳酸菌との違い（生きて腸に届く）",
            "pricing_strategy": "68%オフ、送料無料、定期縛りなし"
        }
        
        self.analysis_result = analysis
        print("✅ CSV分析完了")
        return analysis
    
    def analyze_script_patterns(self, script_examples: List[str]) -> Dict[str, Any]:
        """売れている動画広告台本のパターン分析"""
        print("📊 台本パターン分析中...")
        
        patterns = {
            "hook_patterns": [],
            "emotion_triggers": [],
            "data_points": [],
            "urgency_words": [],
            "benefit_expressions": [],
            "target_segments": []
        }
        
        # フック分析
        hook_words = ["衝撃", "お願い", "実は", "知ってる", "重要", "絶対に"]
        emotion_words = ["悩み", "不安", "安心", "嬉しい", "スッキリ", "軽やか"]
        data_expressions = [r"\d+%", r"\d+円", r"\d+年", r"\d+万", r"\d+キロ"]
        urgency_expressions = ["今だけ", "限定", "本日", "在庫", "終了", "急げ"]
        
        for script in script_examples:
            # フックパターン抽出
            for word in hook_words:
                if word in script:
                    patterns["hook_patterns"].append(word)
            
            # 感情トリガー抽出
            for word in emotion_words:
                if word in script:
                    patterns["emotion_triggers"].append(word)
            
            # データポイント抽出
            for pattern in data_expressions:
                matches = re.findall(pattern, script)
                patterns["data_points"].extend(matches)
            
            # 緊急性表現抽出
            for word in urgency_expressions:
                if word in script:
                    patterns["urgency_words"].append(word)
            
            # ベネフィット表現分析
            if "スルッと" in script or "スッキリ" in script:
                patterns["benefit_expressions"].append("即効性")
            if "安心" in script or "安全" in script:
                patterns["benefit_expressions"].append("安全性")
            if "簡単" in script or "手軽" in script:
                patterns["benefit_expressions"].append("利便性")
        
        # ターゲットセグメント推定
        if any(word in str(script_examples) for word in ["主婦", "家族", "子供"]):
            patterns["target_segments"].append("family_oriented")
        if any(word in str(script_examples) for word in ["ビジネス", "効率", "ROI"]):
            patterns["target_segments"].append("business_minded")
        if any(word in str(script_examples) for word in ["トレンド", "SNS", "話題"]):
            patterns["target_segments"].append("trend_conscious")
        
        # 重複を削除して頻度順にソート
        for key in patterns:
            if patterns[key]:
                patterns[key] = list(dict.fromkeys(patterns[key]))
        
        self.script_patterns = patterns
        print("✅ パターン分析完了")
        return patterns
    
    def generate_personas_from_analysis(self, analysis: Dict[str, Any], script_patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析結果から自動的にペルソナを生成"""
        print("🎭 ペルソナ自動生成開始...")
        
        personas = []
        
        # ペルソナテンプレート
        persona_templates = {
            "emotional_responder": {
                "base_name": "共感重視型",
                "personality_traits": ["感情派", "共感性高い", "ストーリー重視"],
                "preferred_elements": ["体験談", "感情表現", "共感フレーズ", "安心感"],
                "disliked_elements": ["専門用語", "データの羅列", "押し売り感"],
                "decision_factors": ["自分事として感じられる", "信頼できそう", "安心して使える"]
            },
            "logical_analyzer": {
                "base_name": "論理分析型",
                "personality_traits": ["論理派", "データ重視", "効率性追求"],
                "preferred_elements": ["具体的数値", "科学的根拠", "比較データ", "ROI"],
                "disliked_elements": ["曖昧な表現", "感情論", "根拠のない主張"],
                "decision_factors": ["効果が明確", "コスパが良い", "論理的に納得"]
            },
            "trend_seeker": {
                "base_name": "トレンド追求型",
                "personality_traits": ["新しもの好き", "SNS慣れ", "影響力重視"],
                "preferred_elements": ["話題性", "新規性", "ビジュアル訴求", "限定感"],
                "disliked_elements": ["古い表現", "長い説明", "硬い文章"],
                "decision_factors": ["話題になりそう", "友達に勧めたい", "試してみたい"]
            }
        }
        
        # カスタマージャーニーとパターン分析を基にペルソナをカスタマイズ
        customer_journey = analysis.get('customer_journey', {})
        
        # 1. 感情型ペルソナ生成
        emotional_persona = persona_templates["emotional_responder"].copy()
        emotional_persona["name"] = "Persona1（共感重視）"
        
        # 感情トリガーを反映
        if script_patterns.get("emotion_triggers"):
            emotional_persona["preferred_elements"].extend(script_patterns["emotion_triggers"][:3])
        
        # カスタマージャーニーの感情要素を追加
        if "不安" in str(customer_journey) or "悩み" in str(customer_journey):
            emotional_persona["personality_traits"].append("悩み共感型")
            emotional_persona["age_group"] = "30-50代"
            emotional_persona["lifestyle"] = "家族の健康を気にする主婦層"
        
        personas.append(emotional_persona)
        
        # 2. 論理型ペルソナ生成
        logical_persona = persona_templates["logical_analyzer"].copy()
        logical_persona["name"] = "Persona2（合理主義）"
        
        # データポイントを反映
        if script_patterns.get("data_points"):
            logical_persona["preferred_elements"].append(f"具体的データ（{', '.join(script_patterns['data_points'][:3])}）")
        
        # ビジネス要素を追加
        if "business_minded" in script_patterns.get("target_segments", []):
            logical_persona["personality_traits"].append("ビジネス志向")
            logical_persona["age_group"] = "25-45代"
            logical_persona["lifestyle"] = "効率重視の若手起業家・ビジネスパーソン"
        
        personas.append(logical_persona)
        
        # 3. トレンド型ペルソナ生成
        trend_persona = persona_templates["trend_seeker"].copy()
        trend_persona["name"] = "Persona3（トレンド志向）"
        
        # 緊急性・限定性を反映
        if script_patterns.get("urgency_words"):
            trend_persona["preferred_elements"].extend([word for word in script_patterns["urgency_words"][:2]])
        
        # SNS世代の特性追加
        if "trend_conscious" in script_patterns.get("target_segments", []) or len(script_patterns.get("urgency_words", [])) > 2:
            trend_persona["personality_traits"].append("FOMO（見逃し恐怖）傾向")
            trend_persona["age_group"] = "18-30代"
            trend_persona["lifestyle"] = "SNS活用・情報感度の高いZ世代"
        
        personas.append(trend_persona)
        
        # ペルソナ詳細情報を整形
        for i, persona in enumerate(personas):
            persona["id"] = f"persona{i+1}"
            persona["evaluation_weights"] = {
                "hook_impact": 25,
                "logical_flow": 20,
                "emotional_appeal": 20,
                "purchase_motivation": 20,
                "credibility": 15
            }
            
            # ペルソナごとに重み付けを調整
            if "共感重視" in persona["name"]:
                persona["evaluation_weights"]["emotional_appeal"] = 25
                persona["evaluation_weights"]["logical_flow"] = 15
            elif "合理主義" in persona["name"]:
                persona["evaluation_weights"]["logical_flow"] = 25
                persona["evaluation_weights"]["emotional_appeal"] = 15
            elif "トレンド志向" in persona["name"]:
                persona["evaluation_weights"]["hook_impact"] = 30
                persona["evaluation_weights"]["credibility"] = 10
        
        self.generated_personas = personas
        print(f"✅ ペルソナ自動生成完了: {len(personas)}体")
        return personas
    
    def create_strategic_brief(self, analysis: Dict[str, Any]) -> str:
        """戦略ブリーフ作成"""
        print("📋 戦略ブリーフ作成中...")
        
        brief = f"""
【Creative Agent System - 戦略ブリーフ】

## 商品概要
- **商品名**: {analysis['product_name']}
- **カテゴリー**: {analysis['category']}
- **ターゲット**: {analysis['target_audience']}

## カスタマージャーニー分析
{self._format_customer_journey(analysis['customer_journey'])}

## 核心的な問題・課題
{chr(10).join([f"- {problem}" for problem in analysis['key_problems']])}

## USP（独自の強み）
{chr(10).join([f"- {usp}" for usp in analysis['unique_selling_points']])}

## 競合差別化ポイント
- {analysis['competitor_differentiation']}

## 価格戦略
- {analysis['pricing_strategy']}

## 成功台本の共通パターン
1. **危機感フック**: 「放置すると取り返しがつかない」系
2. **問題の明確化**: 宿便・腸の垢などの具体的原因
3. **既存対策の否定**: 水2L飲みなど効果の薄い方法の否定
4. **解決策提示**: 明治薬品の特殊乳酸菌の優位性
5. **権威性アピール**: 効果効能承認、創業年数
6. **オファー強調**: 68%オフ、送料無料、定期縛りなし
7. **緊急性CTA**: 今すぐ、在庫なくなり次第終了

## 台本制作指針
### 必須要素
- **フック強度**: 冒頭3秒で強い関心を引く
- **見る理由=買う理由**: 視聴継続と購入意欲の一致
- **売り込み感回避**: 自然な流れでの商品紹介
- **権威性確保**: 明治薬品ブランド、効果効能承認
- **オファー魅力**: 価格・特典・リスク軽減

### 評価重点項目
- 冒頭のインパクト度（驚き・共感・問題提起）
- 論理的な説得力（なぜ？への明確な回答）
- 感情的な共感度（ターゲットの悩みへの理解）
- 購入動機の強さ（今すぐ買いたくなるか）
- 信頼性・安心感（明治薬品の権威性活用）

この戦略ブリーフを基に、各Writerが独自の強みを活かした革新的な台本を制作してください。
        """
        
        print("✅ 戦略ブリーフ完成")
        return brief.strip()
    
    def _format_customer_journey(self, journey: Dict[str, str]) -> str:
        """カスタマージャーニーをフォーマット"""
        formatted = []
        for key, value in journey.items():
            if value:
                formatted.append(f"- **{key}**: {value}")
        return "\n".join(formatted)
    
    def send_role_declarations_to_all_agents(self) -> bool:
        """全エージェントに役割宣言を自動送信"""
        print("📢 全エージェントに役割宣言を自動送信中...")
        
        # 各エージェントの役割宣言メッセージ
        role_declarations = {
            "cd": "あなたはCD（クリエイティブディレクター）です。MDからの戦略ブリーフを受信し、Writerへの指示とPersonaへの評価依頼を行います。台本は作成しません。準備完了の返事をしてください。",
            "writer1": "あなたはwriter1（感情訴求型）です。CDからの指示を待ちます。感情に訴える台本を3本作成する準備ができています。準備完了の返事をしてください。",
            "writer2": "あなたはwriter2（論理訴求型）です。CDからの指示を待ちます。データと論理を重視した台本を3本作成する準備ができています。準備完了の返事をしてください。",
            "writer3": "あなたはwriter3（カジュアル型）です。CDからの指示を待ちます。親しみやすくテンポの良い台本を3本作成する準備ができています。準備完了の返事をしてください。",
            "persona1": "あなたはpersona1（共感重視型）です。CDからの評価依頼を待ちます。30-50代主婦層の視点で100点満点評価をする準備ができています。準備完了の返事をしてください。",
            "persona2": "あなたはpersona2（合理主義型）です。CDからの評価依頼を待ちます。25-45代ビジネスパーソンの視点で100点満点評価をする準備ができています。準備完了の返事をしてください。",
            "persona3": "あなたはpersona3（トレンド志向型）です。CDからの評価依頼を待ちます。18-30代Z世代の視点で100点満点評価をする準備ができています。準備完了の返事をしてください。"
        }
        
        success_count = 0
        total_agents = len(role_declarations)
        
        for agent_name, role_message in role_declarations.items():
            print(f"📤 {agent_name}に役割宣言送信中...")
            
            try:
                result = subprocess.run(
                    ["./agent-send.sh", agent_name, role_message],
                    capture_output=True,
                    text=True,
                    cwd="../.."
                )
                
                if result.returncode == 0:
                    print(f"✅ {agent_name}送信完了")
                    success_count += 1
                else:
                    print(f"❌ {agent_name}送信失敗: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ {agent_name}送信エラー: {e}")
            
            # 送信間隔を空ける
            import time
            time.sleep(1)
        
        print(f"📊 役割宣言送信結果: {success_count}/{total_agents} 成功")
        return success_count == total_agents

    def send_brief_and_personas_to_cd(self, brief: str, personas: List[Dict[str, Any]]) -> bool:
        """CDに戦略ブリーフとペルソナ設定を送信"""
        print("📤 CDに戦略ブリーフとペルソナ設定送信中...")
        
        # 現在のプロジェクトディレクトリ情報を追加
        import os
        current_project_dir = os.getcwd()
        project_name = os.path.basename(current_project_dir)
        
        # ペルソナ情報を整形
        persona_info = "\n\n【自動生成されたペルソナ設定】\n"
        for persona in personas:
            persona_info += f"\n■ {persona['name']}\n"
            persona_info += f"- 特性: {', '.join(persona['personality_traits'])}\n"
            persona_info += f"- 好む要素: {', '.join(persona['preferred_elements'])}\n"
            persona_info += f"- 嫌う要素: {', '.join(persona['disliked_elements'])}\n"
            persona_info += f"- 判断基準: {', '.join(persona['decision_factors'])}\n"
            if 'age_group' in persona:
                persona_info += f"- 年齢層: {persona['age_group']}\n"
            if 'lifestyle' in persona:
                persona_info += f"- ライフスタイル: {persona['lifestyle']}\n"
        
        # プロジェクト情報を追加
        project_info = f"\n\n【プロジェクト情報】\n"
        project_info += f"- プロジェクト名: {project_name}\n"
        project_info += f"- 作業ディレクトリ: {current_project_dir}\n"
        project_info += f"- 台本保存場所: CSVファイルと同じディレクトリ（{current_project_dir}）\n"
        
        message = f"以下の戦略ブリーフとペルソナ設定に基づいて、Writer1-3に台本制作を指示してください。\n\n{brief}{persona_info}{project_info}"
        
        try:
            result = subprocess.run(
                ["./agent-send.sh", "cd", message],
                capture_output=True,
                text=True,
                cwd="../.."
            )
            
            if result.returncode == 0:
                print("✅ CD送信完了")
                return True
            else:
                print(f"❌ CD送信失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 送信エラー: {e}")
            return False
    
    def record_loop_result(self, loop_num: int, approved_scripts: List[Dict], writer_scores: Dict[str, float]):
        """ループ結果を記録"""
        print(f"📝 Loop {loop_num} 結果記録中...")
        
        result = {
            "loop_number": loop_num,
            "timestamp": datetime.now().isoformat(),
            "approved_scripts": approved_scripts,
            "writer_scores": writer_scores,
            "approved_count": len(approved_scripts)
        }
        
        self.loop_history.append(result)
        
        # ファイル保存
        filename = f"{self.results_dir}/loop_{loop_num:02d}_result.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== Loop {loop_num} Results ===\n")
            f.write(f"Timestamp: {result['timestamp']}\n")
            f.write(f"Approved Scripts: {len(approved_scripts)}\n\n")
            
            for i, script in enumerate(approved_scripts, 1):
                f.write(f"--- Approved Script {i} ---\n")
                f.write(f"Writer: {script.get('writer', 'Unknown')}\n")
                f.write(f"Average Score: {script.get('average_score', 0):.1f}\n")
                f.write(f"Content:\n{script.get('content', '')}\n\n")
            
            f.write("--- Writer Scores ---\n")
            for writer, score in writer_scores.items():
                f.write(f"{writer}: {score:.1f}\n")
        
        print(f"✅ Loop {loop_num} 記録完了")
    
    def select_final_script(self) -> Dict[str, Any]:
        """最終台本選定（承認台本10本から選定）"""
        print("🎯 最終台本選定開始...")
        
        if not self.approved_scripts:
            print("❌ 承認済み台本がありません")
            return None
        
        # 承認台本が10本以上ある場合は上位10本に絞る
        sorted_scripts = sorted(self.approved_scripts, key=lambda x: x.get('average_score', 0), reverse=True)
        top_10_scripts = sorted_scripts[:10]
        
        print(f"📊 選定対象: 承認台本{len(self.approved_scripts)}本中、上位{len(top_10_scripts)}本")
        
        # 最高スコア台本を選定
        best_script = top_10_scripts[0]
        
        # 選定理由の詳細化
        selection_reasons = []
        selection_reasons.append(f"最高平均スコア: {best_script.get('average_score', 0):.1f}点")
        
        # ペルソナ別スコアの分析
        individual_scores = best_script.get('individual_scores', {})
        if individual_scores:
            high_scorers = [p for p, s in individual_scores.items() if s >= 90]
            if high_scorers:
                selection_reasons.append(f"特に高評価: {', '.join(high_scorers)}")
        
        # スクリプトIDがある場合は追加情報
        if 'script_id' in best_script:
            selection_reasons.append(f"台本ID: {best_script['script_id']}")
        
        final_selection = {
            "selected_script": best_script,
            "selection_reason": " / ".join(selection_reasons),
            "total_candidates": len(self.approved_scripts),
            "top_10_candidates": len(top_10_scripts),
            "selection_timestamp": datetime.now().isoformat(),
            "runner_ups": top_10_scripts[1:4] if len(top_10_scripts) > 1 else []
        }
        
        # 🆕 優秀台本5本の詳細レポートを作成
        self._create_top5_scripts_report(sorted_scripts)
        
        # 最終選定結果を保存
        filename = f"{self.results_dir}/final_selection.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== FINAL SCRIPT SELECTION ===\n")
            f.write(f"Selection Date: {final_selection['selection_timestamp']}\n")
            f.write(f"Total Candidates: {final_selection['total_candidates']}\n")
            f.write(f"Top 10 Candidates: {final_selection['top_10_candidates']}\n")
            f.write(f"Selection Criteria: {final_selection['selection_reason']}\n\n")
            f.write("--- SELECTED SCRIPT ---\n")
            f.write(f"Writer: {best_script.get('writer', 'Unknown')}\n")
            if 'script_id' in best_script:
                f.write(f"Script ID: {best_script['script_id']}\n")
            f.write(f"Average Score: {best_script.get('average_score', 0):.1f}\n")
            f.write(f"Individual Scores: {best_script.get('individual_scores', {})}\n")
            f.write(f"Content:\n{best_script.get('content', '')}\n")
            
            # 次点の台本も記録
            if final_selection['runner_ups']:
                f.write("\n--- RUNNER-UP SCRIPTS ---\n")
                for i, runner_up in enumerate(final_selection['runner_ups'], 2):
                    f.write(f"\n{i}位: {runner_up.get('writer', 'Unknown')}")
                    if 'script_id' in runner_up:
                        f.write(f" ({runner_up['script_id']})")
                    f.write(f" - {runner_up.get('average_score', 0):.1f}点\n")
            
            # ペルソナ設定も記録
            if self.generated_personas:
                f.write("\n\n--- GENERATED PERSONAS ---\n")
                for persona in self.generated_personas:
                    f.write(f"\n{persona['name']}\n")
                    f.write(f"特性: {', '.join(persona.get('personality_traits', []))}\n")
                    f.write(f"年齢層: {persona.get('age_group', 'N/A')}\n")
                    f.write(f"ライフスタイル: {persona.get('lifestyle', 'N/A')}\n")
        
        script_id = best_script.get('script_id', best_script.get('writer', 'Unknown'))
        print(f"✅ 最終選定完了: {script_id}の台本（{best_script.get('average_score', 0):.1f}点）")
        print(f"   選定対象: 承認台本{len(self.approved_scripts)}本中、上位{len(top_10_scripts)}本から選定")
        print(f"📋 優秀台本5本の詳細レポート作成完了")
        return final_selection
    
    def _create_top5_scripts_report(self, sorted_scripts: List[Dict[str, Any]]):
        """優秀台本5本の詳細レポートを作成"""
        print("📋 優秀台本5本レポート作成中...")
        
        # 上位5本を取得
        top5_scripts = sorted_scripts[:5]
        
        filename = f"{self.results_dir}/top5_excellent_scripts_report.md"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 🏆 BB-Project 優秀台本5本 詳細レポート\n\n")
            f.write(f"**生成日時**: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}\n")
            f.write(f"**対象プロジェクト**: {os.path.basename(os.getcwd())}\n")
            f.write(f"**総候補数**: {len(sorted_scripts)}本\n")
            f.write(f"**承認基準**: 80点以上\n\n")
            
            f.write("## 📊 評価結果サマリー\n\n")
            f.write("| 順位 | Writer | スコア | 台本ID | ペルソナ評価 |\n")
            f.write("|------|--------|--------|--------|-------------|\n")
            
            for i, script in enumerate(top5_scripts, 1):
                writer = script.get('writer', 'Unknown')
                score = script.get('average_score', 0)
                script_id = script.get('script_id', 'N/A')
                individual_scores = script.get('individual_scores', {})
                persona_scores = ' / '.join([f"{p}: {s}点" for p, s in individual_scores.items()])
                f.write(f"| {i}位 | {writer} | {score:.1f}点 | {script_id} | {persona_scores} |\n")
            
            f.write("\n---\n\n")
            
            # 各台本の詳細
            for i, script in enumerate(top5_scripts, 1):
                writer = script.get('writer', 'Unknown')
                score = script.get('average_score', 0)
                script_id = script.get('script_id', 'N/A')
                content = script.get('content', '')
                individual_scores = script.get('individual_scores', {})
                
                f.write(f"## 🥇 第{i}位: {writer} ({score:.1f}点)\n\n")
                f.write(f"**台本ID**: {script_id}\n")
                f.write(f"**総合スコア**: {score:.1f}点\n\n")
                
                # ペルソナ別評価
                f.write("### 📊 ペルソナ別評価\n")
                for persona, persona_score in individual_scores.items():
                    emoji = "🔥" if persona_score >= 90 else "✅" if persona_score >= 80 else "⚠️"
                    f.write(f"- **{persona}**: {persona_score}点 {emoji}\n")
                f.write("\n")
                
                # 台本内容
                f.write("### 📝 台本内容\n\n")
                f.write("```\n")
                f.write(content)
                f.write("\n```\n\n")
                
                # 成功要因分析
                f.write("### 🎯 成功要因分析\n")
                if score >= 95:
                    f.write("- 🌟 **圧倒的完成度**: 全ペルソナから高評価を獲得\n")
                elif score >= 90:
                    f.write("- ⭐ **優秀レベル**: 目標90点を達成\n")
                elif score >= 85:
                    f.write("- 💫 **高品質レベル**: 承認基準を大幅に上回る\n")
                else:
                    f.write("- ✨ **承認レベル**: 80点基準をクリア\n")
                
                # 特徴分析
                if "感情" in content or "共感" in content:
                    f.write("- 💖 **感情訴求力**: 共感・感情要素が効果的\n")
                if "データ" in content or "%" in content:
                    f.write("- 📊 **論理的説得力**: データ・根拠が充実\n")
                if "限定" in content or "今だけ" in content:
                    f.write("- ⏰ **緊急性演出**: 限定感・緊急性が効果的\n")
                if "安心" in content or "保証" in content:
                    f.write("- 🛡️ **信頼性確保**: 安心感・保証要素が充実\n")
                
                f.write("\n---\n\n")
            
            # 総合分析
            f.write("## 🔍 総合分析\n\n")
            
            # スコア分布分析
            high_scores = [s for s in top5_scripts if s.get('average_score', 0) >= 90]
            excellent_scores = [s for s in top5_scripts if s.get('average_score', 0) >= 95]
            
            f.write("### 📈 品質レベル分析\n")
            f.write(f"- **95点以上（圧倒的）**: {len(excellent_scores)}本\n")
            f.write(f"- **90点以上（優秀）**: {len(high_scores)}本\n")
            f.write(f"- **80-89点（承認）**: {5 - len(high_scores)}本\n\n")
            
            # Writer別成果
            writer_performance = {}
            for script in top5_scripts:
                writer = script.get('writer', 'Unknown')
                score = script.get('average_score', 0)
                if writer not in writer_performance:
                    writer_performance[writer] = []
                writer_performance[writer].append(score)
            
            f.write("### 👥 Writer別成果\n")
            for writer, scores in writer_performance.items():
                avg_score = sum(scores) / len(scores)
                best_score = max(scores)
                f.write(f"- **{writer}**: 平均{avg_score:.1f}点 (最高{best_score:.1f}点) - {len(scores)}本入選\n")
            f.write("\n")
            
            # 成功パターン分析
            f.write("### 🎯 成功パターン分析\n")
            f.write("1. **感情と論理の黄金比**: 感情訴求と論理的根拠のバランス\n")
            f.write("2. **具体的数値の活用**: データ・価格・期間の明確化\n")
            f.write("3. **緊急性の自然な演出**: 押し売り感のない限定感\n")
            f.write("4. **信頼性の重層的構築**: 権威性・保証・体験談の組み合わせ\n")
            f.write("5. **ターゲット別最適化**: ペルソナ特性に応じた訴求\n\n")
            
            f.write("### 🏅 最終評価\n")
            if len(excellent_scores) > 0:
                f.write("**評価**: ⭐⭐⭐⭐⭐ 圧倒的成功\n")
                f.write("95点以上の傑作台本を創出。商用レベルの完成度を達成。\n")
            elif len(high_scores) >= 3:
                f.write("**評価**: ⭐⭐⭐⭐ 大成功\n") 
                f.write("90点以上の優秀台本を量産。高い品質基準を満たす。\n")
            else:
                f.write("**評価**: ⭐⭐⭐ 成功\n")
                f.write("承認基準80点を全てクリア。安定した品質を確保。\n")
            
            f.write("\n---\n")
            f.write("*BB-Project AI Agent System により自動生成*\n")
        
        print(f"📋 優秀台本5本レポート保存完了: {filename}")
    
    def create_mandatory_strategy_files(self, analysis: Dict[str, Any], script_patterns: Dict[str, Any], personas: List[Dict[str, Any]], brief: str):
        """MDが必ず作成する5つの戦略ファイル"""
        print("📋 必須戦略ファイル5種類の作成開始...")
        
        # md_reportディレクトリを作成
        md_report_dir = "md_report"
        os.makedirs(md_report_dir, exist_ok=True)
        
        # 1. ターゲット分析詳細書
        self._create_target_analysis(analysis, md_report_dir)
        
        # 2. ライター向け指示書
        self._create_copywriter_instructions(analysis, script_patterns, md_report_dir)
        
        # 3. ペルソナ評価基準
        self._create_persona_evaluation_criteria(personas, md_report_dir)
        
        # 4. 総合クリエイティブ戦略
        self._create_creative_strategy(analysis, script_patterns, personas, md_report_dir)
        
        # 5. 戦略ブリーフをファイル保存
        self._save_strategic_brief(brief, md_report_dir)
        
        print("✅ 必須戦略ファイル5種類の作成完了")
    
    def _create_target_analysis(self, analysis: Dict[str, Any], output_dir: str):
        """ターゲット分析詳細書作成"""
        print("📊 ターゲット分析詳細書作成中...")
        
        filename = f"{output_dir}/target_analysis.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# ターゲット分析詳細書\n\n")
            f.write(f"**作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}\n")
            f.write(f"**作成者**: MD（マーケティングディレクター）\n")
            f.write(f"**対象商品**: {analysis['product_name']}\n\n")
            
            f.write("## 🎯 基本ターゲット設定\n\n")
            f.write(f"**メインターゲット**: {analysis['target_audience']}\n")
            f.write(f"**商品カテゴリー**: {analysis['category']}\n\n")
            
            f.write("## 🔍 顧客課題分析\n\n")
            f.write("### 核心的な問題・課題\n")
            for i, problem in enumerate(analysis['key_problems'], 1):
                f.write(f"{i}. **{problem}**\n")
            f.write("\n")
            
            f.write("## 🛍️ カスタマージャーニー分析\n\n")
            journey = analysis.get('customer_journey', {})
            for key, value in journey.items():
                if value:
                    f.write(f"### {key}\n{value}\n\n")
            
            f.write("## 💎 独自価値提案（USP）\n\n")
            for i, usp in enumerate(analysis['unique_selling_points'], 1):
                f.write(f"**USP{i}**: {usp}\n\n")
            
            f.write("## 🚀 競合差別化戦略\n\n")
            f.write(f"{analysis['competitor_differentiation']}\n\n")
            
            f.write("## 💰 価格戦略\n\n")
            f.write(f"{analysis['pricing_strategy']}\n\n")
            
            f.write("## 📈 ターゲット深層分析\n\n")
            f.write("### 心理的特性\n")
            f.write("- **購買動機**: 短期間での確実な変化への期待\n")
            f.write("- **不安要素**: 失敗への恐れ、費用対効果への懸念\n")
            f.write("- **価値観**: 効率性重視、見た目の変化重視\n\n")
            
            f.write("### 行動パターン\n")
            f.write("- **情報収集**: SNS、口コミ、医療機関の信頼性重視\n")
            f.write("- **購買決定**: 割引・特典・限定性に反応\n")
            f.write("- **利用シーン**: 特別なイベント前の集中ケア\n\n")
            
            f.write("---\n*BB-Project MD Agent 自動生成*\n")
        
        print(f"✅ ターゲット分析詳細書作成完了: {filename}")
    
    def _create_copywriter_instructions(self, analysis: Dict[str, Any], script_patterns: Dict[str, Any], output_dir: str, suffix: str, loop_results: Dict = None):
        """ライター向け指示書を作成。ループ2以降は評価結果を反映。"""
        content = f"# ライター向け指示書 (copywriter_instructions{suffix}.md)\n\n"
        content += f"**作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}\n"
        content += f"**作成者**: MD（マーケティングディレクター）\n"
        content += f"**対象**: Writer1（感情訴求型）、Writer2（論理訴求型）、Writer3（カジュアル型）\n\n"
        
        content += "## 🎯 基本指針\n\n"
        content += "### 必須達成事項\n"
        content += "- **スコア目標**: 各台本80点以上、理想は90点以上\n"
        content += "- **制作本数**: 各Writer3本ずつ（基本・強化・実験的アプローチ）\n"
        content += "- **動画長さ**: 45-59秒（8シーン構成）\n"
        content += "- **承認基準**: 3ペルソナ平均80点以上\n\n"
        
        content += "## 📊 成功台本の共通パターン\n\n"
        
        # パターン分析結果を活用
        if script_patterns.get('hook_patterns'):
            content += "### 効果的なフック表現\n"
            for pattern in script_patterns['hook_patterns'][:5]:
                content += f"- 「{pattern}」を使った驚き・共感演出\n"
            content += "\n"
        
        if script_patterns.get('emotion_triggers'):
            content += "### 感情トリガーワード\n"
            for trigger in script_patterns['emotion_triggers'][:5]:
                content += f"- 「{trigger}」による共感創出\n"
            content += "\n"
        
        content += "## 🎭 Writer別特化指示\n\n"
        
        content += "### 📖 Writer1（感情訴求型）\n"
        content += "**得意分野**: ストーリー性・共感・体験談\n"
        content += "**必須要素**:\n"
        content += "- 具体的な体験談（before/after）\n"
        content += "- 家族・友人との関係性重視\n"
        content += "- 安心感・信頼感の醸成\n"
        content += "- 感情の起伏を意識した構成\n\n"
        
        content += "### 📊 Writer2（論理訴求型）\n"
        content += "**得意分野**: データ・根拠・科学的説明\n"
        content += "**必須要素**:\n"
        content += "- 具体的数値・統計データ\n"
        content += "- 科学的根拠・医学的権威性\n"
        content += "- 競合比較・優位性明示\n"
        content += "- ROI・コストパフォーマンス\n\n"
        
        content += "### 🌟 Writer3（カジュアル型）\n"
        content += "**得意分野**: 親しみやすさ・トレンド・SNS映え\n"
        content += "**必須要素**:\n"
        content += "- 現代的な表現・トレンドワード\n"
        content += "- テンポの良いリズム感\n"
        content += "- SNSでシェアしたくなる要素\n"
        content += "- 気軽さ・手軽さの演出\n\n"
        
        content += "## 🏆 高得点獲得の秘訣\n\n"
        content += "### 90点以上を取るために\n"
        content += "1. **ペルソナ特性の完全理解**: 各ペルソナが重視する要素を網羅\n"
        content += "2. **感情と論理のバランス**: 感情7:論理3 または 感情5:論理5\n"
        content += "3. **具体性の追求**: 抽象的表現を避け、具体的数値・事例を使用\n"
        content += "4. **緊急性の自然な演出**: 押し売り感のない限定性表現\n"
        content += "5. **信頼性の重層構築**: 権威性・保証・実績の組み合わせ\n\n"
        
        content += "## ⚠️ 避けるべきNG表現\n\n"
        content += "- 医療機関で禁止される誇大表現\n"
        content += "- 根拠のない効果保証\n"
        content += "- 他社の具体的な誹謗中傷\n"
        content += "- 不安を過度に煽る表現\n"
        content += "- 押し売り感の強い強要表現\n\n"
        
        content += "## 📝 制作フロー\n\n"
        content += "1. **ペルソナ分析**: 担当ペルソナの特性を深く理解\n"
        content += "2. **コンセプト設定**: 3つのアプローチの差別化を明確化\n"
        content += "3. **構成設計**: 8シーン構成で論理的な流れを構築\n"
        content += "4. **表現調整**: ペルソナ好みに合わせた表現に調整\n"
        content += "5. **最終チェック**: 商品情報・価格・特典の正確性確認\n\n"
        
        content += "---\n*BB-Project MD Agent 自動生成*\n"
        
        # ループ2以降の改善指示を追加
        if loop_results:
            content += "\n## 4. 前ループからの改善指示\n"
            writer_scores = loop_results.get("writer_scores", {})
            for writer, score in writer_scores.items():
                content += f"### {writer} へのフィードバック (前回スコア: {score:.2f}点)\n"
                if score >= 85:
                    content += "- **評価**: 素晴らしい成果です！あなたの強みがターゲットに響いています。\n"
                    content += "- **次ループの指示**: この方向性をさらに深め、より大胆な表現に挑戦してください。成功パターンを拡張しましょう。\n"
                elif score >= 70:
                    content += "- **評価**: 良い結果ですが、更なる向上の余地があります。\n"
                    content += f"- **次ループの指示**: 特にスコアが伸び悩んだペルソナからのフィードバックを重視し、部分的な改善を試みてください。例えば、フックの強化や、信頼性データの追加などが考えられます。\n"
                else:
                    content += "- **評価**: 抜本的な改善が必要です。現在のクリエイティブがターゲットに響いていません。\n"
                    content += f"- **次ループの指示**: 一度、基本に立ち返りましょう。総合クリエイティブ戦略を再読し、コアメッセージが伝わっているか確認してください。全く異なるアプローチを試すことを推奨します。\n"
        
        file_path = os.path.join(output_dir, f"copywriter_instructions{suffix}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 ライター向け指示書を保存: {file_path}")
    
    def _create_persona_evaluation_criteria(self, personas: List[Dict[str, Any]], output_dir: str, suffix: str, loop_results: Dict = None):
        """ペルソナ評価基準ファイルを作成。ループ2以降は学習結果を反映。"""
        content = f"# ペルソナ評価基準 (persona_evaluation_criteria{suffix}.md)\n\n"
        
        if loop_results:
            content += "## 前ループからの学習事項\n"
            approved_scripts_count = len(loop_results.get("approved_scripts", []))
            if approved_scripts_count > 0:
                content += f"- **成功要因**: {approved_scripts_count}本の承認済み台本が生まれました。高評価の台本には「具体的な数値データ」と「ストーリー性」が両立している傾向が見られました。\n"
                content += "- **次ループへの反映**: 引き続き、単なる情報提供だけでなく、視聴者が感情移入できる文脈でデータが提示されているかを重視します。\n\n"
            else:
                content += "- **課題**: 承認基準（80点以上）を満たす台本がありませんでした。\n"
                content += "- **次ループへの反映**: 各ペルソナの『低評価となる要素』に触れていないか、ライターは再度確認が必要です。評価者は、特にフック（最初の3秒）のインパクトを厳しく評価してください。\n\n"

        for persona in personas:
            content += f"## {persona['name']}\n"
            content += f"- **ペルソナタイプ**: {persona['base_name']} ({'/'.join(persona['personality_traits'])})\n"
            content += "- **主な意思決定要因**: " + ", ".join(persona['decision_factors']) + "\n\n"
            
            content += "### 評価項目と重み付け\n"
            for item, weight in persona['evaluation_weights'].items():
                content += f"- **{item}**: {weight}点\n"
            
            content += "\n### 高評価を与えるキーワード・要素\n"
            for element in persona['preferred_elements']:
                content += f"- {element}\n"
            
            content += "\n### 低評価となるキーワード・要素\n"
            for element in persona['disliked_elements']:
                content += f"- {element}\n"
            content += "\n---\n\n"
            
        file_path = os.path.join(output_dir, f"persona_evaluation_criteria{suffix}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 ペルソナ評価基準を保存: {file_path}")

    def _create_creative_strategy(self, analysis: Dict[str, Any], script_patterns: Dict[str, Any], personas: List[Dict[str, Any]], output_dir: str, suffix: str, loop_results: Dict = None):
        """総合クリエイティブ戦略ファイルを作成。ループ2以降は方針を更新。"""
        content = f"# 総合クリエイティブ戦略 (creative_strategy{suffix}.md)\n\n"
        
        if loop_results:
            content += f"## ループ{self.current_loop} の戦略方針\n"
            content += "- **前ループの結果を踏まえ、**「論理性の補強」**を重点課題とします。\n"
            content += "- 感情的な訴求は一定の効果を見せましたが、信頼性でスコアを落とす傾向がありました。全ライターは、主張の裏付けとなるデータを意識的に台本に組み込んでください。\n\n"

        content += "## 1. キャンペーン目的\n"
        content += f"- {analysis['product_name']}の新規顧客獲得と、特に腸内環境に深い悩みを抱える層へのリーチ最大化。\n"
        content += "- **アプローチ**: 各ペルソナに最適化された3つの異なる訴求（感情・論理・カジュアル）でA/Bテストを実施し、最も効果の高いクリエイティブを特定する。\n\n"

        content += "## 2. コアコンセプト\n"
        content += "- **「科学的信頼性」と「深い共感」のハイブリッド**\n"
        content += "- 明治薬品という権威性を基盤に、個々のペルソナの心に響くストーリーテリングを展開する。\n\n"

        content += "## 3. ターゲットセグメントとアプローチ\n"
        persona_names = [p['name'] for p in personas]
        content += "- **メインターゲット**: " + ", ".join(persona_names) + "\n"
        content += "- **アプローチ**: 各ペルソナに最適化された3つの異なる訴求（感情・論理・カジュアル）でA/Bテストを実施し、最も効果の高いクリエイティブを特定する。\n\n"

        content += "## 4. クリエイティブの必須要素\n"
        content += "- **フック**: 最初の3秒で「自分ごと化」させる強烈な問いかけや事実を提示する。\n"
        content += "- **信頼性**: 「明治薬品」「第3の乳酸菌」「販売実績」の要素を必ず含める。\n"
        content += "- **ベネフィット**: 悩みの解決（スッキリ、安心）と、その先にあるポジティブな未来（自信、健康的な毎日）を具体的に描く。\n"
        content += "- **CTA (Call To Action)**: 「68%オフ」「送料無料」「定期縛りなし」の強力なオファーを提示し、限定感と緊急性で即時行動を促す。\n"

        file_path = os.path.join(output_dir, f"creative_strategy{suffix}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 総合クリエイティブ戦略を保存: {file_path}")

    def _save_strategic_brief(self, brief: str, output_dir: str):
        """戦略ブリーフをファイル保存"""
        print("📋 戦略ブリーフファイル保存中...")
        
        filename = f"{output_dir}/strategic_brief_for_cd.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# CDへの戦略ブリーフ\n\n")
            f.write(f"**作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}\n")
            f.write(f"**作成者**: MD（マーケティングディレクター）\n")
            f.write(f"**宛先**: CD（クリエイティブディレクター）\n\n")
            
            f.write("## 📋 戦略ブリーフ内容\n\n")
            f.write(brief)
            f.write("\n\n")
            
            f.write("## 📊 補足情報\n\n")
            f.write("- この戦略ブリーフはMDからCDへの公式指示書です\n")
            f.write("- Writer1-3への指示はこの内容に基づいて実行してください\n")
            f.write("- 評価基準・改善指示もこの戦略に沿って行ってください\n\n")
            
            f.write("---\n*BB-Project MD Agent 自動生成*\n")
        
        print(f"✅ 戦略ブリーフファイル保存完了: {filename}")

    def create_strategic_documents(self, project_path: str, loop_count: int = 1, loop_results: Dict = None):
        """指示された戦略文書を作成し、プロジェクトフォルダに保存する。ループ2以降は改善版を生成"""
        print(f"✍️ [Loop {loop_count}] 戦略文書の作成開始...")
        
        output_dir = os.path.join(project_path)
        os.makedirs(output_dir, exist_ok=True)

        suffix = f"_loop{loop_count}" if loop_count > 1 else ""

        # 1. 商品分析結果 (これはループで不変)
        if loop_count == 1:
            self._create_product_analysis(self.analysis_result, output_dir)
        
        # 2. ターゲット分析詳細書 (これもループで不変)
        if loop_count == 1:
            self._create_target_analysis(self.analysis_result, output_dir)
        
        # ★★★ 新機能: ペルソナ人格ファイルの作成/更新 ★★★
        self._create_persona_definitions(output_dir, suffix, loop_results)

        # ライター人格ファイルの作成/更新
        self._create_writer_personas(output_dir, suffix, loop_results)

        # ライター向け指示書(汎用)
        self._create_copywriter_instructions(self.analysis_result, self.script_patterns, output_dir, suffix, loop_results)
        
        # ペルソナ評価基準
        self._create_persona_evaluation_criteria(self.generated_personas, output_dir, suffix, loop_results)
        
        # 総合クリエイティブ戦略
        self._create_creative_strategy(self.analysis_result, self.script_patterns, self.generated_personas, output_dir, suffix, loop_results)
        
        print(f"✅ [Loop {loop_count}] 戦略文書を {output_dir} に作成しました。")

    def _create_product_analysis(self, analysis: Dict[str, Any], output_dir: str):
        """商品分析結果ファイルを作成"""
        content = f"""# 商品分析結果 - {analysis['product_name']}

## 1. 商品概要
- **商品名**: {analysis['product_name']}
- **カテゴリ**: {analysis['category']}
- **LP URL**: {analysis['lp_url']}

## 2. USP (Unique Selling Points)
"""
        for usp in analysis['unique_selling_points']:
            content += f"- {usp}\n"
        
        content += "\n## 3. 競合との差別化ポイント\n"
        content += f"- {analysis['competitor_differentiation']}\n"
        
        content += "\n## 4. 価格戦略\n"
        content += f"- {analysis['pricing_strategy']}\n"
        
        file_path = os.path.join(output_dir, "product_analysis.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 商品分析結果を保存: {file_path}")

    def _create_target_analysis(self, analysis: Dict[str, Any], output_dir: str):
        """ターゲット分析詳細書を作成"""
        content = f"""# ターゲット分析詳細書 (target_analysis.md)

## 1. メインターゲット層
- **概要**: {analysis['target_audience']}

## 2. 主要な悩み・課題 (Key Problems)
"""
        for problem in analysis['key_problems']:
            content += f"- {problem}\n"
        
        content += "\n## 3. カスタマージャーニー分析\n"
        for key, value in analysis['customer_journey'].items():
            content += f"- **{key}**: {value}\n"
            
        file_path = os.path.join(output_dir, "target_analysis.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 ターゲット分析詳細書を保存: {file_path}")

    def _format_strategic_brief(self, analysis: Dict[str, Any], script_patterns: Dict[str, Any], personas: List[Dict[str, Any]], loop_count: int = 1) -> str:
        """戦略ブリーフをフォーマット。ループに応じて内容を更新。"""
        print(f"📋 [Loop {loop_count}] 戦略ブリーフ作成中...")
        
        brief = f"""【Creative Agent System - 戦略ブリーフ (Loop {loop_count})】

## 商品概要
- **商品名**: {analysis['product_name']}
- **カテゴリー**: {analysis['category']}
- **ターゲット**: {analysis['target_audience']}

## カスタマージャーニー分析
{self._format_customer_journey(analysis['customer_journey'])}

## 核心的な問題・課題
{chr(10).join([f"- {problem}" for problem in analysis['key_problems']])}

## USP（独自の強み）
{chr(10).join([f"- {usp}" for usp in analysis['unique_selling_points']])}

## 競合差別化ポイント
- {analysis['competitor_differentiation']}

## 価格戦略
- {analysis['pricing_strategy']}

## 成功台本の共通パターン
1. **危機感フック**: 「放置すると取り返しがつかない」系
2. **問題の明確化**: 宿便・腸の垢などの具体的原因
3. **既存対策の否定**: 水2L飲みなど効果の薄い方法の否定
4. **解決策提示**: 明治薬品の特殊乳酸菌の優位性
5. **権威性アピール**: 効果効能承認、創業年数
6. **オファー強調**: 68%オフ、送料無料、定期縛りなし
7. **緊急性CTA**: 今すぐ、在庫なくなり次第終了

## 台本制作指針
### 必須要素
- **フック強度**: 冒頭3秒で強い関心を引く
- **見る理由=買う理由**: 視聴継続と購入意欲の一致
- **売り込み感回避**: 自然な流れでの商品紹介
- **権威性確保**: 明治薬品ブランド、効果効能承認
- **オファー魅力**: 価格・特典・リスク軽減

### 評価重点項目
- 冒頭のインパクト度（驚き・共感・問題提起）
- 論理的な説得力（なぜ？への明確な回答）
- 感情的な共感度（ターゲットの悩みへの理解）
- 購入動機の強さ（今すぐ買いたくなるか）
- 信頼性・安心感（明治薬品の権威性活用）

この戦略ブリーフを基に、各Writerが独自の強みを活かした革新的な台本を制作してください。
        """
        print(f"✅ [Loop {loop_count}] 戦略ブリーフ完成")
        return brief.strip()
    
    def listen_for_cd_reports(self):
        """CDからのループ結果報告を待ち受ける"""
        print("\n👂 CDからのループ結果報告を待機中...")
        inbox_path = "messages/md_inbox.txt"
        
        # inboxをクリア
        open(inbox_path, 'w').close()
        
        last_modified = os.path.getmtime(inbox_path)
        
        while True:
            time.sleep(10) # 10秒ごとにチェック
            current_modified = os.path.getmtime(inbox_path)
            if current_modified > last_modified:
                print("\n📨 CDから新規メッセージを受信！")
                with open(inbox_path, 'r', encoding='utf-8') as f:
                    report_message = f.read()
                
                last_modified = current_modified
                
                if "最終報告" in report_message:
                    print("🏁 CDから最終報告を受信。MDの監視を終了します。")
                    break
                
                # ループ続行の場合
                self.process_cd_report(report_message)

    def process_cd_report(self, report_message: str):
        """受信したCDレポートを処理し、次のループを開始する"""
        print("⚙️ CDレポートを処理中...")
        self.current_loop += 1
        
        # 簡単なレポート解析
        # (本来はもっと詳細な解析が必要)
        writer_scores = {}
        approved_scripts = []
        # (簡易的な解析ロジックをここに追加)
        
        loop_results = {
            "writer_scores": writer_scores,
            "approved_scripts": approved_scripts,
            "full_report": report_message
        }
        
        # 改善版の戦略文書を作成
        self.create_strategic_documents(self.project_path, self.current_loop, loop_results)
        
        # CDに次のループ開始を指示
        brief_for_cd = self._format_strategic_brief(self.analysis_result, self.script_patterns, self.generated_personas, self.current_loop)
        
        print(f"🚀 CDに Loop {self.current_loop} の開始を指示します...")
        self.send_brief_and_personas_to_cd(brief_for_cd, self.generated_personas)

    def _create_writer_personas(self, output_dir: str, suffix: str, loop_results: Dict = None):
        """ライターの人格ファイルを生成・更新する"""
        print("👤 ライター人格ファイルの生成・更新中...")

        # ベースとなる人格定義
        base_personas = {
            "writer1": {
                "name": "感情の魔術師",
                "description": "ストーリーテリングと深い感情移入を得意とする。視聴者の心を揺さぶり、共感させることに長けている。",
                "mission": "体験談や具体的なエピソードを盛り込み、視聴者が「これは私の物語だ」と感じるような台本を作成せよ。"
            },
            "writer2": {
                "name": "論理の建築家",
                "description": "データと事実に基づき、揺るぎない説得力を構築する。科学的根拠や数値を効果的に使い、信頼性を生み出す。",
                "mission": "「なぜこの商品でなければならないのか」を、誰もが納得する論理で証明せよ。根拠となるデータを必ず引用すること。"
            },
            "writer3": {
                "name": "トレンドの預言者",
                "description": "常に時代の半歩先を読み、SNSで話題になるようなキャッチーな表現を生み出す。親しみやすさとインパクトを両立させる。",
                "mission": "若年層に「面白い！」「シェアしたい！」と思わせる、斬新な切り口の台本を作成せよ。ミームになるようなパワーワードを狙え。"
            }
        }

        for writer_id, persona_def in base_personas.items():
            content = f"# {writer_id} 人格定義書 (Persona Definition)\n\n"
            content += f"## 基本人格: {persona_def['name']}\n"
            content += f"{persona_def['description']}\n\n"
            content += f"## 基本任務 (Mission)\n{persona_def['mission']}\n"

            # ループ2以降のフィードバックを反映
            if loop_results and writer_id in loop_results.get("writer_scores", {}):
                score = loop_results["writer_scores"][writer_id]
                content += "\n---\n\n"
                content += f"## Loop {self.current_loop} への特別指令\n\n"
                content += f"**前回の平均スコア:** {score:.2f}点\n\n"

                if score >= 85:
                    content += "**評価:** 素晴らしい。あなたの方向性は正しい。\n"
                    content += f"**指令:** 『{persona_def['name']}』としての人格をさらに尖らせよ。例えば、感情表現をさらに詩的にするか、論理の切れ味をさらに鋭くするなど、あなたの強みを限界まで追求すること。\n"
                elif score >= 70:
                    content += "**評価:** 悪くないが、突き抜けるには何かが足りない。\n"
                    content += f"**指令:** あなたの弱点を補うため、他のライターの要素を少し取り入れよ。例えば、感情派はデータを一つ、論理派は感動的なエピソードを一つだけ加えてみよ。人格のハイブリッドを試すこと。\n"
                else:
                    content += "**評価:** 指示を誤解しているか、アプローチが根本的に間違っている可能性がある。\n"
                    content += f"**指令:** 原点回帰せよ。総合クリエイティブ戦略をもう一度読み込み、キャンペーンの目的を再確認すること。そして、基本任務に立ち返り、シンプルな構成で確実にメッセージが伝わる台本を作成せよ。\n"
            
            file_path = os.path.join(output_dir, f"{writer_id}_persona{suffix}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        print("   ✅ 全ライターの人格ファイルを保存しました。")

    def _create_persona_definitions(self, output_dir: str, suffix: str, loop_results: Dict = None):
        """ペルソナの人物像定義ファイルを生成・更新する"""
        print("👤 ペルソナ人格定義ファイルの生成・更新中...")

        base_personas = {
            "persona1": {
                "name": "美咲 (Misaki)",
                "age": 38,
                "occupation": "主婦、パートタイマー",
                "personality": "慎重で、家族の健康を第一に考える。広告はあまり信じないが、信頼できる友人や専門家の意見は参考にする。コストパフォーマンスを重視する現実主義者。",
                "evaluation_stance": "「本当にこの商品は私の家族にとって安全？」「価格に見合う価値はあるの？」という母親目線で厳しくチェックする。感情的な煽りよりも、具体的なメリットと安心感を求める。"
            },
            "persona2": {
                "name": "健一 (Kenichi)",
                "age": 45,
                "occupation": "ITエンジニア",
                "personality": "論理的思考の持ち主。製品のスペックや科学的根拠を重視する。感情論や曖昧な表現を嫌い、データに基づいた判断を好む。",
                "evaluation_stance": "「その効果に科学的な裏付けはあるのか？」「他の製品と比較して、どの指標が優れているのか？」という視点で、矛盾点や根拠の薄い部分を徹底的に洗い出す。"
            },
            "persona3": {
                "name": "あやか (Ayaka)",
                "age": 24,
                "occupation": "アパレル販売員",
                "personality": "トレンドに敏感で、SNSでの「映え」や口コミを重視する。新しいものが好きで、インフルエンサーの意見に影響されやすい。直感的で飽きっぽい一面も。",
                "evaluation_stance": "「これってインスタで自慢できる？」「友達に『何それ、面白い！』って言われるかな？」という視点で評価する。最初の3秒で惹きつけられない広告は即スキップする。"
            }
        }

        for persona_id, definition in base_personas.items():
            content = f"# {persona_id} 人格定義書 (Persona Definition)\n\n"
            content += f"## 名前: {definition['name']}\n"
            content += f"## 年齢: {definition['age']}歳\n"
            content += f"## 職業: {definition['occupation']}\n"
            content += f"## 性格・価値観\n{definition['personality']}\n\n"
            content += f"## 評価スタンス\n{definition['evaluation_stance']}\n"

            # TODO: Add logic for loop > 1 to reflect previous evaluation results
            # For now, the definitions are static per loop.

            file_path = os.path.join(output_dir, f"{persona_id}_definition{suffix}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print("   ✅ 全ペルソナの人物像定義ファイルを保存しました。")

def main():
    """MDエージェントのメイン実行フロー"""
    print("🚀 MD Agent 起動...")
    agent = MDAgent()
    
    # 役割宣言の自動送信
    if not agent.send_role_declarations_to_all_agents():
        print("❌ 役割宣言の送信に失敗しました。処理を中断します。")
        return
        
    # プロジェクトディレクトリの選択
    project_dir = "projects"
    projects = [d for d in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, d))]
    print("\n📁 利用可能なプロジェクト:")
    for i, p in enumerate(projects):
        print(f"  {i+1}: {p}")
    
    choice = input(f"\nプロジェクト番号を選択してください (1-{len(projects)}): ")
    try:
        project_name = projects[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ 不正な選択です。")
        return

    project_path = os.path.join(project_dir, project_name)
    agent.project_path = project_path # プロジェクトパスをエージェントに保存
    print(f"📂 プロジェクト '{project_name}' を使用します。")
    
    # CSVファイルの検索
    csv_files = [f for f in os.listdir(project_path) if f.endswith('.csv')]
    if not csv_files:
        print(f"❌ プロジェクト '{project_name}' にCSVファイルが見つかりません。")
        return
    csv_path = os.path.join(project_path, csv_files[0])
    
    # 1. CSV分析
    analysis_result = agent.analyze_csv_data(csv_path)
    
    # 2. 売れる台本パターンの分析
    script_patterns = agent.analyze_script_patterns(analysis_result["script_examples"])
    
    # 3. ペルソナ生成
    personas = agent.generate_personas_from_analysis(analysis_result, script_patterns)
    
    # 4. ★★★ 5つの必須戦略文書を作成 ★★★
    agent.create_strategic_documents(project_path, 1, None)
    
    # 5. 戦略ブリーフ作成 (CDへの指示)
    brief_for_cd = agent._format_strategic_brief(analysis_result, script_patterns, personas)
    
    # 6. CDへブリーフとペルソナ情報を送信
    if agent.send_brief_and_personas_to_cd(brief_for_cd, personas):
        print("\n✅ CDへの戦略ブリーフ送信完了。MDの初期タスクは完了です。")
        # ★★★ ここからCDからの報告待機ループに入る ★★★
        agent.listen_for_cd_reports()
    else:
        print("\n❌ CDへの戦略ブリーフ送信に失敗しました。")

if __name__ == "__main__":
    main()