#!/usr/bin/env python3
"""
Phase 3最終レポート生成スクリプト

全ループの合格台本を集計し、Writer別・ループ別にまとめた
最終レポートを生成する。
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

def load_json(file_path: str) -> Dict[str, Any]:
    """JSONファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return {}

def collect_loop_results(product_name: str) -> Dict[str, Any]:
    """全ループの結果を収集"""
    approved_scripts_dir = Path(product_name) / 'approved_scripts'
    artifacts_dir = Path(product_name) / 'artifacts'
    
    loop_results = {}
    all_approved_scripts = []
    writer_stats = {}
    
    # 各ループディレクトリを探索
    if approved_scripts_dir.exists():
        for loop_dir in sorted(approved_scripts_dir.glob('loop_*')):
            loop_num = loop_dir.name.replace('loop_', '')
            
            # そのループのフィルタリング結果を読み込み
            filtering_results_path = artifacts_dir / f'filtering_results_loop_{loop_num}.json'
            if not filtering_results_path.exists():
                # 互換性のため、通常のパスもチェック
                filtering_results_path = artifacts_dir / 'filtering_results.json'
            
            if filtering_results_path.exists():
                results = load_json(str(filtering_results_path))
                
                # ループ結果を保存
                loop_results[f'loop_{loop_num}'] = {
                    'loop_number': int(loop_num),
                    'total_approved': results.get('approved_count', 0),
                    'approval_rate': results.get('approval_rate', 0),
                    'threshold': results.get('threshold_used', 0),
                    'date': results.get('filtering_date', ''),
                    'scripts': []
                }
                
                # 承認台本の詳細を収集
                for script in results.get('approved_scripts', []):
                    script_info = {
                        'file': script.get('script_file', ''),
                        'writer': script.get('writer', ''),
                        'score': script.get('average_weighted_score', 0),
                        'loop': int(loop_num),
                        'rank': script.get('rank', 0)
                    }
                    
                    loop_results[f'loop_{loop_num}']['scripts'].append(script_info)
                    all_approved_scripts.append(script_info)
                    
                    # Writer別統計を更新
                    writer = script.get('writer', 'unknown')
                    if writer not in writer_stats:
                        writer_stats[writer] = {
                            'total_approved': 0,
                            'scripts': [],
                            'best_score': 0,
                            'loops_participated': set()
                        }
                    
                    writer_stats[writer]['total_approved'] += 1
                    writer_stats[writer]['scripts'].append(script_info)
                    writer_stats[writer]['best_score'] = max(
                        writer_stats[writer]['best_score'],
                        script.get('average_weighted_score', 0)
                    )
                    writer_stats[writer]['loops_participated'].add(int(loop_num))
    
    # Writer統計を整理
    for writer in writer_stats:
        writer_stats[writer]['loops_participated'] = sorted(list(writer_stats[writer]['loops_participated']))
        writer_stats[writer]['scripts'] = sorted(
            writer_stats[writer]['scripts'],
            key=lambda x: x['score'],
            reverse=True
        )
    
    return {
        'loop_results': loop_results,
        'all_approved_scripts': all_approved_scripts,
        'writer_stats': writer_stats
    }

def generate_summary_json(product_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """集計JSONを生成"""
    loop_results = data['loop_results']
    all_approved_scripts = data['all_approved_scripts']
    writer_stats = data['writer_stats']
    
    # 統計計算
    total_loops = len(loop_results)
    total_approved = len(all_approved_scripts)
    
    # 最初と最後のループの比較
    if total_loops > 0:
        sorted_loops = sorted(loop_results.keys(), key=lambda x: int(x.replace('loop_', '')))
        first_loop = loop_results[sorted_loops[0]]
        last_loop = loop_results[sorted_loops[-1]]
        
        improvement_rate = 0
        if first_loop['total_approved'] > 0:
            improvement_rate = ((last_loop['total_approved'] - first_loop['total_approved']) / 
                              first_loop['total_approved']) * 100
    else:
        improvement_rate = 0
        first_loop = last_loop = {'total_approved': 0}
    
    # 最高パフォーマンスのWriter
    best_writer = max(writer_stats.keys(), key=lambda w: writer_stats[w]['total_approved']) if writer_stats else None
    
    summary = {
        'product_name': product_name,
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_loops': total_loops,
        'final_status': 'completed' if total_loops > 0 else 'no_data',
        'approved_scripts_by_loop': {},
        'approved_scripts_by_writer': {},
        'all_approved_scripts': sorted(all_approved_scripts, key=lambda x: x['score'], reverse=True),
        'summary': {
            'total_approved_scripts': total_approved,
            'best_performing_writer': best_writer,
            'improvement_rate': f"{improvement_rate:.1f}%",
            'first_loop_approved': first_loop['total_approved'],
            'final_loop_approved': last_loop['total_approved'],
            'writers_achieving_target': len([w for w in writer_stats.values() if w['total_approved'] >= 3])
        }
    }
    
    # ループ別データを追加
    for loop_key, loop_data in loop_results.items():
        summary['approved_scripts_by_loop'][loop_key] = {
            'total_approved': loop_data['total_approved'],
            'approval_rate': loop_data['approval_rate'],
            'threshold': loop_data['threshold'],
            'date': loop_data['date'],
            'scripts': loop_data['scripts']
        }
    
    # Writer別データを追加
    for writer, stats in writer_stats.items():
        summary['approved_scripts_by_writer'][writer] = {
            'total_approved': stats['total_approved'],
            'best_score': stats['best_score'],
            'loops_participated': stats['loops_participated'],
            'scripts': stats['scripts']
        }
    
    return summary

def generate_markdown_report(summary: Dict[str, Any]) -> str:
    """Markdownレポートを生成"""
    lines = [
        f"# 台本生成最終レポート",
        f"",
        f"## 概要",
        f"- **商品名**: {summary['product_name']}",
        f"- **レポート生成日時**: {summary['generation_date']}",
        f"- **総ループ数**: {summary['total_loops']}回",
        f"- **最終合格台本数**: {summary['summary']['total_approved_scripts']}本",
        f"- **改善率**: {summary['summary']['improvement_rate']}",
        f"",
        f"## ループ別成果",
        f""
    ]
    
    # ループ別詳細
    for loop_key in sorted(summary['approved_scripts_by_loop'].keys(), 
                          key=lambda x: int(x.replace('loop_', ''))):
        loop_data = summary['approved_scripts_by_loop'][loop_key]
        loop_num = loop_key.replace('loop_', '')
        
        lines.extend([
            f"### Loop {loop_num}",
            f"- **実行日時**: {loop_data['date']}",
            f"- **合格台本数**: {loop_data['total_approved']}本",
            f"- **承認率**: {loop_data['approval_rate']}%",
            f"- **承認閾値**: {loop_data['threshold']}",
            f""
        ])
        
        # Writer別内訳
        writer_counts = {}
        for script in loop_data['scripts']:
            writer = script['writer']
            writer_counts[writer] = writer_counts.get(writer, 0) + 1
        
        if writer_counts:
            lines.append("**Writer別内訳**:")
            for writer, count in sorted(writer_counts.items()):
                lines.append(f"- {writer}: {count}本")
            lines.append("")
    
    # Writer別最終成果
    lines.extend([
        f"## Writer別最終成果",
        f""
    ])
    
    for writer in sorted(summary['approved_scripts_by_writer'].keys()):
        writer_data = summary['approved_scripts_by_writer'][writer]
        
        lines.extend([
            f"### {writer}",
            f"- **最終合格数**: {writer_data['total_approved']}本",
            f"- **最高スコア**: {writer_data['best_score']:.2f}点",
            f"- **参加ループ**: {', '.join(map(str, writer_data['loops_participated']))}",
            f""
        ])
        
        # 上位3本の台本
        if writer_data['scripts']:
            lines.append("**上位台本**:")
            for i, script in enumerate(writer_data['scripts'][:3], 1):
                lines.append(f"{i}. {script['file']} (Loop {script['loop']}, スコア: {script['score']:.2f})")
            lines.append("")
    
    # 合格台本一覧（上位20本）
    lines.extend([
        f"## 合格台本一覧（上位20本）",
        f"",
        f"| ランク | ファイル名 | Writer | ループ | スコア |",
        f"|--------|-----------|--------|--------|--------|"
    ])
    
    for i, script in enumerate(summary['all_approved_scripts'][:20], 1):
        lines.append(
            f"| {i} | {script['file']} | {script['writer']} | "
            f"{script['loop']} | {script['score']:.2f} |"
        )
    
    lines.extend([
        f"",
        f"## 統計サマリー",
        f"",
        f"- **最高パフォーマンスWriter**: {summary['summary']['best_performing_writer']}",
        f"- **目標達成Writer数**: {summary['summary']['writers_achieving_target']}",
        f"- **初回合格数**: {summary['summary']['first_loop_approved']}本",
        f"- **最終合格数**: {summary['summary']['final_loop_approved']}本",
        f"- **改善率**: {summary['summary']['improvement_rate']}",
        f"",
        f"---",
        f"*このレポートは自動生成されました。*"
    ])
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Generate final report for Phase 3')
    parser.add_argument('--product-name', required=True, help='Product name')
    parser.add_argument('--output-dir', required=True, help='Output directory for reports')
    
    args = parser.parse_args()
    
    print(f"📊 Generating final report for {args.product_name}...")
    
    # データ収集
    data = collect_loop_results(args.product_name)
    
    if not data['all_approved_scripts']:
        print("⚠️ No approved scripts found. Skipping report generation.")
        return
    
    # 出力ディレクトリ作成
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSONサマリー生成
    summary = generate_summary_json(args.product_name, data)
    summary_path = output_dir / 'approved_scripts_summary.json'
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON summary saved to: {summary_path}")
    
    # Markdownレポート生成
    markdown_report = generate_markdown_report(summary)
    report_path = output_dir / 'approved_scripts_report.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"✅ Markdown report saved to: {report_path}")
    
    # 統計表示
    print(f"")
    print(f"📈 Final Statistics:")
    print(f"   Total loops: {summary['total_loops']}")
    print(f"   Total approved scripts: {summary['summary']['total_approved_scripts']}")
    print(f"   Best performing writer: {summary['summary']['best_performing_writer']}")
    print(f"   Improvement rate: {summary['summary']['improvement_rate']}")

if __name__ == '__main__':
    main()