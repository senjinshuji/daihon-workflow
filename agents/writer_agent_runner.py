#!/usr/bin/env python3
"""
Writer Agent Runner - Automated Writer Agents
Handles automated script creation based on dynamic instructions.
"""

import sys
import os
import re
import time
from datetime import datetime
from message_handler import AgentRunner
from writer_agents import WriterAgent # Use the new flexible agent

class WriterAgentRunner(AgentRunner):
    """Automated Writer Agent Runner"""
    
    def __init__(self, writer_id: str):
        super().__init__(writer_id)
        self.writer_id = writer_id
        # Create a single, flexible writer agent instance
        self.writer_agent = WriterAgent(writer_id)
        
    def initialize_agent(self):
        """Initialize writer agent"""
        print(f"✍️ {self.writer_id.upper()} Agent 自動化モード開始")
        print("📋 CD指示待機中...")
    
    def process_message(self, message: str):
        """Process incoming messages from CD"""
        print(f"📨 {self.writer_id} 受信: {message[:100]}...")
        
        # New instruction format: [PROJECT:{project_name}] [LOOP:{loop_num}]
        match = re.search(r"\[PROJECT:(.+?)\] \[LOOP:(\d+)\]", message)
        
        if match:
            project_name = match.group(1)
            loop_num = int(match.group(2))
            self._handle_script_generation_task(project_name, loop_num)
        else:
            print(f"💭 {self.writer_id}: 未対応のメッセージ形式です。`[PROJECT:...] [LOOP:...]` 形式を待機します。")
    
    def _handle_script_generation_task(self, project_name: str, loop_num: int):
        """Handles the entire script generation process based on parsed instructions."""
        print(f"📝 {self.writer_id} 台本制作開始... (Project: {project_name}, Loop: {loop_num})")

        # 1. Construct file paths
        project_path = os.path.join("projects", project_name)
        suffix = f"_loop{loop_num}" if loop_num > 1 else ""
        
        persona_file = os.path.join(project_path, f"{self.writer_id}_persona{suffix}.md")
        instructions_file = os.path.join(project_path, f"copywriter_instructions{suffix}.md")

        # 2. Read instruction files
        try:
            with open(persona_file, 'r', encoding='utf-8') as f:
                persona_content = f.read()
            with open(instructions_file, 'r', encoding='utf-8') as f:
                instructions_content = f.read()
        except FileNotFoundError as e:
            error_message = f"❌ {self.writer_id}: 必要な指示書ファイルが見つかりません: {e}"
            print(error_message)
            self.send_message("cd", f"【{self.writer_id.upper()} ERROR】\n{error_message}")
            return

        # 3. Build the full prompt for the agent
        full_prompt = f"""
# あなたの人格 (Persona)
{persona_content}

---

# 全体指示書 (General Instructions)
{instructions_content}
"""
        
        # 4. Call the agent to create scripts
        scripts = self.writer_agent.create_scripts_from_prompt(full_prompt)
        
        if not scripts or "エラー:" in scripts[0]:
            error_message = f"❌ {self.writer_id}: 台本生成中にエラーが発生しました。"
            print(error_message)
            self.send_message("cd", f"【{self.writer_id.upper()} ERROR】\n{error_message}\n{scripts[0]}")
            return
            
        # 5. Auto-save scripts to the project directory
        self._auto_save_scripts(scripts, project_name, loop_num)
        
        # 6. Format and send the completion report to CD
        report = self._create_completion_report(scripts, loop_num)
        print(f"📤 {self.writer_id} 台本完了報告送信中...")
        self.send_message("cd", report)
        
        print(f"✅ {self.writer_id} [Loop {loop_num}] の全タスク完了。次指示待機中...")

    def _create_completion_report(self, scripts: list, loop_num: int) -> str:
        """Create a formatted completion report for the CD."""
        style_info = self.writer_agent.get_writing_style()
        
        report_title = f"【{self.writer_id.upper()} Loop {loop_num} 台本完了報告】"
        
        report = f"""{report_title}

制作台本数: {len(scripts)}本

"""
        
        for i, script in enumerate(scripts, 1):
            # Generic approach name, as the variation is inside the script itself
            approach = f"提案{i}"
            report += f"""--- 台本{i} ({approach}) ---\n{script}\n\n"""
        
        report += f"""---
制作コンセプト: {style_info['concept']}
完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report

    def _auto_save_scripts(self, scripts: list, project_name: str, loop_num: int):
        """Saves the generated scripts to the correct project directory."""
        try:
            project_dir = os.path.join("projects", project_name, "results")
            os.makedirs(project_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            print(f"📁 {self.writer_id} 台本自動保存開始...")
            
            for i, script in enumerate(scripts, 1):
                # Simplified and robust filename
                filename = f"{self.writer_id}_台本{i}_loop{loop_num}_{timestamp}.md"
                filepath = os.path.join(project_dir, filename)
                
                # Create script content for the file
                style_info = self.writer_agent.get_writing_style()
                content = f"""# {self.writer_id.upper()} 台本{i}

## 制作情報
- **Project**: {project_name}
- **Writer**: {self.writer_id}
- **Loop**: {loop_num}
- **制作日時**: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}
- **人格**: {style_info['concept']}

## 台本内容

{script}

---
*BB-Project自動生成台本*
"""
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   -> 保存完了: {filename}")
            
            print(f"✅ {self.writer_id}: 全{len(scripts)}本の台本を {project_dir} に保存しました。")
            
        except Exception as e:
            print(f"❌ {self.writer_id} 台本自動保存エラー: {e}")
            # Optionally, report this error back to the CD
            self.send_message("cd", f"【{self.writer_id.upper()} SAVE ERROR】\n台本の自動保存に失敗しました: {e}")

def main():
    """Run Writer Agent"""
    if len(sys.argv) < 2:
        print("実行引数エラー: python writer_agent_runner.py [writer1|writer2|writer3]")
        sys.exit(1)
        
    writer_id = sys.argv[1]
    
    runner = WriterAgentRunner(writer_id)
    runner.run()

if __name__ == "__main__":
    main()