# セッションログ基盤の移植候補・既存テスト棚卸し

作成日：2026-07-27

```yaml
lifecycle: provisional
normative_status: non-normative
promotion_required: true
```

## 1. 目的

ReviewCompass3 の第0段で扱うセッションログ基盤について、ReviewCompass と
ReviewCompass2 に存在する実装、テスト、設定、フック、既知の失敗を責務単位で整理する。

本記録は移植を承認するものではない。ファイルを一括コピーせず、次のTDDサイクルで
契約とテストを選ぶための候補一覧とする。

## 2. 固定した調査対象

| 参照元 | 固定コミット |
|---|---|
| ReviewCompass | `35ef8d4cc66b9a00aca9c6da10b645837b06564b` |
| ReviewCompass2 | `d6bbb01500002872c713412bfbd63b702a291c99` |

全追跡ファイル一覧と照合値は
`records/reference-baselines/2026-07-27/baseline.toml` からたどれる。
調査時の未コミット差分は対象に含めていない。

## 3. 調査方法と範囲

- 固定コミットの全追跡ファイル名を、`session`、`record`、`capture`、`transcript`、
  `redact`、`provenance`、`backup`、`restore` などで機械検索した。
- 実装の呼び出し関係、テスト関数、設定、フック、計画、issue、限界文書を確認した。
- 実際に生成されたセッション記録とレビュー応答は、実装候補ではないため一覧から除いた。
- 旧リポジトリのテストは再実行していない。固定コミット内のテストの存在と内容、
  保存されている実行記録を調査対象とした。

## 4. 責務単位の候補

### 4.1 生ログの発見と入力形式の分離

ReviewCompass2 の主候補：

- `tools/session_capture/config.py`
- `tools/session_capture/events.py`
- `tools/session_capture/parse_claude.py`
- `tools/session_capture/sources.py`
- `tests/test_session_capture_config.py`
- `tests/test_session_capture_parse.py`
- `tests/test_session_capture_sourcekind.py`
- `tests/test_session_capture_sources.py`

ReviewCompass の補完候補：

- `tools/session_record_extractor/sources.py`
- `tools/session_record_extractor/transcript.py`
- `tools/session-record-capture-previous-claude.py`
- `tools/session-record-capture-previous-codex.py`
- `tests/tools/test_session_record_capture_previous_claude.py`
- `tests/tools/test_session_record_capture_previous_codex.py`
- `tests/tools/test_session_record_extractor.py`

確認した性質：

- ReviewCompass2 は再帰探索、対象外理由、壊れた行、補助記録、管理記録を明示的に扱う。
- ReviewCompass2 の実行経路は Claude のみで、Codex は語彙だけが存在する。
- ReviewCompass は Claude と Codex の両方を解析し、現在・記録済み・未記録を区別する。
- 入力形式の境界は両実装で異なるため、どちらかをそのまま正本にしない。

### 4.2 rawログからの転写

ReviewCompass2 の主候補：

- `tools/session_capture/transcript.py`
- `tests/test_session_capture_transcript.py`

ReviewCompass の比較候補：

- `tools/session_record_extractor/transcript.py`
- `tests/tools/test_session_record_extractor.py`

確認した性質：

- ReviewCompass2 は利用者・アシスタント・道具呼び出し・道具結果・思考を転写する。
- ReviewCompass2 は思考の署名だけを本文から除き、その事実を注記する。
- ReviewCompass は思考を除外し、道具結果を先頭・末尾と文字数で縮約する。
- 「全文」の意味と除外対象は、新しい入出力契約で決め直す必要がある。

### 4.3 人が読む要約

ReviewCompass2 の主候補：

- `tools/session_capture/summary.py`
- `tests/test_session_capture_summary.py`

ReviewCompass の比較候補：

- `tools/session_record_extractor/record.py`
- `tests/tools/test_session_record_extractor.py`

確認した性質：

- 両実装とも、利用者発言、コミット、変更対象ファイルを決定的に列挙する。
- 両実装とも、機械が利用者の決定を推測せず、決定欄を定型文にする。
- ReviewCompass2 は補助記録に含まれる利用者発言も出所付きで残す。
- ReviewCompass2 は要約を転写からではなく、生ログから直接生成する。

### 4.4 機微情報の伏字化と報告

ReviewCompass2 の主候補：

- `tools/session_capture/redact.py`
- `config/defaults.yaml`
- `tests/test_session_capture_redact.py`
- `tests/test_session_capture_registration.py`

ReviewCompass の補完候補：

- `tools/session_record_extractor/redact.py`
- `tools/session-record-allowlist.py`
- `.reviewcompass/session-extraction/redaction-rules.yaml`
- `tests/tools/test_redaction_high_entropy_masking.py`
- `tests/tools/test_session_record_backfill_cli.py`

確認した性質：

- 両実装とも既知パターンと高エントロピー候補を扱う。
- ReviewCompass2 はリポジトリ内、ホーム配下、その他の絶対パスを区別して正規化する。
- ReviewCompass2 は機微情報の報告をGit対象外へ分離する。
- ReviewCompass は残存検出時のfail-closed、機微報告、許可リスト追加CLIを持つ。
- 規則変更時の版上げ忘れは、ReviewCompass2で機械検出できない既知の穴である。

### 4.5 来歴、再生成、改変検知

ReviewCompass2 の主候補：

- `tools/session_capture/provenance.py`
- `tools/session_capture/verify.py`
- `tests/test_session_capture_provenance.py`
- `tests/test_session_capture_verify.py`

ReviewCompass の比較候補：

- `tools/session_record_extractor/provenance.py`
- `tests/tools/test_session_record_provenance.py`

確認した性質：

- ReviewCompass2 は引用元の相対パス、取り込み行数、取り込み範囲のSHA-256、
  道具種別、層、伏字化情報を来歴に持つ。
- ReviewCompass2 は取り込み範囲から本文を再生成し、1バイト一致を検査する。
- ReviewCompass2 は引用元への追記後も、取り込み済み範囲が同じなら一致を維持する。
- ReviewCompass は引用元ファイル全体のSHA-256を持ち、一致するファイルを探索する。
- 現計画の「取り込み範囲」と「再生成」にはReviewCompass2の方式が近いが、
  そのまま正式契約にはしない。

### 4.6 冪等性、変更検知、追記専用更新

ReviewCompass2 の主候補：

- `tools/session_capture/merge.py`
- `tools/session_capture/capture.py`
- `tests/test_session_capture_merge.py`
- `tests/test_session_capture_command.py`

ReviewCompass の比較候補：

- `tools/session_record_extractor/merge.py`
- `tools/session-record-backfill.py`
- `tests/tools/test_session_record_append_merge.py`
- `tests/tools/test_session_record_single_capture.py`

確認した性質：

- ReviewCompass2 は作成、更新、変更なし、保全の4行動を区別する。
- ReviewCompass2 は出来事列の接頭辞一致を追記とみなし、縮小、途中欠落、並べ替え、
  途中挿入では既存記録を保全する。
- ReviewCompass2 は転写の判定を要約へ連動させ、片方だけの更新を防ぐ。
- ReviewCompass は本文の部分列判定を使う。途中挿入を許すため、ReviewCompass2で
  記録喪失につながる穴として改められた。

### 4.7 統括CLI、出力配置、保存区分

ReviewCompass2 の主候補：

- `tools/session-capture.py`
- `tools/session_capture/capture.py`
- `tools/session_capture/layout.py`
- `tools/session_capture/config.py`
- `config/defaults.yaml`
- `tests/test_session_capture_command.py`
- `tests/test_session_capture_layout.py`
- `tests/test_session_capture_registration.py`

ReviewCompass の比較候補：

- `tools/session-record-extractor.py`
- `tools/session-record-backfill.py`
- `tools/session-record-draft.py`
- `tools/session-record-promote-draft.py`
- `tests/tools/test_session_record_extractor_cli.py`
- `tests/tools/test_session_record_bulk_guard.py`
- `tests/tools/test_session_record_promote_draft.py`

確認した性質：

- ReviewCompass2 は転写をGit対象外、要約をGit対象、機微報告をGit対象外に分ける。
- ReviewCompass2 は通常取り込み、dry-run、検証を1つの入口にまとめる。
- ReviewCompassは転写と要約をともにGit対象へ出すため、現計画の保存区分と異なる。
- ReviewCompassには進行中の下書きと正式記録の分離、現在セッションの直接取り込み防止がある。

### 4.8 開始時・終了時フック

ReviewCompass2 の主候補：

- `.claude/hooks/session-capture-on-start.sh`
- `.claude/hooks/session-capture-on-end.sh`
- `.claude/hooks/session-capture-run.sh`
- `tests/test_session_capture_hooks.py`

ReviewCompass の補完候補：

- `.claude/hooks/session-record-capture.sh`
- `.claude/hooks/session-record-capture-previous.sh`
- `.codex/hooks/session-record-capture-current-on-session-end.sh`
- `.codex/hooks/session-record-capture-previous-codex.sh`
- `.codex/hooks/session-record-promote-previous-draft.sh`
- `templates/hooks/session-record-capture-current-on-session-end.sh.template`
- `templates/hooks/session-record-capture-previous-codex.sh.template`
- `templates/hooks/session-record-promote-previous-draft.sh.template`
- `tests/hooks/test_codex_session_record_capture_current_on_session_end.py`
- `tests/hooks/test_codex_session_record_promote_previous.py`
- `tests/hooks/test_session_record_capture.py`
- `tests/hooks/test_session_record_capture_previous.py`

確認した性質：

- ReviewCompass2 は開始時と終了時の両方から同じ冪等な入口を呼ぶ。
- フックは標準出力を出さず、失敗を標準エラーと非Git領域の実行記録へ残し、
  セッション自体は正常に継続させる。
- ReviewCompassでは依存解決失敗を `|| true` が隠し、何も生成されない既知不具合があった。
  成功時だけ完了扱いにすることと、失敗を可視化することが再発防止候補になる。
- ReviewCompassにはCodex用フックがあるが、ReviewCompass2の統括CLIにはCodex経路がない。

### 4.9 生ログの別領域保全と復元

実装候補は、両固定コミット内に見つからなかった。

ReviewCompass2の調査・issue：

- `.reviewcompass/backlog/issues/issue-2026-07-26-raw-session-log-preservation.yaml`
- `.reviewcompass/evidence/research/2026-07-26-raw-log-lifetime.md`
- `docs/design/2026-07-26-session-capture-limitations.md`

確認した事象：

- 生ログは取り込みツールの外にあり、原本を複製・照合・復元する実装がない。
- ReviewCompass2の調査では、生ログの既定30日削除と既存ログの消失が報告されている。
- 保全範囲、保全先、復元方法、定期実行は未決で、issueはopenのままである。

### 4.10 セッション非利用期間の定期保全

実装候補は、両固定コミット内に見つからなかった。

ReviewCompass2のフック案件は、定期実行を明示的に対象外としている。したがって、
開始時・終了時フックだけでは長期間セッションを使わない場合の保全を満たさない。

## 5. 既存テストの一覧

### 5.1 ReviewCompass2

固定コミット内で、ファイル名が `test_session_capture` に一致する14ファイル、
テスト関数291件を確認した。

| テストファイル | テスト関数数 |
|---|---:|
| `tests/test_session_capture_command.py` | 24 |
| `tests/test_session_capture_config.py` | 17 |
| `tests/test_session_capture_hooks.py` | 18 |
| `tests/test_session_capture_layout.py` | 13 |
| `tests/test_session_capture_merge.py` | 29 |
| `tests/test_session_capture_parse.py` | 26 |
| `tests/test_session_capture_provenance.py` | 29 |
| `tests/test_session_capture_redact.py` | 31 |
| `tests/test_session_capture_registration.py` | 11 |
| `tests/test_session_capture_sourcekind.py` | 10 |
| `tests/test_session_capture_sources.py` | 16 |
| `tests/test_session_capture_summary.py` | 23 |
| `tests/test_session_capture_transcript.py` | 23 |
| `tests/test_session_capture_verify.py` | 21 |

限界文書には、フック導入前の取り込み基盤304件の緑、実データ353本の取り込み、
生成物364件の全件一致が記録されている。フック案件には全体322件の緑が記録されている。
本棚卸しでは再実行していないため、これらは既存証跡として扱う。

### 5.2 ReviewCompass

直接関係する17ファイル、テスト関数172件を確認した。

| テストファイル | テスト関数数 |
|---|---:|
| `tests/hooks/test_codex_session_record_capture_current_on_session_end.py` | 4 |
| `tests/hooks/test_codex_session_record_promote_previous.py` | 18 |
| `tests/hooks/test_session_record_capture.py` | 6 |
| `tests/hooks/test_session_record_capture_previous.py` | 4 |
| `tests/tools/test_redaction_high_entropy_masking.py` | 15 |
| `tests/tools/test_session_record_append_merge.py` | 5 |
| `tests/tools/test_session_record_backfill_cli.py` | 3 |
| `tests/tools/test_session_record_bulk_guard.py` | 4 |
| `tests/tools/test_session_record_capture_previous_claude.py` | 11 |
| `tests/tools/test_session_record_capture_previous_codex.py` | 12 |
| `tests/tools/test_session_record_contract.py` | 12 |
| `tests/tools/test_session_record_extractor.py` | 48 |
| `tests/tools/test_session_record_extractor_cli.py` | 4 |
| `tests/tools/test_session_record_promote_draft.py` | 2 |
| `tests/tools/test_session_record_provenance.py` | 13 |
| `tests/tools/test_session_record_single_capture.py` | 8 |
| `tests/tools/test_t024_v_session_record_realworld.py` | 3 |

`tests/tools/test_session_record_contract.py` は旧仕様との整合を検査するため、そのまま移植する
候補ではない。入出力契約を確認する証拠としてだけ扱う。

## 6. 既知の失敗と制約

1. ReviewCompassのフックは、Python依存解決の失敗を正常終了処理が隠し、無出力で何も
   生成しない状態になった。フック障害をセッションへ伝播させないことと、失敗を
   観測可能にすることを分けて設計する必要がある。
2. ReviewCompass2では、LF以外でも分割する処理によりJSONが壊れたが、実装と検査が
   同じ誤りを共有していたため一致し続けた。実データと独立した数え直しが必要である。
3. ReviewCompass2では、要約に出来事マーカーがないため毎回更新される不具合が後続工程で
   見つかった。層ごとの変更検知方法を明示する必要がある。
4. ReviewCompass2では、規則の内容を変えて版を上げ忘れると、再取り込みしても不一致が
   解消しない。規則本文のdigestを候補として再検討する必要がある。
5. ReviewCompass2の道具別境界はClaudeだけで検証されており、Codex追加時の妥当性は
   未確認である。
6. 両実装とも、生ログの別領域保全・復元・定期保全を実装していない。

## 7. 棚卸し結果

- 主たる構造候補はReviewCompass2の責務分割とテスト群である。
- Codex対応と過去セッション選択取り込みはReviewCompassの補完候補である。
- 伏字化は両実装の性質を比較し、新しいfail-closed条件をテストから決める必要がある。
- 保存区分はReviewCompass2が現計画に近い。
- 生ログ保全、復元、定期保全は移植ではなく新規のTDD対象になる。
- 採否と正式な入出力契約は未決であり、本棚卸しから直接実装へ進めない。
