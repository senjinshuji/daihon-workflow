#!/usr/bin/env python3
"""
承認台本フィルタリングスクリプト

平均評価結果と承認閾値を基に台本をフィルタリングし、
承認台本を抽出する。各ライターの承認台本数をチェックし、
Writer調整の必要性を判定する。
"""

import json
import argparse
import os
import sys
import shutil
from datetime import datetime
from typing import Dict, List, Any

def load_json(file_path: str) -> Dict[str, Any]:
    """JSONファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return {}

def load_threshold(threshold_file: str) -> float:
    """承認閾値を読み込む"""
    try:
        with open(threshold_file, 'r', encoding='utf-8') as f:
            threshold_str = f.read().strip()
            return float(threshold_str)
    except (FileNotFoundError, ValueError) as e:
        print(f"Warning: Could not load threshold from {threshold_file}: {e}", file=sys.stderr)
        return 70.0  # デフォルト閾値

def copy_script_file(script_file: str, product_name: str, output_dir: str, loop_number: int = 1) -> bool:
    """台本ファイルを承認ディレクトリにコピー"""
    source_path = os.path.join(product_name, 'bulk_scripts', f'loop_{loop_number}', script_file)
    dest_path = os.path.join(output_dir, script_file)
    
    try:
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            return True
        else:
            print(f"Warning: Script file not found: {source_path}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Error copying {source_path} to {dest_path}: {e}")
        return False

def filter_scripts(evaluation_data: Dict[str, Any], 
                  threshold: float, 
                  product_name: str, 
                  output_dir: str,
                  loop_number: int = 1) -> Dict[str, Any]:
    """台本をフィルタリングして承認台本を抽出"""
    
    if 'script_evaluations' not in evaluation_data:
        raise ValueError("No script evaluations found in evaluation data")
    
    script_evaluations = evaluation_data['script_evaluations']
    approved_scripts = []
    writer_breakdown = {}
    
    print(f"Filtering {len(script_evaluations)} scripts with threshold: {threshold}")
    
    # 各台本を評価
    for evaluation in script_evaluations:
        script_file = evaluation['script_file']
        writer = evaluation['writer']
        avg_score = evaluation['average_weighted_score']
        
        # ライター別統計を初期化
        if writer not in writer_breakdown:
            writer_breakdown[writer] = {
                'total_scripts': 0,
                'approved_scripts': 0,
                'approval_rate': 0,
                'average_score': 0,
                'approved_files': [],
                'rejected_files': []
            }
        
        writer_breakdown[writer]['total_scripts'] += 1
        
        # 承認判定
        if avg_score >= threshold:
            # 承認台本
            approved_scripts.append(evaluation)
            writer_breakdown[writer]['approved_scripts'] += 1
            writer_breakdown[writer]['approved_files'].append({
                'file': script_file,
                'score': avg_score,
                'rank': evaluation['rank']
            })
            
            # ファイルをコピー
            copy_success = copy_script_file(script_file, product_name, output_dir, loop_number)
            if not copy_success:
                print(f"Warning: Failed to copy approved script: {script_file}", file=sys.stderr)
        else:
            # 却下台本
            writer_breakdown[writer]['rejected_files'].append({
                'file': script_file,
                'score': avg_score,
                'rank': evaluation['rank']
            })
    
    # ライター別統計を計算
    for writer, stats in writer_breakdown.items():
        if stats['total_scripts'] > 0:
            stats['approval_rate'] = (stats['approved_scripts'] / stats['total_scripts']) * 100
            
            # 平均スコアを計算（承認・却下含む全台本）
            writer_scores = []
            for eval in script_evaluations:
                if eval['writer'] == writer:
                    writer_scores.append(eval['average_weighted_score'])
            stats['average_score'] = sum(writer_scores) / len(writer_scores) if writer_scores else 0
    
    # Writer調整の必要性を判定
    writer_adjustment_needed = False
    insufficient_writers = []
    
    for writer, stats in writer_breakdown.items():
        if stats['approved_scripts'] < 3:  # 各ライター3本未満
            writer_adjustment_needed = True
            insufficient_writers.append({
                'writer': writer,
                'approved_count': stats['approved_scripts'],
                'total_count': stats['total_scripts'],
                'average_score': stats['average_score']
            })
    
    # 全体統計
    total_generated = len(script_evaluations)
    total_approved = len(approved_scripts)
    approval_rate = (total_approved / total_generated * 100) if total_generated > 0 else 0
    
    results = {
        'filtering_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'loop_number': loop_number,
        'threshold_used': threshold,
        'total_generated': total_generated,
        'approved_count': total_approved,
        'approval_rate': round(approval_rate, 2),
        'writer_adjustment_needed': writer_adjustment_needed,
        'insufficient_writers': insufficient_writers,
        'writer_breakdown': writer_breakdown,
        'approved_scripts': approved_scripts,
        'summary': {
            'ready_for_phase4': not writer_adjustment_needed,
            'min_scripts_per_writer': 3,
            'writers_meeting_requirement': len([w for w in writer_breakdown.values() if w['approved_scripts'] >= 3]),
            'total_writers': len(writer_breakdown)
        }
    }
    
    return results

def generate_report(results: Dict[str, Any], product_name: str) -> str:
    """評価レポートを生成"""
    report_lines = [
        f"# 台本評価・フィルタリング結果レポート",
        f"",
        f"**商品名**: {product_name}",
        f"**ループ番号**: {results.get('loop_number', 1)}",
        f"**実行日時**: {results['filtering_date']}",
        f"**承認閾値**: {results['threshold_used']}",
        f"",
        f"## 全体サマリー",
        f"",
        f"- **生成台本数**: {results['total_generated']}本",
        f"- **承認台本数**: {results['approved_count']}本",
        f"- **承認率**: {results['approval_rate']}%",
        f"- **Phase 4準備状況**: {'✅ 準備完了' if results['summary']['ready_for_phase4'] else '⚠️ Writer調整が必要'}",
        f"",
        f"## ライター別結果",
        f""
    ]
    
    for writer, stats in results['writer_breakdown'].items():
        status = "✅ 要件達成" if stats['approved_scripts'] >= 3 else "❌ 要件未達"
        report_lines.extend([
            f"### {writer}",
            f"",
            f"- **ステータス**: {status}",
            f"- **承認台本数**: {stats['approved_scripts']}/5本",
            f"- **承認率**: {stats['approval_rate']:.1f}%",
            f"- **平均スコア**: {stats['average_score']:.2f}",
            f""
        ])
        
        if stats['approved_files']:
            report_lines.append("**承認台本**:")
            for file_info in stats['approved_files']:
                report_lines.append(f"- {file_info['file']} (スコア: {file_info['score']:.2f}, ランク: {file_info['rank']})")
            report_lines.append("")
    
    if results['writer_adjustment_needed']:
        report_lines.extend([
            f"## Writer調整が必要",
            f"",
            f"以下のWriterは承認台本数が3本未満のため、人格調整が必要です：",
            f""
        ])
        
        for writer_info in results['insufficient_writers']:
            report_lines.append(f"- **{writer_info['writer']}**: {writer_info['approved_count']}/5本承認 (平均スコア: {writer_info['average_score']:.2f})")
    
    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description='Filter approved scripts based on evaluation results')
    parser.add_argument('--product-name', required=True, help='Product name')
    parser.add_argument('--evaluation-file', required=True, help='Averaged evaluation results file')
    parser.add_argument('--threshold-file', required=True, help='Approval threshold file')
    parser.add_argument('--output-dir', required=True, help='Output directory for approved scripts')
    parser.add_argument('--results-file', required=True, help='Output file for filtering results')
    parser.add_argument('--loop-number', type=int, default=1, help='Current loop iteration number')
    
    args = parser.parse_args()
    
    print(f"Filtering scripts for product: {args.product_name}")
    
    # 入力データを読み込み
    evaluation_data = load_json(args.evaluation_file)
    threshold = load_threshold(args.threshold_file)
    
    if not evaluation_data:
        raise ValueError(f"Could not load evaluation data from {args.evaluation_file}")
    
    # 出力ディレクトリを作成
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.results_file), exist_ok=True)
    
    # フィルタリングを実行
    results = filter_scripts(evaluation_data, threshold, args.product_name, args.output_dir, args.loop_number)
    
    # 結果を保存
    with open(args.results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # レポートを生成・保存
    report_content = generate_report(results, args.product_name)
    report_file = os.path.join(os.path.dirname(args.results_file), 'script_evaluation_report.md')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f" Filtering completed")
    print(f"   Approved scripts: {results['approved_count']}/{results['total_generated']} ({results['approval_rate']}%)")
    print(f"   Writer adjustment needed: {results['writer_adjustment_needed']}")
    print(f"   Results saved to: {args.results_file}")
    print(f"   Report saved to: {report_file}")
    
    if results['writer_adjustment_needed']:
        print(f"  The following writers need adjustment:")
        for writer_info in results['insufficient_writers']:
            print(f"     - {writer_info['writer']}: {writer_info['approved_count']}/5 approved")

if __name__ == '__main__':
    main()
