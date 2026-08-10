# Human裁定：範囲固定前の5手順を恒久規約とする

- 裁定日：2026-08-10
- 裁定者：Human（kenoogl）
- 裁定文言（原文）：「恒久的な規約にする。あとでリマインドするように。」
- 経緯：Humanの問い「中々収束しない。漏れが多くないか？　原因は何？」に対する
  Pilotの原因分析（同日）で提案した5手順を、恒久規約とすることが確定した。

## 1. 確定した規約（範囲固定前の事前走査）

`role_neutral_pilot_review` modeで範囲固定を書く**前**に、次の5つを機械実行し、
結果を範囲固定の一節として記録する。

1. **欠陥の所在をcodeで特定する**。上流Finding記載のmodule名を信じず、
   実際に該当処理があるfileを読んで確かめる。
2. **対象fileをimportするtestを列挙する**。
3. **対象fileの現在のSHA-256で全文検索**し、Digestを固定している
   record・testを列挙する。
4. **実運用への接続点を列挙する**（hook登録・入口module・CLI・conftest等）。
   「機能を作る」と「実際に効かせる」が別fileに分かれている場合を落とさない。
5. **受入条件と変更可能pathを同じ一覧から書く**。同じ集合を2か所に別々に書かない。

## 2. 規約化の根拠（実測）

- `tools/`配下の先頭40 moduleを調べたところ、**32件**の現在Digestが
  repository内の別fileに書かれていた。
- 実行時にDigestを再計算して照合するtestが**16 file**存在する。
- 2026-08-10の守り役後追い修正4単位で、範囲の作り直し**8回**、
  実装中の停止**4回**が発生した。内訳の主因は
  (a) Finding記載module名の誤信、(b) Digest固定の網の未調査、
  (c) 実運用接続点の欠落、(d) 同じ集合の二重記載、
  (e) 反証testの失敗理由の未確認。

## 3. 適用と反映

- **即時適用**：守り役後追い修正 group Cの範囲固定v4から適用する。
- **文書への反映は別単位**：`docs/development/role-neutral-pilot-review-collaboration.md`
  （または`work-review-protocol.md`）へ必須節として入れる改定は、
  進行中の作業単位を閉じてから別単位で行う。Humanの指示
  「あとでリマインドするように」に従い、Pilotは次の機会に本件を想起させる。

## 4. リマインドの仕込み先

1. 本record（repository内の正本）。
2. Pilotの永続memory（session跨ぎ）。
3. TODO_NEXT_SESSION.mdへの反映（Closerが次の完了処理で行う）。

## 5. 本裁定が決めていないこと

- 5手順を`work-review-protocol.md`と`role-neutral-pilot-review-collaboration.md`の
  どちらへ置くか。
- 事前走査を人手commandで行うか、toolとして実装するか。
- low riskの単位にも同じ手順を課すか（現時点では課す前提で運用し、
  改定時にHumanが確定する）。
