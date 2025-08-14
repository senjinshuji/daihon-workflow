#!/usr/bin/env python3
"""
Extract sample scripts for evaluation from internal data (Random Sampling)
Phase 2 Step 1: データ抽出 - ランダムサンプリングによる15本抽出
"""
import os
import sys
import argparse
import pandas as pd
import json
import logging
import random
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def extract_sample_scripts(product_name, data_dir, random_seed=None):
    """内部データから各グループ5本ずつ、計15本の台本をランダム抽出"""
    
    logger = setup_logging()
    
    # ランダムシード設定（再現性のため）
    if random_seed is not None:
        random.seed(random_seed)
        logger.info(f"🎲 ランダムシード設定: {random_seed}")
    else:
        # デフォルトシードは商品名のハッシュ値
        import hashlib
        seed = int(hashlib.md5(product_name.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        logger.info(f"🎲 デフォルトランダムシード設定: {seed} (商品名ベース)")
    
    artifacts_dir = Path(f"{product_name}/artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # CSVファイル読み込み
    files = {
        'top': 'internal_top_group.csv',
        'middle': 'internal_middle_group.csv',
        'bottom': 'internal_bottom_group.csv'
    }
    
    extracted_scripts = []
    group_mapping = {}
    
    for group, filename in files.items():
        filepath = Path(data_dir) / filename
        if not filepath.exists():
            logger.error(f"❌ ファイルが見つかりません: {filepath}")
            continue
        
        try:
            # CSVを読み込み（複数行のテキストに対応）
            df = pd.read_csv(filepath, encoding='utf-8')
            # インデックスをリセット
            df = df.reset_index(drop=True)
            logger.info(f"📊 {group}グループ: {len(df)}本の台本")
            
            # カラム名を確認して適切に取得
            logger.debug(f"利用可能なカラム: {df.columns.tolist()}")
            
            # 台本カラムの特定
            content_col = None
            if '台本' in df.columns:
                content_col = '台本'
            elif 'script' in df.columns:
                content_col = 'script'
            elif 'content' in df.columns:
                content_col = 'content'
            elif len(df.columns) > 0:
                content_col = df.columns[0]  # 最初のカラムを使用
            
            # スコアカラムの特定
            score_col = None
            if 'CTR×CVR' in df.columns:
                score_col = 'CTR×CVR'
            elif 'score' in df.columns:
                score_col = 'score'
            elif 'CVR' in df.columns:
                score_col = 'CVR'
            
            # ランダムに5本を抽出（データが5本未満の場合は全て取得）
            if len(df) <= 5:
                sample_scripts = df
                logger.warning(f"⚠️ {group}グループは{len(df)}本しかありません。全て抽出します。")
            else:
                # ランダムサンプリング
                sample_indices = random.sample(range(len(df)), 5)
                sample_scripts = df.iloc[sample_indices]
                logger.info(f"🎲 {group}グループから{len(sample_scripts)}本をランダム抽出")
            
            for i, (idx, row) in enumerate(sample_scripts.iterrows()):
                try:
                    # コンテンツの取得
                    content = row.get(content_col, '') if content_col else ''
                    
                    # スコアの取得と変換
                    score_value = 0
                    if score_col and score_col in row:
                        try:
                            score_value = float(row[score_col])
                        except (ValueError, TypeError):
                            score_value = 0
                    
                    script_data = {
                        'id': f"{group}_{i+1:02d}",  # 連番でID生成（ランダム抽出後の順序）
                        'original_group': group,
                        'title': row.get('title', f"{group}_script_{i+1}"),
                        'content': str(content),  # 文字列に変換
                        'score': score_value,
                        'metadata': {
                            'source_file': filename,
                            'source_index': idx if isinstance(idx, int) else i,  # エラー対策
                            'extraction_order': i + 1  # 抽出後の順序
                        }
                    }
                    extracted_scripts.append(script_data)
                    group_mapping[script_data['id']] = group
                    
                except Exception as row_error:
                    logger.error(f"❌ {group}グループの行 {i} の処理中にエラー: {row_error}")
                    continue
                    
        except Exception as e:
            logger.error(f"❌ {group}グループのデータ読み込みに失敗: {e}")
            continue
    
    # 抽出結果を保存
    extraction_result = {
        'total_scripts': len(extracted_scripts),
        'groups': {
            'top': len([s for s in extracted_scripts if s['original_group'] == 'top']),
            'middle': len([s for s in extracted_scripts if s['original_group'] == 'middle']),
            'bottom': len([s for s in extracted_scripts if s['original_group'] == 'bottom'])
        },
        'scripts': extracted_scripts,
        'group_mapping': group_mapping,
        'extraction_timestamp': pd.Timestamp.now().isoformat()
    }
    
    # 結果保存
    output_file = artifacts_dir / 'sample_scripts_for_evaluation.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extraction_result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 合計{len(extracted_scripts)}本の台本をランダム抽出しました")
    logger.info(f"📁 保存先: {output_file}")
    logger.info(f"📊 内訳: Top {extraction_result['groups']['top']}本, Middle {extraction_result['groups']['middle']}本, Bottom {extraction_result['groups']['bottom']}本")
    
    return len(extracted_scripts)

def main():
    parser = argparse.ArgumentParser(description='Extract sample scripts for evaluation')
    parser.add_argument('--product-name', required=True, help='Product name')
    parser.add_argument('--data-dir', required=True, help='Directory containing CSV data')
    parser.add_argument('--random-seed', type=int, help='Random seed for reproducible sampling')
    
    args = parser.parse_args()
    
    try:
        scripts_count = extract_sample_scripts(
            args.product_name, 
            args.data_dir, 
            random_seed=args.random_seed
        )
        print(f"scripts_count={scripts_count}")
        print(f"completed={'true' if scripts_count > 0 else 'false'}")
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"❌ データ抽出に失敗: {str(e)}")
        import traceback
        logger.error(f"詳細なエラー情報:\n{traceback.format_exc()}")
        print("scripts_count=0")
        print("completed=false")
        sys.exit(1)

if __name__ == "__main__":
    main()
