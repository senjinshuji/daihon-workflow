# プルリクエストベースのワークフロー（オプション）

## 現在の動作
現在のワークフローは、各フェーズ完了時に**直接mainブランチ**にコミット・プッシュします。

## プルリクエストベースに変更する方法

### 方法1: 各フェーズごとにPRを作成

`finalize`ジョブを以下のように変更：

```yaml
finalize:
  needs: [...]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    
    - name: Create feature branch
      run: |
        BRANCH_NAME="phase1-${{ inputs.product_name }}-$(date +%Y%m%d-%H%M%S)"
        git checkout -b $BRANCH_NAME
    
    - name: Commit changes
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git add -A
        git commit -m "✅ [${{ inputs.product_name }}] Phase 1 完了"
    
    - name: Push branch
      run: |
        git push origin $BRANCH_NAME
    
    - name: Create Pull Request
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        gh pr create \
          --title "✅ [${{ inputs.product_name }}] Phase 1: 分析・ペルソナ・ライター生成" \
          --body "## 概要
          Phase 1の実行が完了しました。
          
          ### 生成内容
          - 商品分析
          - ターゲット分析（3種）
          - ペルソナ（3種）
          - ライター人格（3種）
          
          ### 次のステップ
          このPRをマージ後、Phase 2を実行してください。" \
          --base main \
          --head $BRANCH_NAME
```

### 方法2: 全フェーズ完了後に1つのPRを作成

最終フェーズ（Phase 3）の最後に：

```yaml
- name: Create comprehensive PR
  if: needs.evaluate_and_filter.outputs.approval_rate >= 60
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    BRANCH_NAME="campaign-${{ inputs.product_name }}-complete"
    git checkout -b $BRANCH_NAME
    git add -A
    git commit -m "🎉 [${{ inputs.product_name }}] 全フェーズ完了: 台本生成ワークフロー"
    git push origin $BRANCH_NAME
    
    gh pr create \
      --title "🎉 [${{ inputs.product_name }}] 台本生成ワークフロー完了" \
      --body "## 📊 実行結果サマリー
      
      ### Phase 1: 分析・ペルソナ生成 ✅
      - 商品分析完了
      - ターゲット分析（3種）完了
      - ペルソナ生成（3種）完了
      - ライター生成（3種）完了
      
      ### Phase 2: 評価基準最適化 ✅
      - 精度: ${{ needs.check_precision.outputs.accuracy_rate }}%
      - 承認閾値設定完了
      
      ### Phase 3: 台本生成 ✅
      - 生成台本数: 15本
      - 承認台本数: ${{ needs.evaluate_and_filter.outputs.approved_count }}本
      - 承認率: ${{ needs.evaluate_and_filter.outputs.approval_rate }}%
      
      ### 📁 生成ファイル
      - \`${{ inputs.product_name }}/artifacts/\` - 分析結果
      - \`${{ inputs.product_name }}/personas/\` - ペルソナ定義
      - \`${{ inputs.product_name }}/writers/\` - ライター定義
      - \`${{ inputs.product_name }}/scripts/\` - 生成台本
      - \`${{ inputs.product_name }}/evaluations/\` - 評価結果
      
      ### ✅ レビューチェックリスト
      - [ ] 商品分析の内容確認
      - [ ] ペルソナ設定の妥当性確認
      - [ ] 承認台本の品質確認
      - [ ] 制作開始の承認" \
      --base main \
      --head $BRANCH_NAME
```

### 方法3: 保護ブランチ設定でレビューを強制

GitHub リポジトリ設定で：
1. Settings → Branches
2. Add rule でmainブランチを保護
3. 以下を有効化：
   - Require pull request reviews before merging
   - Require review from CODEOWNERS
   - Dismiss stale pull request approvals

## メリット・デメリット

### 直接プッシュ（現在）
**メリット**:
- シンプルで高速
- 自動化がスムーズ
- 中間結果がすぐ反映

**デメリット**:
- レビューなし
- 履歴が複雑

### PRベース
**メリット**:
- レビュー可能
- 変更履歴が明確
- ロールバック容易

**デメリット**:
- 手動承認が必要
- ワークフローが複雑化
- 実行時間増加

## 推奨設定

1. **開発・テスト時**: 直接プッシュ（現在の設定）
2. **本番運用時**: PRベースまたは別ブランチで実行
3. **ハイブリッド**: 
   - Phase 1-2は直接プッシュ
   - Phase 3完了時のみPR作成