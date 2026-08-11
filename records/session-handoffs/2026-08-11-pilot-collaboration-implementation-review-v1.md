# 操縦者別連携 production実装 独立レビュー v1

- 日付：2026-08-11
- 対象commit：`0974769d2ce91210dfb62a7a9a6179fd98e7f614`
- parent commit：`d88f4f3`
- 実装指示：`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md`
- 実装指示SHA-256：`5ab9474b425162df9c192124c7558754b4b371402d2e4d67adfab448cbbb3b5d`
- Human補足裁定：`records/session-handoffs/2026-08-11-pilot-collaboration-rt-pc-002-human-clarification-v1.md`
- Human補足裁定SHA-256：`c0c985689e5e2878e1351a6267597499f02eeb8771adff599fed9d794f705add`
- 固定RED確認：`records/session-handoffs/2026-08-11-pilot-collaboration-red-test-rereview-v4.md`
- 固定RED確認SHA-256：`da0c56616b101987158ceb624da25bfb2bf2cb012d56dbdbe755fe17ca30699c`
- 実装担当モデル：`gpt-5.6-sol`
- レビュー担当モデル：`gpt-5.6-terra`（新しい会話状態）
- 未加工結果保存：`specified_only`。最終応答は主担当の会話で受領したが、不変保存処理は未接続
- 判定：`reported_unverified`

## 1. 独立再実行

- 変更範囲：v6で許可した8 pathだけ
- 固定4 test fileのSHA-256：固定RED値と一致
- 固定受入test：73 passed、終了コード0
- 既存bootstrap review test：27 passed、終了コード0
- 公式全test：1543 passed、終了コード0
- 差分検査：合格
- worktree：clean
- 外部CLI起動・外部送信：未実施

## 2. 所見

| ID | 種別 | 段階 | 事象 | 修正方向 |
| --- | --- | --- | --- | --- |
| `IR-PC-001` | blocking・類型4（private root／symlink境界破り） | safety | private root自身だけをsymlink検査するため、repositoryを指す親symlink配下のprivate rootが通り、repository実体内へrunを作成できた | 親componentを含むsymlink解決とrepository containmentを一貫して検査する |
| `IR-PC-002` | blocking・類型3（保存物改竄の誤った合格） | completion／safety | event参照済みattemptだけを読むため、`launch/`、`raw/`、`parsed/`へ孤児JSONを注入しても`status`が成功した | eventと3 directoryの全file集合を相互照合し、孤児・余剰・参照欠落を`stored_record_invalid`にする |
| `IR-PC-003` | blocking・類型1（stale優先のauthority不一致） | completion | current instruction差異と保存raw改竄が同時にあると、保存物検査が先に走り`stored_record_invalid`／`blocked`となった | manifest検証後、artifact検証より前にcurrent source差異を調べ、`stale_input`／`stale`を優先する |
| `IR-PC-004` | blocking・類型1（CLI応答契約不一致） | completion | configまたはCLI引数からrun IDが判明していても、停止例外へ補完せず応答の`run_id`がnullとなった | 構文解析済みrun IDを停止応答のfallbackとして保持する |

## 3. 独立反証

1. repositoryへのsymlinkを親に持つ`repository-alias/private`をprivate rootにすると、prepareが終了コード0となり、
   repository実体内にrun directoryを作成した。
2. prepared状態の`launch/`、`raw/`、`parsed/`へそれぞれ`orphan.json`を注入してstatusすると、全変種が
   終了コード0、`ready_for_prompt_audit`となった。
3. current instruction差異と保存raw改竄を同時に置くと、statusは終了コード2、`stored_record_invalid`／
   `blocked`となり、要求された`stale_input`／`stale`を返さなかった。
4. 有効なrun IDを含むprepare configのsource digestを不一致にすると、終了コード2だがCLI応答のrun IDがnullだった。
   statusでも既知のrun IDに対する保存物エラー時にnullだった。

## 4. Human判断境界

4件はいずれも固定受入test外で見つかった新規所見である。Humanが採用・不採用を裁定するまで再実装せず、
本縦切りの完了または次段開始へ進まない。採用時は4件を一つの再実装単位とし、反証testをproduction修正前に
追加してREDを確認する。修正後は固定73件、追加反証、既存bootstrap review test、公式全test、差分検査を
再実行し、別の新しい会話状態で独立再レビューする。
