#!/usr/bin/env python3
"""
Message Handler for BB-project Agents
Provides message reception and processing capabilities for automated agents
"""

import os
import time
import threading
from typing import Callable, Optional, Dict, Any
from datetime import datetime

class MessageHandler:
    """Base message handler for BB-project agents"""
    
    def __init__(self, agent_name: str, message_processor: Callable[[str], None]):
        self.agent_name = agent_name
        self.message_processor = message_processor
        self.message_file = f"../messages/{agent_name}_inbox.txt"
        self.processed_messages = set()
        self.listening = False
        self.listen_thread = None
        
    def start_listening(self):
        """Start listening for incoming messages"""
        if self.listening:
            print(f"🔊 {self.agent_name} は既にメッセージ受信中です")
            return
        
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        print(f"🔊 {self.agent_name} メッセージ受信開始")
    
    def stop_listening(self):
        """Stop listening for messages"""
        self.listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        print(f"🔇 {self.agent_name} メッセージ受信停止")
    
    def _listen_loop(self):
        """Message listening loop"""
        while self.listening:
            try:
                self._check_for_messages()
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"❌ {self.agent_name} メッセージ受信エラー: {e}")
                time.sleep(5)  # Wait longer if error occurs
    
    def _check_for_messages(self):
        """Check for new messages in inbox file"""
        if not os.path.exists(self.message_file):
            return
        
        try:
            with open(self.message_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and line not in self.processed_messages:
                    self._process_message(line)
                    self.processed_messages.add(line)
                    
        except Exception as e:
            print(f"❌ {self.agent_name} メッセージファイル読み込みエラー: {e}")
    
    def _process_message(self, message_line: str):
        """Process a single message line"""
        try:
            # Extract timestamp and message
            if message_line.startswith('[') and '] ' in message_line:
                timestamp_end = message_line.find('] ')
                timestamp = message_line[1:timestamp_end]
                message = message_line[timestamp_end + 2:]
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = message_line
            
            print(f"📨 {self.agent_name} メッセージ受信 [{timestamp}]: {message[:100]}...")
            
            # Process the message using the provided processor
            self.message_processor(message)
            
        except Exception as e:
            print(f"❌ {self.agent_name} メッセージ処理エラー: {e}")
    
    def send_message(self, target_agent: str, message: str):
        """Send message to another agent"""
        try:
            import subprocess
            result = subprocess.run(
                ["./agent-send.sh", target_agent, message],
                capture_output=True,
                text=True,
                cwd="../.."
            )
            
            if result.returncode == 0:
                print(f"📤 {self.agent_name} → {target_agent}: メッセージ送信完了")
            else:
                print(f"❌ {self.agent_name} → {target_agent}: 送信失敗 - {result.stderr}")
                
        except Exception as e:
            print(f"❌ {self.agent_name} メッセージ送信エラー: {e}")


class AgentRunner:
    """Base runner class for automated agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.message_handler = MessageHandler(agent_name, self.process_message)
        self.running = False
    
    def start(self):
        """Start the agent"""
        print(f"🚀 {self.agent_name} Agent 起動中...")
        self.running = True
        self.message_handler.start_listening()
        self.initialize_agent()
        
        try:
            while self.running:
                self.agent_loop()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n🛑 {self.agent_name} Agent 停止中...")
        finally:
            self.shutdown_agent()
    
    def stop(self):
        """Stop the agent"""
        self.running = False
        self.message_handler.stop_listening()
    
    def initialize_agent(self):
        """Initialize agent-specific setup (override in subclasses)"""
        pass
    
    def agent_loop(self):
        """Main agent loop (override in subclasses)"""
        pass
    
    def process_message(self, message: str):
        """Process incoming messages (override in subclasses)"""
        print(f"💬 {self.agent_name} デフォルトメッセージ処理: {message[:50]}...")
    
    def shutdown_agent(self):
        """Cleanup when shutting down (override in subclasses)"""
        print(f"👋 {self.agent_name} Agent 終了")
    
    def send_message(self, target_agent: str, message: str):
        """Send message to another agent"""
        self.message_handler.send_message(target_agent, message)


if __name__ == "__main__":
    # Demo usage
    print("Message Handler Demo")
    
    def demo_processor(message):
        print(f"DEMO: 受信メッセージ = {message}")
    
    handler = MessageHandler("demo", demo_processor)
    handler.start_listening()
    
    try:
        print("デモ実行中... Ctrl+C で終了")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handler.stop_listening()
        print("\nデモ終了")