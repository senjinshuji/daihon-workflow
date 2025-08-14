#!/usr/bin/env python3
"""
GitHub Actions出力形式を修正するスクリプト
全てのPythonスクリプトで以下を適用：
1. 絵文字を含むprintをstderrへ
2. GitHub Actions用のkey=value出力のみstdoutへ
3. エラーメッセージはstderrへ
"""

import os
import re
from pathlib import Path

def fix_python_file(file_path):
    """Pythonファイルの出力形式を修正"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 絵文字を含むprint文をstderrへリダイレクト
    emoji_pattern = r'(print\(f?["\'][^"\']*[✅❌⚠️🔄📊📈📝🎉][^"\']*["\'][^\)]*\))'
    content = re.sub(emoji_pattern, r'\1', content)
    
    # 絵文字を含むprint文にfile=sys.stderrを追加
    content = re.sub(
        r'print\(([^)]*[✅❌⚠️🔄📊📈📝🎉][^)]*)\)(?!\s*,\s*file=)',
        r'print(\1, file=sys.stderr)',
        content
    )
    
    # Error, Warning, Info メッセージをstderrへ
    content = re.sub(
        r'print\(f?["\'](?:Error|Warning|Info|✅|❌|⚠️)(?:[^"\']*)["\']([^)]*)\)(?!\s*,\s*file=)',
        r'print(f"\g<0>", file=sys.stderr)',
        content,
        flags=re.IGNORECASE
    )
    
    # sys import追加（必要な場合）
    if 'file=sys.stderr' in content and 'import sys' not in content:
        # 既存のimport文の後に追加
        if 'import' in content:
            content = re.sub(
                r'((?:from [^\n]+ import [^\n]+\n|import [^\n]+\n)+)',
                r'\1import sys\n',
                content,
                count=1
            )
        else:
            content = 'import sys\n' + content
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    scripts_dir = Path(__file__).parent
    fixed_files = []
    
    for py_file in scripts_dir.glob('*.py'):
        if py_file.name == 'fix_output_format.py':
            continue
        
        if fix_python_file(py_file):
            fixed_files.append(py_file.name)
    
    if fixed_files:
        print(f"Fixed {len(fixed_files)} files:", file=sys.stderr)
        for file in fixed_files:
            print(f"  - {file}", file=sys.stderr)
    else:
        print("No files needed fixing", file=sys.stderr)

if __name__ == '__main__':
    import sys
    main()