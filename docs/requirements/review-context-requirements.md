---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
---

# Review Task入力構成 requirements

対象機能：`FEAT-REVIEW-CONTEXT`

## REQ-CONTEXT-001 Review Task定義

Review Taskを開始する前に、利用者はGoal、Target、Constraints、
Expected Output、Context Requirements、Validation PolicyおよびProvenanceを
確認できなければならない。

- 入力
  - Review Taskの目的と判定基準
  - 一意に識別されたTarget
  - 実行上の制約と期待出力
  - 必要なContext材料の種別
- 出力
  - 版付きのReview Task入力定義
- 停止条件
  - 必須項目が欠けるか未解決である
  - Targetが一意に定まらない
- 復旧条件
  - 不足項目を補い、新しい版として再検証する
  - Targetを訂正し、参照先を再検証する
- 失敗時に保存するもの
  - 拒否された入力候補と項目別の診断
- 受け入れ条件
  - 必須項目を1つ欠く入力はContext生成前に拒否される
  - 同一入力から同一のTask入力Digestが得られる
- 対象外
  - Task内部の実行経路をこの定義へ固定すること
  - LLMへ必須項目の採否を暗黙に委ねること

## REQ-CONTEXT-002 材料束の実体化

システムはTargetとsource materialsを、役割、内容、出所およびDigestを持つ
一つの材料束として実体化しなければならない。

- 入力
  - Targetとsource materialの参照
  - 各材料の本文、役割および出所
- 出力
  - Targetを含むExecution Context材料束
- 停止条件
  - 本文または出所が欠ける
  - 宣言したDigestと本文が一致しない
  - 参照先が存在しない
- 復旧条件
  - 正しい出所から材料を再取得し、新しい材料束を作る
- 失敗時に保存するもの
  - 拒否された材料束、宣言値、実測値および診断
- 受け入れ条件
  - Targetを含み、すべてのentryに本文と出所がある
  - 任意の本文変更をDigest不一致として検出する
- 対象外
  - Promptの文章表現を固定すること
  - Digestだけで材料内容の真実性を保証すること

## REQ-CONTEXT-003 Scope contract

システムはレビュー母集合、対象範囲、除外条件および分類結果をScope contractとして
固定し、対象漏れと判断競合を検出しなければならない。

- 入力
  - 固定した候補母集合
  - include、exclude、deferの判定基準
  - Review TaskのTarget
- 出力
  - 全候補の分類を含む版付きScope contract
- 停止条件
  - unknownまたは未分類が残る
  - 同じ候補に競合する分類がある
  - 分類中に母集合が変わる
- 復旧条件
  - 未分類または競合を解消し、新しいScope版を作る
  - 変更後の母集合を再固定して全件を再検査する
- 失敗時に保存するもの
  - 全分類判断、競合、未分類および母集合の変更記録
- 受け入れ条件
  - 全候補が重複なく許可された分類のいずれかに入る
  - 独立検査が同じ材料Digestから全件を再判定できる
- 対象外
  - 常にプロジェクト全体をレビュー対象にすること
  - LLMの非公開推論だけで対象範囲を確定すること

## REQ-CONTEXT-004 Context identityとstale検出

システムはExecution Contextの内容をDigestで固定し、入力変更後に旧結果を
再利用せずstaleとして停止しなければならない。

- 入力
  - 固定済みExecution Context材料束
  - Scope contract
  - 各入力の取得状態とDigest
- 出力
  - Execution Context identityとfreshness検査結果
- 停止条件
  - 入力Digestが固定値と一致しない
  - Context確定後に参照元が変わる
- 復旧条件
  - 変更後の材料から新しいContext identityを作る
  - 旧結果を残したまま新しいReview Runを開始する
- 失敗時に保存するもの
  - 旧identity、実測Digest、不一致箇所および検出時刻
- 受け入れ条件
  - 同じ正規化入力から同じidentityが得られる
  - 1つの入力変更で旧結果の再利用が拒否される
- 対象外
  - Digestで意味的正しさを保証すること
  - staleな履歴を新しい結果で上書きすること

## REQ-CONTEXT-005 Context Composition

システムは呼び出し側が指定した材料と採用目的を明示的に構成し、暗黙の資料を
Execution Contextへ追加してはならない。

- 入力
  - 呼び出し側が指定した採用材料
  - 材料の採用目的
  - 任意の候補材料と候補生成条件
- 出力
  - 材料の採否と根拠を含むComposition記録
  - 検証済みExecution Context
- 停止条件
  - 採用材料の出所または採用主体を追跡できない
  - 候補の採否が未解決である
- 復旧条件
  - 呼び出し側または利用者が採用材料を訂正する
  - 訂正後の材料から新しいComposition記録を作る
- 失敗時に保存するもの
  - 候補一覧、採否、判断主体、目的および未解決事項
- 受け入れ条件
  - 全採用材料を明示指定または決定的な採用規則へたどれる
  - 指定されていない材料をLLMが暗黙に追加できない
- 対象外
  - Context候補探索から採用までを完全自律化すること
  - 会話履歴全体を既定のContextとして扱うこと

## REQ-CONTEXT-006 再開引継ぎ

システムは確認済み成果、未解決事項、変更方針および再開地点をDigest付きの
handoff packageへ固定し、失敗後も確認済み成果を壊さず再開できなければならない。

- 入力
  - 確認済み成果とそのDigest
  - 未解決事項と変更方針
  - 再開対象のReview TaskとContext identity
- 出力
  - 照合可能なhandoff package
- 停止条件
  - 確認済み成果のDigestが欠けるか一致しない
  - 再開対象または変更方針が一意に定まらない
- 復旧条件
  - 保存済みの確認済み成果からpackageを再構成する
  - 入力変更時は新しいReview Runとして再開する
- 失敗時に保存するもの
  - 既存の確認済み成果、失敗履歴および不一致診断
- 受け入れ条件
  - 再開操作が確認済み成果の内容とDigestを変更しない
  - 同一入力だけを再利用し、変更入力では新しいRunを作る
- 対象外
  - staleな成果から処理を継続すること
  - 再開のために失敗履歴を削除すること
