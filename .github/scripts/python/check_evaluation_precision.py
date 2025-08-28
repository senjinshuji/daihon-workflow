#!/usr/bin/env python3
"""
Check evaluation precision by comparing persona rankings with original groups
Phase 2 Step 3: 精度確認
"""
import os
import sys
import argparse
import json
import pandas as pd
import logging
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def check_precision(product_name):
    """ペルソナ評価の精度確認"""
    
    logger = setup_logging()
    artifacts_dir = Path(f"{product_name}/artifacts")
    
    # 元データ読み込み
    sample_file = artifacts_dir / 'sample_scripts_for_evaluation.json'
    evaluation_file = artifacts_dir / 'persona_evaluation_results.json'
    
    if not sample_file.exists() or not evaluation_file.exists():
        logger.error("❌ 必要なファイルが見つかりません")
        return False, 0, True
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
    
    with open(evaluation_file, 'r', encoding='utf-8') as f:
        evaluation_data = json.load(f)
    
    # 元のグループマッピング
    original_groups = sample_data['group_mapping']
    
    # ペルソナ評価に基づくランキング
    script_scores = evaluation_data.get('averaged_scores', {})
    
    # スコア順にソート（降順）
    sorted_scripts = sorted(script_scores.items(), key=lambda x: x[1], reverse=True)
    
    # ランキングに基づくグループ分け
    total_scripts = len(sorted_scripts)
    group_size = total_scripts // 3
    
    evaluated_groups = {}
    
    # 上位グループ
    for i in range(group_size):
        script_id = sorted_scripts[i][0]
        evaluated_groups[script_id] = 'top'
    
    # 中位グループ
    for i in range(group_size, group_size * 2):
        script_id = sorted_scripts[i][0]
        evaluated_groups[script_id] = 'middle'
    
    # 下位グループ
    for i in range(group_size * 2, total_scripts):
        script_id = sorted_scripts[i][0]
        evaluated_groups[script_id] = 'bottom'
    
    # 精度計算：各グループ内での一致率
    group_accuracy = {}
    
    for group in ['top', 'middle', 'bottom']:
        original_scripts = [sid for sid, grp in original_groups.items() if grp == group]
        evaluated_scripts = [sid for sid, grp in evaluated_groups.items() if grp == group]
        
        # 一致する台本数
        correct_scripts = set(original_scripts) & set(evaluated_scripts)
        
        group_accuracy[group] = {
            'original_count': len(original_scripts),
            'evaluated_count': len(evaluated_scripts),
            'correct_count': len(correct_scripts),
            'accuracy': len(correct_scripts) / len(original_scripts) if original_scripts else 0
        }
    
    # 全体精度をトップグループの精度のみで計算
    overall_accuracy = group_accuracy['top']['accuracy']
    
    # トップグループの精度が不足している場合に最適化が必要
    needs_optimization = False
    top_correct = group_accuracy['top']['correct_count']
    top_total = group_accuracy['top']['original_count']
    
    # トップグループで5本中4本以上正解していない場合は最適化が必要
    if top_correct < 4:
        needs_optimization = True
        logger.warning(f"⚠️ トップグループの精度が不足: {top_correct}/{top_total}本のみ正解")
    
    # 結果保存
    precision_result = {
        'overall_accuracy': overall_accuracy,
        'overall_accuracy_percent': round(overall_accuracy * 100, 2),
        'group_accuracy': group_accuracy,
        'original_groups': original_groups,
        'evaluated_groups': evaluated_groups,
        'needs_optimization': needs_optimization,
        'ranking_details': {
            'sorted_scripts': sorted_scripts,
            'score_distribution': script_scores
        },
        'precision_threshold': 80.0,
        'meets_threshold': overall_accuracy >= 0.8,  # トップグループの精度が80%以上
        'check_timestamp': pd.Timestamp.now().isoformat()
    }
    
    output_file = artifacts_dir / 'precision_check.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(precision_result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"📊 トップグループ精度: {precision_result['overall_accuracy_percent']}% ({top_correct}/{top_total}本)")
    logger.info(f"🎯 最適化必要: {'はい' if needs_optimization else 'いいえ'}")
    logger.info(f"✅ 閾値達成: {'はい (5本中4本以上正解)' if precision_result['meets_threshold'] else 'いいえ'}")
    
    return precision_result['meets_threshold'], precision_result['overall_accuracy_percent'], needs_optimization

def main():
    parser = argparse.ArgumentParser(description='Check evaluation precision')
    parser.add_argument('--product-name', required=True, help='Product name')
    
    args = parser.parse_args()
    
    try:
        meets_threshold, accuracy, needs_opt = check_precision(args.product_name)
        
        print(f"precision_check={'pass' if meets_threshold else 'fail'}")
        print(f"accuracy_rate={accuracy}")
        print(f"needs_optimization={'true' if needs_opt else 'false'}")
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"❌ 精度確認に失敗: {str(e)}")
        print("precision_check=fail")
        print("accuracy_rate=0")
        print("needs_optimization=true")
        sys.exit(1)

if __name__ == "__main__":
    main()
