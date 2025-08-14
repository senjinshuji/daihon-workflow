# AIクリエイティブ自動生成ワークフロー図

## 1. 全体フロー図

```mermaid
graph TB
    Start([開始: 商品名入力]) --> Phase1{Phase 1<br/>初期分析}
    
    Phase1 --> |並列実行| P1A[データ取得<br/>Google Sheets]
    Phase1 --> |並列実行| P1B[Web検索<br/>Gemini API]
    
    P1A --> P1C[商品・市場分析<br/>Claude SDK]
    P1B --> P1C
    
    P1C --> |並列実行| P1D[ペルソナ生成<br/>3名]
    P1C --> |並列実行| P1E[ライター生成<br/>3名]
    
    P1D --> P1F[評価基準初期化<br/>criteria.json]
    P1E --> P1F
    
    P1F --> Phase2{Phase 2<br/>最適化ループ}
    
    Phase2 --> P2A[台本生成<br/>3×5=15本]
    P2A --> P2B[ペルソナ評価<br/>3×3×5=45評価]
    P2B --> P2C[スコア分析]
    P2C --> P2D{改善率<br/>>5%?}
    
    P2D -->|Yes| P2E[基準最適化]
    P2E --> P2F[ループ番号+1]
    P2F --> Phase2
    
    P2D -->|No| Phase3{Phase 3<br/>最終生成}
    
    Phase3 --> P3A[最終台本生成<br/>15本]
    P3A --> P3B[最終評価<br/>45評価]
    P3B --> P3C[ランキング作成]
    P3C --> P3D[レポート生成]
    P3D --> P3E[納品物パッケージ]
    P3E --> End([完了])
    
    style Start fill:#e1f5fe
    style End fill:#c8e6c9
    style Phase1 fill:#fff3e0
    style Phase2 fill:#fce4ec
    style Phase3 fill:#f3e5f5
```

## 2. Phase 1 詳細フロー

```mermaid
graph LR
    subgraph "Phase 1: 初期分析とペルソナ生成"
        A[商品名入力] --> B{並列処理}
        
        B --> C[Google Sheets API]
        B --> D[Gemini API]
        
        C --> E[4つのCSV取得<br/>- market_bestsellers<br/>- internal_top<br/>- internal_middle<br/>- internal_bottom]
        
        D --> F[Web検索実行<br/>- 商品レビュー<br/>- 競合分析<br/>- 市場トレンド]
        
        E --> G[Claude SDK<br/>データ統合]
        F --> G
        
        G --> H[分析レポート生成<br/>- product_analysis.md<br/>- market_analysis.md]
        
        H --> I{並列生成}
        
        I --> J[ペルソナ×3<br/>- persona1: 実用性<br/>- persona2: 革新性<br/>- persona3: 安定性]
        
        I --> K[ライター×3<br/>- writer1: 感情型<br/>- writer2: 論理型<br/>- writer3: ハイブリッド]
        
        J --> L[criteria.json<br/>初期化]
        K --> L
    end
```

## 3. Phase 2 詳細フロー（最適化ループ）

```mermaid
graph TB
    subgraph "Phase 2: 評価と最適化ループ"
        Start[ループ開始<br/>n=2] --> GenScripts{並列生成}
        
        GenScripts --> W1[Writer1<br/>5台本]
        GenScripts --> W2[Writer2<br/>5台本]
        GenScripts --> W3[Writer3<br/>5台本]
        
        W1 --> Eval{並列評価<br/>9プロセス}
        W2 --> Eval
        W3 --> Eval
        
        Eval --> E1[W1×P1]
        Eval --> E2[W1×P2]
        Eval --> E3[W1×P3]
        Eval --> E4[W2×P1]
        Eval --> E5[W2×P2]
        Eval --> E6[W2×P3]
        Eval --> E7[W3×P1]
        Eval --> E8[W3×P2]
        Eval --> E9[W3×P3]
        
        E1 --> Analysis[評価分析<br/>45件集計]
        E2 --> Analysis
        E3 --> Analysis
        E4 --> Analysis
        E5 --> Analysis
        E6 --> Analysis
        E7 --> Analysis
        E8 --> Analysis
        E9 --> Analysis
        
        Analysis --> Optimize[基準最適化<br/>Claude SDK]
        
        Optimize --> Check{改善率判定}
        
        Check -->|>5%| Update[基準更新<br/>n++]
        Update --> Start
        
        Check -->|≤5%| Exit[Phase 3へ]
    end
```

## 4. Phase 3 詳細フロー

```mermaid
graph LR
    subgraph "Phase 3: 最終生成と納品"
        A[最適化済み基準] --> B[最終台本生成<br/>15本]
        
        B --> C[最終評価<br/>45評価実行]
        
        C --> D[スコア集計]
        
        D --> E[ランキング作成<br/>TOP 10]
        
        E --> F[レポート生成]
        
        F --> G[deliverables/<br/>├── final_report.md<br/>├── summary.json<br/>└── selected_scripts/]
        
        G --> H[Git Commit<br/>& Push]
        
        H --> I[完了通知]
    end
```

## 5. 並列処理マトリックス

```
Phase 2 評価マトリックス（9並列プロセス）:

         Persona1    Persona2    Persona3
        ┌─────────┬──────────┬──────────┐
Writer1 │ Process │ Process  │ Process  │
        │   1     │    2     │    3     │
        ├─────────┼──────────┼──────────┤
Writer2 │ Process │ Process  │ Process  │
        │   4     │    5     │    6     │
        ├─────────┼──────────┼──────────┤
Writer3 │ Process │ Process  │ Process  │
        │   7     │    8     │    9     │
        └─────────┴──────────┴──────────┘

各プロセス: 5台本を評価 → 合計45評価
```

## 6. データフロー図

```
┌──────────────────────────────────────────────────────┐
│                    INPUT DATA                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
│  │Google      │  │Web Search  │  │Product     │    │
│  │Sheets CSV  │  │Results     │  │Name        │    │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘    │
│        │               │               │            │
└────────┼───────────────┼───────────────┼────────────┘
         │               │               │
         ▼               ▼               ▼
┌──────────────────────────────────────────────────────┐
│                 CLAUDE CODE SDK                      │
│  ┌─────────────────────────────────────────────┐    │
│  │  Analysis → Generation → Evaluation         │    │
│  │  ↓         ↓            ↓                  │    │
│  │  Reports   Personas     Scores             │    │
│  │            Writers      Rankings           │    │
│  │            Scripts                         │    │
│  └─────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│                    OUTPUT FILES                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
│  │Analysis    │  │Scripts     │  │Final       │    │
│  │Reports     │  │(15×n)      │  │Deliverables│    │
│  └────────────┘  └────────────┘  └────────────┘    │
└──────────────────────────────────────────────────────┘
```

## 7. 実行タイムライン

```
時間軸（分）
0    5    10   15   20   25   30   35   40   45   50   55   60
├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
│
├─Phase 1 (15分)─────────┤
│ ├Data─┤                │
│ ├Web──┤                │
│      ├Analysis─┤       │
│           ├Gen──┤      │
│
                         ├─Phase 2 Loop (25分)──────────────┤
                         │ ├Scripts──┤                      │
                         │          ├Evaluate──┤           │
                         │                   ├Opt┤         │
│
                                                           ├─Phase 3 (20分)───────┤
                                                           │ ├Final Gen──┤        │
                                                           │           ├Eval─┤    │
                                                           │              ├Rep┤  │
```

## 8. システムアーキテクチャ図

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Runner                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │   Workflow   │───▶│ Claude Code  │──▶│   Python     │  │
│  │   Trigger    │    │     SDK      │   │   Scripts    │  │
│  └──────────────┘    └──────────────┘   └──────────────┘  │
│         │                    │                   │         │
│         ▼                    ▼                   ▼         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    File System                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │  Prompts │  │   Data   │  │    Artifacts     │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  External APIs                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │ Claude   │  │  Gemini  │  │  Google Sheets   │  │  │
│  │  │   API    │  │    API   │  │      API         │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 9. 決定木フロー

```
                    [商品入力]
                        │
                        ▼
                  ┌───────────┐
                  │  Phase 1  │
                  │   実行    │
                  └─────┬─────┘
                        │
                        ▼
                   [Loop n=2]
                        │
                        ▼
                  ┌───────────┐
                  │  Phase 2  │
                  │   実行    │
                  └─────┬─────┘
                        │
                        ▼
                  ┌───────────┐
                  │ 改善率    │
                  │  >5%?     │
                  └──┬────┬───┘
                     │    │
                  Yes│    │No
                     ▼    ▼
                [n++]  ┌───────────┐
                  │    │  Phase 3  │
                  │    │   実行    │
                  │    └─────┬─────┘
                  │          │
                  └──────┐   ▼
                        │  [完了]
                        │
                        └────┘
```

## 10. モジュール依存関係図

```mermaid
graph TD
    subgraph "Orchestrators"
        O1[orchestrator-phase1]
        O2[orchestrator-phase2]
        O3[orchestrator-phase3]
    end
    
    subgraph "Modules"
        M1[module-fetch-sheets]
        M2[module-web-search]
        M3[module-analyze-product]
        M4[module-generate-personas]
        M5[module-generate-writers]
        M6[module-generate-scripts]
        M7[module-evaluate-scripts]
        M8[module-optimize-criteria]
    end
    
    O1 --> M1
    O1 --> M2
    O1 --> M3
    O1 --> M4
    O1 --> M5
    
    O2 --> M6
    O2 --> M7
    O2 --> M8
    
    O3 --> M6
    O3 --> M7
    
    M1 --> M3
    M2 --> M3
    M3 --> M4
    M3 --> M5
    M6 --> M7
    M7 --> M8
```

---

これらの図により、ワークフロー全体の構造と処理の流れが視覚的に理解できます。