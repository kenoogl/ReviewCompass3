# Work 4B本体 設計束提案 v1

- 状態：`human_decision_pending`（Human承認まで実装・REDを開始しない）
- 作成日：2026-08-07
- 位置づけ：`DEC-WORK5B-DISCUSSION-OUTCOMES-001`の合意順序②。4構成を一枚で判断できる形にまとめ、
  個別の再提案を避ける。

## 1. 固定入力

| 固定入力 | path | SHA-256 |
| --- | --- | --- |
| 設計議論の証跡Decision | `records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md` | `8cfc4a1581ed53513d97f70fa78323f6dc574eb2555bbd35ed78c7a4e1214a9d` |
| Work 4A早期完了Decision | `records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md` | `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e` |
| Current Plan（§12 Work 4B） | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Work 5B残項目defer Decision | `records/development/2026-08-07-work5b-ledger-item-defer-decision-v1.md` | `1aa07f006481e684c97f54cc26a7ae97996655b04e6b72da7d8eee461106f788` |
| Work 4B最小試行 GREEN Evidence | `records/development/2026-08-07-work4b-reuse-search-green-evidence-v1.md` | `3284f77507a2ad09992404cae1ced846a6fe5ccdd564af8c8c0e8772e0588e0c` |
| Work 5B検査器 GREEN Evidence | `records/development/2026-08-07-work5b-checker-green-evidence-v1.md` | `020db589b586e6db741e0d5d347d31c30c89a077c390ebd2232c42dfccbb7d2c` |

実データの現行identityはWork 4A v3.3（routine 1003件、group 682件、2026-08-05観測）である。

## 2. 構成A：統合除外宣言と絞り込み順位表（合意の「すぐ対処」）

**目的**：LLM意味判断（三段目）へ渡す候補groupを、機械計算だけで順位付けし、
統合してはいけないものを先に外す。

**A-1 統合除外宣言（承認先行）**：`.reviewcompass/workflow/integration-exclusions/`へ
new-onlyのJSON recordとして置く。entryは`対象（module pathまたはsymbol_id接頭）`、`理由種別
（version_pinned | frozen_lane | historical_retained | superseded_kept）`、`根拠Decision参照`を持つ。
初版の候補entryは、版付きvalidator（要件系v1、旧Pilot検証器）、凍結レーン（旧Pilot仕分け・Issue置き場）、
歴史保持record群である。**宣言の内容はHuman承認事項**（本提案の承認とは別に、初版entry一覧を
候補として提示し裁定を受ける）。

**A-2 絞り込み順位表**：ProfileとDiscoveryから決定的に生成する順位record。順位の計算は
合意済み4観点——(1)basis_kindの強さ（`structural_exact_match`最上位）、(2)現に変更する範囲との
交差、(3)守り役moduleの含有（トリアージメモの一覧を機械参照）、(4)member数・行数・跨り・乖離の
兆候——の重み付き合成とし、重みは初版では単純な辞書式順（1→3→4→2）とする。除外宣言に該当する
groupは順位表から機械的に落ち、落とした件数を順位表自身が表示する（silent capの禁止）。

## 3. 構成B：Profile再観測の検索への組み込み

**目的**：検索が「5日時点の地図」に縛られる鮮度問題（Work 5Bで実例1件）を解消する。

再観測は既存の`work4a_rebuild_v3.py`の経路（source universe再観測→Profile v3生成、new-only）を
そのまま使い、新しい生成器は作らない。組み込み方は次の2段とする。

1. `reuse_search_record`の生成時に、Profileの観測時点とHEADの乖離（観測後にcommitされた
   `tools/`配下の変更file数）を機械計測し、recordへ`freshness`欄として記録する。
2. 乖離が閾値（初版は「対象範囲のfileに観測後の変更が1件でもある」）を超える場合、gateは
   `start_allowed: false`（`profile_stale`）を返し、再観測してからの再検索を要求する。

## 4. 構成C：検索recordの外部化（証明書方式）

**目的**：1件数百KBの検索recordでGit repositoryが太る問題を、Work 4Aの先例で解決する。

- 検索record本体は外部DATA_ROOT（`<runtime_root>/projects/reviewcompass3/development/data/`）の
  `work4b/reuse-searches/<content_digest>.json`へnew-onlyで置く。
- project内（`records/development/`）には小さな**Attestation（証明書）**だけを置く：
  subject、外部recordのrelative path、content digest、source identity、hit件数、gate判定。
  形式はWork 4Aの`work4a_observation_attestation`の型を踏襲する。
- gate判定（`gate_check`）はAttestation経由で外部recordを解決し、Digest一致まで確認して判定する。
  外部recordが失われた場合はfail-closed（`record_unavailable`）。
- 既存2件の検索record（924KB・647KB）は移行対象とし、移行はbyte一致検証つきの別作業単位で行う
  （書庫移行と同じ型。旧位置はrollback用に保持し、削除は別途Human判断）。

## 5. 構成D：台帳（Entry・Relation・Baseline）の最小形

**目的**：Human確定の処置labelと部品の系譜を、実装関門から参照できる正本にする。
Work 5Bのdefer項目（helper 2件の台帳Entry）の再開条件でもある。

- 置き場：`.reviewcompass/workflow/routine-ledger/`（new-only、path単独では正本にしない）。
- **Entry**：一routine（または一部品）の台帳項目。symbol_id、code_reference、処置label
  （`reuse | extend | merge | split | as_is`）、労定Decision参照、由来（新設／継承／統合）。
  **labelはHuman裁定Decisionへの参照なしには書けない**（検証器で拒否）。
- **Relation**：部品間の型付き関係（`duplicate_of | extracted_to | replaces | depends_on`）。
  Work 5Bで可視化された実例（正規化digest計算3箇所など）が初期候補。
- **Baseline**：Human承認済みの共通部品集合のsnapshot。統合の進捗はBaselineの版で追う。
- 初版はEntryとRelationの schema・検証器・手作業記入経路だけを実装し、Baselineは最初の統合
  Work Itemが承認された時点で開始する。台帳の自動記入・一括分類は行わない。

## 6. 実装順（推奨）

1. **A-1** 統合除外宣言（Human承認が先行）
2. **B** 再観測の組み込み（順位表の鮮度の前提）
3. **A-2** 絞り込み順位表
4. **D** 台帳最小形 → Work 5B defer項目の完了戻し（helper 2件のEntry記録）
5. **C** 検索recordの外部化と既存2件の移行

各構成は独立の作業単位とし、実装前に本提案の該当節を規範宣言へ展開して宣言→RED対応表を作り
（照合は恒久検査器`declaration_red_map_check.py`）、REDを固定してから実装する。すべて
実装前の再利用検索gateを通す。

## 7. 非対象

- LLM意味判断の実行（絞り込み順位表の生成までが本提案。LLM起動は別承認）
- レビューbacklogの着手（合意順序③として本設計束の後）
- RC2先行資産の取り込み、外部APIレビュー（合意順序④、台帳整備後）
- 全1003 routineの一括分類・一括台帳化
- 順位重みの調整・学習（初版は固定の辞書式順。実測後の変更はHuman判断）

## 8. risk（work-review-protocol §3）

構成B（gateの鮮度判定）、構成C（gateの外部解決とDigest照合）、構成D（labelの裁定参照検証）は
いずれも守り役codeの拡張であり既定`high`。構成Cの既存record移行は不可逆操作を含むため`high`
（byte一致検証と旧位置保持で緩和する）。

## 9. Human判断点

1. 本設計束の承認・修正・却下（構成単位の部分承認も可）
2. A-1の除外宣言の初版entry一覧（本提案の承認後、候補一覧を別途提示して裁定）
3. 実装順（§6の推奨どおりか）
4. C の閾値・B の閾値（初版値でよいか）
