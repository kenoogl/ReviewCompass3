# Codex PilotによるClaudeセッション確立の範囲固定 v1

- 状態：試行前の範囲固定
- 日付：2026-08-11
- collaboration_mode：`role_neutral_pilot_review`
- pilot：Codex
- reviewer：Claude
- closer：Codex
- work_item：`codex-pilot-claude-session-bootstrap`
- risk提案：`high`
- 固定入力の出自：判断選定（Pilotが既存連携正本3件、開発入口、現行TODOを選定）

## 1. Humanの指示と承認

Humanは「今回はまずコーデックスをパイロットとしたセッション確立を目指す」と指示した。
その後、Claude Codeは契約プランの利用枠で動かし、API課金を使わないことを確認したうえで、
「進めて」と実行を承認した。

本試行では、Claude Codeの導入、契約プランによる認証、Anthropicへの非機密payload送信を
承認済みとして扱う。APIキーによる従量課金、追加利用枠の購入、repository内容の送信は
承認範囲に含めない。

## 2. 開始時点

- base commit：`c310ea44cad34f2b73eb864156b35e2af6c24c2e`
- branch：`main`
- worktree：clean
- Claude Code：`2.1.220`
- 認証確認：APIキー等を起動環境から除外した通常環境で、`loggedIn: true`、
  `authMethod: claude.ai`、`apiProvider: firstParty`
- Claude Desktopの画面取得：応答せず、初回経路には不採用

## 3. 固定入力

| path | SHA-256 |
| --- | --- |
| `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |
| `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c` |
| `TODO_NEXT_SESSION.md` | `c361baee7b84de372383249534e1890deb06638931e455006b35ae9eae59bc77` |

## 4. 最小E2E

E2E（入口から結果確認までの一連の試験）は、次の2往復だけとする。

1. Codexが新しいClaudeセッションを指定した識別子で起動し、固定したJSON応答を求める。
2. Codexが同じ識別子で再開し、1回目の合言葉を答えさせる。
3. Codexが2応答のJSON、同一セッション識別子、認証方式、終了状態を機械確認する。

Claudeへ送る業務情報は本recordのうち次の固定payloadだけとする。repository path、commit、
利用者情報、環境変数、認証情報、ソースコード、他recordの内容は送らない。

```text
あなたはClaude Reviewerです。Codex Pilotからの疎通確認です。
ツールを使わず、他のエージェントを起動せず、次のJSONだけを返してください。
{"protocol":"codex-pilot-claude-bootstrap-v1","role":"reviewer","nonce":"RC3-CPC-20260811-A","reinvoke":false}
```

2回目の固定payload：

```text
同じセッションの継続確認です。前回のnonceを使い、次のJSONだけを返してください。
{"protocol":"codex-pilot-claude-bootstrap-v1","continued":true,"nonce":"<前回のnonce>","reinvoke":false}
```

## 5. 権限profile

- Claudeの組込みtoolはすべて無効にする。
- MCP（外部機能を接続する仕組み）もすべて無効にする。
- project設定、plugin、hook、memoryを読み込まない安全設定を使う。
- 1回の起動につき応答は1回に制限する。
- APIキー、独自認証token、接続先上書きを起動環境から除外する。
- 契約プランの認証状態を送信前に通常環境で確認する。
- 起動権はPilotのCodexだけに置く。ClaudeはCodexも別agentも起動しない。

## 6. 受入条件

- Claude Codeの終了codeが2回とも`0`である。
- 1回目の結果が指定JSONと意味的に一致する。
- 2回目が同じセッションを再開し、nonce
  `RC3-CPC-20260811-A`を保持したJSONを返す。
- 2回ともtool使用がなく、`reinvoke`が`false`である。
- APIキーではなく`claude.ai`認証を使う。
- 送信payloadが§4の2件だけである。
- repositoryの作業treeを変更しない。

## 7. 停止条件

- 認証方式が`claude.ai`でない。
- 追加課金、追加利用枠、APIキー利用を求められる。
- Claudeがtool利用や別agent起動を求める。
- 応答がJSONとして解析できない、または指定schemaから外れる。
- 同一セッションを再開できない。
- repositoryに予期しない変更が生じる。

停止時はHuman中継へ自動で切り替えず、事象、commandの終了code、未実施範囲を報告する。

## 8. 変更可能pathと禁止path

変更可能path：

- 本範囲固定record
- 成立後に作る同work itemのEvidence record
- 必要な場合だけ`TODO_NEXT_SESSION.md`

禁止path：上記以外の全path。製品code、test、schema、既存authorityは変更しない。

## 9. 検証とcommit境界

本作業は文書と外部疎通の試行であり、RED／GREENは適用しない。

1. 本範囲固定recordを単独commitする。
2. 2往復を実行し、Codexが機械照合する。
3. 結果、終了code、認証方式、送信payloadのDigest、応答のDigest、未実施範囲をEvidenceへ固定する。
4. Evidenceを単独commitし、完了扱いにはHumanの判断を残す。

恒久的な連携方式への格上げ、既存authorityの改定、API方式・MCP方式との比較、実作業の
Claude委譲は今回実施しない。
