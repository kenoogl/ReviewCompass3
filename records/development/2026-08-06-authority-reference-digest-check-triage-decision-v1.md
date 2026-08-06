# 参照Digest検査候補のHuman仕分け判断 v1

- Decision ID：`DEC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- decision maker：Human
- decided at：`2026-08-06T13:33:25+09:00`
- decision class：`improvement_candidate_triage`
- authority mode：`human`

## 0. この記録の形式について

**これは正規の手順ではなく、正規の置き場所が使えないための代替である。**

改善候補に対するHuman仕分け判断は、本来
`.reviewcompass/workflow/triage-decisions`（V1）または
`.reviewcompass/workflow/triage-decisions-v4`（V4）へ機械可読なrecordとして置く。しかし現在、
どちらへも置けない。

| 置き場所 | 置けない理由 |
| --- | --- |
| V1 `triage-decisions` | `tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`が`len(decision_files) <= 1`を、`tests/test_issue_intake_v4.py::test_k6_legacy_v1_decision_and_pilot_validation_keep_passing`がfile名の完全一致を要求する。2件目を置くとどちらも落ちる |
| V4 `triage-decisions-v4` | `candidate_ref`のkey集合が`bundle_path`／`bundle_sha256`／`bundle_schema_version`／`candidate_id`／`candidate_content_digest`に厳密固定されており、単体候補recordを指す形が無い。さらに`test_k7_repository_decision_set_has_no_conflict`が、全decisionが同一bundleを指すことを要求する |

したがって本判断を、先例
`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`
（`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`）と同じく、`records/development/`配下のDecision recordとして
残す。既存Testは1件も変更していない。

## 1. 判断対象の候補

| 項目 | 値 |
| --- | --- |
| candidate ID | `IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001` |
| path | `.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json` |
| file SHA-256 | `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6` |
| content digest | `760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f` |
| 観測record | `records/development/2026-08-06-authority-reference-digest-drift-observation-v1.json`、SHA-256 `6ccf3d15c28c56a5b74730a9ac056ef3abe13967da0427549e05308cc0ab3841` |
| containing commit | `235a7d3` |

候補は`config/development-issue-resolution-pilot-v3.json`のvalidatorに合格している
（`record_kind: improvement_candidate`、exit 0）。

## 2. Humanの判断

Humanは「対処すべきだが急ぎではないに同意」と述べた。その後、正式Issue登録の扱いについて
「経路が直るまで保留」という読み方を確認し、承認した。

| 判断項目 | 値 |
| --- | --- |
| 分類 | `process_improvement`、`test_or_oracle`（候補の`classification_candidates`をそのまま採る） |
| 対処するか | **対処すべき** |
| blocking | **`false`**。現行Workを停止しない |
| 着手時期 | **急ぎではない。後回し** |
| route | `issue_resolution`相当。ただし正式Issue登録は保留 |
| 正式Issue登録 | **保留**。仕分け判断を機械可読に置ける経路が直るまで登録しない |
| selected consumer | `reviewcompass3-development` |

`registered`相当の扱いであり、`in_progress`にはしない。現在の`in_progress` Issueは0件のままである。

## 3. 将来、正式レーンへ取り込むために必要な値

経路が直った時点で、次の値をそのまま機械可読recordへ移せる。

```text
candidate_id            : IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001
candidate file sha256   : d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6
candidate content digest: 760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f
decision_maker          : human
disposition             : issue_resolution
blocking                : false
promote_to_issue        : 保留（このDecisionでは承認していない）
unresolved              : true
recurrence              : true（2026-08-04以降、参照欄が10 commitの上流改定に追随しなかった）
impact                  : medium（読み手が古い版を正本と誤認しうる。safety・authorityは損なわない）
priority                : low（急ぎではない）
selected_consumer       : reviewcompass3-development
```

`impact`と`priority`はHumanの「対処すべきだが急ぎではない」という文言からClaudeが機械可読語彙へ
写したものである。**Humanがこの2語をそのまま述べたわけではない。**取り込み時に再確認する。

## 4. 判断の理由

- 参照Digestのずれは実際に発生し、修復した（commit `e732995`）。再発の経緯も測定済みで、
  当該欄が最後に更新された`c475bec`から測定commitまでの間に、Current Planは7 commit、
  Development Policyは3 commit改定されたが、参照側に触れたcommitは修復の1件だけであった。
- 一方、safety、authority、Acceptanceの真偽、必須Provenance、不可逆side effectのいずれも
  損なっていない。現行Workを停止する条件に該当しない。
- 検査器を作る前に「どのfront matter keyが現在有効を意味するか」の判別規則を宣言する必要があり、
  その宣言自体がHuman承認を要する。急いで実装すると、正しい過去pinを誤検知する。

## 5. この判断が承認しないもの

- 検査器の実装、validator・test・configの変更。
- 判別規則（対象keyのallowlist）の確定。
- 正式Issueの登録。
- Issue Intake設計のやり直しの範囲と着手。
- 既存Testの書換え、凍結レーンへの追加。

## 6. 関連する未解決の問題

本判断が正規の置き場所へ置けないこと自体が未解決の問題であり、その原因はIssue Intake V4設計の
欠陥にある。当日発生した問題の全体は
`records/development/2026-08-06-encountered-problem-inventory-v1.md`へ一覧化する。

参考record：

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-frozen-lane-guidance-correction-decision-v1.md` | `9c0b58bdfc868e03d9d4a3dd05c179157ec05324c88bffdc9a51a12fce2e8994` |
| `records/development/2026-08-06-deep-dive-stop-rule-decision-v1.md` | `b28e5b2de79f6ccb6df413f4ecc33c64fc29ab55f7f44f944460bba1e4c82401` |

## 7. 既存recordへの影響

new-onlyで作成した。既存record、候補、観測record、Test、config、凍結レーンの内容は変更していない。
