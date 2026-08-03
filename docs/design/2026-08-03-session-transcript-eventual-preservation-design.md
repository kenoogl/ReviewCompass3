---
document_id: RC3-DESIGN-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-2026-08-03-V1
recorded_at: 2026-08-03T23:44:09+09:00
status: human_directed_design
implementation_status: not_started
activation_status: not_authorized
authority_scope: session_transcript_preservation_design_direction
confidentiality_class: project-internal
---

# Session Transcript Eventual Preservation Design

## 1. 結論

Session Logの保全は、session終了時に一度だけ動くhookを正しさの前提にしない。Codex／Claudeが書いた
source logを機械的に継続回収し、定期再走査と起動時再照合によって取りこぼしを後から回収する
`eventual preservation`を基本方式とする。

hook、file watcher、session終了通知は回収を早める補助手段として利用できるが、それらが呼ばれない場合でも、
次の定期走査または起動時走査で復旧できなければならない。sessionの完了判定は保存の必要条件にしない。

本書は設計方向を固定する。collector実装、保存場所、保存期間、暗号化、OS schedulerの有効化、現在の
private log取得は別のTask ContractとHuman判断まで開始しない。

## 2. 背景と問題

ReviewCompassとReviewCompass2では自動保存を試してきたが、session終了時だけに依存する方法では次の状況を
安全に扱いにくい。

- Codex Desktop、Codex CLI、Claudeでsource形式とlifecycle通知が異なる。
- applicationまたはterminalの異常終了時に終了hookが呼ばれない。
- source logが書込み中で、末尾に不完全なJSONL行が存在し得る。
- sessionの休止、再開、compaction、追記と完了を一意に区別できない。
- collector自身が途中で停止し、raw保存とcursor更新の片方だけが完了し得る。
- 元の会話情報が後から移動または削除され、抜粋だけでは原因解明に必要な情報が失われ得る。

したがって、保証対象を「終了時に必ず一度保存する」から「sourceが利用可能な間に機械処理が観測した範囲を、
中断と再実行に耐えて最終的に保全する」へ変更する。

## 3. 保証目標

この設計が保証対象とするのは次の性質である。

1. 同じsource範囲を何度取得しても重複しない。
2. sourceへの追記を前回の続きとして保全できる。
3. collectorが途中停止しても、次回実行で安全に再開できる。
4. hookまたはwatcherが動かなくても、定期走査または起動時走査で回収できる。
5. session完了を判断できなくても、観測済み範囲を保全できる。
6. sourceの短縮、置換、並べ替えを追記として誤って上書きしない。
7. 読める会話録が失われても、保全rawから再生成できる。
8. 未対応source／event、部分取得、source消失、Digest不一致を正常な空sessionとして扱わない。
9. privateな会話内容をGit管理対象へ書き込まない。

次は保証しない。

- sourceへ書かれる前の会話をReviewCompass側だけで復元すること
- hard real-timeの保存
- 終了時点を常に正確に判定すること
- sourceがcollectorの初回観測前に消失した場合の復元
- hook、watcher、特定Desktop applicationだけによる完全性保証

## 4. artifactの関係

```text
Codex／Claude native source log
  -> preserved raw（byte正本、private、append-only）
    -> private verbatim transcript（完全な会話内容、private）
      -> redacted transcript／summary（共有可能な派生物）
    -> provenance／cursor／integrity ledger（機械照合用）
```

| artifact | 役割 | 完全性 | 既定配置境界 |
|---|---|---|---|
| native source log | Codex／Claudeが生成する取得元 | ReviewCompass管理外 | provider固有local root |
| preserved raw | 観測したsource byteを改変せず保存する復元正本 | byte-exact | local non-Git private root |
| private verbatim transcript | user、developer、assistant、tool call／resultを省略せず読むための会話録 | 会話event完全、内部echoとreasoning表示は除外 | local non-Git private root |
| redacted transcript | secret等を伏字化した閲覧用派生物 | verbatimではない | policyで許可したroot |
| summary | 抜粋・要約 | 原因調査の正本にしない | policyで許可したroot |
| provenance | raw範囲、parser、rule、派生物Digestの結線 | 決定的に再計算可能 | sensitive値を含めないroot |
| cursor | sourceごとの観測・保全・解析位置 | machine state | local state root |
| integrity ledger | preserved rawのsizeとDigest | machine verification | local stateまたは安全なrecord root |

`verbatim`は選択された会話eventの本文を縮約しないことを意味し、native fileの全recordをそのまま表示すること
ではない。reasoning、metadata、重複通知はrawには残すが、会話録本文には混ぜない。伏字化を行った成果物は
`private verbatim transcript`ではなく、別identityの`redacted transcript`として扱う。

## 5. component責務

### 5.1 Source Adapter

provider固有sourceを識別し、共通eventへ変換する。現行実装はClaude、`codex_exec_json`、
`codex_rollout`を扱う。未知形式を別形式として推測しない。

### 5.2 Collector

source rootを探索し、前回観測以降のbyteを取得する。Collectorはsourceを削除・短縮・修正せず、取得した
snapshotとcursor更新を別段階として扱う。collectorは未実装であり、既存のdiscoveryとpreservationを
再利用または拡張する。

### 5.3 Raw Archive

取得済みrawを追記専用で保全する。incoming sourceが既存rawのbyte prefixを維持する場合だけ更新し、短縮、
置換、途中変更では既存rawを上書きしない。現行`preservation.py`のprefix検査、atomic replace、lock、
integrity ledgerを基礎にする。

### 5.4 Cursor Store

sourceごとに最低限、次を決定的に保持する。

- source kindとprovider
- native session IDまたは代替source identity
- local source locator
- 初回record Digest
- observed byte size
- rawへcommit済みのbyte offsetとprefix Digest
- 完全なJSONL行まで解析済みのbyte offset
- 最終観測時刻、最終成功run ID、現在状態

cursorは正本rawより先に進めない。raw commit後、cursor commit前に停止した場合は、次回runでraw Digestを
照合して同じ範囲を再適用し、重複なしでcursorを進める。

### 5.5 Reconciler

source、preserved raw、cursor、integrity ledger、派生物Provenanceを再照合する。起動時、定期実行時、
手動検証時に同じ処理を使用する。個々のsourceの失敗を他sourceの正常保全へ偽装しない。

### 5.6 Transcript Generator

完全なJSONL行までの保全rawを共通eventへ変換し、private verbatim transcriptを生成する。その後、必要な
場合だけ別工程でredactionとsummaryを生成する。派生物はraw範囲、source Digest、parser version、rule
Digestへ結線する。

### 5.7 Trigger Adapter

次の入口は同じcollector／reconcilerを起動するだけとし、保存ロジックを重複実装しない。

- applicationまたはworker起動時
- OS schedulerによる定期実行
- session start／end hook
- file watcher
- Humanによる手動reconcile

定期実行と起動時再照合をcorrectness pathとし、hookとwatcherはlatency改善用とする。

## 6. 状態モデル

| state | 意味 | 次の機械処理 |
|---|---|---|
| `discovered` | sourceを初めて発見した | identityとcursorを作りsnapshot取得 |
| `capturing` | 新しいbyteを観測している | rawへatomic commit後cursor更新 |
| `quiescent` | 一定期間追記を観測していない | 定期再走査を継続 |
| `source_missing` | 既知sourceを現在読めない | preserved rawを維持し、次回再走査 |
| `diverged` | sourceが既存prefixと一致しない | 上書き停止、conflict Evidence作成 |
| `parse_incomplete` | 末尾が不完全行または解析不能 | raw保全、解析offsetを進めず再試行 |
| `reconciled` | source、raw、cursor、派生物が照合済み | 次の走査まで維持 |

`quiescent`は完了ではなく、再追記で`capturing`へ戻れる。`closed`を保存の必須stateとして導入しない。

## 7. 回収と復旧の手順

1. 許可済みsource rootを機械探索する。
2. source identityを解決し、対応するcursorとpreserved rawを読む。
3. source byteをsnapshotとして読み、既存rawとのprefix関係を確認する。
4. 同一なら`unchanged`、純粋な追記ならrawをatomic更新する。
5. 短縮、置換、途中変更なら`diverged`として既存rawを保持する。
6. 完全な最終改行までを解析対象とし、部分行は次回へ残す。
7. event IDを第一候補、source identity・位置・event fingerprintを補助identityとして重複を排除する。
8. private verbatim transcriptと必要な派生物を生成する。
9. raw範囲と派生物Digestを再読込照合した後にcursorを進める。
10. run receiptへsource別の`created | updated | unchanged | missing | diverged | failed`を記録する。

同じrunを再実行しても、raw、会話event、派生物が増殖しないことをidempotency関門とする。

## 8. failureと復旧規則

| failure | 停止・保全 | 復旧 |
|---|---|---|
| source末尾が部分行 | raw snapshotは保全可、解析offsetは進めない | 次回追記後に完全行として再解析 |
| raw書込み失敗 | 既存rawとcursorを維持 | temporary file除去後に再実行 |
| raw成功・cursor失敗 | rawを上書きせずcursor未更新を保持 | 次回Digest照合後にcursorだけ進める |
| source短縮・置換 | 既存rawを保持して`diverged` | 別instance扱いまたはHuman判断 |
| source消失 | preserved rawと派生物を保持 | source再出現時にidentity照合 |
| 未知source／event | 推測せずsource別に失敗記録 | adapter追加後にrawから再生成 |
| hook／watcher失敗 | session操作を妨げず失敗receiptを残す | scheduler／起動時reconcile |
| scheduler停止 | 現行rawを変更しない | 次回起動または手動reconcile |
| ledger不一致 | restoreと派生物更新を停止 | preserved rawとledgerを独立監査 |
| 同時collector | source単位lockで一方を待機・停止 | lock解放またはstale lock復旧後に再実行 |

## 9. LLMと機械処理の境界

次はすべて機械処理とする。

- source探索、identity解決、byte読取り、cursor更新
- prefix比較、offset計算、JSONL完全行の判定
- event抽出、重複排除、並び順の維持
- atomic write、lock、Digest、Provenance、receipt
- 再走査、再生成、stale／divergence検出
- source別成否集計と機密値を含めない報告材料生成

LLMは、保全済み会話内容の意味分析、原因候補の説明、改善候補の文章化に限定する。LLMがoffset、Digest、
重複、保存成否、session完了を目視で裁定しない。

## 10. securityとauthority境界

- native source、preserved raw、private verbatim transcript、cursorのlocal locatorはprivateとして扱う。
- private artifactをrepository root配下またはGit管理対象へ置かない。
- redacted transcript、summary、Provenanceを共有可能とする場合も、別artifact identityと検証を要求する。
- collectorは明示的に許可したsource root以外を探索しない。
- source logを削除、移動、短縮、編集しない。
- 外部送信、cloud同期、無期限retentionを本設計から承認しない。
- 本書はWork 4開始、製品release、scheduler／hook有効化のauthorityにならない。

## 11. Acceptance候補

実装前に少なくとも次を固定fixtureとnegative testへする。

1. Claude、Codex exec JSONL、Codex rolloutの初回取得。
2. 追記後の増分取得と同一入力再実行時の無変更。
3. raw commit直後、cursor commit前の強制停止と再開。
4. JSONL末尾の部分行を解析せず、次回追記後に一度だけ採用すること。
5. source短縮、途中置換、event並べ替えで既存rawを上書きしないこと。
6. hook未実行でも定期走査が回収し、scheduler未実行でも起動時走査が回収すること。
7. source消失後もpreserved rawからprivate verbatim transcriptを再生成できること。
8. 未知source／eventを空sessionまたは既知形式へ誤分類しないこと。
9. 2 collectorの競合、stale lock、atomic write失敗で既存artifactを壊さないこと。
10. private verbatim transcriptとredacted transcriptを同一identityにしないこと。
11. raw、cursor、transcript、ProvenanceのDigest不一致で完了報告を停止すること。
12. 実行報告にsource別の成功、未取得、divergence、再試行対象を値非表示で出せること。

## 12. 現行実装との対応

| design責務 | 現行資産 | 状態 |
|---|---|---|
| 3 source kind解析 | `tools/session_logs/source_adapter.py` | 実装・Test済み |
| source探索 | `tools/session_logs/discovery.py` | provisional、単一root探索 |
| raw prefix保全 | `tools/session_logs/preservation.py` | provisional、再利用候補 |
| event追記判定 | `tools/session_logs/updates.py` | provisional、再利用候補 |
| atomic派生物保存 | `tools/session_logs/storage.py` | provisional、再利用候補 |
| 再生成とDigest照合 | `tools/session_logs/regeneration.py` | 3 source kind対応済み |
| scheduler | `tools/session_logs/scheduler.py`ほかplatform adapter | provisional、補助trigger候補 |
| session hook | `tools/session_logs/hooks.py` | provisional、補助trigger候補 |
| durable cursor | 該当実装なし | 追加設計・TDDが必要 |
| 起動時reconcile | 統一ownerなし | 追加設計・TDDが必要 |
| private verbatim artifact | parserは完全本文を保持、storage前にredaction | artifact分離のTDDが必要 |

既存機能が存在することと、自動保全が有効であることを混同しない。現時点ではscheduler、hook、collectorを
実環境へ有効化しておらず、現在のprivate会話も取得していない。

## 13. 実装順序候補

1. collector／cursor／reconcilerのTask Contractと固定fixtureを作る。
2. 初回、追記、再実行、部分行、crash recovery、divergenceのREDを確認する。
3. 単一source・手動実行の最小collectorを実装する。
4. private verbatim transcriptとredacted派生物を別identityへ分離する。
5. 起動時reconcileと定期実行を同じownerへ接続する。
6. hook／watcherを任意の補助triggerとして接続する。
7. 実private dataを使わないfixtureでE2Eとmutation assuranceを行う。
8. 保存場所、retention、暗号化、実行間隔をHumanが判断する。
9. 明示承認後だけ限定deploymentを行い、取りこぼしと誤取得を実測する。

## 14. 未決事項

- OSごとのnative source rootとsource availability期間
- local raw、private verbatim、cursor、ledgerの具体的保存root
- 定期走査間隔とcapture deadline
- retention、削除、backup、暗号化、access control
- source rename／移動時の安定identity
- 複数端末間での重複と外部同期を扱うか
- redacted transcript／summaryをGit管理対象にできる条件
- collectorをReviewCompass製品機能、開発補助tool、独立serviceのどれとして所有するか

これらは本書で推測せず、実装または有効化前のHuman判断へ渡す。
