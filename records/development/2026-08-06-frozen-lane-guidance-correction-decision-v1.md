# 凍結レーンへ案内した手順の訂正と再発防止 承認Decision v1

- Decision ID：`DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001`
- decision maker：Human
- decided at：`2026-08-06T12:51:33+09:00`
- decision：`approved`
- decision class：`operational_guidance_correction`
- 訂正対象：`DEC-IMPROVEMENT-CANDIDATE-LANE-GUIDANCE-001`
  （`records/development/2026-08-06-improvement-candidate-lane-guidance-decision-v1.md`）

## 1. 何が起きたか

`DEC-IMPROVEMENT-CANDIDATE-LANE-GUIDANCE-001`により`AGENTS.md`へ追記した改善候補の登録手順は、
検証までしか書いておらず、**Humanの仕分け判断をどこへ記録するかを示していなかった**。

その先にある旧Pilotの仕分け判断とIssueの置き場所は各1件で凍結されている。凍結は
`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`
と`tests/test_issue_intake_v4.py::test_k6_legacy_v1_decision_and_pilot_validation_keep_passing`が
件数とfile名で固定しており、意図的な設計判断である。根拠は
`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` §1.1「旧記録は旧versionの規則の
まま保持し、新規則で再判定しない」である。

結果として、追記した手順は**凍結されたレーンへ案内する行き止まり**になっていた。
実際に`IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の仕分け判断を記録しようとして停止した。

## 2. 原因

1. 凍結が機械可読な形でどこにも宣言されていない。置き場所にも設定にも表示が無く、
   commit message、設計提案の本文、Testのassertに散在している。
2. 版番号付きの成果物のうちどれが現行かが宣言されていない。
3. `AGENTS.md`へ運用手順を書く前に、指し先が現行かを確かめる手順が定まっていなかった。

Claudeは委任先の調査報告に含まれていた「新Issueは後継directory側に置く必要がある」という指摘を、
案の要約段階で反映しなかった。

## 3. Humanが承認した対応（①と②）

### ① `AGENTS.md`の訂正

改善候補の経路の記述を2項目へ分け、仕分け判断の保存先を`records/development/`のDecision recordと
明示した。あわせて、旧Pilotの置き場所が各1件で凍結されていること、V4の置き場所は固定bundle参照
だけを受け付けるため単体候補は現時点で載らないこと、この制約の解消は別のHuman判断とすることを
記した。凍結されたpathは保存先として名指ししていない。

### ② 再発を止めるTest

`tests/test_agents_lane_guidance.py`を新設し、RED先行で次を固定した。

| test | 要求 |
| --- | --- |
| `test_agents_lane_guidance_names_the_triage_decision_destination` | 改善候補の経路を説明する箇所に、仕分け判断の保存先pathが現れること |
| `test_agents_does_not_name_frozen_lanes_as_record_destinations` | 凍結された置き場所を名指ししていないこと。後継の`-v4`は誤検出しない |
| `test_frozen_lane_inventory_is_not_stale` | 凍結2件と後継2件のdirectoryが実在し、凍結リストが古びていないこと |

凍結リストはtest冒頭のmodule定数として、根拠のcommentつきで宣言した。

RED時点は`1 failed, 1019 passed`（total 1020）で、失敗は保存先の欠落1件だけであった。
訂正後は`1020 passed`（failed 0、errors 0、Python 3.9.6、pytest 8.4.2、fallback `false`）。

## 4. Claude側の作業手順（承認不要、Claudeが徹底する）

版番号付きの成果物（設定、置き場所、形式）を手順書や指示へ書く前に、次を機械的に確認する。

- 後継の版が存在しないか（番号違いのfileを探す）
- その置き場所についてTestが何を断言しているか（Testを検索する）

## 5. 非承認範囲

- V4の置き場所が単体候補を直接参照できるようにする変更。Humanから提案があったが、
  schema変更と既存Test（`test_k7`、`test_l6`）の改定を伴うため、実現方法を調査したうえで
  別途Human判断とする。
- 凍結状態を設定へ宣言する仕組み（③）。今日見つかった参照Digest driftの候補と同じ
  「現行か歴史かが機械可読でない」という不足に属し、束ねて扱うかを別途判断する。
- `IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の仕分け判断そのもの。未記録である。

## 6. 固定Evidence

| path | SHA-256 |
| --- | --- |
| `AGENTS.md`（訂正後） | `eb2e5535a0bcb03ad1ace973178b90da60eb1acd6d34c76276919b574e622ade` |
| `tests/test_agents_lane_guidance.py` | `2916ba1ae0bcfdffffefc6248c239324e11271227fa4411b7eba788b03071000` |
| `records/development/2026-08-06-improvement-candidate-lane-guidance-decision-v1.md` | `3603549405c8f4962410fa4c4d301a94fac6b79fea1b16f9f2f41b3f79b265af` |

RED commitは`ff20380`である。

## 7. 既存recordへの影響

new-onlyで作成した。`DEC-IMPROVEMENT-CANDIDATE-LANE-GUIDANCE-001`は削除も書換えもせず、
その§2の追記文言だけを本Decisionが置換する。同Decisionの§4が既に「直接の入口は無いままである」と
記していた不足が、実際に行き止まりとして現れた事例である。
