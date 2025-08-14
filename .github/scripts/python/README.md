# Python Scripts for Phase 2 Orchestrator

## 概要

このディレクトリには、Phase 2の評価基準最適化ループで使用されるPythonスクリプトが含まれています。

## スクリプト一覧

### Phase 2用スクリプト（新規作成）

#### 1. `extract_sample_scripts.py`
- **目的**: Step 1 - データ抽出
- **機能**: internal_*.csvから各グループ5本ずつ、計15本の台本を抽出
- **使用法**: 
  ```bash
  python extract_sample_scripts.py --product-name "商品名" --data-dir "data/"
  ```
- **出力**: `sample_scripts_for_evaluation.json`

#### 2. `calculate_persona_averages.py`
- **目的**: Step 2.5 - ペルソナ評価平均値計算とランキング作成
- **機能**: 3つのペルソナ評価結果から平均値を計算し、ランキングを作成
- **使用法**:
  ```bash
  python calculate_persona_averages.py --product-name "商品名"
  ```
- **出力**: `persona_evaluation_results.json`（平均値・ランキング・詳細分析）

#### 3. `check_evaluation_precision.py`
- **目的**: Step 3 - 精度確認
- **機能**: ペルソナ評価結果と元グループの一致率確認（3本以上差分チェック）
- **使用法**:
  ```bash
  python check_evaluation_precision.py --product-name "商品名"
  ```
- **出力**: `precision_check.json`

#### 4. `execute_next_action.py`
- **目的**: Step 4 - 条件分岐とアクション
- **機能**: 精度達成時の承認閾値設定とPhase 3起動
- **使用法**:
  ```bash
  python execute_next_action.py --product-name "商品名" --precision-check "pass" --accuracy-rate "85.0"
  ```

## 実装方針について

**Phase 1・Phase 3はPythonスクリプト未使用**

Phase 1とPhase 3では、PythonスクリプトではなくGitHub Actionsモジュールで直接Claude Code SDKを呼び出す実装となっています：

- **Phase 1**: `modules/module-*.yml` でデータ取得・分析・生成を実行
- **Phase 3**: `modules/module-*.yml` で台本生成・評価・フィルタリングを実行

これにより、Phase 2のみPythonスクリプトによる詳細なデータ処理・精度確認を行い、他のフェーズはシンプルなモジュール構成となっています。

## 削除されたスクリプト

### Phase 1・Phase 3用スクリプト（削除済み）
実装方針変更により、以下のスクリプトは削除されました：
- `analyze_products.py` - 商品・市場分析（module-analyze-product.ymlで実装）
- `fetch_sheets_data.py` - データ取得（module-fetch-data.ymlで実装）
- `web_search.py` - Web検索（module-web-search.ymlで実装）
- `generate_personas.py` - ペルソナ・ライター生成（各moduleで実装）
- `generate_scripts.py` - 台本生成（module-generate-bulk-scripts.ymlで実装）
- `evaluate_scripts.py` - 台本評価（module-evaluate-and-filter.ymlで実装）
- `filter_approved_scripts.py` - 台本フィルタリング（module-evaluate-and-filter.ymlで実装）

### Phase 2旧バージョン（削除済み）
Phase 2の新仕様により以下のスクリプトは不要となり削除されました：
- `calculate_accuracy.py` - 精度計算（新しい基準に変更）
- `evaluate_ranking.py` - ランキング評価（module化）
- `extract_samples.py` - サンプル抽出（新仕様で置換）
- `improve_writers.py` - ライター改善（Phase 3で実装）
- `optimize_criteria.py` - 基準最適化（Claude Code SDKで実装）
- `set_threshold.py` - 閾値設定（新スクリプトで統合）

## 使用方法

各スクリプトは、オーケストレーターワークフローから以下のように呼び出されます：

```yaml
- name: Execute Python Script
  run: |
    python .github/scripts/python/script_name.py \
      --product-name "${{ inputs.product_name }}" \
      --other-params "value" | \
    while read line; do
      echo "$line" >> $GITHUB_OUTPUT
    done
```

## 依存関係

```bash
pip install pandas numpy
```

## 出力形式

各スクリプトは以下の形式でGitHub Actionsに結果を出力します：

```
key=value
status=success/fail
```
