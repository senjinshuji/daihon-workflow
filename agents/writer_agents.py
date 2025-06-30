#!/usr/bin/env python3
"""
Writer Agent - A flexible, prompt-driven creative agent for BB-project.
"""
import json
import os
import re
from typing import List, Dict

# anthropicライブラリや他のAPI呼び出しライブラリを想定
# from some_api import call_llm 

class WriterAgent:
    """
    A single, flexible writer agent that generates scripts based on a dynamic prompt.
    The persona and instructions are not hardcoded but provided in the prompt.
    """
    
    def __init__(self, writer_id: str):
        self.writer_id = writer_id
        self.model = "claude-3-sonnet-20240229" # or another powerful model

    def _call_anthropic_api(self, prompt: str) -> str:
        """
        Placeholder for calling a powerful language model like Claude 3.
        In a real implementation, this would use the anthropic library,
        handle API keys, and include error handling.
        For now, it returns a structured JSON string for simulation.
        """
        print(f"🤖 {self.writer_id}: LLM API呼び出し（シミュレーション）...")
        # Simulate a delay for the API call
        import time
        time.sleep(5)

        # This is a mock response. A real LLM would generate this based on the prompt.
        mock_scripts = [
            f"【{self.writer_id}作: 台本アプローチ1】\n結婚式のスピーチ、緊張しますよね？「おめでとう」の気持ち、しっかり伝わっていますか？... (シミュレーションされた台本)...",
            f"【{self.writer_id}作: 台本アプローチ2】\n「感動のスピーチだった」って言われたいあなたへ。実は、たった3つのコツがあるんです。... (シミュレーションされた台本)...",
            f"【{self.writer_id}作: 台本アプローチ3】\n友人代表スピーチで、新郎の昔の失敗談を話すのはもう古い！今、心に響くのは... (シミュレーションされた台本)...",
            f"【{self.writer_id}作: 台本アプローチ4】\nデータで見る、成功する結婚式スピーチ。9割の人が知らない、たった1つの共通点とは？... (シミュレーションされた台本)...",
            f"【{self.writer_id}作: 台本アプローチ5】\nスマホのメモを読むだけのスピーチ、やめませんか？あなたの言葉で、最高の祝福を。... (シミュレーションされた台本)..."
        ]
        
        mock_response = {"scripts": mock_scripts}
        
        print(f"🤖 {self.writer_id}: LLM API応答受信（シミュレーション）")
        return json.dumps(mock_response)

    def create_scripts_from_prompt(self, full_prompt: str) -> List[str]:
        """
        Generates multiple script variations from a single, comprehensive prompt.
        The prompt should contain the persona, instructions, and task.
        """
        print(f"✍️ {self.writer_id}: 新しい人格と指示に基づき、5本の台本制作を開始...")

        # The system prompt sets the stage for the AI's task.
        system_prompt = """
あなたは、与えられた人格と指示書を完璧に理解し、多様なアウトプットを出すプロの動画広告台本作家です。
最終的なアウトプットは、必ず指定されたJSON形式で返してください。他のテキストは一切含めないでください。
"""

        # The user prompt combines the instructions from the files with the specific task.
        final_user_prompt = f"""
{full_prompt}

---
【最終タスク】
上記の人格と指示書に完全になりきり、以下の要件で5本の動画広告台本を制作してください。

1.  **多様性**: 5本はそれぞれ異なる切り口やアプローチを試してください。例えば、「基本」「感情強調」「意外な事実」「ターゲットへの問いかけ」「大胆な提案」など、創造性を発揮してください。
2.  **品質**: 各台本は、それ単体で成立する完成度を持つ必要があります。
3.  **形式**: 結果は必ず以下のJSON形式で出力してください。キーは "scripts" とし、値は5本の台本文字列を含む配列とします。

【出力形式の例】
{{
  "scripts": [
    "1本目の台本テキスト...",
    "2本目の台本テキスト...",
    "3本目の台本テキスト...",
    "4本目の台本テキスト...",
    "5本目の台本テキスト..."
  ]
}}
"""
        # In a real implementation, you would use the 'anthropic' library like this:
        # client = anthropic.Anthropic(api_key="YOUR_API_KEY")
        # response = client.messages.create(
        #     model=self.model,
        #     max_tokens=4096,
        #     system=system_prompt,
        #     messages=[{"role": "user", "content": final_user_prompt}],
        #     response_format={"type": "json_object"},
        # )
        # raw_json_response = response.content[0].text
        
        # For this project, we use our simulation function.
        raw_json_response = self._call_anthropic_api(final_user_prompt)

        try:
            # The response is expected to be a JSON string.
            data = json.loads(raw_json_response)
            scripts = data.get("scripts", [])
            if isinstance(scripts, list) and len(scripts) == 5:
                print(f"✅ {self.writer_id}: 5本の台本生成に成功しました。")
                return scripts
            else:
                print(f"❌ {self.writer_id}: LLMからのJSON形式が不正です。 received: {scripts}")
                return [f"エラー: LLMからの応答形式が不正でした。{raw_json_response}"] * 5
        except json.JSONDecodeError:
            print(f"❌ {self.writer_id}: LLMからの応答がJSONとしてパースできませんでした。")
            return [f"エラー: LLMの応答がJSONではありませんでした。{raw_json_response}"] * 5

    def get_writing_style(self) -> Dict[str, str]:
        """
        Returns a generic description. The true style is now defined by the prompt.
        """
        return {
            "concept": "プロンプトに基づく動的人格",
            "target": "プロンプトに基づく",
            "characteristics": "MDの指示により毎回変化"
        }


class WriterAgentManager:
    """Writer エージェント管理クラス"""
    
    def __init__(self):
        self.writers = {
            "writer1": WriterAgent("writer1"),
            "writer2": WriterAgent("writer2"),
            "writer3": WriterAgent("writer3")
        }
    
    def process_instruction(self, writer_id: str, instruction: str):
        """特定のWriterに指示処理"""
        if writer_id in self.writers:
            writer = self.writers[writer_id]
            writer.receive_instruction(instruction)
            writer.report_completion()
        else:
            print(f"❌ 不明なWriter ID: {writer_id}")
    
    def get_all_writers(self) -> Dict[str, WriterAgent]:
        """全Writer取得"""
        return self.writers


def main():
    """Writer エージェント実行"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用法: python writer_agents.py [writer1|writer2|writer3]")
        return
    
    writer_id = sys.argv[1]
    print(f"🚀 {writer_id.upper()} Agent 起動...")
    
    manager = WriterAgentManager()
    
    # デモ指示（実際はCDから受信）
    demo_instruction = """【台本制作指示】
戦略ブリーフ: ラクトロン腸内環境改善サプリの台本制作
要件: 45-59秒の動画広告台本
スタイル: 各Writerの特性を活かした独自アプローチ
"""
    
    manager.process_instruction(writer_id, demo_instruction)

if __name__ == "__main__":
    main()