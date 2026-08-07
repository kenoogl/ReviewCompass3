# 反証I-4 処置 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-ADVERSARIAL-REMEDY-I4-001`
- 対応表：`records/development/2026-08-07-adversarial-remedy-i4-declaration-red-map-v1.json`
  （宣言N1〜N3、恒久検査器で`passed`）

## 1. 塞いだ穴

V4 Issue recordの`problem`本文が、引用元の改善候補の本文と一致しない場合、検証器が拒否する。
候補側の改竄は既存の指紋照合が拒否していたが（反証I-3は`held`）、**Issue側だけを別内容へ
差し替える経路**は塞がれていなかった（反証I-4）。

- targeted：`tests/test_adversarial_remedy_i4.py` 3 test。N2・N3はRED→GREEN、N1は境界例として
  実装前から成功（本文一致検査が既存の健全recordを壊さないことの固定）。
- 公式全Test：`1096 passed`、exit `0`。

## 2. 実装中に判明した設計上の区別（記録）

最初の実装は形式を問わず本文一致を要求したため、**bundle形式のIssue 3件が失敗した**。原因は
実装の欠陥ではなく形式の設計差である。

- **単体形式（N1形式）**：`build_v4_issue_record`が候補の`problem`をそのまま写すため、
  本文は一致するのが正しい。
- **bundle形式**：候補の`quotation`はTODOから機械抽出した**原文の引用**であり、Issueの
  `problem`はHumanが仕分け時に一般化して記述した**問題文**である。両者が異なるのが設計である。

したがって本文一致検査は単体形式に限定した。**bundle形式のIssue本文の差し替えは塞げない**
という限界を、`tools/development/issue_intake_v4.py`のcommentと本Evidenceへ記録する。
bundle形式のIssueは3件（`ISSUE-HTC-*`）で、いずれも`registered`のまま着手されていない。

## 3. stale閉包（検証器変更に伴う再検査）

現存するV4 Issue record 7件を新しい検証器で全件再検査した【実測】：**7件すべて合格**
（単体4件・bundle 3件）。repository全体の検証（同一candidateへの有効Issue重複の拒否を含む）も
合格し、有効Issueは7件である。

## 4. 残余

- bundle形式のIssue本文の差し替え（上記§2の限界）。
- B群・C群の11件は設計提案待ち（`DEC-ADVERSARIAL-REMEDY-I4-001` §1）。次の作業単位で提案を作る。
