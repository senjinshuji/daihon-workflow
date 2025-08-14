#!/usr/bin/env python3
"""
Calculate persona evaluation averages and create ranking
Phase 2 Step 2.5: ペルソナ評価平均値計算とランキング作成
"""
import os
import sys
import argparse
import pandas as pd
import json
import logging
import statistics
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def load_persona_evaluation(product_name, persona_id):
    """個別ペルソナ評価結果を読み込み"""
    logger = setup_logging()
    
    eval_file = Path(f"{product_name}/artifacts/{persona_id}_evaluation.json")
    
    if not eval_file.exists():
        logger.error(f"❌ {persona_id}の評価ファイルが見つかりません: {eval_file}")
        return None
    
    try:
        with open(eval_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"✅ {persona_id}評価データ読み込み完了: {data.get('evaluation_metadata', {}).get('total_scripts_evaluated', 0)}本")
        return data
    
    except Exception as e:
        logger.error(f"❌ {persona_id}評価データ読み込みエラー: {str(e)}")
        return None

def calculate_averages_and_ranking(product_name):
    """3ペルソナの評価平均値を計算してランキング作成"""
    
    logger = setup_logging()
    
    # 3つのペルソナ評価を読み込み
    persona_evaluations = {}
    for persona_id in ['persona1', 'persona2', 'persona3']:
        eval_data = load_persona_evaluation(product_name, persona_id)
        if eval_data is None:
            logger.error(f"❌ {persona_id}の評価データが取得できません")
            return False
        persona_evaluations[persona_id] = eval_data
    
    # 全台本のIDを取得
    all_script_ids = set()
    for persona_data in persona_evaluations.values():
        all_script_ids.update(persona_data['evaluations'].keys())
    
    logger.info(f"📊 対象台本数: {len(all_script_ids)}本")
    
    # 平均値計算
    averaged_results = {}
    detailed_analysis = {}
    
    for script_id in all_script_ids:
        scores = []
        detailed_scores = {}
        evaluation_reasons = []
        
        for persona_id, persona_data in persona_evaluations.items():
            if script_id in persona_data['evaluations']:
                eval_data = persona_data['evaluations'][script_id]
                total_score = eval_data['total_score']
                scores.append(total_score)
                
                # 動的に評価軸を取得（criteria.jsonの内容に基づく）
                axis_scores = {}
                for key, value in eval_data.items():
                    if key not in ['total_score', 'evaluation_reason'] and isinstance(value, (int, float)):
                        axis_scores[key] = value
                
                detailed_scores[persona_id] = {
                    'total_score': total_score,
                    **axis_scores  # 動的な評価軸スコアを展開
                }
                evaluation_reasons.append(f"{persona_id}: {eval_data.get('evaluation_reason', '理由なし')}")
        
        if len(scores) == 3:
            # 平均値計算
            avg_score = statistics.mean(scores)
            score_variance = statistics.variance(scores) if len(scores) > 1 else 0
            
            # コンセンサスレベル判定
            if score_variance <= 25:  # 標準偏差5点以下
                consensus_level = "high"
            elif score_variance <= 100:  # 標準偏差10点以下
                consensus_level = "medium"
            else:
                consensus_level = "low"
            
            averaged_results[script_id] = round(avg_score, 2)
            
            detailed_analysis[script_id] = {
                'persona_scores': scores,
                'average_score': round(avg_score, 2),
                'score_variance': round(score_variance, 2),
                'consensus_level': consensus_level,
                'detailed_scores': detailed_scores,
                'evaluation_reasons': evaluation_reasons,
                'divergent_reasons': f"分散: {round(score_variance, 2)} ({'高' if consensus_level == 'low' else '中' if consensus_level == 'medium' else '低'}一致)"
            }
        else:
            logger.warning(f"⚠️ {script_id}: 3ペルソナ全ての評価がありません（{len(scores)}個）")
    
    # ランキング作成（平均スコア降順）
    ranking = sorted(averaged_results.items(), key=lambda x: x[1], reverse=True)
    
    # 結果統計
    all_avg_scores = list(averaged_results.values())
    result_stats = {
        'total_scripts': len(all_avg_scores),
        'average_of_averages': round(statistics.mean(all_avg_scores), 2) if all_avg_scores else 0,
        'median_score': round(statistics.median(all_avg_scores), 2) if all_avg_scores else 0,
        'score_range': {
            'min': round(min(all_avg_scores), 2) if all_avg_scores else 0,
            'max': round(max(all_avg_scores), 2) if all_avg_scores else 0
        },
        'high_consensus_count': len([a for a in detailed_analysis.values() if a['consensus_level'] == 'high']),
        'medium_consensus_count': len([a for a in detailed_analysis.values() if a['consensus_level'] == 'medium']),
        'low_consensus_count': len([a for a in detailed_analysis.values() if a['consensus_level'] == 'low'])
    }
    
    # 結果保存
    final_results = {
        'calculation_metadata': {
            'timestamp': datetime.now().isoformat(),
            'product_name': product_name,
            'calculation_method': '3ペルソナ平均値',
            'personas_included': ['persona1', 'persona2', 'persona3'],
            'total_scripts_processed': len(averaged_results)
        },
        'averaged_scores': averaged_results,
        'ranking': [{'rank': i+1, 'script_id': script_id, 'average_score': score} 
                   for i, (script_id, score) in enumerate(ranking)],
        'detailed_analysis': detailed_analysis,
        'result_statistics': result_stats,
        'persona_summaries': {
            persona_id: {
                'persona_summary': data.get('persona_summary', f'{persona_id}要約'),
                'total_scripts_evaluated': data.get('evaluation_metadata', {}).get('total_scripts_evaluated', 0),
                'average_score_given': round(statistics.mean([
                    eval_data['total_score'] 
                    for eval_data in data['evaluations'].values()
                ]), 2) if data['evaluations'] else 0
            }
            for persona_id, data in persona_evaluations.items()
        }
    }
    
    # 保存
    artifacts_dir = Path(f"{product_name}/artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = artifacts_dir / 'persona_evaluation_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ ペルソナ評価平均値計算完了")
    logger.info(f"📊 処理台本数: {len(averaged_results)}本")
    logger.info(f"📈 平均スコア範囲: {result_stats['score_range']['min']} - {result_stats['score_range']['max']}")
    logger.info(f"🎯 高一致: {result_stats['high_consensus_count']}本, 中一致: {result_stats['medium_consensus_count']}本, 低一致: {result_stats['low_consensus_count']}本")
    logger.info(f"📁 保存先: {output_file}")
    
    # TOP5を表示
    logger.info("🏆 TOP5ランキング:")
    for i, item in enumerate(ranking[:5]):
        script_id, score = item
        logger.info(f"  {i+1}位: {script_id} ({score}点)")
    
    return len(averaged_results)

def main():
    parser = argparse.ArgumentParser(description='Calculate persona evaluation averages and ranking')
    parser.add_argument('--product-name', required=True, help='Product name')
    
    args = parser.parse_args()
    
    try:
        scripts_count = calculate_averages_and_ranking(args.product_name)
        print(f"scripts_processed={scripts_count}")
        print(f"calculation_completed={'true' if scripts_count > 0 else 'false'}")
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"❌ 平均値計算に失敗: {str(e)}")
        print("scripts_processed=0")
        print("calculation_completed=false")
        sys.exit(1)

if __name__ == "__main__":
    main()
