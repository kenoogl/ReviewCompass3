# Claude Reviewerによる範囲レビュー結果・承認済みClaude送信経路 v1

- 状態：実装前の独立範囲レビュー結果
- 日付：2026-08-11
- collaboration_mode：`role_neutral_pilot_review`
- pilot：Codex
- reviewer：Claude
- closer：Codex
- work_item：`approved-claude-send-path`
- risk：`high`（提案どおり。過小分類なし。§6で妥当性を述べる）
- 対象：`records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v1.md`
- 判定：`reported_unverified`

判定根拠は`work-review-protocol.md`§11.1の「blocking Findingの列挙」による。blocking Finding 4件を
§5へ列挙する。範囲固定の作成とcommit自体は指示どおり行われており、報告と事後状態の競合
（`report_execution_mismatch`）ではない。

## 1. レビュー開始時に固定したもの

| 項目 | 内容 |
| --- | --- |
| 作業指示 | Humanの依頼（risk `high`の実装前独立範囲レビュー）と対象範囲固定record |
| 開始状態 | base commit `7f58333aa5bc1f275f59bc672fc1f0722fc813da`、branch `main` |
| review対象commit | `c9d128e48f1313c07a917de39426ea24bea5f900`（`Scope approved Claude send path`） |
| review開始時HEAD | `c9d128e48f1313c07a917de39426ea24bea5f900` |
| review終了時HEAD | `1bf90a0a32bd8efa7381f8fee90ca430d30bed73`（§11.1の並行commit） |
| review時点worktree | 本record以外に未追跡・変更fileなし |
| 許可範囲 | 判定recordの新規作成と単独commitのみ |
| 禁止範囲 | 実装、test追加、既存authorityの変更、外部送信 |
| risk | `high`（守り役code＋不可逆な外部送信。`work-review-protocol.md`§3の既定） |

## 2. 変更範囲の確認

`git log --oneline 7f58333..HEAD`は1件、`git show --name-status c9d128e`は次の1 pathのみである。

```text
A	records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v1.md
```

範囲外変更、既存利用者差分、一括stage、履歴書換えはない。§12が定める`SCOPE`の単独commit境界を
満たしている。判定record path
`records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md`について
`git check-ignore --no-index`を単独commandで実行し、exit codeは`1`（ignoredでない）であった。
予約substring`claude-to-codex`も含まない。

## 3. 固定入力と成果物の再照合

範囲固定§3の14件すべてを報告値から転記せず、fileから再計算した。**14件一致、不一致0件**である。

payloadは範囲固定§4の`text`fenceから逐語で取り出し、末尾改行を含めずに再計算した。

| 対象 | 再計算値 | 記載値との一致 |
| --- | --- | --- |
| payload 1（296 bytes、1行） | `18059aa0f32b93bae5b117092a45fbf4e985381546b8c64507168f0226f4ad64` | 一致 |
| payload 2（221 bytes、1行） | `c2309f2624ba0d0f36fd00894dcbc67ccd66e83429960c4083f4e10b2f18982a` | 一致 |
| list digest（既存`payload_list_digest`） | `967e9410e0cf3bb722fca084b7ffa91b1d282c6f02674843362bd6893a25bf89` | 一致 |

開始状態§2のうち機械照合可能な項目も確認した。Claude Code実行fileのversionは`2.1.220`、SHA-256は
§2の記載値と一致した（user固有の絶対pathは本recordへ記録しない）。

既存`tools/egress/approval.py`の`scan_outbound_text`を2 payloadへ適用した結果は、いずれも検出0件で
あった。

## 4. 上流authorityから独立導出した受入条件

Pilotのtest案・実装案をoracleにせず、次の上流から受入条件を導出した。導出元は出口設計v4
（§4承認7項目、§5関門9条件、§7証跡、§8段階）、`DEC-EGRESS-METHOD-CONCLUSION-001`、
`work-review-protocol.md`§3・§5、`role-neutral-pilot-review-collaboration.md`§3・§4、
先行試行の停止Evidenceである。

| 導出元 | 独立導出した条件 | 範囲固定§7での扱い |
| --- | --- | --- |
| v4 §4-1 | `approved_by: user` | §6.2に含意。§7の列挙には無い |
| v4 §4-2 | 送信物一覧digestの一致 | §7-2で明示 |
| v4 §4-3 | provider・modelの固定 | §7-2で明示 |
| v4 §4-4 | 有効期限 | §7-2で明示 |
| v4 §4-5 | 一回性（排他claimによる消費管理） | §7-7で明示（配置に欠陥。F4） |
| v4 §4-6 | 目的 | §7-2で明示 |
| v4 §4-7 | 材料方針3項が全て有効 | **列挙なし**（F2） |
| v4 §5-1・5-2 | 構成の検証・由来の解決 | 新用途では固定payload照合へ置換。置換の裁定なし（F1） |
| v4 §5-3 | 一覧の照合 | §7-2で明示 |
| v4 §5-4 | 伏字化の適用（合格を根拠にしない） | **記載なし**（F2） |
| v4 §5-5 | 承認recordとpayloadの結線 | §7-2で明示 |
| v4 §5-6 | 送信前機械検査の単一実装（二重実装禁止） | **満たさない**（F2） |
| v4 §5-7 | content-addressed目録の検証＋排他消費 | §5-1に手順、§7の受入条件に無し（F2） |
| v4 §5-8 | 復旧経路の印字（自動修正しない） | **記載なし**（F2） |
| v4 §5-9 | 応答不全のエスカレート | §6.2で明示 |
| v4 §7 | 逐語保存とSHA-256、応答raw保存、実行仕様保存、保存不能なら送信も失敗 | §6.2・§7-9で概ね満たす |
| v4 §8-4 | 段階4は別提案とし、改めてHuman承認を要する | §1でHuman境界を明示（維持） |
| `DEC-EGRESS-METHOD-CONCLUSION-001`§4 | `tools/egress/`とv4は完成資産として保持。場面1の段階3・4は着手しない | 新用途として区別。裁定なし（F1） |
| work-review §3 | 守り役code・不可逆操作は既定`high` | §risk提案`high`と一致 |
| role-neutral §3 | `high`は範囲レビュー合格とHuman明示承認まで実装停止 | §1・§11で維持 |
| 停止Evidence §3 | 現repositoryに本payloadを実送信できる承認済み経路はない | §1の前提と一致 |

## 5. blocking Finding

いずれも段階は`scope`、`work-review-protocol.md`§11.1の閉じた4類型に対応づける。

### F1（blocking、類型1）新用途に対する上流authorityが特定されていない

範囲固定§4は「本作業は出口設計v4 §8が実送信の前提とした『段階4の別提案』に相当する」とする。
しかし上流の実状態は次のとおりである。

- 出口設計v4の状態は`human_confirmation_pending`であり、確定authorityではない。v4自身が
  「残る確認は1点のみ：本文書がこれらの判断を正確に反映しているか」と述べている。
- v4が扱うのは場面1（部品の実装同一性判定）だけである（§0・§3・§9）。場面2は明示的に対象外であり、
  今回の`claude_session_bootstrap`はそのどちらでもない新用途である。したがってv4 §8の段階4は
  今回の用途を覆っていない。
- `DEC-EGRESS-METHOD-CONCLUSION-001`（2026-08-08、確定Decision）§4は、`tools/egress/`とv4を
  「完成済みの資産として保持する」とし、段階3・4に着手しないとしている。今回は同じ`tools/egress/`へ
  新moduleと新purposeを足す作業であり、凍結した資産へ触れることの裁定がない。
- 範囲固定§1が引くHumanの逐語承認は「ReviewCompass3の承認済み送信経路を通さず」送る内容であり、
  承認済み送信経路を新設する本作業を覆っていない。§1自身も「進めて」の効力を範囲固定recordの作成と
  レビュー依頼までに限定している。

影響：確定していない設計文書と、用途の異なる段階区分を根拠として、新しい外部送信の用途が
開かれる。境界の上流整合が成立しない。

必要な措置：v4を根拠とする記述を撤回し、(a) 新用途`claude_session_bootstrap`を許すかどうか、
(b) 凍結資産`tools/egress/`へ新経路を足すかどうか、の2点をHuman裁定recordとして固定したうえで、
次versionのscopeでその裁定を固定入力に置く。

### F2（blocking、類型1）v4が承認済みとする関門条件が、裁定なく落ちている

F1と同じ根で、承認済みの判断点4・5・6・判断点3の各条件が受入条件へ引き継がれていない。
`work-review-protocol.md`§11.3に従い、同じ類型の変種を同一周回で掃き出す。

1. **送信前検査の単一実装（v4 §5-6、判断点4でHuman承認済み）**：既存`tools/egress/gate.py`は
   docstringで「どの呼び出し経路もこの1実装を通ること（二重実装禁止）」と宣言している。範囲固定§9は
   `gate.py`を変更禁止pathとし、§8は`trusted_claude_send.py`に独自の送信前検査を新設する。結果として
   送信前検査は2実装になる。受入条件§7-11が保証するのは「actual outbound processを作成できる
   production moduleが一つ」であって「送信前検査が単一実装」ではない。
2. **伏字化の適用（v4 §5-4、判断点5でHuman承認済み）**：範囲固定に伏字化の記述が一切ない。既存
   `gate.py`は`APPROVED_REDACTION_HOOK`以外を実行せず拒否し、内容が変化したら混入の兆候として
   拒否する。新経路にこの信号が無い。
3. **復旧経路の印字（v4 §5-8、判断点4でHuman承認済み）**：§6.2と§11はfail-closed停止とHumanへの
   報告を述べるが、「理由と実行可能な次の手順を印字する」ことが受入条件§7に無い。既存`gate.py`は
   `GateResult.recovery`として構造化している。
4. **材料方針3項（v4 §4-7、判断点3でHuman承認済み）**：§5-2と§7-2の承認検証列挙に
   `material_policy`（`require_secret_scan`／`forbid_credentials`／`forbid_personal_identifiers`）が
   無い。既存`validate_approval_record`は3項が全て`True`でなければ拒否する。
5. **content-addressed目録の検証（v4 §5-7）**：§5-1の手順には「content-addressedな目録」とあるが、
   目録のfile名が内容のSHA-256と一致することの検査が受入条件§7に無い。§7-12は入口が目録と承認だけを
   受け取ることを求めるが、目録自体の偽造検出を求めていない。

影響：新経路は、既存経路がfail-closedで拒否する事象（伏字化の変化、材料方針の欠落、目録の偽造）を
受入条件上は通してしまう。「誤った合格」が静かに成立する方向の欠陥である。

必要な措置：各条件について「新用途へ引き継ぐ」か「引き継がない理由をHuman裁定で固定する」かを
次versionのscopeで一つずつ明示する。

### F3（blocking、類型3）受入条件11が機械判定できず、迂回を許す

受入条件§7-11は「actual outbound processを作成できるproduction moduleは今回のtrusted入口一つだけで
あり、ASTまたはmodule inventoryの独立検査で他の迂回経路がないことを確認できる」とする。この条件は
現状のrepositoryに対して機械判定できない。

**機械実行した反証**：`tools/development/structured_argv_executor.py`の`subprocess_runner`は、
module levelの公開関数として、任意のargvをそのまま実process化する。template検査は
`run_read_only_operations`側にあり、`subprocess_runner`自身は行わない。外部送信を伴わない安全な
argvで確認した。

```text
python3 -c "from tools.development.structured_argv_executor import subprocess_runner; \
print(subprocess_runner(['/bin/echo','arbitrary-argv-executed'], cwd='.'))"
→ returncode 0、stdout `arbitrary-argv-executed`
```

`git status --porcelain`templateに一致しないargvが起動している。したがって、callerがargvを組める限り、
trusted入口を増やさずにprocessを起動できる。

同じ類型の変種も同一周回で掃き出す。

- **名前ベース検査の回避**：検査を「`claude`という実行file名を含むmodule」で行うと、上記の汎用runnerは
  名前を持たないため合格する（偽陰性）。
- **module数ベース検査の破綻**：`subprocess`を参照するproduction moduleは`tools/`配下に18件ある。
  検査を「subprocess呼出しを持つmoduleは1件」とすると既存18件で失敗する（偽陽性）。個別に除外すると、
  除外一覧そのものが迂回の隠し場所になる。
- **「actual outbound」「production」の未定義**：`tools/development/`配下がproductionに含まれるか、
  「outbound」がネットワーク送信か外部process生成かが範囲固定に定義されていない。定義次第で同じ
  repositoryが合格にも不合格にもなる。

影響：受入条件11は、実装後の完了レビューで「合格」と判定できてしまう一方、実際の迂回可能性を
排除しない。守り役codeの受入条件として偽陰性を持つ。

必要な措置：次versionのscopeで、(a)「actual outbound」と「production」の機械判定可能な定義、
(b) 汎用argv runnerを含む既存経路の扱い、(c) 検査器の具体的な判定規則（許可listと、その一覧自体の
固定方法）を受入条件へ書き下ろす。

### F4（blocking、類型3）一回性の状態がGit外runtimeにあり、承認recordと分離して再消費できる

§6.2は「承認消費markerとreceiptはdevelopment profileの`STATE_ROOT`」へ置くとし、§8は承認record自体を
Git管理下の`records/development/2026-08-11-approved-claude-send-path/`へ置く。この分離により、一回性
（v4 §4-5、受入条件§7-7）が破れる経路が生じる。

- 既存`validate_approval_record`は、承認record内の`consumed`が`False`であることを合格条件にする。
  Git上のrecordは`consumed: false`のまま変わらない。
- 消費の事実はrepository外のstateだけが持つ。`tools/layout/baseline.py`は外部rootを
  allowlist環境変数（`REVIEWCOMPASS3_STATE_ROOT`等）から解決できる。state rootを差し替えるか消せば、
  同一の承認recordが再び未消費として合格する。
- 既存`mark_consumed`は承認record fileを書き換える設計であり、`approval_claim`は承認recordと同じ
  directoryに`.<name>.consume-claim`を作る。承認recordがrepository内にあるため、既存実装をそのまま
  再利用すると実Run中にrepository内へ差分とclaim fileが生じ、§11停止条件「repositoryに範囲外変更が
  生じる」に自ら抵触する。

影響：`high` riskの中心的な安全性である「承認は一回だけ消費できる」が、環境変数またはstate root削除で
無効化される。範囲固定§5末尾の「再実行には新しいHuman承認を要求する」も同時に成立しなくなる。

必要な措置：次versionのscopeで、承認recordの配置（Git内／runtime）、`consumed`fieldと外部markerの
どちらを一回性の正本にするか、state rootが差し替わった場合の扱いを一つに決め、受入条件へ固定する。

## 6. risk分類の妥当性

`high`は妥当であり、過小分類はない。守り役code（承認検証・環境除外・応答検証）と不可逆操作
（外部送信）の両方に該当し、`work-review-protocol.md`§3の既定`high`と一致する。上位riskへ変更する
根拠は見当たらない。

## 7. non-blocking（実装時確認事項）

`work-review-protocol.md`§11.2に従い、実装手段の詳細は完了レビューで検証する。

- **N1：`--max-turns`がClaude Code `2.1.220`に存在しない（実測）**。範囲固定§6.1は起動argvを
  9個のflagの閉じたallowlistとするが、`claude --help`（230行）を照合した結果、`--print`、
  `--safe-mode`、`--tools`、`--disallowedTools`、`--strict-mcp-config`、`--disable-slash-commands`、
  `--no-chrome`、`--output-format`の8個は実在し、`--max-turns`だけが存在しない。これは範囲固定§11の
  停止条件「Claude CLIのflagが実測と一致せず、安全設定を固定できない」に該当するため、§12に従い
  次versionのscopeで訂正する必要がある。あわせて`--tools`と`--disallowedTools`は可変長引数
  （`<tools...>`）であり、`--tools ""`と`--disallowedTools "*"`が意図どおり全tool無効を意味するかは
  未実測である。Humanが固定した「Claudeの全toolを無効にする」条件の成立可否に直結するため、
  実測で確定してから受入条件へ書く。
- **N2：payload list digestは順序を束縛しない（実測）**。既存`payload_list_digest`は
  `json.dumps(sorted(...))`であり、docstringも「順序に依らず決定的である」とする。2 payloadの
  digestを逆順で与えても同じ`967e9410…`となることを確認した。範囲固定§4の「上記順序のDigest列を
  …計算した値」という表現は、list digestが順序を保証するとの誤解を招く。受入条件§7-2と§5-1は
  「順序」を別項目として挙げているため条件自体は欠落していないが、順序検査を承認検証と同じ
  fail-closed境界に置くことを実装時に確認する。
- **N3：root名の表記**。範囲固定§6.2は`STATE_ROOT`／`SENSITIVE_ROOT`と書くが、
  `tools/layout/baseline.py`の論理root名は`state_root`／`sensitive_root`である。
- **N4：既存挙動の非回帰**。`APPROVED_PURPOSES`への新purpose追加が場面1経路へ影響しないこと
  （`gate.py`は`purpose="implementation_sameness_judgment"`を直接指定している）を、完了レビューで
  既存egress testにより確認する。

## 8. 独立再実行

いずれも単独commandで実行し、exit codeで判定した。

| 実行 | 結果 |
| --- | --- |
| 公式全Test `python3 -m tools.development.policy_test_runner --suite full` | `status: passed`、exit code 0、1470 passed／failed 0／errors 0／skipped 0、Python 3.9.6、pytest 8.4.2、`fallback_used: False` |
| 固定入力14件のSHA-256再計算 | 14件一致、不一致0件 |
| payload 2件とlist digestの再計算 | 3件とも記載値と一致 |
| `payload_list_digest`の順序依存性確認 | 正順・逆順で同一値（N2の根拠） |
| `scan_outbound_text`をpayload 2件へ適用 | 検出0件 |
| `subprocess_runner`への非template argv | returncode 0で起動（F3の反証） |
| `claude --version` と実行fileのSHA-256 | `2.1.220`、digestは§2と一致 |
| `claude --help`のflag照合 | 8件実在、`--max-turns`のみ不在（N1の根拠） |
| `git check-ignore --no-index`（本record path） | exit code 1（ignoredでない） |

全Testは実装前のbaselineとして取得したものであり、本作業による変更は含まない。

## 9. Human境界

維持されている。範囲固定§1は「進めて」の効力を範囲固定recordの作成と独立範囲レビューの依頼までに
限定し、`high` riskの実装開始、送信時承認、実送信をそれぞれ別のHuman境界として残している。
`role-neutral-pilot-review-collaboration.md`§3の「`high`は範囲レビュー合格とHumanの明示承認まで
実装へ進めない」と一致する。ただしF1のとおり、新用途そのものを許すHuman裁定が未取得である。

## 10. 未実施の確認

事後状態から次を確認した。停止地点より後の成果物は作られていない。

- `tools/egress/`の内容は`__init__.py`、`approval.py`、`dry_run.py`、`gate.py`、`payload.py`、
  `prefilter.py`、`sender.py`のみ。`claude_session.py`と`trusted_claude_send.py`は存在しない。
- `tests/test_trusted_claude_send.py`と`tests/test_trusted_claude_send_adversarial.py`は存在しない。
- `records/development/2026-08-11-approved-claude-send-path/`は存在しない。
- 外部送信、push、PR、CIは行っていない。Reviewer側でも実装fileとtestを変更していない。
- 本レビューではClaude Code実行fileに対し`--version`と`--help`だけを実行した。payloadの送信、
  session生成、model指定を伴う起動は行っていない。

## 11. 並行作業（`work-review-protocol.md`§7）

### 11.1 レビュー中に進んだHEAD

レビュー実施中の2026-08-11 05:59:12 +0900に、review対象commitの後へ
`1bf90a0a32bd8efa7381f8fee90ca430d30bed73`（`Define pilot-specific Claude Codex roles`）が入った。
変更は`docs/development/pilot-specific-claude-codex-collaboration.md`の新規追加1件のみである。
このcommit後に固定入力14件のSHA-256を再計算し、**14件とも一致**することを確認した。したがって
範囲固定§3の「範囲レビュー後にDigestが不一致となった場合は本scopeをstale」には該当しない。

### 11.2 追加された役割文書と本レビューの関係（non-blocking）

新文書は§1で「`pilot: codex`でClaudeをレビュー担当にする方式は使わない」とし、§7でも同様に禁じる。
本作業の役割割当（pilot：Codex、reviewer：Claude）はこれに当たるが、次の理由で本レビューは有効である。

- 新文書§1は`collaboration_method: pilot_specific_claude_codex`を開始時に固定した作業だけに適用され、
  同じ作業へ`role_neutral_pilot_review`を同時に適用しないと定めている。本作業は範囲固定§で
  `collaboration_mode: role_neutral_pilot_review`を固定している。
- 新文書§2は「この決定は、既存の作業記録を遡って変更しない。本書を参照して開始する新しい作業から
  適用する」と定める。本作業の範囲固定commit `c9d128e`は新文書のcommit `1bf90a0`より前である。

新文書は範囲固定§3の固定入力ではないため、本レビューのoracleには使っていない。ただし本作業を
次versionのscopeで再開する場合、どちらの連携文書を適用するかはHumanが決める事項となる。

## 12. 次

Humanの判断を一つ求める。**F1〜F4を反映した範囲固定v2の作成をPilotへ指示するか、本作業自体を保留に
するか**である。

`verified`ではないため、`high` riskの実装開始（`RED`）の根拠にはならない。
`role-neutral-pilot-review-collaboration.md`§8に従い、Findingの修正はReviewerではなくPilotが別作業
単位で行う。本record作成時点で、Reviewerは実装fileとtestを一切変更していない。
