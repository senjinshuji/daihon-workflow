# Phase 2 - タスク4: ペルソナ評価基準（persona_evaluation_criteria.yaml）

## 📋 このタスクの概要
ペルソナが台本を評価する際の基準となるYAMLファイルを作成します。

## 実行手順

### ステップ1: 評価基準ファイルの作成

```bash
echo "📊 ペルソナ評価基準を作成します..."

cat > projects/$PROJECT_NAME/loop1/persona_evaluation_criteria.yaml << 'EOF'
# ペルソナ評価基準
# 成功した動画広告の共通要素抽出と評価フレームワーク

task: "動画広告台本の評価"
description: "提供された台本を以下の基準で評価し、改善点を提案する"

## 必須評価項目（各10点満点）
evaluation_criteria:
  1_appeal_clarity:
    name: "訴求方向性の明確性・一貫性"
    max_score: 10
    check_points:
      - "価格・権威性・効果のいずれかが明確か"
      - "最初から最後まで一貫しているか"
      - "混在して曖昧になっていないか"

  2_differentiation:
    name: "他選択肢との差別化の明確性"
    max_score: 10
    check_points:
      - "競合サービスとの違いが明確か"
      - "代替手段との違いが示されているか"
      - "なぜ他ではダメなのかが分かるか"

  3_usp_strength:
    name: "独自価値提案(USP)の強度"
    max_score: 10
    check_points:
      - "この商品独自の価値が明確か"
      - "ユニークさが際立っているか"
      - "記憶に残る独自性があるか"

  4_reason_clarity:
    name: "選ばれる理由の決定的明確性"
    max_score: 10
    check_points:
      - "なぜこれを選ぶべきか明確か"
      - "決定的な理由が示されているか"
      - "納得感のある根拠があるか"

  5_hook_impact:
    name: "冒頭フックの強烈さ"
    max_score: 10
    check_points:
      - "最初の5秒で興味を引けるか"
      - "続きを見たくなるか"
      - "右脳に直接訴えかけるか"

  6_natural_flow:
    name: "売り込み感の排除度"
    max_score: 10
    check_points:
      - "自然な流れで商品が登場するか"
      - "押し売り感がないか"
      - "視聴者が自発的に興味を持つか"

  7_character_edge:
    name: "キャラクターのエッジ立ち"
    max_score: 10
    check_points:
      - "語り手の個性が明確か"
      - "ターゲットに合った口調か"
      - "信頼感や親近感があるか"

  8_strategic_integration:
    name: "WHO-FMT-USP戦略的統合性"
    max_score: 10
    check_points:
      - "ターゲット設定が適切か"
      - "フォーマットが効果的か"
      - "USPが戦略的に組み込まれているか"

  9_flow_naturalness:
    name: "構成フローの自然さ"
    max_score: 10
    check_points:
      - "各パートの繋がりが自然か"
      - "情報の出し方が適切か"
      - "最後まで飽きずに見られるか"

  10_emotional_impact:
    name: "右脳直撃インパクト"
    max_score: 10
    check_points:
      - "感情に訴える要素があるか"
      - "理屈より感覚に響くか"
      - "行動したくなる衝動があるか"

  11_trust_building:
    name: "先回り対処による信頼構築"
    max_score: 10
    check_points:
      - "想定される不安に答えているか"
      - "疑問を先回りして解消しているか"
      - "信頼できる根拠が示されているか"

## 台本構成の評価ポイント
script_structure_evaluation:
  hook_0_5sec:
    importance: "最重要"
    evaluation_points:
      - "視聴者が「なんで？」と感じるか"
      - "強い興味を引く要素があるか"
      - "見る理由＝買う理由になっているか"

  development_5_20sec:
    importance: "重要"
    evaluation_points:
      - "冒頭の疑問に答えているか"
      - "共感や納得を生んでいるか"
      - "ターゲットの悩みに寄り添っているか"

  solution_20_40sec:
    importance: "重要"
    evaluation_points:
      - "解決策が明確に示されているか"
      - "独自性が伝わっているか"
      - "他の選択肢との違いが分かるか"

  credibility_40_50sec:
    importance: "標準"
    evaluation_points:
      - "信頼できる根拠があるか"
      - "実績や事例が示されているか"
      - "不安が解消されるか"

  cta_50_60sec:
    importance: "重要"
    evaluation_points:
      - "行動を促す仕掛けがあるか"
      - "限定性・緊急性が示されているか"
      - "具体的なアクションが明確か"

## 総合評価の算出方法
scoring_method:
  total_score: "11項目の合計（110点満点）"
  grade_scale:
    S: "99点以上（90%以上）"
    A: "88-98点（80-89%）"
    B: "77-87点（70-79%）"
    C: "66-76点（60-69%）"
    D: "65点以下（60%未満）"

## 評価レポートフォーマット
report_format:
  summary:
    - "総合スコア"
    - "グレード"
    - "最も優れた点"
    - "最も改善が必要な点"
  
  detailed_scores:
    - "11項目の個別スコア"
    - "各項目のコメント"
  
  improvement_suggestions:
    - "具体的な改善提案"
    - "参考になる成功事例"
    - "次回への推奨事項"
EOF

echo "✅ persona_evaluation_criteria.yaml 作成完了"
```

### 完了確認
```bash
if [ -f "projects/$PROJECT_NAME/loop1/persona_evaluation_criteria.yaml" ]; then
    echo "✅ Phase 2 タスク4: persona_evaluation_criteria.yaml の作成が完了しました"
    echo "📊 11項目の評価基準が設定されました"
else
    echo "❌ エラー: persona_evaluation_criteria.yaml の作成に失敗しました"
fi
``` 