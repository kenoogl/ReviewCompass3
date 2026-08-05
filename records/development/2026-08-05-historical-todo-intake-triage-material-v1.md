# 過去TODO候補41件のHuman triage資料 v1

## この資料の位置づけ

- これはHumanの判断を助けるための**非権威の説明資料**である。
- 正本は次の候補一覧である。この資料ではない。
  - `records/development/2026-08-05-historical-todo-intake-candidates-v1.json`
  - SHA-256（この資料作成時点）：`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`
- 候補の原文引用とsource位置（どのfileの何行目か）は、上記の候補一覧を正本とする。この資料の要約が原文と食い違う場合は、原文が正しい。
- Claudeによる要約、束（グループ）分け、確認順は**提案**であり、Humanの裁定ではない。
- この資料は、正式Issue、triage decision（採否の裁定）、Plan、Workを作る根拠にならない。
- Claudeは、採否、priority（優先順位）、正式Issueへの昇格、統合、作業再開のいずれも決めていない。

---

## 1. 全体像

### 見出し別の内訳（合計41件）

| 元の見出し | 件数 |
| --- | --- |
| 未実施 | 7 |
| 残余risk | 15 |
| 手戻り・機械化候補 | 14 |
| blocker・Human判断待ち | 5 |

すべての候補は、同じ一つの記録から機械抽出されている。

- 抽出元：`records/session-handoffs/2026-08-04-todo-before-compaction-001.md`
- 抽出元のSHA-256：`16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`

### 状態

- 重複疑い（`duplicate_suspect`）は0件である。
- すべての候補の`human_fields`（未解決・再発性・影響・priority・Issue昇格）は未記入（`null`）である。
- 正式Issueへ昇格した候補は0件である（`promotion_status: none`）。

### 重要な前提

- **「候補がある」ことは「問題が未解決である」ことを意味しない。** 候補は機械が原文から切り出した文であり、すでに解決済みの記述、単なる方針の確認、判断不要の記録も含まれうる。未解決かどうかは、Humanが確認して初めて決まる。
- **`duplicate_suspect: false`は、引用文を正規化した機械的な照合で重なりが無かったという意味だけである。** 意味の上で同じことを言っている候補が無いことは保証しない。意味的な重複の有無は、Humanが読んで判断する。

---

## 2. Humanが判断する5項目の説明

各候補について、Humanは次の5項目を決める。

| 項目 | 平易な説明 |
| --- | --- |
| 未解決（unresolved） | いま現在も片付いていない事柄か。すでに直っている・すでに決まっているなら未解決ではない。 |
| 再発性（recurrence） | 放っておくと同じことがまた起きるか。一度きりの出来事か、繰り返す性質のものか。 |
| 影響（impact） | 起きたときに何がどれだけ困るか。成果物、安全性、作業のやり直し量などへの効き方。 |
| priority（優先順位） | 他の候補と比べて、どれを先に扱うか。 |
| Issueへ昇格（promote_to_issue） | 正式なIssueとして登録して追跡するか、登録せずに閉じるか。 |

---

## 3. 確認用の束（テーマ別のまとまり）

以下は、Humanがまとめて読めるように候補をテーマで並べた提案である。

- 各候補IDは、全体でちょうど一回だけ現れる（合計41件）。
- **束は「同じ処置をすべき」という結論ではない。** 似た候補を隣に置いて比較しやすくするための並べ方にすぎない。
- 引用文を言い換えた説明は、原文の範囲を超えないよう努めているが、短い引用や文脈が切れている引用については`原文確認が必要`と明記する。

### 束A：機械が組み立てるべき命令をLLMが直接組み立てて失敗した（5件）

**まとめた理由**：いずれも「shellやtool呼び出しの文字列、または実行権限の選択をLLMが直接行い、その場で一度失敗した」という同じ形をしている。比較すると、共通の対策（構造化した命令の受け渡し、権限の事前振り分け）で足りるかどうかを一度に見られる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-C9F6C917 | `.git`が読み取り専用と事前に分かっていたのに、最初の`git add`を通常権限で実行して一度止まった。原文は、Git metadataへの書き込みを最初からGit書き込み権限で実行するよう機械的に振り分け、失敗後に権限を切り替える運用をやめる、という恒久対策を記している。 |
| HTC-477EA1A4 | コンパイル確認が作業領域の外にcacheを書こうとして、sandboxに拒否された。task専用のcache置き場を指定して通った。原文は手作業起因ではないとしている。 |
| HTC-186E9B83 | 検索語に含まれるバッククォートをshellが解釈してしまい、補助的な検索が一度だけ失敗した。原文は成果物・capture・Testへの影響は無いとしている。 |
| HTC-9DCE8503 | zshの特殊変数`path`をループ変数に使ったためコマンド検索パスが壊れ、`shasum`が一度`command not found`になった。原文は成果物変更前の読み取り専用照合であり影響は無いとしている。 |
| HTC-A5D1BCCA | 並列実行するJavaScriptの出力区切りを誤記し、構文エラーが一度発生した。原文は成果物への影響は無いとしている。 |

### 束B：記録そのものの生成・配置を機械化する候補（5件）

**まとめた理由**：いずれも「記録（patch適用、Testの数値、完了時刻、commit後のTODO、記録の置き場所）を人手または場当たりで作った結果、訂正や追加作業が発生した」という形をしている。記録生成をどこまで機械に任せるかを、まとめて検討できる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-C2E642ED | checklistへの文章挿入で、挿入位置の特定をLLMが行ったため実際のfileと合わず、patch適用が一度失敗した。読み直した後のpatchは成功したと原文にある。 |
| HTC-66C3E6CA | 引き継ぎ照合で、Test時間が記録上`2.26s`なのにTODOへ`2.29s`と手入力されていた転記差を検出し、記録側の値へ訂正した。 |
| HTC-D34A113E | 完了記録を作った後に追加の検証を行ったため最終検証時刻が後ろにずれ、完了記録の時刻を訂正した。原文は、すべての必須検証が終わってから時刻を確定すべきだとしている。 |
| HTC-5C059B48 | commit後の照合で、自分自身のSHAなどをTODOへ書き写すための追加commitが発生した。原文は、恒久対策としてcommit前に検査するvalidator等を実装し、Testに合格したと記している。 |
| HTC-E183A02B | 現行Issueの改定記録の置き場所を誤り、一つの主題に一件という制約に反して公式Testが一度失敗した。既存Testが検出し、正しい経路へ修正して再合格したと原文にある。 |

### 束C：機械側で起きた観測で、その場で閉じたもの（4件）

**まとめた理由**：いずれも原文が「手作業が原因ではない」または「その場で解決した／そもそも手戻りが無かった」と述べている。未解決として残すものが本当に無いかを、まとめて確認できる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-D65B4A8E | 昇格前監査の初回表示が、旧37件と追加13件の区分の分かりにくい集計になっていた。区分し直して解消したと原文にある。 |
| HTC-75C717E1 | 不正なUTF-8の扱いに関する契約が変わってしまう回帰を、公式全Testが1件検出した。エラーをそのまま伝播させる形に戻し、全Test合格へ復旧したと原文にある。 |
| HTC-3AFBA652 | 一時的な監査スクリプトが項目名を誤って仮定し`KeyError`で一度停止した。既存の共通の読み取り関数へ切り替えて合格したと原文にある。 |
| HTC-E7E2F692 | その回の文書化では失敗・手戻り・転記訂正が発生せず、新しい手戻り候補は無い、という記述である。判断対象になる問題を含まない可能性がある。`原文確認が必要`。 |

### 束D：着手していない実装・設計の項目（6件）

**まとめた理由**：いずれも元の見出しが「未実施」で、引用が短い項目名だけの箇条書きである。すべて`原文確認が必要`（一行の項目名からは、範囲・現在の状況・依存関係が読み取れない）。まとめて見ると、どれが今も未着手のままかを一度に確認できる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-1D5B5102 | 「WI-006以降、WI-001の実snapshot／manifest生成、TODO compaction、Resolution Verdict」という未実施項目の列挙。`原文確認が必要`。 |
| HTC-328144E4 | Deployment Manifest、package builder、原子的な切替、rollbackを含むWork 7の実装が未実施、という項目。`原文確認が必要`。 |
| HTC-BE5E1F67 | Work 4のDesign差分、代表シナリオ、最初のvertical sliceの選定が未実施、という項目。`原文確認が必要`。 |
| HTC-45B611EF | Project Bindingのdurable保存（恒久的な保存）が未実施、という項目。`原文確認が必要`。 |
| HTC-D7E1F8C3 | 実施報告照合の自動Claim抽出、Provenance対応、完了stateの結線が未実施、という項目。`原文確認が必要`。 |
| HTC-243BE1FF | session hook、Desktop監視、Claude hook、scheduler、background serviceの有効化が未実施、という項目。`原文確認が必要`。 |

### 束E：記録の保存場所・保存期間・自動化に関する運用判断（4件）

**まとめた理由**：いずれも「どこに保存するか、いつまで残すか、暗号化するか、自動実行を有効にするか」という運用上の取り扱いに触れている。安全性と外部への影響に関わりうるため、まとめて見ると判断が揃えやすい。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-045A8FB5 | 運用上の保存物がproject外の一時的な作業領域にあり、その識別子とDigestを完了候補へ固定した、という記述。保存場所そのものについて何を決めたかは`原文確認が必要`。 |
| HTC-4ED2C5B1 | 会話記録の手動収集・突き合わせ・限定的な取得は完了しているが、取得後に追記された会話は次回の手動突き合わせ対象であり、自動実行は未実装・未有効である、という記述。 |
| HTC-BEB5E0BD | 非公開の会話記録について、長期保存、削除、アプリケーション層での暗号化、backupの運用判断が未実施、という項目。`原文確認が必要`。 |
| HTC-CD984CD0 | 2026-09-03の保存期間見直し、暗号化、自動実行の有効化が、後続のHuman判断待ちである、という記述。 |

### 束F：どれが正本かと、古い版の保持（7件）

**まとめた理由**：いずれも「現行の正本はどれか」「候補fileを二つ目の正本にしない」「古い版は履歴として残し消さない」という同じ主題を扱っている。並べて読むと、正本の扱いに関する記述が互いに矛盾していないかを確認できる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-C05BE65C | ある文書改定が`digest-only`（要約値だけ）の履歴として残るが、現行の固定入力とWork 1AのEvidenceはGitから再構築できる、という記述。 |
| HTC-C3193ABF | Intent／用語集の候補fileは昇格前の写しであり、現行の正本は外部の承認Decisionと承認対象のDigestである、という記述。 |
| HTC-ECE89CA2 | session `001`と旧候補のDigestは、問題が起きた証拠として保持するが、現在の判断の関門には使わない、という記述。 |
| HTC-49795CC0 | coverage matrixの現行の正本は外部の承認Decisionであり、候補fileを二つ目の正本にしない、という記述。 |
| HTC-094589CA | identity／stale規則とRequirements配置規則の正本も外部Decisionと承認対象Digestであり、CI adapter、Build Artifact実装、provider操作は引き続き対象外である、という記述。 |
| HTC-876989C2 | directory、schema、validator等一式を作成し、旧legacy bindingとauthority v1はsupersededな履歴として保持、現行の権威は50件の定義だけである、という記述。 |
| HTC-ABE70CFC | 旧37件のRequirementは機械的に移行済みで、現行は50件の定義・legacy binding 0件であり、旧版は履歴として残し削除・上書きしない、という記述。 |

### 束G：承認された範囲と、まだ承認していない範囲の境界（4件）

**まとめた理由**：いずれも「ここまでは承認済み、ここから先は未承認・暫定」という線引きを述べている。受入基準に関わるため、比較して読むと線引きが一貫しているかを確認できる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-8AEF6A5F | Layout validatorはWork 1Aの固定規則を確認するための暫定的な判定手段であり、正式な製品Runtimeではない、という記述。 |
| HTC-152E0FB3 | 現行のPlanと追加13要件は暫定・レビュー候補の状態であり、baselineの確認だけで承認済みとして扱わない、という記述。 |
| HTC-7DDF463E | NFR Profileの接続はHuman承認済みだが、数値の閾値、Architecture Policy、shared／distributed scopeは承認も実装もしていない、という記述。 |
| HTC-B53A2670 | 先送りした13件はHuman承認のうえ初期releaseの`nonblocking`（公開を妨げない扱い）に固定したが、各機能の実装・有効化は別の合意とHuman判断まで開始しない、という記述。 |

### 束H：検証手順と報告様式の取り決め（2件）

**まとめた理由**：どちらも「今後の作業でどう検証し、どう報告するか」という手続きの決めごとである。すでに守られているか、追加の作業が要るかを一緒に確認できる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-7071DD99 | 公式Testはpolicy runner経由に変更し、素の`python3 -m pytest -q`はrunner内部のコマンド扱いとする。今後の完了Evidenceにはrunnerのreceiptを要求する、という記述。 |
| HTC-62719E1C | Policy v5により、今後の作業後報告には手戻りと手作業の因果、期待／実executor、Evidence、機械処理候補、routeを含める。決定的な処理をLLMが行った場合は手戻りが無くても改善候補として報告する、という記述。 |

### 束I：作業の開始・再開の条件（blocker）（4件）

**まとめた理由**：いずれも「何が終わるまで次を始めないか」という開始条件・保留条件を述べている。他の候補の扱いに先立って現在の状態を確認する必要がありうる。

| 候補ID | 平易な説明 |
| --- | --- |
| HTC-14D810C7 | blockerは無いが、WI-006のGREENを含むcommitを確認するまでWI-007を開始しない、という記述。この条件が現在満たされているかは`原文確認が必要`。 |
| HTC-1AB699F7 | 当時のWI-007作業について、追加のHuman判断は無い、という記述。 |
| HTC-21C3CE46 | 実snapshotはWI-006のGREEN commit後、TODO compactionはWI-007を含むcommit後まで開始しない、という保留条件の記述。 |
| HTC-6ABDDC35 | 再開条件は、WI-006のGREENを含むcommitの確認、作業ツリーがcleanであること、transitionの合格である、という記述。 |

---

## 4. Humanの確認順の提案

以下は提案であり、priorityやdisposition（採否）を確定するものではない。束の単位で並べてある。

### 段階1：先に一件ずつ確認することを勧めるもの（12件）

- **束I（4件）** — 開始・再開の条件そのものであり、他の候補をどう扱うかの前提になりうるため。また、条件がすでに満たされているかどうかは記録を見ないと分からない。
- **束E（4件）** — 保存場所、保存期間、暗号化、自動実行の有効化に触れており、安全性と外部への影響に関わりうるため。
- **束G（4件）** — 「どこまでが承認済みか」という受入基準の線引きに触れており、取り違えると後続の判断がずれるため。

### 段階2：束でまとめて比較してから確認することを勧めるもの（23件）

- **束A（5件）** — 同じ形の手戻りが並んでおり、個別に見るより共通の原因があるかを比較したほうが判断しやすいため。
- **束B（5件）** — いずれも記録生成の機械化候補であり、どこまで機械化するかをまとめて見たほうが判断しやすいため。
- **束C（4件）** — いずれも原文が「その場で閉じた」旨を述べており、残すものがあるかを横並びで確認したほうが速いため。
- **束F（7件）** — 正本の扱いという同一主題であり、記述どうしの整合を見るのに並列比較が向くため。
- **束H（2件）** — 手続きの取り決めであり、すでに守られているかを一緒に確認できるため。

なお、束Aの`HTC-C9F6C917`はGitの書き込み権限の扱いに触れているため、Humanが段階1に近い扱いを選ぶ余地がある。この資料ではその位置を確定しない。

### 段階3：後回しにできる可能性があるもの（6件）

- **束D（6件）** — 元の見出しが「未実施」であり、引用が項目名だけで現在の状況が読み取れない。すでに着手済み・不要になっている可能性もあるため、現状確認の負担に対して急ぐ理由が段階1・2より弱い可能性がある。ただしこれは「影響が小さい」という判定ではなく、原文と現状を確認するまで分からない。

---

## 5. Human用の判断表（未記入）

`未解決`以降の欄はHumanが記入する。Claudeは値を入れていない。

| candidate ID | 平易な要約 | 未解決 | 再発性 | 影響 | priority | Issueへ昇格 | Humanメモ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HTC-C2E642ED | patch適用位置の特定をLLMが行い、一度適用に失敗した（束B） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-66C3E6CA | Test時間の転記差（2.26s→2.29s）を検出し訂正した（束B） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-D65B4A8E | 昇格前監査の初回集計表示が分かりにくく、区分し直した（束C） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-D34A113E | 完了記録の時刻を、追加検証の後にずれたため訂正した（束B） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-3AFBA652 | 一時監査スクリプトが項目名を誤仮定し停止、共通関数へ切替（束C） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-75C717E1 | 不正UTF-8の扱いの回帰を全Testが検出し、復旧した（束C） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-E7E2F692 | その回は手戻り・転記訂正なしという記述（束C、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-A5D1BCCA | 並列実行のJavaScript出力区切りを誤記し構文エラー（束A） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-477EA1A4 | 作業領域外へのcache書込みをsandboxが拒否した（束A） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-186E9B83 | 検索語のバッククォートをshellが解釈し検索が一度失敗（束A） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-C9F6C917 | `.git`が読取専用と分かっていたのに通常権限で`git add`し停止（束A） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-5C059B48 | commit後のTODO転記のために追加commitが発生した（束B） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-9DCE8503 | zsh特殊変数`path`の上書きで`shasum`が一度実行できなかった（束A） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-E183A02B | 改定記録の置き場所を誤り、単一主題制約のTestが失敗した（束B） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-1D5B5102 | 実snapshot／manifest生成等の未実施項目の列挙（束D、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-328144E4 | Work 7（Deployment Manifest等）の実装が未実施（束D、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-BE5E1F67 | Work 4のDesign差分・代表シナリオ等の選定が未実施（束D、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-45B611EF | Project Bindingの恒久保存が未実施（束D、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-D7E1F8C3 | 実施報告照合の自動化・完了state結線が未実施（束D、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-BEB5E0BD | 非公開会話記録の保存期間・削除・暗号化・backupの運用判断（束E、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-243BE1FF | hook／監視／scheduler等の有効化が未実施（束D、原文確認が必要） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-045A8FB5 | 運用保存物がproject外の一時領域にあり、identityとDigestを固定した（束E） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-8AEF6A5F | Layout validatorは暫定の判定手段で、正式な製品Runtimeではない（束G） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-C05BE65C | 改定履歴は要約値だけ残るが、固定入力とEvidenceはGitから再構築可能（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-C3193ABF | Intent／用語集の候補fileを二つ目の正本にしない（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-ECE89CA2 | 旧sessionと旧候補のDigestは証拠として保持し、判断の関門に使わない（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-152E0FB3 | 現行Planと追加13要件は暫定であり、承認済み扱いにしない（束G） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-49795CC0 | coverage matrixの正本は外部の承認Decisionである（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-094589CA | identity／配置規則の正本も外部Decisionで、CI等は対象外（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-876989C2 | 一式を作成し、旧版は履歴保持、現行の権威は50件の定義だけ（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-7DDF463E | NFR Profile接続は承認済みだが、閾値とPolicyは未承認・未実装（束G） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-B53A2670 | 先送り13件を`nonblocking`に固定、実装は別判断まで開始しない（束G） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-ABE70CFC | 旧37件は移行済みで、旧版は削除・上書きせず履歴保持（束F） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-7071DD99 | 公式Testはrunner経由に変更し、完了Evidenceにreceiptを要求（束H） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-62719E1C | Policy v5の報告様式（因果・executor・Evidence・route）を必須化（束H） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-4ED2C5B1 | 会話記録の手動運用は完了、自動実行は未実装・未有効（束E） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-14D810C7 | blockerなし。WI-006 GREEN commit確認前はWI-007を開始しない（束I） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-1AB699F7 | 当時のWI-007作業について追加のHuman判断なし（束I） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-21C3CE46 | 実snapshotとTODO compactionの開始を特定commit後まで保留（束I） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-CD984CD0 | 2026-09-03の保存期間見直し・暗号化・自動化有効化はHuman判断待ち（束E） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |
| HTC-6ABDDC35 | 再開条件はGREEN commit確認・clean worktree・transition合格（束I） | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 | Human記入 |

行数：41行（候補一覧の41件と一致）。
