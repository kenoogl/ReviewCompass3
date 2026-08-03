---
record_id: RC3-SOURCE-PREDECESSOR-DEPLOYMENT-PACKAGE-2026-08-04-V1
recorded_at: 2026-08-04T06:18:11+09:00
source_kind: predecessor-implementation-observation
normative_status: evidence-only
---

# 前身実装のデプロイパッケージ方式観測記録

## 1. 目的

ReviewCompassとReviewCompass2で実際に採用または計画された配布境界を固定し、ReviewCompass3で
デプロイ方式とProject Artifact配置を決める際のEvidenceにする。本記録は観測事実を保持するsourceであり、
ReviewCompass3のRequirement、Layout Baselineまたは設計判断を単独では変更しない。

## 2. 観測方法

- 対象repositoryのHEADを`git rev-parse HEAD`で取得した。
- 配布一覧、package builder、path解決、対象appの入口文書を再読込した。
- 各固定sourceのSHA-256を`shasum -a 256`で取得した。
- 生成済みpackageのfile数を`find <root> -type f | wc -l`で確認した。

## 3. ReviewCompassで観測した方式

### 3.1 固定source

| source | fixed identity | SHA-256 |
|---|---|---|
| ReviewCompass repository | commit `cab302d4b32af790628b811b3566f39d55781fa5` | - |
| `/Users/Daily/Development/ReviewCompass/deploy-manifest.yaml` | filesystem content | `0f39b39f6e967b4c14f50d830a8d9b53b1a18a5bcf5ad8481924f158a379325f` |
| `/Users/Daily/Development/ReviewCompass/tools/build-deploy-package.py` | filesystem content | `eb658519d2ca209331a575a3c1037da8ff1b380a4731c09ad4e7b4dc4ac9412b` |
| `/Users/Daily/Development/WindTurbineWake/LLMGP/.reviewcompass/AGENT_ENTRY.md` | filesystem content | `a0166de3ca51aa7fa3fe3ef7401a5079863c927ad93dd2eabe03a0d1a796f2e0` |

### 3.2 観測事実

- `deploy-manifest.yaml`は`source_policy.mode: allowlist`を宣言し、生成先を
  `build/deploy/ReviewCompass`としている。
- `build-deploy-package.py`はmanifestのincludeからfileを選択し、選択したfileだけを生成先へ
  `shutil.copy2`で複製する。
- 生成済み`/Users/Daily/Development/ReviewCompass/build/deploy/ReviewCompass`には観測時点で
  358 fileが存在した。
- 対象app側の`AGENT_ENTRY.md`は、対象app rootと配布物directoryを区別し、配布物として
  `/Users/Daily/Development/WindTurbineWake/ReviewCompass`を参照している。
- 同じ対象app workspace内の配布物copyには観測時点で360 fileが存在した。

### 3.3 観測から直接言えること

ReviewCompassは開発repositoryを対象appから直接参照する方式だけに依存せず、allowlist manifestから
独立packageを生成し、対象appがcopyされた配布物を参照できる構造を持っていた。

## 4. ReviewCompass2で観測した方式

### 4.1 固定source

| source | fixed identity | SHA-256 |
|---|---|---|
| ReviewCompass2 repository | commit `d6bbb01500002872c713412bfbd63b702a291c99` | - |
| `/Users/Daily/Development/ReviewCompass2/deploy-manifest.yaml` | filesystem content | `88daeff76716e2153ae9345f61f0e739abf9f228733670af6b4b082838c80ce1` |
| `/Users/Daily/Development/ReviewCompass2/tools/paths.py` | filesystem content | `24abb990be50f35f2895dabee355a99c7a0721c7ba9a08233e0c1f97c10aa337` |
| `/Users/Daily/Development/ReviewCompass2/.reviewcompass/backlog/issues/issue-2026-07-26-distribution-package.yaml` | filesystem content | `f43739f1845388381111eb7fd2dde292575c1014c48be53451aaf2d28af0c17b` |
| `/Users/Daily/Development/ReviewCompass2/docs/plan/2026-07-23-plan-c-rebuild-minimal-base.md` | filesystem content | `75915b28557b4e83b74e18670b1b80a5f1274cd391faa1ab0974419cb4b97e6b` |

### 4.2 観測事実

- `deploy-manifest.yaml`は`tools/`、`schemas/`、`templates/`、設定既定値、規律を配布対象とし、
  `.reviewcompass/`と`.claude/`をapp側、docs、tests、TODO等を非配布として分類している。
- `tools/paths.py`は実行中の`tools/`の親をrepositoryまたは配布先rootとして扱い、同じroot直下の
  `.reviewcompass/`をapp側区画として解決する。
- distribution package Issueは、配布一覧はあるが一覧からpackageを組み立てる手段が未実装であると
  記録している。
- Planは配布物とapp側の配置規約を初日に固定し、package生成tool自体は後続とする方針を記録している。

### 4.3 観測から直接言えること

ReviewCompass2は配布境界をmanifestで分類していたが、観測した固定sourceの範囲では独立package生成工程は
未実装だった。自己適用時には、実行中tool rootとapp側`.reviewcompass/`が同じworkspace rootを共有できる
path解決になっていた。

「開発repository全体をそのままcopyすること」が正式な配布方式だったとは確認できない。むしろmanifestは
docs、tests、TODO等を非配布としている。

## 5. ReviewCompass3へ渡す観測上の示唆

以下は観測を基にした設計上の示唆であり、本source record自体のDecisionではない。

- 配布対象のallowlistとpackage生成を一体にしたReviewCompass方式は、開発sourceと安定配布物を分離しやすい。
- ReviewCompass2の「配置境界を先に決める」方針は維持する価値がある。
- package生成を後回しにして開発rootを実質的な配布rootとして使い続けると、stableとdevelopmentの
  分離を実証しにくい。
- app側のIssue、Plan、Decision、Evidenceを配布packageへ含めなければ、package更新時のProject Artifact
  移動を避けられる。

## 6. 限界

- 観測は記載したcommitとfilesystem contentに対するものであり、その後の変更を自動追随しない。
- package file数の差2件について内容差分は本記録の対象外である。
- 実際のinstall、更新、原子的切替、rollbackの成否は観測していない。
- ReviewCompass3での採否と追加制約は別のHuman Decisionへ記録する。
