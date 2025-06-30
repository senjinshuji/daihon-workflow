#!/usr/bin/env python3
"""
Persona Agent Runner - Automated Persona Evaluation Agents
Handles automated script evaluation based on dynamic, file-based instructions.
"""

import sys
import os
import re
import glob
import json
from datetime import datetime
from message_handler import AgentRunner
from persona_agents import PersonaAgent # Use the new flexible agent

class PersonaAgentRunner(AgentRunner):
    """Automated Persona Agent Runner"""
    
    def __init__(self, persona_id: str):
        super().__init__(persona_id)
        self.persona_id = persona_id
        # Create a single, flexible persona agent instance
        self.persona_agent = PersonaAgent(persona_id)
        
    def initialize_agent(self):
        """Initialize persona agent"""
        print(f"📊 {self.persona_id.upper()} Agent 自動化モード開始")
        print("📋 CD評価依頼待機中...")
    
    def process_message(self, message: str):
        """Process incoming messages from CD"""
        print(f"📨 {self.persona_id} 受信: {message[:100]}...")
        
        # New instruction format: [PROJECT:{project_name}] [LOOP:{loop_num}] [EVALUATE]
        match = re.search(r"\[PROJECT:(.+?)\] \[LOOP:(\d+)\] \[EVALUATE\]", message)
        
        if match:
            project_name = match.group(1)
            loop_num = int(match.group(2))
            self._handle_evaluation_task(project_name, loop_num)
        else:
            print(f"💭 {self.persona_id}: 未対応のメッセージ形式です。`[PROJECT:...] [LOOP:...] [EVALUATE]` 形式を待機します。")
    
    def _handle_evaluation_task(self, project_name: str, loop_num: int):
        """Handles the entire evaluation process based on parsed instructions."""
        print(f"📊 {self.persona_id} 評価タスク開始... (Project: {project_name}, Loop: {loop_num})")

        project_path = os.path.join("projects", project_name)
        suffix = f"_loop{loop_num}" if loop_num > 1 else ""

        # 1. Read definition and criteria files
        try:
            persona_def_file = os.path.join(project_path, f"{self.persona_id}_definition{suffix}.md")
            criteria_file = os.path.join(project_path, f"persona_evaluation_criteria{suffix}.md")

            with open(persona_def_file, 'r', encoding='utf-8') as f:
                persona_def_content = f.read()
            with open(criteria_file, 'r', encoding='utf-8') as f:
                criteria_content = f.read()
        except FileNotFoundError as e:
            self._report_error(f"必要な定義/基準ファイルが見つかりません: {e}")
            return

        # 2. Find and read all script files for the current loop
        scripts_content, script_files_map = self._find_and_read_scripts(project_path, loop_num)
        if not scripts_content:
            self._report_error(f"Loop {loop_num} の評価対象台本が '{project_path}' に見つかりません。")
            return

        # 3. Build the full prompt for the agent
        full_prompt = f"""
# あなたのペルソナ (Your Persona)
{persona_def_content}

---

# 評価基準 (Evaluation Criteria)
{criteria_content}

---

# 評価対象台本 (Scripts to Evaluate)
{scripts_content}
"""
        # 4. Call the agent to evaluate all scripts at once
        evaluations = self.persona_agent.evaluate_scripts(full_prompt)
        
        if "error" in evaluations:
            self._report_error(f"台本評価中にエラーが発生しました: {evaluations['error']}", evaluations.get('raw_response'))
            return
            
        # 5. Format and send the completion report to CD
        report = self._create_evaluation_report(evaluations, script_files_map)
        self.send_message("cd", report)
        
        print(f"✅ {self.persona_id} [Loop {loop_num}] の全評価タスク完了。次依頼待機中...")

    def _find_and_read_scripts(self, project_path: str, loop_num: int) -> tuple[str, dict]:
        """Finds all script files for the loop, reads them, and returns combined content."""
        print(f"  🔍 {project_path} 内で Loop {loop_num} の台本を検索中...")
        # Adhering to the new rule: scripts are in the project folder root
        # We also need to correct the writer to save here. For now, we search both.
        search_path_root = os.path.join(project_path, f"*_loop{loop_num}_*.md")
        search_path_results = os.path.join(project_path, "results", f"*_loop{loop_num}_*.md")
        
        script_files = glob.glob(search_path_root) + glob.glob(search_path_results)
        
        # Filter out non-script files like instructions
        script_files = [f for f in script_files if re.search(r'writer\d+_台本\d+', os.path.basename(f))]

        if not script_files:
            return "", {}

        print(f"  📂 {len(script_files)}個の台本ファイルを発見。")
        
        all_scripts_text = ""
        script_map = {}
        for i, file_path in enumerate(script_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_name = os.path.basename(file_path)
                script_map[f"script_{i+1}"] = file_name # Generic key for the mock, real would use filename
                
                all_scripts_text += f"## 台本ファイル名: {file_name}\n\n"
                all_scripts_text += f"```markdown\n{content}\n```\n\n---\n\n"
            except Exception as e:
                print(f"   -> ⚠️ ファイル読み込みエラー: {file_path} ({e})")
                continue
                
        return all_scripts_text, script_map

    def _create_evaluation_report(self, evaluations: dict, script_files_map: dict) -> str:
        """Creates a formatted evaluation report for the CD."""
        profile = self.persona_agent.get_persona_profile()
        report_title = f"【{self.persona_id.upper()} 評価完了報告】"
        
        report = f"""{report_title}

ペルソナタイプ: {profile['personality']} ({self.persona_id})
評価完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        # The mock response from the agent uses generic keys like "script_1".
        # A real response would use the filenames as keys. We handle both.
        # This mapping part is a bit of a hack to make the simulation work.
        is_mock_response = any(key.startswith("script_") for key in evaluations.keys())
        
        sorted_eval_items = sorted(evaluations.items(), key=lambda item: str(item[0]))

        for key, evaluation in sorted_eval_items:
            file_name = script_files_map.get(key, key) # Get real filename if available
            
            report += f"### 評価対象: {file_name}\n"
            report += f"**総合スコア: {evaluation.get('total_score', 'N/A')}/100点**\n\n"
            report += f"**総評:**\n{evaluation.get('feedback', '評価コメントがありません。')}\n\n"
            
            if "breakdown" in evaluation and isinstance(evaluation['breakdown'], dict):
                report += "**詳細評価:**\n"
                for criterion, details in evaluation['breakdown'].items():
                    score = details.get('score', 'N/A')
                    feedback = details.get('feedback', '')
                    report += f"- **{criterion}:** {score}点\n  - {feedback}\n"
            report += "\n---\n"
            
        return report

    def _report_error(self, error_message: str, raw_response: str = None):
        """Reports an error to the console and to the CD."""
        print(f"❌ {self.persona_id}: {error_message}")
        full_error = f"【{self.persona_id.upper()} ERROR】\n{error_message}"
        if raw_response:
            full_error += f"\n\n[RAW_RESPONSE]\n{raw_response[:500]}..."
        self.send_message("cd", full_error)

def main():
    """Run Persona Agent"""
    if len(sys.argv) < 2:
        print("実行引数エラー: python persona_agent_runner.py [persona1|persona2|persona3]")
        sys.exit(1)
        
    persona_id = sys.argv[1]
    
    runner = PersonaAgentRunner(persona_id)
    runner.run()

if __name__ == "__main__":
    main()