# 第3段 試験と現行正本の整合方針 限定修正後確認 v1

- 確認日：2026-08-14
- 先行結果commit：`1975944e263ed8f40cc69cbfef296667f08e87f0`
- 先行レビューcommit：`9002ca731810b893c01774e4aa5378778a666208`
- 修正commit：`7b9df68587214a3a3d7573218e12302b8f4be547`
- 先行指摘：`CR-ST3-AUTH-001`
- 確認範囲：先行指摘一件の変更点だけ
- 判定：`verified`

## 1. 判定

【判断】`CR-ST3-AUTH-001`は解消した。固定した現行正本に含まれない資料への直接参照を、
変更・廃止された正本への参照と同じく矛盾候補へ含める条件が、立て直し計画、開発方針、
重要度別確認メモ、方針修正判断、TODOに揃っている。

【実測】止める指摘は0件、報告不一致は0件である。

## 2. 先行指摘の解消

【実測】修正後の五文書は次を明記する。

- 立て直し計画第3段：固定した確認基準に含まれない資料への直接参照、または確認基準の変更・廃止と
  関係するものを矛盾候補として抽出する。
- 開発方針：直接参照を機械列挙し、固定した確認基準に含まれない資料への参照、または確認基準の
  変更・廃止に関係する候補だけを人が確認する。
- 重要度別確認メモ§2.2：開発方針と同じ二つの候補条件を明記する。
- 方針修正判断§4・§6：同じ候補条件と、集合外の直接参照を候補に含める完了条件を明記する。
- TODO：次の軽量作業票の機械抽出対象へ、現行正本に含まれない直接参照を含める。

【判断】これにより、最初から暫定、履歴、不採用で、現行正本に一度も含まれなかった資料を試験が
合否基準にしている場合も、機械抽出後の人による候補確認へ送れる。全試験の人手確認、新機構、
新しい検査器・試験・関門は追加していない。

## 3. 止める指摘

【判断】0件。

## 4. 報告不一致

【実測】0件。修正commitの親は先行レビューcommitであり、変更pathは申告された六件だけだった。
コード、試験、設定、Issue、先行レビュー記録には差分がない。

TODOに記録された関連試験27件は、この一回限りの変更点確認では再実行していない。既存の実行報告を
完了根拠に使わず、候補条件の文言、参照内容識別値、差分範囲だけで判定した。

## 5. 限定機械確認

【実測】修正commitの差分は次の六pathだけだった。

- `TODO_NEXT_SESSION.md`
- `docs/development/2026-08-02-development-policy.md`
- `docs/development/2026-08-03-initial-development-checklist.md`
- `docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md`
- `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- `records/development/2026-08-14-recovery-plan-v5-stage3-test-authority-consistency-amendment-decision-v1.md`

【実測】各fileのSHA-256再計算値は次のとおりだった。

| file | SHA-256 |
| --- | --- |
| `TODO_NEXT_SESSION.md` | `d1c2dfca0fbf8ecf434482ad03d813a3abe4df0aa4913e5c8ff3eb10c47ca738` |
| `docs/development/2026-08-02-development-policy.md` | `b3c7ce815705ba11915d3d384ee5d7fa2b8175503a03c9ff2417e79c83aeb5dc` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `5890f242253f260bd299af4a3f0821d03d5a37afdfa6e93eb6d5615049f63d9d` |
| `docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md` | `1090ea3083574c6dfb9cf0345505c070240cfd2e81b87929f6f7c2a50c0c2591` |
| `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md` | `c150187e7e79ddd955942bba5c4a775dbda64537f31931bd048604ab5cb082ad` |
| `records/development/2026-08-14-recovery-plan-v5-stage3-test-authority-consistency-amendment-decision-v1.md` | `83efdd438abbb3a34df1ebafd24c7891f8ae3d265634c8ef54bd817951c2d21c` |

【実測】TODOの現役参照に記載された計画、開発方針、確認メモ、方針修正判断の更新後SHA-256は、
上表の実file再計算値と一致した。`todo_handoff`は終了コード0、`passed`だった。

【実測】初期チェックリストの開発方針参照は
`b3c7ce815705ba11915d3d384ee5d7fa2b8175503a03c9ff2417e79c83aeb5dc`で実fileと一致した。
`authority_reference_checker`は終了コード0、8件中8件一致、欠落・不一致・不正形式0件だった。

| 目的 | command | 終了コード | 結果 |
| --- | --- | ---: | --- |
| commit境界と変更path | `git show --format='%H%n%P' --name-status 7b9df68` | 0 | 親は`9002ca7`、六pathだけ |
| 候補条件 | 五文書を`rg`で限定検索 | 0 | 五文書すべてに集合外参照の条件あり |
| 差分形式 | `git diff --check 7b9df68^ 7b9df68` | 0 | 問題なし |
| TODO検証 | `.venv/bin/python3 -B -m tools.development.todo_handoff TODO_NEXT_SESSION.md` | 0 | `passed` |
| 初期チェックリスト参照 | `.venv/bin/python3 -B -m tools.development.authority_reference_checker docs/development/2026-08-03-initial-development-checklist.md` | 0 | 8件一致、不一致0件 |

## 6. 未実施

【未実施】先行レビューで合格した他の事項は再確認していない。全試験の収集・実行、関連試験27件の
再実行、変異検査、矛盾候補抽出、試験の意味確認、コード・試験・設定・Issue・過去記録の変更、
第3段完了判断、外部送信、push、tag、amend、rebase、reset、履歴書換えは行っていない。
