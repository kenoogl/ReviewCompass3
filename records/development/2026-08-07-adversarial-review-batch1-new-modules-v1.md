# 反証レビュー 第1束（本日新設の守り役4 module）結果 v1

- 作成日：2026-08-07
- 承認：`DEC-FOUR-RULINGS-2026-08-07-001`裁定2
- 方法：`docs/development/work-review-protocol.md` §4.4（実装者のfixtureに無い反証を新作して機械で
  試す）・§5（期待挙動を上流から独立導出する）
- 実行者とreviewerは同一（Claude）。**同一実行者による反証であることは限界として記録する**
  （protocol §5：同系modelレビューを唯一の独立oracleにしない）。

## 1. 実施した反証と結果（14件中12件が成立）

反証は隔離tmp環境で1件ずつ実行した（初回試行では反証同士の副作用で3件が誤判定になり、隔離して
再実行した。この誤判定も記録に残す）。

### `reuse_search_record.py`（検索・鮮度gate・外部化）：6件中5件成立

| ID | 反証 | 結果 |
| --- | --- | --- |
| R-1 | 観測file一覧を空にして乖離を隠す | **held**（gateが現存fileを新規扱いで検出し`profile_stale`） |
| R-2 | freshnessの`target_paths`を実在しない範囲へ縮小し、新規fileを隠す | **REFUTED**（gate通過） |
| R-3 | `hits`を空にした「検索したふり」recordを出す | **REFUTED**（gate通過） |
| R-4 | `declaration`と`freshness`の対象範囲を食い違わせる | **REFUTED**（gate通過） |
| R-5 | 証明書の`hit_count`だけ偽装し自己digestを整合させる | **REFUTED**（gate通過） |
| R-6 | 証明書の`source_identity`を別Profileへ差し替える | **REFUTED**（gate通過） |

### `declaration_red_map_check.py`（対応表検査器）：4件すべて成立

| ID | 反証 | 結果 |
| --- | --- | --- |
| C-1 | `test_files`欄から未対応testを外し「結ばれないtest 0件」を偽装 | **REFUTED** |
| C-2 | 宣言の`summary`が空でも合格する | **REFUTED** |
| C-3 | 5つの宣言すべてを同一の1 testへ結ぶ | **REFUTED** |
| C-4 | `red_now: false`（REDでない）でも合格する | **REFUTED** |

### `integration_exclusions.py`（統合除外宣言）：2件すべて成立

| ID | 反証 | 結果 |
| --- | --- | --- |
| X-1 | `authority_refs`に実在しないDecision IDを書く | **REFUTED**（参照は解決されない） |
| X-2 | targetに`tools/`のような広範囲接頭辞を書き、全体を除外する | **REFUTED** |

### `candidate_ranking.py`（順位表）：2件中1件成立

| ID | 反証 | 結果 |
| --- | --- | --- |
| G-1 | digestを壊した除外宣言recordを渡す | **REFUTED**（検証されずに順位表が生成される） |
| G-2 | 観測を空にして鮮度検査を素通りする | **held**（新規fileをstaleとして検出） |

## 2. 欠陥の性質（共通の型）

成立した12件は、単独の実装ミスではなく**3つの型**に整理できる。

**型1：record内部の整合が検査されない（R-2、R-4、C-1、C-3）**
自己digestは「その内容が改竄されていないこと」しか保証せず、**内容が現実と対応しているか**は
別問題である。範囲を縮めた宣言、片方だけ狭めた欄、1 testの使い回しは、いずれも整合検査が
無いために通る。

**型2：参照先が解決されない（R-5、R-6、X-1、G-1）**
recordは他のrecordを参照するが、参照先を開いて突き合わせる処理が無い。証明書は外部本体の
byte一致だけを見て自身の記述内容（hit数・identity）を照合せず、除外宣言の`authority_refs`は
Decision fileの実在すら確認せず、順位表は受け取った除外宣言のvalidatorを呼ばない。

**型3：宣言の中身が空・自明でも合格する（C-2、C-4、X-2）**
形式は満たすが意味の無い記述（空のsummary、falseの`red_now`、`tools/`全体の除外）を止める
仕組みが無い。とくに**C-4は重い**：関門の名が「宣言→**RED**対応表」でありながら、
`red_now`が実際に失敗するかを検査器は一切見ていない。REDでないものをREDと称して通せる。

## 3. 影響評価

- いずれも**悪意の改竄より、うっかりの範囲縮小・写し間違いで起きやすい**。R-2・R-4は宣言を
  手で書き換えるだけで、gateが「新しいコードが増えていないか」を見なくなる。
- C-4は、この開発で最も重視してきた「テストの無い宣言0件」という保証の**質**に関わる。
  数は数えているが、そのtestがREDであることは誰も機械確認していない。
- 実害の発生は現時点で観測されていない（本日の全実運用は正しい入力で行われた）。

## 4. 処置（未実施。修正はレビューと分離）

work-review-protocol §2-5に従い、**本Evidenceでは修正を行わない**。処置案は次のとおりで、
着手はHuman判断とする。

1. 型2（参照解決）は最も安く効く：証明書の記述照合、`authority_refs`の実在検証、順位表での
   除外宣言validator呼び出し。いずれも既存validatorを呼ぶだけで塞げる。
2. 型1（内部整合）：`declaration.target_paths`と`freshness.target_paths`の一致検査、
   `test_files`と宣言側の対応の双方向検査。
3. 型3（中身の実質）：`red_now`の実行照合（対象testを実際に走らせてREDを確認）は設計判断を
   伴うため、要否からHumanに諮る。空summary・広範囲接頭辞の扱いも同様。

## 5. 限界

- 反証は同一実行者が作成した。異なるモデル・別実行者による独立レビューは未実施であり、
  合意順序④（外部APIレビュー）の対象として残る。
- 対象は本日新設の4 moduleのみ。従来上位2系統（`operation_routing`系、Intake／Pilot検証器群）は
  未実施であり、第1束の残りとして続行する。
