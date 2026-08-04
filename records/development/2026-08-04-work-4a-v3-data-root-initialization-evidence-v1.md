# Work 4A v3 DATA_ROOT Initialization Evidence v1

## 承認

2026-08-04の会話でHumanが、提示したwork4a配下directoryの作成だけを承認した。
提示内容は、解決した実行時root、作成予定の絶対path、初期file無し、作成理由である。

提示時は`observations`と`candidates`の2件として説明したが、実際の作成物は親directory `work4a`を含む
3 directoryである。本記録は事実に合わせて3 directoryとする。

## 解決した実行時root

| 段階 | 結果 |
| --- | --- |
| explicit CLI | 指定なし |
| versioned user setting | `config/`に実行時rootの設定なし |
| allowlisted environment（`REVIEWCOMPASS3_RUNTIME_ROOT`） | 未設定 |
| home default | 採用。`~/.reviewcompass3` |

- runtime root：`/Users/keno/.reviewcompass3`
- project ID：`reviewcompass3`（Project Manifestの固定ID）
- profile：`development`
- root kind：`data`
- data root：`/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data`

Layout v3の`resolve_project_runtime_layout`と、v3実装の`resolve_data_root`が同一pathを返すことを
機械確認した。v3のroot語彙と解決規則がLayout v3へ従属していることの実地確認になる。

## 作成したもの

外部`DATA_ROOT`に3 directoryを作成した。

| 絶対path | 種別 | 作成前 | 作成後 |
| --- | --- | --- | --- |
| `.../development/data/work4a/` | directory | 無 | 有（`drwxr-xr-x`）。子はobservationsとcandidatesの2件のみ |
| `.../development/data/work4a/observations/` | directory | 無 | 有。空 |
| `.../development/data/work4a/candidates/` | directory | 無 | 有。空 |

初期fileは作成していない。`observations`と`candidates`はいずれも空である。
上位の`~/.reviewcompass3`と`.../development/data`は既存であり、新規作成していない。

## 触れなかったもの

`.../development/data`配下の既存3 directoryは、旧Work 4A（v1）の観測である。
削除、移動、書換えのいずれも行っていない。v3は`work4a/`配下だけを使うため混在しない。

- `routine-classification-candidates/`（5件）
- `source-snapshots/`（7件）
- `source-symbol-indexes/`（7件）

これらはv3のfreshness根拠にも正本にも使わない。

## project内への書込み

project内へ書いたのは、本初期化証跡`records/development/2026-08-04-work-4a-v3-data-root-initialization-evidence-v1.md`
の1 fileだけである。

実観測（Source Observation）と候補（Candidate Run）のdataはproject内へ書いていない。
これらは外部`DATA_ROOT`にだけ置く設計であり、この時点ではまだ生成もしていない。
Attestation、Decision、Entry、Relation、Baselineも作成していない。

stable profileの領域には触れていない。

## 現在の停止点

実sourceの観測、Candidate Runの生成、候補routineの選定、Human dispositionは実施していない。
次の作業単位はこれらであり、個別のHuman承認を待つ。
