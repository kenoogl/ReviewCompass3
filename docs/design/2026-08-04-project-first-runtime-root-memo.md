---
lifecycle: proposed
normative_status: non-normative
document_role: runtime-root-layout-design-memo
---

# Project-first Runtime Root配置メモ

## 1. 結論

ReviewCompass3の可変runtime dataは、project内やdeployment package内ではなく、利用者home配下の
`~/.reviewcompass3/`へ置く。複数projectを直感的に扱うため、filesystemの第一階層は論理rootではなく
projectとする。

```text
~/.reviewcompass3/
  config/
  projects/
    <project-id>/
      development/
        data/
        state/
        cache/
        logs/
        evaluation/
        sensitive/
      runtime/
        data/
        state/
        cache/
        logs/
        evaluation/
        sensitive/
```

`project-id`はProject Manifestの安定した明示IDであり、absolute path、checkout path、content Digestから
導出しない。ReviewCompass3自身の現在の開発では、最初に必要なdirectoryは
`~/.reviewcompass3/projects/reviewcompass3/development/data/`だけである。他のdirectoryは必要になるまで
作成しない。

## 2. この形を選ぶ理由

利用者はまず「どのprojectのdataか」を知りたい。`data/`、`state/`を全project共通の第一階層にすると、
安全ではあっても日常の探索、backup、調査、削除が分かりにくい。project-firstにすると、project単位で
可変dataを把握・隔離できる。

一方、同じprojectでもReviewCompass3自身の開発dataと、利用者向けdeploymentでのruntime dataを混ぜない。
そのため`development/`と`runtime/`を物理的に分ける。各profile内で`data`、`state`、`cache`、`logs`、
`evaluation`、`sensitive`を分けることで、Layout Baselineの論理root分離を保つ。

## 3. 各directoryの責務

| directory | 内容 | Git／deployment |
|---|---|---|
| `data/` | Source Snapshot、Source Symbol Index、Provenance、Run、Context、compiled Plan、Discovery Record | Git対象外、packageへ含めない |
| `state/` | checkpoint、lock、scheduler state | Git対象外、packageへ含めない |
| `cache/` | 再生成可能なcache | Git対象外、削除可能、packageへ含めない |
| `logs/` | 実行・診断log | Git対象外、packageへ含めない |
| `evaluation/` | Evaluation Observation、Label、派生結果 | Git対象外、packageへ含めない |
| `sensitive/` | raw会話録、secretを含み得る未検査data、quarantine | Git・通常export・packageから既定除外 |
| top-level `config/` | 利用者・端末固有のroot resolver設定 | Git・packageから既定除外 |

Contract、Policy、Decision、Reusable Routine Ledger、verified artifactのようにproject間で共有・reviewするものは、
引き続きproject内の`.reviewcompass/`または`records/`に置く。runtime rootには置かない。

## 4. 複数projectと複数checkout

複数projectの最小分離は`project-id`で足りる。`project-id`ごとにdirectoryが別なので、Snapshot、Index、
state、log、sensitive dataが混ざらない。

同じprojectの複数checkoutを同時に扱う`binding-id`は、現時点ではdirectoryへ入れない。Source Snapshot IDが
HEAD、対象path、file Digest、source universeから作られるため、異なるsource内容は既に別IDになる。
checkout固有lock、ローカル絶対path、同時schedulerが実際に必要になった場合だけ、後続Layout versionで
`bindings/<binding-id>/`を追加する。その変更は通常編集ではなくmigrationとして扱う。

## 5. deployment、更新、削除

deployment packageはcode、Manifest、schema、generatorを含むが、`~/.reviewcompass3/`のdataを含まない。
導入先では、対象projectをbindした後にSource SnapshotとIndexを機械再生成する。

generator、schema、source universeまたは対象sourceが変わったIndexはstaleとし、新versionを生成する。
既存dataを黙ってコピー、上書き、削除しない。data migration、project unregister、export、sensitive dataの
移送は、対象project、影響範囲、backup／rollback、Human承認を持つ別操作とする。

## 6. platformとsecurity

`~/.reviewcompass3/`を共通の論理既定pathとする。macOS／Linuxではhome配下のdot directory、Windowsでは
`%USERPROFILE%\\.reviewcompass3`へ解決できる。CLI明示指定、versioned user setting、許可環境変数、
この既定pathの順で解決し、absolute pathを共有artifactへ保存しない。

Unix系ではrootと`sensitive/`を`0700`、機微fileを`0600`とする。Windowsでは利用者のみのACLを適用する。
credentialは通常fileではなく、macOS Keychain、Windows DPAPI、Linux Secret ServiceなどのOS秘密保管庫を
優先する。`sensitive/`はraw transcriptやquarantine data用であり、秘密保管庫の代替ではない。

## 7. 段階導入と非目標

本メモは現行Layout Baselineを置換しない。実装前に、resolver規則、directory作成時の権限、deployment
Manifestの除外、project／profile isolation、migration入口をLayout Baselineの新versionとして承認する。

当面の実装は、ReviewCompass3の`development/data/`を明示的に設定して、Work 4AのSnapshotとIndexを保存する
ところまでに限定する。次は先送りする。

- `binding-id` directoryと複数checkout専用state
- binding間のSnapshot／Index共有と重複排除
- profile選択UI
- retention、prune、unregisterの自動化
- platformごとのnative application-data directoryへの分散
- data migrationの実装

この限定により、複数projectを最初から分離しつつ、将来の利用実態がない構造を先回りして固定しない。
