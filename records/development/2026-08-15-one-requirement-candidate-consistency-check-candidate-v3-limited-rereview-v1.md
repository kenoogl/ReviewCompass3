# 一件の要求候補整合検査 契約候補v3限定再確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-15
- Reviewer：Codex
- 判定：`開始可`
- Finding：blocking 0件、non-blocking 0件
- 未接続条件：0件

## 1. 固定対象と開始状態

- 依頼record：`records/session-handoffs/2026-08-15-g24-contract-v3-limited-rereview-codex-request-v1.md`
  - commit：`dd3449a356c0d1d4b886a58c54372ea2db725697`
  - SHA-256：`47ae10f6ef13e990a0d10a1bd5e292d2849129c4c5267402029f95169a7dc712`
- 対象契約：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md`
  - 固定commit：`2935825df00274d7c6b782687305b8e0c171eb44`
  - SHA-256：`7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- 先行レビュー：`records/development/2026-08-15-one-requirement-candidate-consistency-check-contract-v2-independent-rereview-v1.md`
  - SHA-256：`270505d0f073fb59daf4d963824ca0eb9e2c854c580ed46dde2f63181242eb38`
- 直前版契約：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v2.md`
  - SHA-256：`a4d544e29d877ac45dca65b748557387bd1b04f58adda59ffacf91fc47a216bb`
- 開始時HEAD：`dd3449a356c0d1d4b886a58c54372ea2db725697`
- branch：`main`
- 危険度：`high`（対象契約の固定値）
- 許可範囲：依頼record§3の鮮度検査、§4の限定再確認、本recordの作成と単独commit
- 禁止範囲：全面再走査、契約・製品コード・既存試験・TODO・他recordの変更、契約採用、実装、外部送信、後続作業

【実測】起動中sessionの`turn_context`から、冒頭のmodel名とreasoning effortが
`gpt-5.6-sol`／`high`であることを確認した。

## 2. 結論

【判断】`開始可`とする。先行レビューの停止原因だった規則内容識別値の計算方法未定義は閉じた。
契約候補v3の§6.2と受入条件13には、計算方法または基準値を実装者が後決めする要素が残っていない。
v2からの変更は依頼record§2の訂正範囲に限られ、v2で閉じた3系統と§6.1・§6.3に退行はない。

【判断】本判定は契約採用、縮小境界の利用者判断、案Cの採用、製品実装の開始を承認しない。
これらのHuman境界は維持されている。

## 3. 鮮度検査

【実測】Git履歴から`Codex`を含む引継ぎrecordを作成commit時刻順に機械列挙した。最新は本依頼recordで、
commitは`dd3449a356c0d1d4b886a58c54372ea2db725697`だった。その直前は旧方式の依頼recordを追加した
`d6d9ad62f0a30ebf35ffa0c486591bc07c50d48d`であり、本依頼recordが旧recordをsupersedeするという記載と一致した。

【実測】開始時の`git status --short`は空だった。対象固定commitは実在し、現在HEADの祖先だった。
固定commitから現在まで対象契約の差分は0だった。

【実測】依頼record§2の3 fileを機械計算し、対象契約、先行レビュー、直前版契約のSHA-256は、
それぞれ依頼record記載値と一致した。宛先違い、内容識別値不一致、固定commit不一致はなかった。

## 4. 訂正1点の限定再確認

【実測】契約§6.2は、機微情報候補検査の照合対象を次の現物へ限定している。

- `tools/session_logs/redaction.py`のSHA-256：
  `aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`
- 公開関数：`default_pattern_rules`、`find_high_entropy`
- `default_pattern_rules()`が返す既定pattern：5件

【実測】現物を再計算・実行照合し、fileのSHA-256、公開関数2名の存在、既定pattern 5件は全て一致した。
先行レビューで未定義とされた規則内容識別値
`3c736257fc01740dbd8e5b3eba53c810b401640cae7c31201cbc0b85840bd328`は、契約候補v3で0件だった
（`rg`の一致なし、終了コード1）。

【実測】受入条件13は、§6.2のfile内容識別値、公開関数2名の存在、既定pattern件数5の実行前後照合だけを求める。
照合対象、計算方法、基準値は上記の固定fileと整数値から一意に得られる。

【判断】訂正1点は閉じた。実装者による計算方法または基準値の後決めは不要である。

## 5. 退行の限定再確認

【実測】固定したv2とv3の全文差分は4区画だった。

1. 見出し、契約版、supersedes、訂正根拠、訂正範囲、利用者判断
2. §6.2の規則内容識別値撤回とfile内容識別値による変更検出
3. 受入条件13の照合対象限定
4. §15の次作業文

【実測】階層を考慮した節単位の機械比較で、§1、§6.1、§6.3、§8.2、§9、§10、§11の7節は
v2とv3で完全一致した。これにより、目的縮小、識別子の機微漏えい、正常・停止形式の非一意性という
先行レビューで閉じた3系統と、§6.1・§6.3の固定基準に本文変更はない。

【実測】§6.1のG08固定3 fileと§6.3のG24保護10 pathは、契約記載のSHA-256に13件全て一致した。
G24保護10 pathは保護基準commit`0583863e4612f7f14b5db131beb627677b99017a`との差分も0だった。

【判断】依頼record§2に記載されていない本文変更はなく、限定対象に退行はない。

## 6. 独立再実行

【実測】次の各commandを単独実行し、終了コードを個別に判定した。

- `.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`
  - 59件成功、終了コード0
- `.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`
  - 21件成功、終了コード0
- `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
  - 107件成功、終了コード0
- `git diff --exit-code 0583863e4612f7f14b5db131beb627677b99017a -- tools/requirements/boundary_relations.py tools/requirements/feature_partition.py tools/requirements/fixed_inputs.py tools/requirements/requirement_batch.py tools/requirements/source_trace.py tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`
  - 差分0、終了コード0

## 7. Finding、Human境界、未実施

【実測】blocking Findingは0件、non-blocking Findingは0件、未接続条件は0件である。

【判断】契約採用、縮小境界、案Cの採用、実装開始、最終受入はHuman判断のまま維持されている。

【未実施】全面再走査、契約訂正、製品コード・既存試験・TODO・他recordの変更、契約採用、実装、
要求昇格、外部送信、利用者への質問・提案、判定後の後続作業は行っていない。

## 8. 手戻り

【実測】手戻り2件を次のとおり機械的に解消した。

| 対象操作 | 期待executor | 実executor | 手作業理由 | 事象とEvidence | 機械処理候補 | route |
| --- | --- | --- | --- | --- | --- | --- |
| 最新依頼の履歴列挙 | Codex→zsh→Git | Codex→zsh。Gitと`tr`は未起動 | なし | zshの特殊配列名`path`を反復変数に使い、`command not found` | 変数名を`file_path`へ変更 | 本限定再確認内で再実行し、終了コード0で解消 |
| v2・v3の節単位比較 | Codex→`.venv/bin/python3` | 同左 | なし | 下位見出しを節境界に含め、§6.2まで§6.1として比較して`AssertionError` | 見出し階層を考慮する比較 | 本限定再確認内で再実行し、7節一致・終了コード0で解消 |

## 9. 停止点

【未実施】本recordの単独commit後に停止する。依頼record§1がClaudeへ割り当てた事後照合、利用者への一判断提示、
契約訂正または実装には着手しない。
