# 一件の要求候補整合検査 独立完了レビュー v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- Reviewer：Codex
- 判定：`verified`
- 共通手順上の状態：`verified`
- 確認段階：`completion`
- Finding：blocking 0件、non-blocking 0件
- 未接続条件：0件
- 危険度：`high`

## 1. 固定対象と開始状態

【実測】作業指示は次の依頼recordへ固定した。

- path：`records/session-handoffs/2026-08-16-g24-requirement-candidate-check-completion-review-codex-request-v1.md`
- commit：`0a9ca3c22da34e74e2850b34314cd9d536392f99`
- SHA-256：`c602fdcace6e113e30e7c3ce7276c17f7ff81240314b7e82e6e0526f92bc59d2`

【実測】開始時HEADは`0a9ca3c22da34e74e2850b34314cd9d536392f99`、branchは`main`、
`git status --short`は空だった。レビュー中の再確認時にも、判定record作成前のworktreeは空だった。

【実測】対象commit列は次の順で現在HEADの祖先だった。

1. 利用者採用判断：`18731d6981dd5dd19bf164a2e5956f6472180a8d`
2. 失敗試験固定commit：`da8c700ea0bdadac66035eda6f604dc112dd1740`
3. 実装commit：`db36e1de8de250a4cb2b3b0e313c336a0087562d`
4. 本依頼commit：`0a9ca3c22da34e74e2850b34314cd9d536392f99`

【実測】先行レビューは
`records/development/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3-limited-rereview-v1.md`、
SHA-256 `94f2650b0a5a96b273370c15e07097f5fc5675a700ad2597ab4165cb7809678b`だった。

【実測】許可範囲は依頼record§3の鮮度検査、§4の独立完了レビュー、本record 1件の作成と単独commitである。
禁止範囲は製品・試験・契約・TODO・他recordの変更、製品受入、後続実装、外部送信、push、要求昇格、権限変更である。

## 2. Claimの分解

【記録】実装成功EvidenceのClaimを次のように分解した。

- 実施：失敗試験を先に固定し、検査核、入口、正式実行名を実装した。
- 結果：対象111件、G24関連59件、要求artifact関連21件、G08対象107件、隔離条件の正規全試験2,238件が成功した。
- 判断：契約v3と案Cの実装開始は利用者が承認済みである。
- 未実施：独立完了レビューと利用者の製品受入は未実施だった。
- 提案：独立完了レビュー後に利用者へ製品受入を提示する。

【判断】本レビューは実施・結果・未実施をrepositoryの事後状態と独立実行へ照合した。製品受入は本判定に含めない。

## 3. 鮮度検査

【実測】`records/session-handoffs/*codex-request*.md`を対象にGit履歴の最新commitを機械取得した。
最新は本依頼recordを追加した`0a9ca3c22da34e74e2850b34314cd9d536392f99`だった。本recordの依頼先はCodexであり、
宛先違いはなかった。

【実測】依頼record§2の内容識別値を現物から再計算し、7件全てが記載値と一致した。

| 対象 | 再計算したSHA-256 |
| --- | --- |
| 契約v3 | `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081` |
| 利用者採用判断 | `35eb9a0b34d6ecf3e7d503498ca0a0f04234fd4519c33eecee3b816cf8dd5c41` |
| 実装成功Evidence | `50386e4a981e039e21af3bcec1fb3c37ba078739ff506b9afa19d63d806be6d2` |
| 検査核 | `725c886a97bba63fc6d9d5c0d23a5fdc8e67f86eda2752ae587093c9bcdd14d7` |
| 入口 | `db702231fbf179a16c2742e1335d1c7f8198743baae2263ee2b1844e09ca7bd6` |
| 対象試験 | `e746f55a7da7c67d8f208cc6a03b7ecaef52e12017c1eca09f0f5acadb17eab6` |
| `pyproject.toml` | `de5b60d6b37907e4976eeeae36b5b832e96c77a41b2ec59173420c3ec0a63f2b` |

【実測】GREEN commitから開始時HEADまで上記7件の差分は0だった。固定commit不一致、内容識別値不一致、
開始前提不一致はなかった。

## 4. Git、変更範囲、TDD境界

【実測】RED commit `da8c700`の変更は`tests/test_one_requirement_feature_source.py`の新規追加1件だけだった。

【実測】GREEN commit `db36e1d`の変更は次の6 pathだった。

- `TODO_NEXT_SESSION.md`
- `pyproject.toml`
- `records/development/2026-08-16-one-requirement-candidate-consistency-check-green-evidence-v1.md`
- `tests/test_one_requirement_feature_source.py`
- `tools/requirements/one_requirement_feature_source.py`
- `tools/requirements/one_requirement_feature_source_entry.py`

【判断】上記は契約§12の製品4 pathと作業票・成功証拠の上限内であり、変更範囲違反はない。

【実測】REDからGREENまでの既存試験変更はEvidence§3記載の2区画だけだった。一つ目は正規化後の義務を配列位置ではなく
義務IDで特定する訂正、二つ目はSHA-256欄へ20文字のAWS鍵形式を置き、schema検査より先の機微検査を確認する訂正だった。

【判断】2件とも契約§8.2、§10、§11と一致する試験側の訂正であり、実装を合格させるための期待値弱化ではない。

## 5. 契約適合と誤合格・未接続の反証

【実測】契約§8から§11、実装2 file、対象試験111件を再読込みし、受入条件1から17を次の機械結果へ接続した。

- schema、採否、義務対応、件数境界、停止理由と優先順：対象試験111件と実装分岐
- 正準JSON、正規化順、6種の内容識別値：対象試験と独立合成実行の別計算oracle
- 未昇格、人の判断一覧、固定限界、安全表示：対象試験と独立合成実行の出力完全照合
- 機微情報候補、固定規則、path安全、読取り中変更：対象試験とG08対象107件
- 正式実行名、別の現在位置、空の標準エラー：対象試験とrepository外からの独立合成実行
- 禁止作用：構文木による呼出し照合と、独立合成実行中の禁止呼出し監視

【実測】`tools/session_logs/redaction.py`のSHA-256は
`aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`だった。公開関数
`default_pattern_rules`と`find_high_entropy`は呼出し可能で、既定patternは5件だった。対象試験は実行前後にも同じ値を照合した。

【実測】G08固定3 fileのSHA-256は契約§6.1の3値と一致した。入口からG08へ実行時に呼ぶ関数は
`read_input_pair`だけで、停止元変換のため`DesignAcceptanceStop`を捕捉していた。G08の比較処理と正式入口は呼んでいなかった。

【実測】受入条件18はG08固定3値と107件成功、受入条件19はG24保護10 pathの差分0と59件成功へ接続した。
受入条件20は要求artifact関連21件成功に加え、現行権限束v2の現物を`resolve_effective_requirement_ids`へ直接入力して確認した。
結果は`effective`、要求ID 50件、一意ID 50件、終了コード0だった。

【実測】要求artifact関連21件の既存fixtureが直接解決する固定pathは権限束v1だったため、その試験結果だけをv2現物のoracleには
数えなかった。上記のv2直接実行によって受入条件20の現物条件を独立に閉じた。

【実測】受入条件22の独立合成一件を`/private/tmp`に作り、正式実行名をrepository外の現在位置から実行した。
終了コード0、標準エラー0 bytes、原子義務8件、全採否2件、全義務対応、未昇格、人の判断待ち、固定限界5件を確認した。
正規化済み入力から6種の内容識別値を別計算し、全て出力値と一致した。入力自由文、採否理由、出典SHA-256、絶対pathの
正常出力への混入は0件だった。

【実測】既存fixtureにない反証として、候補rootへ`authority_status: effective`を追加し、自動的な権限付与を誘った。
正式実行名は`invalid_schema`、`source: candidate`、終了コード2、標準エラー0 bytesで停止し、追加keyと値を出力しなかった。

【判断】誤った合格、受入条件の未接続、要求候補の自動昇格、権限変更は実証されなかった。受入条件1から22は、
本レビュー完了時点のEvidenceへ接続した。受入条件23の利用者受入はHuman境界の後続として残る。

## 6. 禁止作用と上位目的への影響

【実測】製品2 fileの構文木を機械列挙した。検査核のimportは`hashlib`、`json`、`re`、
`default_pattern_rules`、`find_high_entropy`だけだった。入口の実行時能力は引数処理、`read_input_pair`、検査核、
固定JSONの標準出力に限られた。通信、外部process、Git、環境値解決、file書込み、directory探索、glob、再帰走査を行う
呼出しはなかった。

【実測】独立合成入力を入口へ直接渡し、通信、外部process、書込み系flag、`os.write`、`os.system`、directory列挙、
glob、再帰走査を失敗させる監視下で再実行した。終了コード0で同一bytesを返し、禁止呼出しは0件、入力treeの変更は0件だった。

【実測】保護基準commit `0583863e4612f7f14b5db131beb627677b99017a`からG24保護10 pathの差分は0だった。
採用判断commit `18731d6`からGREEN commitまで`records/requirements/`と`schemas/requirements/`の差分は0だった。
GREEN commitの変更path列にG08固定3 file、要求schema、現行50要求、要求権限束は含まれていなかった。

【判断】G24保護対象、G08固定部品、要求schema、現行50要求への悪影響、入力外探索、要求昇格、権限変更はない。

## 7. 必須commandの独立再実行

【実測】環境はDarwin 25.5.0 arm64、Python 3.13.14だった。次の各commandを単独実行し、終了コードを個別に判定した。

1. `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`
   - 111件成功、終了コード0
2. `.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`
   - 59件成功、終了コード0
3. `.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`
   - 21件成功、終了コード0
4. `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
   - 107件成功、終了コード0
5. `git diff --exit-code 0583863e4612f7f14b5db131beb627677b99017a -- tools/requirements/boundary_relations.py tools/requirements/feature_partition.py tools/requirements/fixed_inputs.py tools/requirements/requirement_batch.py tools/requirements/source_trace.py tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`
   - 差分0、終了コード0
6. `env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK .venv/bin/python3 -m pytest -q`
   - 2,238件成功、終了コード0、44.97秒

## 8. Finding、判定、Human境界

【実測】blocking Findingは0件、non-blocking Findingは0件、未接続条件は0件である。

【判断】判定を`verified`とする。固定commitの成果物は契約v3の受入条件1から22を満たし、報告と事後状態は一致した。
`correction_required`の根拠はない。

【判断】要求候補の正式昇格、最終採否、製品受入、G24全体の完了、次の契約開始はHuman境界のまま維持されている。

【未実施】製品・試験・契約・TODO・他recordの変更、利用者の製品受入、要求昇格、権限変更、外部送信、push、
後続実装、本判定後のClaude事後照合は行っていない。

## 9. 手戻り

【実測】一時反証scriptの保存だけで手戻り1件があった。

| 対象操作 | 期待executor | 実executor | 手作業理由 | 事象とEvidence | 機械処理候補 | route |
| --- | --- | --- | --- | --- | --- | --- |
| `/private/tmp`への一時反証script作成 | Codex→`apply_patch` | Codex→`apply_patch` | なし | 実行環境の承認要求が失敗し、repository変更は0件 | scriptをfileへ保存せずPython標準入力へ渡す | 本レビュー内で同じ反証を再実行し、終了コード0で解消 |

## 10. 停止点

【未実施】本recordだけを単独commitした後に停止する。次は依頼record§6に従い、Claudeがcommit位置、変更path 1件、
判定内容を事後照合する。Codexは製品受入提示、TODO更新、修正、後続作業へ進まない。
