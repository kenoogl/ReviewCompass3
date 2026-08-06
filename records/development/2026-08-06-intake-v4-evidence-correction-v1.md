# Issue Intake V4 Evidence 訂正記録 v1

- 訂正の根拠：`docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md` §4
  （SHA-256 `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358`、Human承認済み）
- 訂正対象1：`records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md`
  （SHA-256 `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f`）
- 関連：`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md`
  （SHA-256 `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e`）
- 記録日時：`2026-08-06T14:44:55+09:00`

## 0. 位置づけ

**旧記録をin-placeで書き換えていない。** 訂正内容を本記録にnew-onlyで固定し、旧記録は当時の
状態の記録として履歴に残す。

## 1. 訂正1：「設計§1.3に従い置き換えた」という記述の誤り

### 旧記述

V4実装のGREEN Evidence（訂正対象1）の「既存testの取扱い」節は、
`test_repository_contains_only_the_single_valid_pilot_subject`の検査対象を
「**設計§1.3に従い**『候補file数が1件』から次へ置き換えた」と記している。

### 誤りの内容

置き換え後の実際の検査は「Issue recordがちょうど1件」「v2候補がv2 configで検証を通る」
「他の候補はV2 configで再判定しない」であり、設計§1.3が求めた
「**未triage候補が滞留していないか**（各候補が`triage_decision_ref`を持つか`untriaged`として
明示されているか）」ではない。§1.3に対応する実装もtestも、2026-08-06の調査時点で存在しなかった
（`records/development/2026-08-06-encountered-problem-inventory-v1.md` #9-a・#9-g）。

節番号の引用により、実際には別の検査へ差し替わったことが読み取れなくなっていた。

### 現在の状態

§1.3の趣旨は、承認済み提案の規範宣言N7・N8・N11により2026-08-06に狭く実装された
（候補置き場の全件検証、歴史allowlistによる明示宣言、bundle内41候補全件の有効decision存在検査。
GREEN Evidence：`records/development/2026-08-06-intake-v4-single-candidate-green-evidence-v1.md`、
SHA-256 `d63bb9330bbed22f1346618e01ed1710884e55a9e5b3d58686962140b7e7629c`）。
「各候補が`triage_decision_ref`を持つ」形は採らない。候補recordは不変であり、後から増える判断を
候補側へ書けないためである（提案§4の設計改定）。

## 2. 関連：閉鎖Evidenceの「未判断0件」

閉鎖Evidence（関連record）の「有効decision 41件、未判断0件」は、記録時点の手作業観測としては
正しかったが、それを維持する機械検査は存在しなかった（問題一覧#9-h）。2026-08-06以降は
`test_n11_every_bundle_candidate_has_an_effective_decision`が機械で維持する。
閉鎖Evidence自体の訂正は不要である（記述は当時の事実と一致している）。

## 3. その他の食い違いの処置（承認済み提案§4の再掲）

| 対象 | 処置 |
| --- | --- |
| §2.3 X4「除外」 | 実装（重複疑いの保持）へ設計を合わせる改定として確定 |
| §3.1／§3.2（一括判断） | Work 8の手作業Pilot評価へ延期として確定 |
| §4.1経路（`improvement_candidate`経由） | 実装形（bundle直結＋単体直結）を正式とする改定として確定 |

## 4. 影響の評価

- 訂正1は、V4の実装・test・41 decision・3 Issueの有効性を変えない。誤っていたのは
  置き換えの根拠の記述だけであり、置き換え後のtest自体は現在も合格している。
- V4承認Decision（`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`）は§1.3を承認根拠に引用していない
  ため、再発行は不要である。

## 5. 既存recordへの影響

new-onlyで作成した。旧Evidence 2件は削除も書換えもしていない。
