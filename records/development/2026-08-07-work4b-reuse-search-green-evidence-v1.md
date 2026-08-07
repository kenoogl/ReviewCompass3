# Work 4B最小試行 reuse_search_record GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MINIMAL-PILOT-SCOPE-001`
- RED Evidence：`records/development/2026-08-07-work4b-reuse-search-red-evidence-v1.md`
- 宣言→RED対応表：`records/development/2026-08-07-work4b-reuse-search-declaration-red-map-v1.json`

## 1. 実装

`tools/development/reuse_search_record.py`を新設した。検索（宣言からの決定的導出）、検証
（結線・new-only形式・処置label禁止・digest）、new-only保存、gate判定（fail-closed）を含む。
既存moduleの変更は行っていない。

## 2. Test結果（機械実行、終了コード直接判定）

- targeted：`tests/test_work4b_reuse_search_record.py` `8 passed`、exit `0`
- 公式全Test：`1055 passed`（既存1047件＋新規8件）、exit `0`。既存Testは変更していない。

## 3. RED後のTest修正（理由記録）

R6のtestは、実データ測定の結果を受けてRED段階（module未実装のまま）で1件修正した。
hitごとにgroup memberの全列を複製する当初形式は、最初の実recordを4,934,260 bytes
（member項目62,113件、正規化後3,493件の約18倍）へ膨張させた。承認済み提案§3の必須field
（symbol_id、code_reference、所属group ID、basis_kind）を超えるfield設計はtest側の過剰であり、
R6の趣旨（memberを上限で切り捨てない）は`groups`欄でgroup一件につき一度だけ全memberを
保持する正規化形で満たす。修正理由はtest内commentとcommit `003f7af`に記録した。

## 4. 実装前検索と再生成一致（提案§5手順3）

- 実装前に、prototype機械操作でhelper自身の再利用検索を実行し、最初の実recordを
  `records/development/2026-08-07-reuse-search-record-helper-reuse-search-v1.json`
  （content digest `dc3f6a2a7450eaeed60f7254fb8e61a7e1d3ca7ed1554b62993ac3cd9ddb46c6`、
  923,860 bytes）としてcommit `89043ca`へ固定した。routine 302件、hit 1,654件、group 341件。
- 実装後、helper本体の`search_existing_routines`で同じ宣言・同じWork 4A実データから再生成し、
  **committed recordと完全一致**（dict等価かつcontent digest一致）を確認した。
- committed recordはvalidator合格、gate判定は`start_allowed: true`である。
- 検索のsource identityはWork 4A v3.3実データ（profile `55fdacd5…`、discovery `4dabb03b…`、
  source content `978da3d1…`）である。

## 5. 検索結果の観察（Human向け要約、処置判断はしない）

hit上位の重なりとして、helperが実装した機能（正規化digest、new-only書込み、record検証）と
同種の既存routineが`tools/development/`配下に複数存在することが記録された（例：
`issue_intake_v4.py`と`issue_resolution_pilot.py`の`_canonical_digest`、`work4a_rebuild_v3.py`の
`_write_new`）。処置label（reuse等）は記録に含めておらず、統合の要否はHuman判断である。

## 6. 状態と次

- Work 4B最小試行の「検索→記録→helper→gate」の縦一周は完了した。
- 残余：gate判定をWork 5Bの内部Implementation Task Contract Pilotで実証する（実装順12後半）。
- 本helperは守り役codeのため`high`であり、work-review-protocol §4.4（fixtureに無い反証の新作）
  による後追いレビューの対象である（`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`の優先度案に
  含める）。
