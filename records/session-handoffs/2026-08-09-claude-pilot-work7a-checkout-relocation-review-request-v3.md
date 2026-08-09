# レビュー依頼 v3：Work 7A第2項 前駆slice — RR-P1-004修正後の再レビュー

- 作成日：2026-08-09
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`
- 先行依頼書：v1（stale）、v2（SHA-256
  `27e66a02fb4397c7ebe049fffc9ea96bce6c1399502f7f3cb84f8994715790ed`。完了Claimは
  再レビューv2によりstale。いずれも変更せず保持）

## 1. 経緯と対象

再レビューv2（`records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v2.md`、
SHA-256 `9d307e0c8cf9d0a1a1fc74f4bb27e69f52d86e91dc2ee1f5309e5eb5ec6e10ad`、判定
`report_execution_mismatch`）で、RR-P1-001〜003は解消と判定され、新たにRR-P1-004
（tracked symlinkのlink payload差が空Change Setになる）がblockingとされた。Humanは
2026-08-09「RR-P1-004の修正を承認する」と承認した。scope・schema境界はscope v2
（SHA-256 `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`）のまま。

## 2. 修正commit列（review request v2 commit以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `d7bacd32cfc4446656567cceb95b1757b719f7b0` | Pilot | review request v2（先行） |
| `0861875e1fb9e49233c8ab8aa2c5cd12981cdee8` | Reviewer | 再レビューv2 result record |
| `0e1952195d0c40c5b3285fc151a55ac0ebf085cf` | Pilot | 修正RED：symlink payload差のTest 1件のみ追加（62行） |
| `2c834b4e686c8c0c95779e5784853b508663ecc3` | Pilot | 修正GREEN：実装修正・GREEN Evidence追記・receipt更新のみ |

本依頼書のcommit SHAは自己参照になるため記載せず、Reviewerがgitから特定する。

## 3. Claim（修正分）

- **実施**：修正REDを単独実行し、新規1件のみが反証どおり（空Change Set）失敗し
  先行22件が合格、exit `1`を確認してcommit。既存Testは弱めず、実装のみ修正してGREEN化。
- **修正内容（RR-P1-004）**：worktree上のtracked symlinkは参照先fileを読まず、
  `readlink`で得たlink payload自体のSHA-256を種別接頭辞付きで`content_identity`へ記録
  （`symlink:<sha256>`。通常fileは`file:<sha256>`で区別し、file⇔symlinkの種別変化も
  identity差になる）。index側はGit blob oidが既にpayloadを反映するため不変。
  untracked symlinkの拒否（`snapshot_path_escape`）契約も不変。dereferenceは行わない。
- **結果**：targeted 23 passed（exit `0`）、関連回帰83 passed（exit `0`）、公式全Test
  1338 passed・status `passed`（exit `0`、receipt再読込みでfailed 0確認）、
  `git diff --check`指摘なし。新Testでbase／candidateの`content_manifest_digest`が
  payload差で異なることも固定。
- **未実施**：scope変更、新schema、耐久Binding、Verification Run、TODO／checklist更新、
  Work 7A第2項checkbox完了。

## 4. 成果物のpathとSHA-256（修正後）

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_checkout_relocation.py`（23 Test。修正RED以後未変更） | `ab8f311dd6099085acec942c8e956523209756e4bcdc585be5e5b89e84b19258` |
| `tools/deployment/checkout_relocation.py` | `2a81b11d1355f5bcde1381ff40dd9cd9337781e2719cbb696befc5d60d44eed1` |
| `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md`（§7へRR-P1-004修正記録追記） | `c20a8d4056cbe55870defd61f7a3f3de61942f945a1fe9cb7bfb696d34105c10` |
| `records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json`（更新） | `b4384813ff82ca0e7aa9a133996dc618710658a7f5a7ca1c405c63805f9d9a9e` |

## 5. 禁止操作の未実施・worktree・停止地点

- 固定入力実装・TODO・checklist・Plan・Decision・scope v1／v2・先行レビューrecord：未変更。
- production APIはread-only Gitのみ。fixture Git操作はTest内・`tmp_path`限定。
- 実ホーム・既存利用者repository・既存保全data：accessなし。
- push・tag・PR・amend・rebase・reset・履歴書換え・`git add -A`／`git add .`：未実施。
- 本依頼書のignore検査：`git check-ignore --no-index` exit `1`（続行可）。
- worktree：本依頼書commit時点でclean。
- 停止地点：本依頼書のcommitをもってPilotは停止し、Codexの再レビュー（元22件＋新1件、
  前回独立3シナリオ、RR-P1-004反証、関連、公式全Test）まで次の作業へ進まない。

## 6. Reviewerへの確認観点（依頼）

- RR-P1-004の追加独立反証（SHA-256
  `2da69bd7206e036b777d733e731ea08288c3144883bd8b6e3db740400223aa12`）が不成立になること
- `symlink:`／`file:`接頭辞のidentity区別が、参照先の内容を読まずにpayload差・種別変化を
  識別していること（dereference非実施）
- 修正REDの失敗理由が反証そのものであること、既存Testを弱めていないこと
- targeted・関連回帰・公式全Testの独立再実行と、Digest再計算
