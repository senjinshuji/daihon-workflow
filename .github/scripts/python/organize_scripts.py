#!/usr/bin/env python3
"""
生成された台本ファイルを正しい場所に整理する

Claude Code SDKで生成された台本ファイルが散在している場合に、
正しいディレクトリ構造（loop_X/writerY/script_Z.md）に整理する。
"""

import os
import shutil
import argparse
import glob
import sys
from pathlib import Path

def organize_scripts(product_name: str, writer_name: str, loop_number: int) -> int:
    """
    散在したファイルを正しい場所に移動

    Args:
        product_name: 商品名
        writer_name: ライター名（writer1, writer2, writer3）
        loop_number: ループ番号

    Returns:
        移動したファイル数
    """

    # ターゲットディレクトリを作成
    target_dir = Path(product_name) / "bulk_scripts" / f"loop_{loop_number}" / writer_name
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Target directory: {target_dir}")

    # 可能性のある場所からファイルを探す
    search_patterns = [
        # パターン1: bulk_scripts直下にwriter名付きで存在
        f"{product_name}/bulk_scripts/{writer_name}_script*.md",
        # パターン2: bulk_scripts/loop_X直下に存在
        f"{product_name}/bulk_scripts/loop_{loop_number}/{writer_name}_script*.md",
        # パターン3: bulk_scripts/loop_X直下にscript_のみで存在
        f"{product_name}/bulk_scripts/loop_{loop_number}/script_*.md",
        # パターン4: writerディレクトリ直下に存在
        f"{product_name}/{writer_name}/script_*.md",
        # パターン5: bulk_scripts直下にscript_のみで存在（writer1の場合のみ）
        f"{product_name}/bulk_scripts/script_*.md" if writer_name == "writer1" else None,
    ]

    moved_count = 0
    found_files = set()  # 重複を避けるため

    for pattern in search_patterns:
        if pattern is None:
            continue

        for file_path in glob.glob(pattern):
            file_path = Path(file_path)

            # 既に正しい場所にある場合はスキップ
            if str(file_path.parent) == str(target_dir):
                print(f"✓ Already in correct location: {file_path}")
                continue

            # 重複チェック
            if str(file_path) in found_files:
                continue
            found_files.add(str(file_path))

            # ファイル名を統一形式に変換
            filename = file_path.name

            # writer名を除去してscript_X.md形式に統一
            if filename.startswith(f"{writer_name}_"):
                new_name = filename.replace(f"{writer_name}_", "")
            elif filename.startswith("script_"):
                new_name = filename
            else:
                # 予期しない形式の場合はスキップ
                print(f"⚠️ Unexpected filename format: {filename}")
                continue

            # 移動先のパス
            destination = target_dir / new_name

            # ファイルを移動
            try:
                if destination.exists():
                    print(f"⚠️ Destination already exists, overwriting: {destination}")
                shutil.move(str(file_path), str(destination))
                moved_count += 1
                print(f"✓ Moved: {file_path} -> {destination}")
            except Exception as e:
                print(f"❌ Failed to move {file_path}: {e}", file=sys.stderr)

    # 最終的なファイル確認
    final_files = list(target_dir.glob("script_*.md"))
    print(f"\n📊 Final status in {target_dir}:")
    print(f"   - Files found and moved: {moved_count}")
    print(f"   - Total files in directory: {len(final_files)}")

    if final_files:
        print("   - Files:")
        for f in sorted(final_files):
            print(f"     • {f.name}")

    # 5つのファイルが揃っているか確認
    expected_files = [f"script_{i}.md" for i in range(1, 6)]
    missing_files = []
    for expected in expected_files:
        if not (target_dir / expected).exists():
            missing_files.append(expected)

    if missing_files:
        print(f"\n⚠️ Warning: Missing expected files: {', '.join(missing_files)}")
    else:
        print(f"\n✅ All 5 expected scripts are present!")

    return moved_count

def main():
    parser = argparse.ArgumentParser(description='Organize generated script files into correct directory structure')
    parser.add_argument('--product-name', required=True, help='Product name')
    parser.add_argument('--writer-name', required=True, help='Writer name (writer1/writer2/writer3)')
    parser.add_argument('--loop-number', type=int, required=True, help='Loop iteration number')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # バリデーション
    if args.writer_name not in ['writer1', 'writer2', 'writer3']:
        print(f"❌ Error: Invalid writer name '{args.writer_name}'. Must be writer1, writer2, or writer3.")
        sys.exit(1)

    if args.loop_number < 1:
        print(f"❌ Error: Invalid loop number {args.loop_number}. Must be >= 1.")
        sys.exit(1)

    print(f"🔧 Organizing scripts for {args.writer_name} (loop {args.loop_number})...")

    # スクリプトを整理
    count = organize_scripts(args.product_name, args.writer_name, args.loop_number)

    if count > 0:
        print(f"\n✅ Successfully organized {count} scripts for {args.writer_name}")
    else:
        print(f"\n⚠️ No scripts were moved. They may already be in the correct location.")

    # Exit code: 0 if successful, 1 if no files were found
    sys.exit(0 if count > 0 or len(list(Path(args.product_name) / "bulk_scripts" / f"loop_{args.loop_number}" / args.writer_name).glob("script_*.md")) > 0 else 1)

if __name__ == "__main__":
    main()