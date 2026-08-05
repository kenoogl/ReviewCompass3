---
candidate_id: IC-SHELL-PATH-VARIABLE-DIGEST-CHECK-001
observed_at: 2026-08-05
origin_stage: initial-development
origin_work: Work 5A Definition Challenge TDD preflight
origin_commit: cfcb334
candidate_kind: improvement_candidate
classification: process改善
priority: P2
status: routed
blocking: false
suggested_route: existing_issue
related_issue: ISSUE-HTC-C9F6C917
confidentiality_class: project-internal
---

# zshの`path`特殊変数をDigest検査shell loopで上書きした

## 1. 対象操作

Work 5A Definition Challengeのblocking改善候補が参照す5 fileのSHA-256を、固定値と
照合する読取り専用検査である。

## 2. 期待executorと実executor

| 項目 | 値 |
| --- | --- |
| 期待executor | 固定pathと期待Digestを構造化入力で受け、一致／不一致を返す専用検査器 |
| 実executor | LLMが都度組み立てたzshの`for` loopと`shasum -a 256` |
| 手作業の理由 | 本作業で使える専用のDigest参照検査器を特定せず、複数pathの一括処理をshellで組み立てた |

## 3. 手戻り事象とEvidence

loop変数に`path`を使った。zshの`path`は`PATH`と結び付いた特殊配列であるため、
一件目の代入でcommand探索pathが置き換わり、各5回の`shasum`が次で失敗した。

```text
zsh:1: command not found: shasum
```

検査対象fileは変更されていない。loopを使わず、5 pathを`shasum -a 256`へ明示列挙して
再実行し、次の期待Digestと一致した。

- Approval Decision：`9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d`
- Definition Challenge設計：`4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f`
- `tools/task_contract/contract.py`：`be7ec9d314492c529ae0fa962458e35777d400586f8ca461dd5ccbe2c88c74cd`
- `REQ-CONTRACT-004`：`5b0835fd9fb50eee64952575f3a98d9f1d2f43e4f9f82037c5a7abdc66985ebf`
- Development Policy：`0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`

## 4. 影響と停止判定

- 影響はread-onlyのDigest検査が1回失敗し、明示path列挙で再実行が必要になったことだけである。
- file書込み、Digest不一致、Test結果の変化、Acceptanceへの影響はない。
- 現行Workの追加停止条件には該当しない。

## 5. 機械処理候補とroute

固定pathと期待SHA-256の組を構造化入力とし、shell変数やloopに依存せず一括照合する
専用validatorを機械処理候補とする。新Issueは作らず、「LLMが機械操作の実行手順を都度組み立てる」
根本原因を追跡する既存Issue `ISSUE-HTC-C9F6C917`へrouteする。

本候補は専用validatorへconsumer接続されていないためclosedにしない。
