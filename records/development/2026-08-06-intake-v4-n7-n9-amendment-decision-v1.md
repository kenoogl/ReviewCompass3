# Intake V4 規範宣言N7・N9改定 承認Decision v1

- Decision ID：`DEC-INTAKE-V4-N7-N9-AMENDMENT-001`
- decision maker：Human
- decided at：`2026-08-06T15:26:29+09:00`
- decision：`approved`
- decision class：`design_amendment_decision`
- 改定対象：`docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md`の
  規範宣言N7・N9（SHA-256 `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358`）

## 1. 経緯

commit `c693af4`でチェックリストへ`CL-6A-09`の完了印を付けた結果、改善候補
`IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の`evidence_refs`（チェックリストを作成時点の
SHA-256で参照）が現行bytesと一致しなくなり、v3 validator検証に落ちた。これにより
`test_n7`と旧`test_n9`を含む4 testが失敗した（残り2件はTODOの参照Digest未追随）。

この失敗は予告されていた。TODOのstale欄に「候補のevidence_refsはchecklistを含むため、
checklistが再改定されると検証に落ちる」と注記済みであり、当日承認したN9の
「v3 validatorで合格し続ける」という宣言は、evidence_refsが**作成時点の固定**である性質と
両立しない誤った宣言だった。「現在有効」と「作成時点の固定」の混同（当日3回発生した型）が
Claude自身の設計へ入り込んだ事例である。

なお、この失敗が数時間で機械検出されたのは、同日実装したN7の全件検査が機能した結果である。

あわせて、commit `c693af4`は全Test赤（4 failed）のまま実行された。これは「統合対象のcommitは
原則green」の違反であり、本改定を含む修復commitで緑へ復帰する。

## 2. 承認した改定

**仕分け済みの候補は歴史扱いとする。**

- **N7改定**：候補置き場の全件検査の充足条件へ第3分岐を追加する。
  「有効なV4 triage decisionが存在する候補」も充足と数える。その際、decisionの
  `candidate_ref`が単体形式なら、`record_sha256`と候補fileの実bytes、
  `candidate_content_digest`と候補recordの`content_digest`の一致を検証する
  （指紋の固定が生きていることの確認）。
- **N9改定**：「v3 validatorで合格し続ける」を廃し、「decisionが候補の指紋を固定し続けている」
  ことの検証へ置き換える。test関数は
  `test_n9_authority_reference_candidate_passes_the_v3_validator`から
  `test_n9_authority_reference_candidate_binding_stays_pinned`へ改名した。

理由：候補の`evidence_refs`は作成時点の固定であり、上位文書は改定され続ける。仕分け後の
候補へ現行bytesとの一致を要求し続けると、チェックリストへ完了印を付けるたびに検証が壊れる。
内容の保証はdecisionの指紋束縛が担っており、失われない。

## 3. 対応表への影響

`records/development/2026-08-06-intake-v4-declaration-red-map-v1.json`のN9行が参照する
test名は旧名のままである。同recordは履歴として保持し、N7・N9の現行対応は本Decisionを
正本とする。

## 4. 既知の限界

- bundle形式のdecisionを持つ候補が将来この置き場に置かれた場合、N7第3分岐は存在確認のみで
  指紋検証をskipする（承認文言どおり。bundle側の指紋はtest_k7が別途固定している）。
- 仕分け済み候補のevidence_refsは以後staleのまま保持される。これは作成時点の観測としての
  保持であり、現行状態の主張ではない。

## 5. 検証

| 項目 | 結果 |
| --- | --- |
| 改定後の対象test file | `11 passed`、SHA-256 `86f0b09864a0def0ed633aa444c1f5317df72d07734e6ac55289d5212bc258e2` |
| 変更範囲 | `tests/test_issue_intake_v4_single_candidate.py`の2関数のみ（38挿入・14削除） |
| 実装（`tools/`）・bundle・既存decision・Issue | 無変更 |

## 6. 既存recordへの影響

new-onlyで作成した。旧宣言を含む提案文書、対応表、候補、decisionはin-placeで書き換えていない。
