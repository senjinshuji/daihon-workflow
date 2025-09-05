#!/usr/bin/env python3
"""
Execute next action based on precision check results
Phase 2 Step 4: 条件分岐とアクション
"""
import os
import sys
import argparse
import json
import subprocess
import logging
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def execute_next_action(product_name, precision_check, accuracy_rate):
    """精度結果に基づく次のアクション実行"""
    
    logger = setup_logging()
    artifacts_dir = Path(f"{product_name}/artifacts")
    precision_file = artifacts_dir / 'precision_check.json'
    
    if not precision_file.exists():
        logger.error("❌ 精度チェック結果が見つかりません")
        return "error"
    
    with open(precision_file, 'r', encoding='utf-8') as f:
        precision_data = json.load(f)
    
    if precision_data['meets_threshold']:
        # 精度達成: 承認閾値を保存してPhase 3起動
        logger.info("✅ 精度要件を満たしました")
        
        # 5番目のスコアを承認閾値として保存
        sorted_scripts = precision_data['ranking_details']['sorted_scripts']
        if len(sorted_scripts) >= 5:
            fifth_score = sorted_scripts[4][1]  # 5番目（インデックス4）のスコア
            
            threshold_file = artifacts_dir / 'approval_threshold.txt'
            with open(threshold_file, 'w') as f:
                f.write(str(fifth_score))
            
            logger.info(f"📊 承認閾値設定: {fifth_score}")
            
            # Phase 3を起動（GITHUB_TOKENは環境変数から取得）
            logger.info("🚀 Phase 3を起動します...")
            try:
                # GITHUB_TOKENが環境変数にセットされていることを確認
                if not os.environ.get('GITHUB_TOKEN'):
                    logger.warning("⚠️ GITHUB_TOKENが設定されていません")
                    
                result = subprocess.run([
                    'gh', 'workflow', 'run', '3-script-generation.yml',
                    '-f', f'product_name={product_name}',
                    '-f', 'loop_number=1'  # 初回ループ
                ], check=True, capture_output=True, text=True)
                logger.info("✅ Phase 3が正常に起動されました")
            except subprocess.CalledProcessError as e:
                logger.warning(f"⚠️ Phase 3の起動に失敗: {e.stderr}")
                logger.info("手動でPhase 3を起動してください")
            
            return "phase3_triggered"
        else:
            logger.error("❌ スコアデータが不足しています")
            return "error"
    else:
        # 精度不足: 評価基準を最適化
        logger.info("⚠️ 精度が不足しています。評価基準を最適化します...")
        
        # 最適化の実行はClaud Code SDKで行う（オーケストレーターで実行）
        # ここでは最適化が必要であることを示すフラグを作成
        optimization_needed_file = artifacts_dir / 'optimization_needed.txt'
        with open(optimization_needed_file, 'w') as f:
            f.write(f"Precision: {precision_data['overall_accuracy_percent']}%\n")
            f.write(f"Threshold: 80%\n")
            f.write(f"Needs optimization: True\n")
        
        logger.info("📝 最適化要求フラグを作成しました")
        
        return "needs_optimization"

def main():
    parser = argparse.ArgumentParser(description='Execute next action based on precision')
    parser.add_argument('--product-name', required=True, help='Product name')
    parser.add_argument('--precision-check', required=True, help='Precision check result')
    parser.add_argument('--accuracy-rate', required=True, help='Accuracy rate')
    
    args = parser.parse_args()
    
    try:
        action = execute_next_action(args.product_name, args.precision_check, args.accuracy_rate)
        print(f"final_action={action}")
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"❌ アクション実行に失敗: {str(e)}")
        print("final_action=error")
        sys.exit(1)

if __name__ == "__main__":
    main()
