# 層1の残り3件 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層1）
- RED Evidence：`records/development/2026-08-07-verification-boundary-layer1-red-evidence-v1.md`
- 対応表：`records/development/2026-08-07-verification-boundary-layer1-declaration-red-map-v1.json`

## 1. 塞いだ穴

| 反証 | 導入した拒否 |
| --- | --- |
| **C-1（完全解消）** | 対応表へ`scope`欄を導入。`complete`（既定）はfileに実在するtest全体を判定対象にし、欄からも宣言からも漏れたtestを検出する。`partial`は列挙分だけを対象にするが、**理由の記載を必須**とする。scope欄が無い対応表は`complete`として扱い、黙って範囲を狭められないようにした |
| **C-2（形式面）** | 宣言の`summary`が空白のみの対応表を拒否する |
| **R-3** | `gate_check`にProfileとDiscoveryを渡すと**検索を再実行**し、記録との`content_digest`一致を確認する。`hits`を空にした「検索したふり」は`search_result_mismatch`で拒否される |
| **I-2（機械化可能部分）** | `check_decision_time_monotonicity`を追加。後継decisionの決定時刻が前版より過去へ戻ることを拒否する。**文面の真偽は依然として層3のまま**であり、版と時刻の矛盾だけを検出する |

- targeted：`tests/test_verification_boundary_layer1.py` 9 test。RED 8＋境界例1 → GREEN 9/9。
- 公式全Test：`1111 passed`、exit `0`。

## 2. 新手順（実行照合）の初適用が誤申告を検出

`DEC-RED-VERIFICATION-ADOPTION-001`の手順をRED固定前に適用したところ、**初回で
`mismatched: 1`**となった。L2（`scope: partial`の挙動）を`red_now: true`と申告していたが、
実装前の検査器は`scope`欄を読まないため実際には成功していた。境界例（`red_now: false`＋
`boundary_reason`）へ訂正し、再照合で`checked=9 verified=9 mismatched=0`となってからcommitした。
**手順の採用初日に、手順が誤りを1件捕まえた。**

## 3. stale閉包（新規則での再検査）

対応表14枚を新しい静的検査で再検査した【実測】。

- **11枚が`passed`**
- 失敗3枚のうち2枚は**superseded済みの歴史record**（Intake v1、処置対応表v1）であり、
  運用検査の対象外である
- 残る1枚**Intake対応表v2**は、`tests/test_issue_intake_v4.py`の他36 testが未対応と判定された。
  これは実装の欠陥ではなく、部分列挙という設計に`scope`欄が無かったためであり、**今回の設計判断が
  解決すべき当のケース**である。意味内容を変えず`scope: partial`＋理由を明示した**v3**を作成し、
  `passed`を確認した（`records/development/2026-08-07-intake-v4-declaration-red-map-v3.json`）

## 4. fixture更新1件

`tests/test_declaration_red_verification.py`のfixtureへ`scope: partial`＋理由を追加した。
このfixtureは`red_now`照合の検証のみを目的とし、file内の全testを扱わないためである。
**検証を弱める変更ではない**（`DEC-ADVERSARIAL-REMEDY-BATCH1-001` §2の許可範囲）。

## 5. 残余

- 層1は完了。残るは層2（O-1分類の下限規則、A-1 pathspec形式検査、X-2影響件数表示）と
  層3（明示）である。
- `gate_check`の再検索は**呼び出し側がProfileとDiscoveryを渡した場合のみ**動く。実運用の
  呼び出し経路へ組み込むかは、層2・層3の実装時にあわせて判断する。
