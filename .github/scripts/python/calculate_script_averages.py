#!/usr/bin/env python3
"""
台本評価の平均値計算スクリプト

3つのペルソナによる台本評価結果を読み込み、
各台本の平均スコアを計算してランキングを作成する。
"""

import json
import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
import numpy as np

def load_persona_evaluation(file_path: str) -> Dict[str, Any]:
    """ペルソナ評価ファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Evaluation file not found: {file_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return None

def extract_evaluation_axes(persona_data: Dict[str, Any]) -> List[str]:
    """評価軸を動的に抽出"""
    if not persona_data or 'script_evaluations' not in persona_data:
        return []
    
    evaluations = persona_data['script_evaluations']
    if not evaluations or 'detailed_scores' not in evaluations[0]:
        return []
    
    return list(evaluations[0]['detailed_scores'].keys())

def calculate_averages(persona1_data: Dict[str, Any], 
                      persona2_data: Dict[str, Any], 
                      persona3_data: Dict[str, Any]) -> Dict[str, Any]:
    """3つのペルソナ評価の平均値を計算"""
    
    # 評価軸を動的に抽出
    evaluation_axes = extract_evaluation_axes(persona1_data)
    if not evaluation_axes:
        evaluation_axes = extract_evaluation_axes(persona2_data)
    if not evaluation_axes:
        evaluation_axes = extract_evaluation_axes(persona3_data)
    
    if not evaluation_axes:
        raise ValueError("No evaluation axes found in any persona data")
    
    print(f"Found evaluation axes: {evaluation_axes}", file=sys.stderr)
    
    # 台本別の評価データを収集
    script_evaluations = {}
    
    # 各ペルソナのデータを処理
    for persona_name, persona_data in [
        ('persona1', persona1_data),
        ('persona2', persona2_data), 
        ('persona3', persona3_data)
    ]:
        if not persona_data or 'script_evaluations' not in persona_data:
            print(f"Warning: No evaluations found for {persona_name}", file=sys.stderr)
            continue
            
        for eval_data in persona_data['script_evaluations']:
            script_file = eval_data['script_file']
            writer = eval_data.get('writer', 'unknown')
            weighted_score = eval_data.get('weighted_score', 0)
            detailed_scores = eval_data.get('detailed_scores', {})
            
            if script_file not in script_evaluations:
                script_evaluations[script_file] = {
                    'script_file': script_file,
                    'writer': writer,
                    'persona_scores': {},
                    'detailed_scores': {axis: [] for axis in evaluation_axes},
                    'weighted_scores': []
                }
            
            # ペルソナ別スコアを記録
            script_evaluations[script_file]['persona_scores'][persona_name] = weighted_score
            script_evaluations[script_file]['weighted_scores'].append(weighted_score)
            
            # 詳細スコアを記録
            for axis in evaluation_axes:
                if axis in detailed_scores:
                    score = detailed_scores[axis].get('score', 0)
                    script_evaluations[script_file]['detailed_scores'][axis].append(score)
    
    # 平均値を計算
    averaged_evaluations = []
    
    for script_file, data in script_evaluations.items():
        # 重み付きスコアの平均
        weighted_scores = data['weighted_scores']
        if weighted_scores:
            avg_weighted_score = np.mean(weighted_scores)
            std_weighted_score = np.std(weighted_scores) if len(weighted_scores) > 1 else 0
        else:
            avg_weighted_score = 0
            std_weighted_score = 0
        
        # 詳細スコアの平均
        avg_detailed_scores = {}
        for axis in evaluation_axes:
            scores = data['detailed_scores'][axis]
            if scores:
                avg_detailed_scores[axis] = {
                    'average_score': float(np.mean(scores)),
                    'std_deviation': float(np.std(scores)) if len(scores) > 1 else 0,
                    'individual_scores': scores
                }
            else:
                avg_detailed_scores[axis] = {
                    'average_score': 0,
                    'std_deviation': 0,
                    'individual_scores': []
                }
        
        # 合意度を計算（標準偏差の逆数）
        consensus_score = 1 / (1 + std_weighted_score) if std_weighted_score >= 0 else 1
        
        averaged_evaluations.append({
            'script_file': script_file,
            'writer': data['writer'],
            'persona_scores': data['persona_scores'],
            'average_weighted_score': float(avg_weighted_score),
            'score_std_deviation': float(std_weighted_score),
            'consensus_score': float(consensus_score),
            'detailed_scores': avg_detailed_scores
        })
    
    # スコア順にソート
    averaged_evaluations.sort(key=lambda x: x['average_weighted_score'], reverse=True)
    
    # ランキングを追加
    for i, evaluation in enumerate(averaged_evaluations):
        evaluation['rank'] = i + 1
    
    # サマリー統計を計算
    all_scores = [eval['average_weighted_score'] for eval in averaged_evaluations]
    writer_stats = {}
    
    for evaluation in averaged_evaluations:
        writer = evaluation['writer']
        if writer not in writer_stats:
            writer_stats[writer] = {
                'script_count': 0,
                'scores': [],
                'average_score': 0,
                'best_score': 0,
                'worst_score': 100
            }
        
        writer_stats[writer]['script_count'] += 1
        writer_stats[writer]['scores'].append(evaluation['average_weighted_score'])
        writer_stats[writer]['best_score'] = max(writer_stats[writer]['best_score'], evaluation['average_weighted_score'])
        writer_stats[writer]['worst_score'] = min(writer_stats[writer]['worst_score'], evaluation['average_weighted_score'])
    
    # ライター別平均を計算
    for writer, stats in writer_stats.items():
        stats['average_score'] = float(np.mean(stats['scores']))
        stats['score_std'] = float(np.std(stats['scores'])) if len(stats['scores']) > 1 else 0
    
    return {
        'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'evaluation_axes': evaluation_axes,
        'total_scripts': len(averaged_evaluations),
        'total_evaluators': 3,
        'script_evaluations': averaged_evaluations,
        'summary_statistics': {
            'overall_average': float(np.mean(all_scores)) if all_scores else 0,
            'overall_std': float(np.std(all_scores)) if len(all_scores) > 1 else 0,
            'highest_score': float(max(all_scores)) if all_scores else 0,
            'lowest_score': float(min(all_scores)) if all_scores else 0,
            'writer_statistics': writer_stats
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Calculate average script evaluation scores')
    parser.add_argument('--product-name', required=True, help='Product name')
    parser.add_argument('--input-dir', required=True, help='Input directory containing persona evaluations')
    parser.add_argument('--output-file', required=True, help='Output file for averaged evaluations')
    
    args = parser.parse_args()
    
    print(f"Calculating average scores for product: {args.product_name}", file=sys.stderr)
    
    # ペルソナ評価ファイルを読み込み
    persona1_file = os.path.join(args.input_dir, 'persona1_script_evaluation.json')
    persona2_file = os.path.join(args.input_dir, 'persona2_script_evaluation.json')
    persona3_file = os.path.join(args.input_dir, 'persona3_script_evaluation.json')
    
    persona1_data = load_persona_evaluation(persona1_file)
    persona2_data = load_persona_evaluation(persona2_file)
    persona3_data = load_persona_evaluation(persona3_file)
    
    # 少なくとも1つのペルソナデータが必要
    valid_personas = [p for p in [persona1_data, persona2_data, persona3_data] if p is not None]
    if not valid_personas:
        raise ValueError("No valid persona evaluation data found")
    
    print(f"Found {len(valid_personas)} valid persona evaluations")
    
    # 平均値を計算
    averaged_results = calculate_averages(persona1_data, persona2_data, persona3_data)
    
    # 出力ディレクトリを作成
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    
    # 結果を保存
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(averaged_results, f, ensure_ascii=False, indent=2)
    
    print(f"Average calculation completed", file=sys.stderr)
    print(f"   Total scripts: {averaged_results['total_scripts']}", file=sys.stderr)
    print(f"   Overall average: {averaged_results['summary_statistics']['overall_average']:.2f}", file=sys.stderr)
    print(f"   Results saved to: {args.output_file}", file=sys.stderr)

if __name__ == '__main__':
    main()
