# 構成C 検索recordの外部化 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001` §4
- RED Evidence：`records/development/2026-08-07-work4b-c-externalization-red-evidence-v1.md`

## 1. 実装

`tools/development/reuse_search_record.py`を変更した（実装前検索gate通過済み）。

- `externalize_reuse_search_record`：record本体を外部DATA_ROOT `work4b/reuse-searches/
  <content digest>.json`へ、証明書（`reuse_search_attestation`：外部相対path・content digest・
  **byte SHA-256**・source identity・hit件数）をproject内へ、いずれもnew-onlyで書く
- `gate_check_attested`：証明書経由で外部recordを解決し、byte一致→content digest一致→
  結線・鮮度の共通判定（`_gate_verdict`として既存gateと共通化）まで確認する。欠落・改竄は
  fail-closedで`record_unavailable`
- `migrate_reuse_search_record`：既存recordのbyte一致移行（旧位置は削除せず保持）

- targeted：外部化4件＋鮮度4件＋R系8件 `16 passed`、exit `0`。固定testは変更していない。
- 公式全Test：`1084 passed`、exit `0`。

## 2. 実移行（7件、全件byte一致）

既存の検索record 7件（累計約2.3MB）を外部DATA_ROOTへbyte一致で移行し、各recordの証明書
（`*-reuse-search-attestation-v1.json`）をproject内へ作成した。**旧位置の7件は削除せず保持**
（削除は旧書庫と同様に別途Human判断）。

証明書gateの判定結果【実測】：

- 5件：`start_allowed: true`（schema 1は`not_assessed`表示、台帳検索は`assessed_fresh`）
- 2件（順位表・外部化自身の検索record）：`profile_stale`——検索後に`reuse_search_record.py`が
  変更され、または対象fileが観測後に新設されたことを判定時点で再計測した**正しい**結果。
  これらのgateは各実装の開始時に役目を果たし済みであり、事後判定の古さ表示は鮮度gateの
  時点意味論（判定はいつでも現在に対して行う）どおりである。

## 3. これで設計束4構成が完了

A-1（除外宣言）→B（鮮度gate）→A-2（順位表）→D（台帳・既存経路再利用）→C（外部化）。
以後の新しい検索recordは外部化＋証明書で保存でき、repository側は小さな証明書だけが増える。

## 4. 残余と限界

- 既存7件の旧位置recordの削除はHuman判断待ち（削除すればrepositoryが約2.3MB軽くなる）
- universe record v2の作成が次の小作業単位（`DEC-UNIVERSE-RECORD-V2-TIMING-001`）
- 本変更も守り役codeの変更であり、反証レビュー対象（backlog Issue）に含まれる
