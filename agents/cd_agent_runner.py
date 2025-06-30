#!/usr/bin/env python3
"""
CD Agent Runner - Automated Creative Director
Handles automated coordination of Writers and Personas
"""

import sys
import os
import re
import time
from message_handler import AgentRunner
from cd_agent import CDAgent

class CDAgentRunner(AgentRunner):
    """Automated CD Agent Runner"""
    
    def __init__(self):
        super().__init__("cd")
        self.cd_agent = CDAgent()
        self.waiting_for_brief = True
        self.waiting_for_writers = False
        self.waiting_for_personas = False
        self.writer_responses = {}
        self.persona_responses = {}
        
    def initialize_agent(self):
        """Initialize CD agent"""
        print("🎬 CD Agent 自動化モード開始")
        print("📋 戦略ブリーフ待機中...")
        
    def process_message(self, message: str):
        """Process incoming messages from MD, Writers, or Personas"""
        print(f"📨 CD受信: {message[:100]}...")
        
        if self.waiting_for_brief and "戦略ブリーフ" in message:
            self._handle_strategic_brief(message)
        elif self.waiting_for_writers and ("台本完了報告" in message or "Writer" in message):
            self._handle_writer_response(message)
        elif self.waiting_for_personas and ("評価完了" in message or "Persona" in message):
            self._handle_persona_response(message)
        else:
            print(f"💭 CD: 未対応メッセージタイプ")
    
    def _handle_strategic_brief(self, message: str):
        """Handle strategic brief from MD"""
        print("📋 戦略ブリーフ受信・処理開始")
        
        # Extract brief and personas from message
        self.cd_agent.receive_strategic_brief_and_personas(message)
        self.waiting_for_brief = False
        
        # Start creation loop
        print("🔄 台本制作ループ開始")
        self._start_creation_cycle()
    
    def _start_creation_cycle(self):
        """Start a creation cycle"""
        self.cd_agent.current_loop += 1
        print(f"=== Loop {self.cd_agent.current_loop} 開始 ===")
        
        # Clear previous responses
        self.writer_responses = {}
        self.persona_responses = {}
        
        # Send instructions to writers
        self._instruct_writers()
        self.waiting_for_writers = True
    
    def _instruct_writers(self):
        """Send instructions to all writers"""
        print("📝 Writer指示送信中...")
        
        writers = ["writer1", "writer2", "writer3"]
        
        for writer in writers:
            instruction = f"""あなたは{writer}です。

{self.cd_agent.writer_prompts[writer]}

【戦略ブリーフ】
{self.cd_agent.strategic_brief}

【台本制作要件】
**動画長さ:** 45〜59秒
**制作本数:** 3本（それぞれ異なるアプローチで制作）

#### **台本の構成（全3本共通）**
1. **フック（1シーン目 / 0.2〜3秒）**
- **最重要ポイント**（視聴者が「なんで？」と感じる驚き・共感・問題提起）
- 強い興味を引く要素
- **共感セグメント**
- **既存概念の否定**
- **「見る理由」＝「買う理由」になっているかをチェック**

2. **2〜3シーン目（3〜15秒）**
- 1シーン目で生じた **視聴者の疑問に即答する構成**
- **「なんで？」の回答をスピーディーに提示し、納得感を生む**

3. **4〜5シーン目（15〜35秒）**
- **徐々に納得感を高める情報を提供**
- **権威性・体験談・視覚的な変化の演出**を活用
- **一貫性を保ち、視聴者がスムーズに「試したくなる」流れを作る**

4. **6〜7シーン目（35〜50秒）**
- **オファー（お得感）提示**
- 価格や特典を視覚的に強調し、**「試してみようかな」と思わせる**

5. **8シーン目（50〜59秒）**
- **CTA（今すぐ行動を促す）**
- **「この動画を見た人だけ！」と特別感を演出**
- **「本日終了、無くなる前に急げ！」のように緊急性を強調**

#### **3本のバリエーション指針**
- **台本1**: 基本アプローチ（あなたのコアスタイルを活かした王道パターン）
- **台本2**: 強化アプローチ（あなたの特徴をさらに強調したバージョン）
- **台本3**: 実験的アプローチ（新しい角度や表現方法にチャレンジ）

Loop {self.cd_agent.current_loop}の台本を3本制作し、完了したら報告してください。

【重要】台本保存について：
制作した台本は以下の形式でCSVファイルと同じディレクトリに自動保存してください：
- ファイル名: {writer}_台本1_{loop}_{timestamp}.md
- ファイル名: {writer}_台本2_{loop}_{timestamp}.md  
- ファイル名: {writer}_台本3_{loop}_{timestamp}.md
- 保存場所: プロジェクトのCSVファイルがあるディレクトリ直下
- 形式: Markdown形式（.md）

例：writer1_台本1_loop1_20241230.md"""

            self.send_message(writer, instruction)
    
    def _handle_writer_response(self, message: str):
        """Handle response from writers"""
        # Extract writer ID from message
        writer_id = None
        for writer in ["writer1", "writer2", "writer3"]:
            if writer.upper() in message:
                writer_id = writer
                break
        
        if writer_id:
            print(f"✅ {writer_id} 台本受信")
            self.writer_responses[writer_id] = message
            
            # Check if all writers have responded
            if len(self.writer_responses) == 3:
                print("📊 全Writer完了・Persona評価開始")
                self.waiting_for_writers = False
                self._instruct_personas()
    
    def _instruct_personas(self):
        """Send evaluation instructions to personas"""
        print("📊 Persona評価指示送信中...")
        
        # Format scripts for evaluation
        scripts_text = self._format_scripts_for_evaluation()
        
        personas = ["persona1", "persona2", "persona3"]
        
        for persona in personas:
            persona_config = self.cd_agent._get_persona_config(persona)
            
            instruction = f"""あなたは{persona}です。

【あなたの特性】
{persona_config}

【評価対象台本】
{scripts_text}

【評価要求】
各台本を以下の基準で100点満点で評価してください：

1. **フックの強度（25点）**: 冒頭のインパクトと関心喚起力
2. **論理性（20点）**: 構成の論理性と説得力
3. **感情的響き（20点）**: ターゲットへの感情的訴求力
4. **購入動機（20点）**: 今すぐ買いたくなる度合い
5. **信頼性（15点）**: 安心感と信頼度

**評価フォーマット**
Writer1-1台本: [点数]/100点
理由: [具体的なフィードバック]

Writer1-2台本: [点数]/100点
理由: [具体的なフィードバック]

Writer1-3台本: [点数]/100点
理由: [具体的なフィードバック]

Writer2-1台本: [点数]/100点
理由: [具体的なフィードバック]

Writer2-2台本: [点数]/100点
理由: [具体的なフィードバック]

Writer2-3台本: [点数]/100点
理由: [具体的なフィードバック]

Writer3-1台本: [点数]/100点
理由: [具体的なフィードバック]

Writer3-2台本: [点数]/100点
理由: [具体的なフィードバック]

Writer3-3台本: [点数]/100点
理由: [具体的なフィードバック]

評価完了後、報告してください。"""

            self.send_message(persona, instruction)
        
        self.waiting_for_personas = True
    
    def _format_scripts_for_evaluation(self) -> str:
        """Format received scripts for persona evaluation"""
        formatted = ""
        
        for writer_id in ["writer1", "writer2", "writer3"]:
            if writer_id in self.writer_responses:
                response = self.writer_responses[writer_id]
                formatted += f"\n== {writer_id.upper()}台本 ==\n"
                formatted += f"{response}\n"
        
        return formatted
    
    def _handle_persona_response(self, message: str):
        """Handle evaluation response from personas"""
        # Extract persona ID from message
        persona_id = None
        for persona in ["persona1", "persona2", "persona3"]:
            if persona.upper() in message:
                persona_id = persona
                break
        
        if persona_id:
            print(f"✅ {persona_id} 評価受信")
            self.persona_responses[persona_id] = message
            
            # Check if all personas have responded
            if len(self.persona_responses) == 3:
                print("📊 全Persona評価完了・集約開始")
                self.waiting_for_personas = False
                self._aggregate_and_report()
    
    def _aggregate_and_report(self):
        """Aggregate evaluations and report to MD"""
        print("📊 評価集約・MD報告中...")
        
        # Simple evaluation aggregation (for demo)
        approved_scripts = []
        writer_scores = {"writer1": 85, "writer2": 88, "writer3": 92}  # Demo scores
        
        # Create report
        report = f"""【Loop {self.cd_agent.current_loop} 完了報告】

## 承認台本数: {len(approved_scripts)}本

### Writer成績
- writer1: {writer_scores['writer1']:.1f}点
- writer2: {writer_scores['writer2']:.1f}点  
- writer3: {writer_scores['writer3']:.1f}点

### 次ステップ
{"🎯 全Writer目標達成！最終選定に進みます。" if all(s >= 90 for s in writer_scores.values()) else "🔄 継続: プロンプト改善が必要"}

### 受信データ
Writer応答数: {len(self.writer_responses)}
Persona応答数: {len(self.persona_responses)}
"""
        
        self.send_message("md", report)
        
        # Check if we should continue
        if all(score >= 90 for score in writer_scores.values()):
            print("🎯 全Writer目標達成！ループ完了")
        else:
            print("🔄 継続判定: プロンプト改善が必要")
            # Could implement automatic loop continuation here
    
    def agent_loop(self):
        """Main agent loop"""
        # The message handler takes care of processing, so we just maintain state
        pass


def main():
    """Run CD Agent"""
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("🎬 CD Agent デモモード")
        # Demo mode for testing
    
    cd_runner = CDAgentRunner()
    cd_runner.start()


if __name__ == "__main__":
    main()