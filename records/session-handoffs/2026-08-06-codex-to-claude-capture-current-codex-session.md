# Codex → Claude：現行Codex session manual reconcile指示

## 1. 承認と目的

Humanは「修復と再承認後、codexのセッションログを記録する」と指示した。

Codexは、active_staleのversion 1を書き換えず、現行Development Policyへ束縛したnew-onlyの
Task Contract version 2と再承認Decisionを作成した。

| artifact | path | SHA-256 |
| --- | --- | --- |
| Task Contract v2 | `records/task-contract/session-transcript-eventual-preservation-v2.json` | `d75049cb8f53dc0d7ae7429270c00ca539e90485133d1984edde07f61158355a` |
| Human Decision | `records/development/2026-08-06-session-transcript-repair-and-recapture-decision-v1.json` | `c6ff5904d86049f4e414e93dd3342b0ab793b1a50d0b4f664f507e2faf5c05a5` |

Claudeは、このCodex turnが終了した後、承認された一件のCodex rolloutだけを既存private archiveへ
manual reconcileする。Claude session、過去Codex session、redacted transcriptは対象外である。

## 2. なぜClaudeから実行するか

Codex自身がライブtaskをcaptureすると、capture用Tool Callがraw末尾へ記録され、そのTool Resultより先に
sourceを読むため、常に新しい未対応Tool Callが一件残る。

Claudeは別sessionのexecutorなので、Codex turn終了後にClaudeから実行すれば、Codex sourceへ新しい
capture Tool Callを追加せず、保存末尾を閉じた状態で取得できる。

## 3. 作業前の照合

1. `AGENTS.md`を全文読む。
2. Task Contract v2とHuman Decisionを全文読み、上記SHA-256を照合する。
3. `validate_fixed_sources_for_contract()`でTask Contract v2のfixed source 5件が合格することを確認する。
4. version 1のTask Contractとprivate artifactを削除、変更、source-pinしない。
5. Git statusを保存し、既存のWork 6A作業差分を列挙する。これらを変更、stage、commitへ混ぜない。
6. provider sourceは`Path.home() / ".codex" / "sessions"`から解決し、Decisionに記載したrelative pathだけを使う。
7. private rootは`resolve_deployment_paths().data_root / "eventual-preservation"`で解決する。
8. 既存保存rawがprovider sourceのbyte-exact prefixであることを再確認する。不一致なら実行せず停止する。

private absolute path、raw本文、逐語録本文、Tool引数・結果本文をterminal出力またはrepository Evidenceへ
書かない。値なしの件数、Digest、byte数、時刻、statusだけを扱う。

## 4. manual reconcile

`tools.session_logs.eventual_preservation.collect_source()`の既存public APIを使用する。

- source root：§3で解決したCodex sessions root
- source relative path：Decisionの`authorized_capture.source_relative_path`
- private root：§3で解決したrepository外private root
- repository root：現在のrepository root
- tool version：`eventual-preservation-v1`（collector実装は変更していないため）
- redaction rules：`None`
- run ID：実行時刻を含む一意なmanual run ID
- observed at：実際のJST ISO 8601時刻

一回目を実行し、`action: updated | unchanged`、`state: reconciled`、source kind `codex_rollout`、
source identityがDecision記載値と一致することを確認する。

同じ入力で直ちに二回目を実行し、`action: unchanged`、同じevent数、同じraw／verbatim Digestであることを
確認する。二回目で追加byteまたは重複eventが生じた場合は停止する。

## 5. 保存後の独立照合

private artifactを再読込みし、本文を出さずに次を機械確認する。

1. rawがUTF-8として読め、全非空行がJSON objectで、invalid JSON 0件、末尾改行あり。
2. parser issue 0件。
3. cursorのraw byte数、parse offset、event数、raw Digestが実fileと一致する。
4. rawから`render_transcript()`で再生成した逐語録が、保存逐語録とbyte単位で一致する。
5. cursor、Provenance、ledgerのsource identity、raw、parse、artifact Digestが一致する。
6. Tool Call／Tool Resultをcall IDで照合し、未対応件数を報告する。
7. fileは`0600`、directoryは`0700`、temporary／lock file残留0件。
8. private artifactがrepository外で、Git statusの既存Work 6A差分がcapture前後で変化していない。

Codex turn終了後の静止sourceを対象にするため、未対応Tool Callは原則0件を期待する。0件でない場合、
acceptedとせず、末尾eventのkind、tool name、line number、call IDのSHA-256だけを報告して停止する。

## 6. repository Evidence

次をnew-onlyで作成する。

- `records/development/2026-08-06-session-transcript-current-codex-recapture-receipt-v1.json`
- `records/development/2026-08-06-session-transcript-current-codex-recapture-evidence-v1.md`

記録する値：

- Task Contract v2とDecisionのpath、SHA-256
- first run／rerunのID、時刻、action、state
- source kindとsource identity
- capture前後のraw byte数、追加byte数、event数、issue数
- raw、verbatim、cursor、Provenance、ledgerのSHA-256
- 再生成一致、prefix一致、Tool pair、permission、temporary file、repository非変更の判定
- Claude／historical Codex／redacted／automation／外部送信を実施していないこと

private absolute path、session本文、prompt、response、Tool引数・結果は記録しない。

## 7. Test、commit、報告

- session log eventual preservation関連Testを実行する。
- 公式全Testは、既存Work 6A差分がGREENの意味単位として実行可能な場合だけ実行する。未完了のRED差分が
  ある場合、capture作業の失敗と混同せず、関連Testだけを実行し、全Test未実行理由をEvidenceへ明記する。
- `git diff --check`を実行する。
- receiptとEvidenceだけを明示stageして一つの意味的commitにする。既存Work 6A差分を混ぜない。
- push、PR、CI、外部送信を行わない。

完了報告はGit管理外の次へ保存する。

`records/session-handoffs/2026-08-06-claude-to-codex-current-codex-session-recapture.md`

commit SHA、first／rerun結果、追加byte数、event数、各Digest、再生成一致、Tool pair、permission、
関連Test、全Testの実施有無、既存Work 6A差分を変更していないことを報告して停止する。
