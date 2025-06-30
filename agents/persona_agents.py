#!/usr/bin/env python3
"""
Persona Agent - A flexible, prompt-driven evaluation agent for BB-project.
"""
import json
import os
import re
from typing import List, Dict, Any

# Assuming a library for LLM calls exists
# from some_api import call_llm 

class PersonaAgent:
    """
    A single, flexible persona agent that evaluates scripts based on a dynamic prompt.
    The persona, criteria, and scripts to evaluate are not hardcoded but provided
    in a comprehensive prompt at runtime.
    """
    
    def __init__(self, persona_id: str):
        self.persona_id = persona_id
        self.model = "claude-3-haiku-20240307" # Use a fast model for evaluation

    def _call_anthropic_api(self, prompt: str) -> str:
        """
        Placeholder for calling a powerful language model like Claude.
        This simulates the API call and returns a structured JSON string.
        """
        print(f"🤖 {self.persona_id}: LLM API呼び出し（評価シミュレーション）...")
        import time
        time.sleep(10) # Evaluation takes time

        # This is a mock response. A real LLM would generate this based on the prompt.
        mock_evaluations = {}
        # The prompt contains script contents, so we can't easily know the IDs here.
        # This mock will just create dummy data for 15 scripts.
        for i in range(1, 16):
            script_key = f"script_{i}" # A generic key
            total_score = 70 + (i % 5) * 5
            mock_evaluations[script_key] = {
                "total_score": total_score,
                "feedback": f"[{self.persona_id}として] この台本はなかな興味深いですが、改善の余地があります。特に... (シミュレーションされたフィードバック)",
                "breakdown": {
                    "項目1": {"score": total_score - 10, "feedback": "具体的なフィードバック..."},
                    "項目2": {"score": total_score + 5, "feedback": "具体的なフィードバック..."},
                }
            }
        
        mock_response = {"evaluations": mock_evaluations}
        
        print(f"🤖 {self.persona_id}: LLM API応答受信（評価シミュレーション）")
        return json.dumps(mock_response)

    def evaluate_scripts(self, full_prompt: str) -> Dict[str, Any]:
        """
        Evaluates multiple scripts based on a single, comprehensive prompt.
        The prompt should contain the persona definition, evaluation criteria,
        and all scripts to be evaluated.
        """
        print(f"📊 {self.persona_id}: 新しい人格と基準に基づき、全台本の一括評価を開始...")

        system_prompt = """
あなたは、与えられた「ペルソナ（人格）」に完璧になりきり、指定された「評価基準」だけを使って、提示された複数の「評価対象台本」を厳密に評価する専門家です。
評価結果は、必ず指示されたJSON形式で、キーと値を正確に守って出力してください。他のテキスト、解説、言い訳などは一切含めないでください。
"""

        final_user_prompt = f"""
{full_prompt}

---
【最終タスク】
上記の「あなたのペルソナ」「評価基準」「評価対象台本」の3つの情報を完全かつ厳密に守り、すべての台本を評価してください。

1.  **ペルソナへの没入**: あなた自身の知識や意見は完全に排除し、指定されたペルソナの性格、価値観、評価スタンスに100%なりきって評価してください。
2.  **基準の遵守**: 指定された評価基準の項目と配点のみを使用してください。それ以外の観点で評価してはいけません。
3.  **JSON形式での出力**: 結果は必ず以下のJSON形式で出力してください。
    -   トップレベルのキーは `evaluations` としてください。
    -   その値は、各台本の「ファイル名」をキーとしたオブジェクトです。
    -   各オブジェクトには `total_score` (数値), `feedback` (文字列), `breakdown` (オブジェクト) を含めてください。
    -   `breakdown` オブジェクトには、評価基準の各項目名をキーとし、`score` (数値) と `feedback` (文字列) を持つオブジェクトを値としてください。

【出力形式の例】
{{
  "evaluations": {{
    "writer1_台本1_loop1_... .md": {{
      "total_score": 85,
      "feedback": "ペルソナになりきった総合的なフィードバック...",
      "breakdown": {{
        "フックのインパクト": {{
          "score": 22,
          "feedback": "最初の3秒の掴みは素晴らしい..."
        }},
        "メッセージの明確さ": {{
          "score": 18,
          "feedback": "伝えたいことは分かるが、少し表現が冗長..."
        }}
      }}
    }},
    "writer1_台本2_loop1_... .md": {{
      "total_score": 72,
      "feedback": "...",
      "breakdown": {{ ... }}
    }}
  }}
}}
"""
        # In a real implementation, you would use the 'anthropic' library
        # raw_json_response = client.messages.create(...)
        
        raw_json_response = self._call_anthropic_api(final_user_prompt)

        try:
            data = json.loads(raw_json_response)
            evaluations = data.get("evaluations", {})
            if isinstance(evaluations, dict) and evaluations:
                print(f"✅ {self.persona_id}: 全台本の評価JSONの解析に成功しました。")
                return evaluations
            else:
                print(f"❌ {self.persona_id}: LLMからのJSON形式が不正です。")
                return {"error": "LLM response was not a valid evaluation dictionary.", "raw_response": raw_json_response}
        except json.JSONDecodeError:
            print(f"❌ {self.persona_id}: LLMからの応答がJSONとしてパースできませんでした。")
            return {"error": "Failed to decode JSON from LLM response.", "raw_response": raw_json_response}

    def get_persona_profile(self) -> Dict[str, Any]:
        """
        Returns a generic description. The true profile is now defined by the prompt.
        """
        return {
            "personality": "プロンプトに基づく動的人格",
            "age_group": "プロンプトに基づく",
            "judgment_criteria": "MDの指示により毎回変化"
        }