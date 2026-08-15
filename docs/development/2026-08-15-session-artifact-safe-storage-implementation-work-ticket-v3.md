# Session記録安全保存 製品TDD実装作業票 v3

- 作業票ID：`RC3-SESSION-ARTIFACT-SAFE-STORAGE-IMPLEMENTATION-2026-08-15-V3`
- 作成日：2026-08-15
- 形式：v2への一点訂正を固定する累積作業票
- supersedes：`docs/development/2026-08-15-session-artifact-safe-storage-implementation-work-ticket-v2.md`
- v2 SHA-256：`96cdfc57006557249143d29c2676f0361e90fec9beb9b3ecf3227b87bb0e0cc0`
- v2訂正レビュー：`records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v2.md`
- 基準commit：`1569495a0bfe33b45c5696ee73a68765208dc6a2`
- 状態：`tdd_boundary_precheck_one_point_corrected / independent_one_point_review_pending`
- 危険度：`high`

## 1. 読み方と正本範囲

【判断】本v3は、固定したv2の全節を取り込み、以下に明示する箇所だけを置き換えまたは追加する。一点訂正後の
実装作業票は「v2の固定内容＋本v3の置換・追加」であり、競合時は本v3を優先する。機能範囲、九境界、受入条件
1から22の対応、変更許可path、禁止事項、実装方法C、順序、停止条件、完了条件は変更しない。

【実測】v2訂正レビューでは、v1の二指摘の中心部分は解消した。新たな止める指摘は、作成した記録directoryと
固定file自体、および後続操作の利用時点における所有者、mode、追加ACL、symlink非追跡open後再確認が、具体的な
REDと最小実装へ固定されていない一件だけだった。

## 2. v2 §5 境界3の置換

v2 §5「境界3：新規一記録の確定保存」の次の三項目を置き換える。

- RED例：合成正常入力を保存できず失敗する。実装後は、作成した二つの記録directoryが実効利用者所有かつ
  0700相当、作成した全通常fileと一時fileが同所有者かつ0600相当で、所有者以外へ許可する追加ACLがないことを、
  symlink非追跡で開いたdirectory/file descriptorのopen後情報から確認する。さらに`derived.json`、`manifest.json`、
  保存結果の全階層に`provenance.source_path`、相対・絶対のSession入力path、home、利用者名、host名、秘密値がなく、
  固定file名にもそれらがなく、二rootのDigestと`commit.json`が一致することをfile再読込みで確認する。作成直後の
  directoryまたはfileのmode、所有者、追加ACL、種類を試験fixtureで不適合にした場合は確定成功を返さない。
- 最小実装：§3.1の許可項目だけを新しい値へ組み立て、内容から記録IDを作る。各記録directoryをdirectory file
  descriptorからsymlink非追跡かつ排他的に0700相当で作り、open後に所有者、directory種別、mode、追加ACLを再確認する。
  固定fileと固定`.tmp`を同じ方法でnew-onlyかつ0600相当で作り、open後に所有者、通常file種別、mode、追加ACLを
  再確認する。各fileと親directoryを同期し、再読込み照合後に同一root内で置換して再びopen後検査を行う。両rootの
  operation、本文、manifestを照合して`commit.json`を最後に作る。
- 不変条件：確定印前、または作成したdirectory/fileの所有者、種類、mode、追加ACL、symlink非追跡open後検査の
  いずれかが不合格なら成功を返さない。保存用派生物、manifest、出力へ`source_path`を写さない。

境界3の利用者から見た意味、REDの主要理由、先取りしない責務、前提・後続、戻せる地点はv2から変更しない。

## 3. v2 §5 境界4から8への横断追加

境界4から8の各「不変条件」へ、次を追加する。

> その操作で開く二つの記録directoryと全固定file・一時fileは、rootからdirectory file descriptorで相対的に
> symlinkを追わずに開き、利用時点のopen後情報で、実効利用者所有、directoryは0700相当、通常fileは0600相当、
> 所有者以外へ許可する追加ACLなし、期待するfile種別であることを再確認する。一つでも不合格なら、本文を返さず、
> 書込み・上書き・削除を開始せず、秘密とpathを含まない固定理由で停止する。

境界4「同一入力の再保存と競合拒否」では、`unchanged`を返す前と排他獲得後にこの検査を行う。境界5「中断した
保存の再開」では既存fileを再利用する前、境界6「再読込み」では本文を返す前、境界7「削除計画」では計画を返す前、
境界8「削除」では計画・確認値の再照合前と各fileを削除する直前に行う。途中で属性が変わった場合は成功側へ推測しない。

## 4. v2 §9 最終検証への追加

v2 §9の「権限と境界」を次で置き換える。

- 権限と境界：root省略、同一・包含、repository内、所有者不一致、mode不適合、追加ACL、途中component symlinkに加え、
  作成直後の記録directoryが所有者限定0700相当、作成直後の全通常file・一時fileが所有者限定0600相当、両者に
  所有者以外へ許可する追加ACLがないことをopen後情報で確認する。保存後にdirectoryまたはfileの所有者、mode、
  追加ACL、種類、symlink状態を一つずつ不適合へ変え、`store`再試行、`load-derived`、`plan-delete`、`delete`の各操作が
  本文を返さず、書込み・上書き・削除を開始せず停止することを確認する。

独立oracleは、契約から固定file集合、保存許可項目、各状態、監査期限に加え、各操作で必要な作成物の期待所有者、
期待種類、期待mode、追加ACLなしを別計算し、実装の利用時点検査と照合する。

## 5. 訂正後の開始判断基準

独立担当はv2と本v3を一つの累積作業票として読み、次を反証する。

1. 作成物の0700／0600相当、所有者、追加ACL、種類、symlink非追跡open後検査が境界3のRED、最小実装、不変条件へ入った。
2. 後続の保存再試行、復旧、再読込み、削除計画、削除は、各利用時点で同じ検査を行い、不合格時に読み書き削除を始めない。
3. 最終検証が、作成直後の正しい属性と、保存後に各属性を不適合へ変えた反例を四操作へ適用する。
4. v2の九境界と契約22条件、機能範囲、禁止事項に新たな矛盾がない。

【判断】判定が`開始可`、止める指摘0件となるまで、製品試験と製品コードを変更しない。

## 6. 未実施

【未実施】本v3の作成時点では、製品コード、製品試験、設定、配布入口、契約、G26、G28、G30、上流候補、
Issueを変更していない。権限変更、保存、再読込み、削除、外部送信、push、履歴書換えも行っていない。
