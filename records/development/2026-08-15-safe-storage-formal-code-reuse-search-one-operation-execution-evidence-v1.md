# 安全保存 正式コード再利用検索 一操作実行Evidence v1

- 実施日：2026-08-15
- Work ID：`WORK-SAFE-STORAGE-FORMAL-CODE-REUSE-SEARCH-ONE-OPERATION-2026-08-15-V1`
- 実行入口：`python3 -m tools.development.formal_code_reuse_search`
- 判定：`completed / freshness_verified / human_adjudication_required`

## 1. 機能と用途

【実測】正式コード再利用検索の一操作入口を、変更なしのローカルcommit
`0a02b519da9c0ac7672b4f61a237dfbadf4c9ad8`へ一回だけ適用した。この開発支援機能は、現在のGit管理コードを
機械列挙し、処理一覧と比較候補を一度作ったうえで、同じ状態から複数の再利用検索と証明書を生成する。

【判断】用途は、安全保存機能を新規実装する前に、正式なSession処理と保留中のG26処理に再利用できる既存処理が
ないかを、更新漏れのある固定一覧ではなく現在commitから調べることである。検索結果は候補であり、正式・暫定・
使用停止の区分や、どの処理を再利用するかはHuman裁定を要する。

## 2. 入力と一回の実行

【実測】次の作業別計画を入力にした。

- plan ID：`FCRS-SAFE-STORAGE-2026-08-15-V1`
- plan SHA-256：`cdecd40cfecf4c945dcf55f0a48de97170caf7858093adb80cb73e04cd796bd5`
- plan内容識別値：`f2762eb20161e23174ad52ce245b840edfb92e619d55dc7a5e66ecc559657261`
- source universe v6内容識別値：`a87816987937eceebaddfbe786dd568b4db8c661584399247ccdeb97963f3230`
- freshness policy v9内容識別値：`0f1c5eb3c85bccf9fc3107fadbdf788c3e3072df14f530d7a2e39c80579e5c52`

【実測】入口は終了コード0、`status: completed`を返した。remote照合、push、network、外部送信、自動commitは
行っていない。外部runtime領域へ観測・処理一覧・比較候補・検索正本を生成し、project内へnew-onlyの証明書二件を
生成した。

## 3. 同じcommitへの結び付き

【実測】二検索は次の同一identityへ結び付いた。

- source file数：152
- source content ID：`c2369093133cea3651b310c4c6f6ebd83fa8eacb906c33036ee2db5e08727b09`
- observation snapshot ID：`5a4e398c8f53ec90cb051f95f5d661c9ccc3c4fc0d3bb8d6071a77b5383302ea`
- routine profile run ID：`dc273a5597bafcc0177ffb6b59dc9ad132d0989984d1af33a6bf479229690b33`
- routine数：1,594
- comparison discovery run ID：`6a53df24a2a5c8fc450acc28bfda0eef1551870a3af23229c3c509a61b5f7842`
- comparison group数：1,042

## 4. 二つの検索結果

### 4.1 正式Session処理11 path

- subject：`safe_storage_formal_code_reuse_candidates_v2`
- hit数：675
- group数：262
- 検索内容識別値：`f3c256c7cf4e305aacc8735e2814f341d66348b977a23863db7b46cd5ea0b75e`
- 証明書：`records/development/2026-08-15-safe-storage-formal-code-reuse-search-attestation-v2.json`
- 証明書SHA-256：`709d72b7a79c1412e25208b7a405f6354059493240daa50e9552346ae5fc01bd`
- 鮮度判定：`start_allowed: true / reuse_search_record_verified`

### 4.2 保留G26処理九path

- subject：`safe_storage_provisional_g26_candidates_v2`
- hit数：1,994
- group数：450
- 検索内容識別値：`49d1413f8413f15e9ced34e6059e6eda1294bb6804698d3fd63cd869e7b5804b`
- 証明書：`records/development/2026-08-15-safe-storage-provisional-g26-reuse-search-attestation-v2.json`
- 証明書SHA-256：`05259d87ec6c2a4b93cda21775bfbbc34994df56c839e9c6c43f5f6ac5e298e8`
- 鮮度判定：`start_allowed: true / reuse_search_record_verified`

【判断】hit数は似た処理を広く抽出した候補数であり、再利用決定数ではない。入口は二検索について
`lifecycle_adjudication_required: true`と`reuse_disposition_adjudication_required: true`を返した。

## 5. 境界と未実施

【実測】製品コード、製品試験、製品設定、Task Contract、TDD実装境界は変更していない。検索元を手書きの中央一覧へ
追加しておらず、作業別計画は今回の検索範囲を示す履歴入力として保持する。

【未実施】候補の意味的採否、保留G26の正式化、正式処理の使用停止、再利用方法の裁定、安全保存のRED試験・製品実装、
push、外部送信は行っていない。次はコード管理機能とは別の作業単位として、TDD開始前の実装境界が小さいRED/GREENへ
分解できるかを確認する。
