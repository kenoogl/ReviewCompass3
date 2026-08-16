# Claude → Codex：機械操作routing後続範囲のPlan提案作成 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-plan-machine-operation-routing-follow-on.md`

Human承認待ちのPlan提案、検証receipt、TODOの現在位置だけを作成し、1つの意味的commitにした。

## commit

- commit SHA：`c3e4d1b98e09492729bee0423d40a366311d4550`
- message：`Propose a plan for the machine operation routing follow-on`
- 3 file（Plan提案、test receipt、TODO）。明示pathだけをstageした。
  `git add -A`と`git add .`は使っていない。
- commit後のread-only照合：`git status --short`は空。
  `python3 tools/development/work_unit_transition.py --work-status completed`は
  `{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`

## Plan提案のpathとDigest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Plan提案 | `docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md` | `ab6d9b3bf33a6348a5718062930a7d58aa1bf8df75c22fc415a7221ba29d024c` |
| test receipt | `records/development/2026-08-05-machine-operation-routing-follow-on-plan-test-receipt-v1.json` | `5248d125f0a961e810dd642893aa4f7a3c2972269f3c128b87f89c756b73ac44` |

状態は`awaiting_human_approval`。冒頭に「実装許可ではない」「正式Decision、Task Contractでもない」
「承認までargv executor、cache root、移行inventory、置換を実装しない」「RED testも作らない」
「Issueは`registered`のまま」と明記した。

固定入力6件（対象Issue、主triage decision、既存正本設計v2、最小縦切りの承認Decision、
receipt整合性の訂正Decision、現在の実装module）をpathと作成時点のSHA-256で固定し、作成後に
再読込して機械照合した。不一致0件、本文で挙げた8 pathの欠落0件、引用した6件の行番号もすべて実在する。

## 現状調査（read-only、件数は推測していない）

`.venv`とegg-infoを除く`.py` **246 file**を機械検索した。

| 事実 | 件数 |
| --- | --- |
| `tools/`配下でGit commandを起動する箇所 | 6（path:lineをPlanに列挙） |
| そのうちGit metadata書込み（add／commit／tag／push） | **0** |
| repository全体の`shell=True` | 1（実使用ではなく、moduleのsource textに現れないことを確かめる禁止語の照合） |
| repository全体の`os.system` | 0 |
| `PYTHONPYCACHEPREFIX`／`dont_write_bytecode`の設定 | 0 |

ここから、repositoryのcodeにはGit metadataを書く経路が無く、書込みはagentが自分の操作として
行っていることを導いた。この事実を、後続3（既存直接操作の移行）の位置づけと優先順の根拠にしている。

## 推奨した段階順

3案を比較し、**案1**を推奨した。

> 設計固定 → RED test → argv executor最小slice → cache root最小slice → 移行inventory →
> 操作種別ごとの段階移行

理由は3点。閉じられる観測が多い層（引用・特殊変数）から着手できること、code内にGit書込みが無いため
移行inventoryを先に作っても直す対象がcode内に無く受け皿を先に用意するほうが自然であること、
段階が小さく失敗の影響が1 sliceに閉じること。推奨はHuman承認まで確定しない。

各段階について、実装しないこと、Human承認が要る条件、既存の動作を変更しない確認方法を表にした。
`unknown`のfail-closed、未取得権限での不起動、scope外host操作、`external`、identity不一致で停止する
既存原則は維持すると明記した。

## Human判断点（4件）

1. argv executorの許容操作種別と実行責任の境界（起動を許す分類、空文字列引数の扱い、
   executorがinventoryとpreflightを再判定しないこと）。
2. cache rootの配置（project内の除外directory／OSの一時領域／利用者の標準cache）と、
   削除するか保持するかの方針。
3. 移行対象の優先順と、最初の実装sliceの承認可否。
4. host側tool構文と外部送信を本Issueで扱わないことの確認。

## 全test結果

公式policy runnerで実行した。

- status：`passed`、exit code：`0`
- 構造化集計：`{"errors": 0, "failed": 0, "passed": 892, "skipped": 0, "total": 892, "xfailed": 0, "xpassed": 0}`

validator結果。

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| compaction validator | 合格（11,359 bytes、active ID 1件） |
| 参照整合 | 25件一致（Evidence節限定・globalとも） |
| `git diff --check` | stage前後とも合格 |

## TODOの更新範囲

現在位置だけを更新した。

- `## 次に行う一作業`を、作業候補の提示から「後続範囲のPlan提案に対するHuman判断を受ける」へ置換し、
  判断点4件を並べた。実装承認ではないことも書いた。
- 完了データの`ISSUE-HTC-C9F6C917`の行に、`registered`かつnonblockingのままであること、
  後続Plan提案がHuman承認待ちであること、推奨した段階順を追記した。
- Evidence節（`## 最新のauthority／Evidence`）は変更していない。機械計測した参照数は25件のままで、
  現在位置に記載した件数と一致している。

## 未実施事項

- code、test、config、policy、既存Plan、既存Decision、Task Contract、Issue recordの変更：していない。
  3 Issueはいずれも`registered`のままで、file digestも変わっていない
  （`56e0911d6f56…`、`a4a1511e6090…`、`66cfe50ce791…`）。
- argv executor、cache root、移行inventory、Git／shell操作の置換：実装していない。
- Git／shell／Python cacheの実行自動化、push、外部送信、hook、watcher、scheduler：開始していない。
- host側tool構文、sandbox／host権限承認、外部tool APIをproject内で解決したとは書いていない。
- RED test：作っていない。今回の成果は文書提案だけである。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
