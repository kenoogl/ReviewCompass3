# 契約010 読取り恒久許可の発見とproject束縛の実装 Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 位置づけ：E2E第6試行後の局所調査（送信なし）と、その結果に基づく訂正の記録

## 1. 利用者の対話実験【記録：利用者提供】

利用者がagyを対話modeで開き「records/session-handoffs/ にある依頼recordを1つ開いて1行で要約して」を
実行したところ、**許可確認は一度も表示されず**、ListDir→Readが即実行されて要約が返った（chat転記）。
「常に許可」を選ぶ場面自体が存在しなかった。

## 2. 設定の局所調査【実測】

`~/.gemini/`（agy CLIの設定置き場）を送信なしで調査した。

- `antigravity-cli/settings.json`：`trustedWorkspaces`に`/Users/Daily/Development/ReviewCompass3`が
  登録済み（対話modeで確認が出ない理由）。
- `config/projects/c6fb567d-0ac5-47c8-b254-828b6fc275b0.json`（project名`ReviewCompass3`）：

```json
"permissionGrants": {
  "permissionGrants": {
    "allow": [
      "read_file(/Users/Daily/Development/ReviewCompass3)"
    ]
  }
}
```

  更新時刻は2026-08-16T07:51Z——**利用者自身が暫定手動体制の対話sessionで与えた読取り恒久許可**が
  保存されている。E2E第3〜6試行の拒否message（`User denied permission for read_file(…)`）の書式と
  完全に一致する。

## 3. 真因の確定

headless起動が**project文脈へ束縛されていなかった**（`--project`旗を渡していない）ため、利用者の
既存許可が適用されず、既定の`request-review`＋承認者不在＝自動拒否となっていた。

## 4. 訂正【実測】

1. `resolve_project_binding(repository)`を新設：agyのproject設定からrepositoryに対応するproject
   （`projectResources.gitFolder.folderUri`一致）を機械解決し、**利用者の既存許可
   `read_file(<repo>)`の存在を確認**してidを返す。projectが無ければ`project_binding_missing`、
   許可が無ければ`read_grant_missing`で起動前に停止する。許可の新設・迂回は行わず、許可を与える
   経路は利用者の対話sessionだけに保たれる。
2. 固定引数へ`--project=<id>`を追加（起動recordへ`project_id`を記録）。
3. 実環境の機械確認：`resolve_project_binding`が実設定から`c6fb567d-0ac5-47c8-b254-828b6fc275b0`を
   解決することを確認（起動なし）。
4. 試験：project模擬設定の補助・固定引数検査の追随・束縛欠如／許可欠如の停止試験2件を追加。
   対象試験35件単独緑、禁止認証隔離条件の正規全試験2,410件成功・終了コード0。

## 5. 安全性の位置づけ

- 本訂正は許可の状態を一切変更しない（読取り専用の設定参照と、既存許可の存在検査だけ）。
- 適用される許可は読取り（`read_file`）のrepository限定grantであり、契約§1の読み取り専用境界と一致
  する。書込み許可は存在せず、`--dangerously-skip-permissions`は不使用のまま。

## 6. 残り

- §9-8実E2Eは未成立。再実施は新識別子`e2e-010-007`で利用者指示を得て行う。
