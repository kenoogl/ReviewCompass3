---
evidence_id: RC3-WORK1A-LAYOUT-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1A
work_name: Layout Baseline
status: verified
workflow_state: completed
confidentiality_class: project-internal
---

# Work 1A Layout Baseline Evidence

## 1. 結果

9 logical root、解決優先順位、Git管理境界、Project Manifest／Binding、stable／development分離、
cross-write禁止、managed path migration規則をLayout Baseline Recordへ固定した。空配置fixtureを別pathへ
移動してもproject identity、Manifest Digest、相対document linkが維持され、Bindingだけがcheckout固有の
repository rootへ変わることを確認した。

Work 1Aは`verified / completed`である。次の一作業はWork 1B「Session Log Bootstrapと現在位置text表示」
であり、本bootstrap Layoutを製品deployment完成と扱わない。

## 2. 固定sourceとartifact

| role | identity／path | SHA-256／tree |
|---|---|---|
| Work 1固定入力 | commit `ee60e3b4baf74c60da949a9d04d793fb83a61e69` | corrective snapshot verified |
| Work 1 Evidence | `records/development/2026-08-03-work-1-fixed-input-evidence-v2.md` | `7997b203935a9e53c56ed2556b4598773cd9d7b13c43079fcf8524b5e06bc9be` |
| Layout implementation commit | `d3add9f2e6bc812bf512a36a24877e29879e9842` | tree `a4aa91ac19b8d323191a7c85e0ff4198d7e11b94` |
| Layout Baseline Record | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |
| bootstrap validator／resolver | `tools/layout/baseline.py` | `3566bf40ff5e4da7ce1e2b832c92a615b38feed5cf08ff1f4e997ca17c2273e6` |
| Acceptance Test | `tests/test_layout_baseline.py` | `3c3d8b0492915724b8bcaed119d8a4557bd7ba91259220c7b02e475d373d5bf5` |
| fixture Project Manifest | `tests/fixtures/layout/empty-project/.reviewcompass/project-manifest.json` | `fc1a249abdc8e1886767d9140371251523218bebd66a2225ec0a8d458c6163ca` |
| fixture document link target | `tests/fixtures/layout/empty-project/docs/layout-entry.md` | `e314b3654805b2100fa273bf6f8d4357c75d94ae2b9f6f11e36505c96fda186f` |
| fixture Git tree inventory | `tests/fixtures/layout/empty-project` | `640a34e307bcac447309e9d2adf7174aefae9345b5de5aca340215ec40386f43` |

## 3. test-first Evidence

### 最初のred

- command：`python3 -m pytest -q tests/test_layout_baseline.py`
- result：`7 failed in 0.07s`
- failure oracle：全7件が`ModuleNotFoundError: No module named 'tools.layout'`で失敗した。
- 判断：期待するLayout moduleとBaseline Recordが未実装であることによる正しいred。

### Binding境界の追加red

- command：`python3 -m pytest -q tests/test_layout_baseline.py`
- result：`1 failed, 6 passed in 0.05s`
- failure oracle：relative `repository_root`を、絶対path違反でなく一般的なroot mismatchとして拒否した。
- 判断：Project Bindingの絶対path契約を明示検査する負例として正しいred。

### greenと回帰

- targeted：`python3 -m pytest -q tests/test_layout_baseline.py`、`7 passed in 0.03s`
- full：`python3 -m pytest -q`、`419 passed in 1.70s`
- syntax：cache書込みを行わない`compile()`で`tools/layout/baseline.py`を検査し、`compile_ok`。
- JSON：Baseline Recordとfixture Project Manifestを`python3 -m json.tool`で検査し、通過。
- diff：`git diff --check`、通過。

通常の`python3 -m py_compile`はsourceでなくmacOS標準Pythonのsandbox外cache作成で
`PermissionError`になった。source構文は上記`compile()`と全Test importで独立に確認したため、Layout不合格には
使用しない。

## 4. logical rootと解決規則

Baseline Recordは次を全件定義する。

| logical root | 主用途 | Git管理 |
|---|---|---|
| `CODE_ROOT` | installed code、検証済みCapability Adapter | project外 |
| `CONFIG_ROOT` | versioned user setting、integration config | project外 |
| `PROJECT_ROOT` | Manifest、Contract、Policy、Design Decision、verified artifact | Git管理 |
| `DATA_ROOT` | Provenance、Run、Context、Plan、Index、Discovery | project外 |
| `STATE_ROOT` | checkpoint、lock、scheduler state | project外 |
| `LOG_ROOT` | runtime／integration log | project外 |
| `CACHE_ROOT` | 再生成可能cache | project外 |
| `SENSITIVE_ROOT` | raw、生session、quarantine、未検査機微情報 | project外・分離access |
| `EVALUATION_ROOT` | Observation、Label、projection、Ledger | project外 |

解決優先順位は`explicit_cli`、`versioned_user_setting`、`allowlisted_environment`、`os_standard`である。
Runtime rootは解決後の絶対pathを必須とし、`PROJECT_ROOT`との包含、外部root同士の包含・同一を拒否する。
相対pathはproject artifactだけに許可し、`PROJECT_ROOT`基準で解決して`..`、絶対path、backslashによる
escapeを拒否する。

OS標準pathの具体値はcallerがplatform adapterから渡す。Work 1Aは特定OSの絶対pathをBaseline Recordへ
保存せず、解決順と検査規則だけを固定する。

## 5. Project ManifestとProject Binding

Project ManifestはGit管理下の`.reviewcompass/project-manifest.json`へ置き、次を持つ。

- `schema_version`
- 絶対path、checkout ID、内容Digestから生成しない安定`project_id`
- project-relativeな`artifact_roots`
- project-relativeな`document_links`

Project Bindingはproject外の`STATE_ROOT`へ置くruntime recordであり、`binding_id`、`project_id`、
`checkout_id`、絶対`repository_root`、`captured_at`、`project_manifest_digest`、`validation`を持つ。
Bindingの絶対pathをProject Manifestへ保存しない。

fixtureを`checkout-a`から`moved/checkout-b`へ移動したTestでは、次を確認した。

- `project_id`は不変。
- `project_manifest_digest`は不変。
- `binding_id`、`checkout_id`、`repository_root`だけがcheckout固有値へ変わる。
- `docs/layout-entry.md`は移動後の`PROJECT_ROOT`から再解決できる。
- Bindingの`project_id`またはManifest Digestが不一致なら拒否する。
- Bindingの`repository_root`が相対pathなら拒否する。

## 6. stable／developmentとcross-write

`stable`と`development`は`PROJECT_ROOT`以外の8 rootを分離する。共有可能な`PROJECT_ROOT`は
`stable`から既定read-only、`development`からread-writeとする。

validatorは次を拒否する。

- 二つのenvironment間で同一または包含関係にある外部root。
- stableからdevelopmentの`DATA_ROOT`等へのwrite。
- stableから共有`PROJECT_ROOT`へのwrite。
- 自environmentの管理対象外rootへのwrite。

`CODE_ROOT`と`CONFIG_ROOT`は通常runtime write対象に含めず、install／updateまたは明示config操作の別関門で
扱う。

## 7. Git境界、機密性、端末固有path

Git管理対象は`PROJECT_ROOT`だけである。project内にraw provider response、生session、secret、lock、
checkpoint、cache、未検査機微情報、端末固有絶対pathを置かない。

fixture全managed fileをJSON構造とtext tokenの両方でscanした結果は
`managed_absolute_path_findings=0`である。Project Bindingが持つcheckout絶対pathはproject外stateであり、
fixtureへ書き戻していない。

## 8. migration規則

Baseline後のmanaged path変更は通常編集で行わない。新しいmigrationは次を全件持つ。

- `from_version`、`to_version`
- `affected_roots`、`impact_closure`
- `link_check`、`data_migration`
- `dry_run`、`rollback`

version非増加、未知root、link検査不合格、dry-run不合格、rollback欠落を拒否する。実migrationはまだ行って
おらず、現在は規則とnegative Testだけを固定した。

## 9. stale、残余risk、後続owner

次の変更で本Evidenceをstaleにする。

- Layout Baseline Record、validator、Project Manifest／Binding schema、root allowlistの変更。
- root解決優先順位、Git境界、stable／development共有規則の変更。
- fixture、移動・link・absolute path・migration oracleの変更。
- Work 1固定入力またはauthorityの変更。

残余riskは次のとおり。

- bootstrap validatorは正式製品Runtimeではなく、Work 1A固定規則の実行可能なoracleである。
- platform別OS標準pathの具体解決、Bindingのdurable保存、permission実測は後続のSession Log Bootstrapと
  deployment E2Eで扱う。
- 既存Session Logの限定的portable configを本turnで書き換えていない。Work 1BでBaselineとの接続を
  test-firstで行う。

これらはWork 1A完了を妨げず、後続Workのownerと開始点が明示されている。

## 10. 完了関門

| 関門 | 判定 | Evidence |
|---|---|---|
| 9 rootの意味と解決規則 | pass | Baseline Record、root resolution Test |
| Git／project外／機密／cache境界 | pass | Baseline Record、absolute path scan |
| Project Manifest／Binding最小構造 | pass | fixture、move／identity negative Test |
| stable／development分離とcross-write禁止 | pass | isolation／write target Test |
| 別checkout／project移動後の相対参照 | pass | empty-project move Test |
| 端末固有絶対pathの非混入 | pass | `managed_absolute_path_findings=0` |
| migration規則 | pass | required-field／rollback negative Test |
| Layout Baseline Recordと空配置Testの固定 | pass | commit `d3add9f` |
| project移動、link、Manifest／Binding照合 | pass | targeted `7 passed`、full `419 passed` |

Work 1A scopeにblocking conflict、blocker、Human判断待ちはない。
