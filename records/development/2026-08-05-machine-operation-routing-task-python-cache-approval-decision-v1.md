# task専用Python cache root最小slice 承認Decision v1

- decision ID：`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`
- decision maker：Human
- decided at：2026-08-05
- 対象Issue：`ISSUE-HTC-C9F6C917`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-task-python-cache-slice.md`

## 1. Humanの承認文言

> Humanは、`ISSUE-HTC-C9F6C917`の次の最小sliceとしてtask専用Python cache rootを実装するよう指示した。

## 2. 配置・所有・保持は新たに決めない

cacheをどこへ置き、誰が持ち、いつ消せるかは、このDecisionでは新しく決めない。
Humanが既に承認したLayout v3（配置の基準を定めた記録）をそのまま使う。

- 正本：`records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`
- 承認：`records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`

Layout v3が定めるcache rootの規則は次である。

| 項目 | 値 |
| --- | --- |
| 外部root | `<runtime_root>/projects/<project_id>/<profile>/cache/` |
| 現在対象のprofile（環境の区分） | `development` |
| 意味 | 再生成できるcacheを置くproject外root |
| Git管理 | しない |
| 所有 | runtime |
| 保持 | `evictable`（消してよい） |
| 削除 | runtimeは自分が所有するcacheを削除してよい |
| runtime rootの既定 | home相対の`.reviewcompass3` |

project IDは`.reviewcompass/project-manifest.json`の固定値（`reviewcompass3`）から読む。
絶対path、checkout ID、内容Digestから導出しない。

## 3. 承認した範囲

- Layout v3のcache root配下に、task（作業）ごとのPython bytecode cache directoryを
  決定的に解決すること。解決だけではdirectoryを作らない。
- 明示的な初期化操作のときだけ、cache rootとそのtask directoryを作ること。
- `PYTHONPYCACHEPREFIX`（Pythonがbytecode cacheの出力先を決める環境変数）だけを持つ
  環境mappingを返すこと。mappingを作るだけでは`os.environ`（実行中processの環境）を変えない。
- 安全境界をfail-closed（判断できなければ止める）で守ること。

## 4. 対象外（この承認に含まれない）

- 実際のホーム配下（`~/.reviewcompass3`）の初期化。今回のTestは一時directoryだけを使う。
- 既存processへの自動適用。`policy_test_runner`や`structured_argv_executor`への接続。
- cleanup（掃除）・retention（保持期限）の自動化、時間ベースの削除。
- 環境変数のglobal（process全体）変更。
- Windows adapter、既存直接操作の移行、移行inventoryの作成。
- Git metadata書込み、project成果物書込み、external操作、host側tool構文、外部送信。
- Issue state、Task Contract、policy、config、既存Decisionの変更。

これは後続Plan全体の承認ではない。`ISSUE-HTC-C9F6C917`のIssue recordのstateは`registered`のまま
変更しない。正式なIssue Resolution Plan、Task Contract、Workflow permitも作らない。

## 5. 参照入力と作成時のSHA-256

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Layout v3正本 | `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` | `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38` |
| Layout v3承認 | `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json` | `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275` |
| 後続Plan提案 | `docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md` | `d5877f9668cc75a00a25b79d0fad9050c7ae3dd243047a4c61ba6e776fceb571` |
| Layout実装 | `tools/layout/baseline.py` | `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7` |
| Project Manifest | `.reviewcompass/project-manifest.json` | `e4e0636cf2d6382c870acd88e82b8a9febe10e14a4cc4ffc40d08af6018f9c30` |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| 本指示 | `records/session-handoffs/2026-08-05-codex-to-claude-implement-task-python-cache-slice.md` | `6fa146fa1977076bad317319fc7cfd64032c95f0564cdb1b49e43043a6f99dea` |

承認範囲は、後続Plan提案の**§2.2（task専用Python cache rootの責任境界）**に対応する。
提案§2.2はA（project内）・B（OS一時領域）・C（利用者の標準cache）を比較していたが、
配置はこのDecisionでLayout v3のcache root（project外・runtime所有）に確定した。
提案本文は履歴としてそのまま残す。

## 6. 維持する停止原則

- unsafeなtask ID、unsafeなprofile、相対runtime root、project内へ重なるruntime root、
  symlinkを含むtarget、directoryとして使えない通常fileは、初期化を一度も呼ばずに拒否する。
- 別のpath規則を作らず、Layout v3のresolverとinitializerだけを使う。
- callerが任意のproject IDを渡して別projectのcacheへ書けないようにする。
- host側の問題をproject内で解決したと書かない。
