# Pilot起動・record正本方式の受け渡し（codex CLI橋渡し）

状態：運用メモ（試行）

関連：`docs/development/role-neutral-pilot-review-collaboration.md`（役割中立mode）、
`docs/development/work-review-protocol.md`（共通レビュー基準）

## 1. 背景とHuman決定

従来、ClaudeとCodexの受け渡しはHumanのchat貼り付けで行っていた。役割中立mode初回試行の
実測（`records/development/2026-08-09-role-neutral-mode-trial-metrics-v1.md`）では受け渡し
13回のうち判断を要したのは6回だけで、残りは運搬だった。さらに運搬起因の事故
（判定の中身が届かない、修正前の古いレビュー結果の再送）が実際に発生した。

2026-08-09、Humanは「人が2エージェント間の仲介をすること自体に無理がある。Humanとの
接点はPilot側のみにすべき」と決定し、codex CLI（terminalでCodexを動かす入口）を導入した。

## 2. 方式の原則

1. **内容の正本はcommitted recordだけ**である。chatの文章、CLIの起動prompt、agentの
   応答文は通知・トリガーにすぎず、判定・Claim・承認対象の正本にしない。
2. **起動はPilotが行う**。Pilotは`codex exec`でReviewer（Codex）を起動する。Humanは
   agent間の運搬を行わない。
3. **起動promptは固定形式**とする。役割の宣言、対象（commit・record path）、作成すべき
   record path、単独commitと停止の指示だけを含み、判定に影響する評価・誘導を書かない。
   Reviewerの入力はrepository上のrecordであり、Pilotの文章ではない。
4. **sandboxを用途で固定する**。読み取り確認は`--sandbox read-only`、record commitを
   伴うレビューは`--sandbox workspace-write`。それ以外の権限を使わない。
5. **起動された側の義務（鮮度検査）**：自分宛の最新recordをGit履歴から機械特定し、
   判定対象commitがそのrecordの前提と一致することを確認してから動く。古い・宛先違い・
   前提不一致なら、作業せずその旨のrecordで停止する。
6. **Pilotの義務（事後照合）**：応答を鵜呑みにせず、(a) 新recordのcommitが判定対象
   commitより後にあること、(b) 変更パスがそのrecord 1件だけであること、(c) recordの
   判定内容、を機械照合してから次へ進む。
7. **Humanに残るもの**：作業項目の指定、risk確定、再開・段完了の承認、意味的裁定の
   文言だけである。これらは従来どおりHumanのchat文言を正とし、範囲固定文書・
   レビュー依頼recordへ転記して固定する。
8. **失敗時のfallback**：CLIが不通・認証切れ・異常応答の場合、Pilotは状況をHumanへ
   報告して停止する。従来のHuman中継（`codex-claude-collaboration.md`）は廃止ではなく
   fallbackとして残る。

## 3. 起動promptのひな型

レビュー起動（record commitあり）：

```text
codex exec --sandbox workspace-write "あなたはReviewerです。
docs/development/work-review-protocol.mdのレビュー手順に従い、次のレビューを実施してください。
対象：<commit SHAまたはrecord path>
先行レビュー：<record path（あれば）>
判定recordを <record path> へ作成し、そのrecordだけを単独commitして停止してください。
record以外のファイルは変更しないでください。"
```

読み取り確認（変更なし）：

```text
codex exec --sandbox read-only "<読み取りだけで答えられる確認内容>"
```

## 4. 試運転第1号の実測（2026-08-09）

- 疎通確認：`--sandbox read-only`でHEAD SHAを正答（約9千token）
- レビュー起動：比例原則修正`886740d`の再々レビューを起動（約7.2万token）
- Codexの出力：判定record v3を作成し単独commit（`99e6285`、record 1件のみ、
  `git diff --check`合格）、判定`verified`・Finding 0
- Pilotの事後照合：鮮度（`886740d`より後）、変更パス、判定を機械確認して合格
- **Humanのchat運搬：0回**

## 5. 未決事項

- `role-neutral-pilot-review-collaboration.md` §1の「ClaudeとCodexは直接通信せず、
  Humanがpathと再開指示を受け渡す」の条項改定（本方式を正、Human中継をfallbackとする）。
  この改定は独立の文書変更作業とし、本方式で起動するCodexレビューを受ける。
- `codex-claude-collaboration.md`（従来方式）へのfallback位置づけの追記。
- token消費の記録方法（試行計測の項目へ追加するか）。
- Reviewer側からPilot（Claude）を起動する逆方向の橋渡しは未検討・未実装。
