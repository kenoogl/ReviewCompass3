"""front matter authority参照Digest検査器の受入テスト（deferred #5）。

範囲固定：records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v2.md
正本authority：ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001（front matterの現在有効参照に限定。
本文参照・時点固定pinは対象外）

固定するのは、(1)Human承認済みallowlist宣言だけが検査対象keyを決めること、
(2)対象参照のpath安全性・実在・現行bytes一致のfail-closed検査、(3)時点固定pin
（allowlist外key）と本文が合否に影響しないこと、(4)空合格の禁止。
正常系はHuman承認済みの実文書2件を使用し、異常・境界系は`tmp_path`の
合成file・合成allowlistを使用する。
"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


ALLOWLIST_KEYS = {
    "authority_order": "mapping_list",
    "operational_policy": "mapping",
    "policy_decision": "mapping",
    "related_design": "mapping_list",
    "intent_ref": "mapping",
    "glossary_ref": "mapping",
    "reconciliation_ref": "mapping",
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _module():
    return importlib.import_module(
        "tools.development.authority_reference_checker"
    )


def _write_allowlist(tmp_path, keys=None):
    payload = {
        "schema_version": 1,
        "keys": dict(ALLOWLIST_KEYS) if keys is None else dict(keys),
    }
    path = tmp_path / "allowlist.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path


def _write_target(root, relative, content):
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _mapping_block(key, relative, digest):
    return "%s:\n  path: %s\n  sha256: %s\n" % (key, relative, digest)


def _document(blocks, body="本文。\n"):
    return "---\n" + "".join(blocks) + "---\n\n" + body


def _run(module, capsys, files, *, allowlist, root):
    exit_code = module.run((
        "--allowlist",
        str(allowlist),
        "--root",
        str(root),
        *[str(item) for item in files],
    ))
    output = capsys.readouterr().out
    return exit_code, json.loads(output)


def test_approved_current_documents_match_all_allowlisted_references(capsys):
    """正例1：承認済み2文書の7 key全種・11参照が現行bytesと一致する。"""

    module = _module()
    checklist = PROJECT_ROOT / (
        "docs/development/2026-08-03-initial-development-checklist.md"
    )
    plan = PROJECT_ROOT / "docs/current/reviewcompass3-plan-current.md"
    allowlist = PROJECT_ROOT / "tools/development/authority_reference_keys.json"

    exit_code, payload = _run(
        module,
        capsys,
        (checklist, plan),
        allowlist=allowlist,
        root=PROJECT_ROOT,
    )

    assert exit_code == 0
    assert payload["status"] == "ok"
    assert payload["totals"]["checked"] == 11
    assert payload["totals"]["matched"] == 11
    assert payload["totals"]["mismatched"] == 0
    assert payload["totals"]["missing"] == 0
    assert payload["totals"]["invalid"] == 0
    assert payload["files"][str(checklist)]["checked"] == 8
    assert payload["files"][str(plan)]["checked"] == 3


def test_allowlist_declaration_controls_extraction(tmp_path, capsys):
    """正例2：宣言からkeyを外すと検査対象から消える（誤digestでも合否に影響しない）。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    blocks = [
        _mapping_block("intent_ref", "docs/intent.md", digest),
        _mapping_block("related_design", "docs/absent.md", "0" * 64),
    ]
    document = root / "doc.md"
    document.write_text(_document(blocks), encoding="utf-8")
    narrowed = _write_allowlist(tmp_path, keys={"intent_ref": "mapping"})

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=narrowed,
        root=root,
    )

    assert exit_code == 0
    assert payload["totals"]["checked"] == 1
    assert payload["totals"]["matched"] == 1


def test_mismatched_digest_fails(tmp_path, capsys):
    """負例3：1文字違いのdigestをmismatchedとしてkey・path・行番号つきで報告する。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    wrong = ("0" if digest[0] != "0" else "1") + digest[1:]
    document = root / "doc.md"
    document.write_text(
        _document([_mapping_block("intent_ref", "docs/intent.md", wrong)]),
        encoding="utf-8",
    )
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 5
    assert payload["status"] == "failed"
    entries = payload["files"][str(document)]["mismatched"]
    assert len(entries) == 1
    assert entries[0]["key"] == "intent_ref"
    assert entries[0]["path"] == "docs/intent.md"
    assert isinstance(entries[0]["line"], int) and entries[0]["line"] >= 2


def test_missing_reference_target_fails(tmp_path, capsys):
    """負例4：参照先fileの欠落をmissingとして報告しexit 5。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    document = root / "doc.md"
    document.write_text(
        _document([_mapping_block("intent_ref", "docs/absent.md", "a" * 64)]),
        encoding="utf-8",
    )
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 5
    entries = payload["files"][str(document)]["missing"]
    assert [(item["key"], item["path"]) for item in entries] == [
        ("intent_ref", "docs/absent.md"),
    ]


@pytest.mark.parametrize("invalid_case", (
    "sha256_missing",
    "hex_too_short",
    "absolute_path",
    "parent_escape",
    "nul_path",
))
def test_invalid_reference_forms_fail_closed(tmp_path, capsys, invalid_case):
    """負例5：許可key配下の不正形と不正経路をfail-closedにする。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    if invalid_case == "sha256_missing":
        block = "intent_ref:\n  path: docs/intent.md\n"
    elif invalid_case == "hex_too_short":
        block = _mapping_block("intent_ref", "docs/intent.md", "a" * 63)
    elif invalid_case == "absolute_path":
        block = _mapping_block("intent_ref", "/etc/hosts", digest)
    elif invalid_case == "parent_escape":
        block = _mapping_block("intent_ref", "../outside.md", digest)
    else:
        block = _mapping_block("intent_ref", "a\x00b", digest)
    document = root / "doc.md"
    document.write_text(_document([block]), encoding="utf-8")
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 5
    assert payload["status"] == "failed"
    assert payload["files"][str(document)]["invalid"] != []


@pytest.mark.parametrize(
    "empty_case",
    ("no_front_matter", "no_allowlisted_keys", "mixed_with_valid"),
)
def test_zero_reference_files_fail(tmp_path, capsys, empty_case):
    """負例6：単独でも正常文書との混在でも参照0件を不合格にする。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    document = root / "doc.md"
    if empty_case == "no_front_matter":
        document.write_text("本文だけの文書。\n", encoding="utf-8")
    elif empty_case == "no_allowlisted_keys":
        document.write_text(
            _document([
                "generated_from:\n  path: docs/x.md\n  sha256: %s\n" % ("b" * 64),
            ]),
            encoding="utf-8",
        )
    else:
        document.write_text("本文だけの文書。\n", encoding="utf-8")
        digest = _write_target(root, "docs/intent.md", "intent\n")
        valid = root / "valid.md"
        valid.write_text(
            _document([
                _mapping_block("intent_ref", "docs/intent.md", digest),
            ]),
            encoding="utf-8",
        )
    allowlist = _write_allowlist(tmp_path)
    files = (valid, document) if empty_case == "mixed_with_valid" else (document,)

    exit_code, payload = _run(
        module,
        capsys,
        files,
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 5
    assert payload["status"] == "failed"
    assert payload["files"][str(document)]["checked"] == 0


@pytest.mark.parametrize("unreadable_case", ("target", "allowlist"))
def test_unreadable_inputs_fail(tmp_path, capsys, unreadable_case):
    """負例7：読めない対象file・読めないallowlist宣言をexit 5にする。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    document = root / "doc.md"
    document.write_text(
        _document([_mapping_block("intent_ref", "docs/intent.md", digest)]),
        encoding="utf-8",
    )
    if unreadable_case == "target":
        files = (root / "absent-doc.md",)
        allowlist = _write_allowlist(tmp_path)
    else:
        files = (document,)
        allowlist = tmp_path / "absent-allowlist.json"

    exit_code = module.run((
        "--allowlist",
        str(allowlist),
        "--root",
        str(root),
        *[str(item) for item in files],
    ))
    output = capsys.readouterr().out

    assert exit_code == 5
    payload = json.loads(output)
    assert payload["status"] in ("failed", "error")


def test_pinned_keys_outside_allowlist_do_not_affect_verdict(tmp_path, capsys):
    """境界8：allowlist外key（時点固定pin）は古いDigestでも合否に影響しない。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    _write_target(root, "docs/plan.md", "plan v2\n")
    blocks = [
        "generated_from:\n  path: docs/plan.md\n  sha256: %s\n" % ("c" * 64),
        _mapping_block("intent_ref", "docs/intent.md", digest),
    ]
    document = root / "doc.md"
    document.write_text(_document(blocks), encoding="utf-8")
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 0
    assert payload["totals"]["checked"] == 1
    assert payload["totals"]["matched"] == 1


def test_same_target_in_multiple_keys_checked_independently(tmp_path, capsys):
    """境界9：同一pathを複数keyが参照する場合、各出現を独立に検査する。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    wrong = ("0" if digest[0] != "0" else "1") + digest[1:]
    blocks = [
        _mapping_block("intent_ref", "docs/intent.md", digest),
        _mapping_block("glossary_ref", "docs/intent.md", wrong),
    ]
    document = root / "doc.md"
    document.write_text(_document(blocks), encoding="utf-8")
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 5
    report = payload["files"][str(document)]
    assert report["checked"] == 2
    assert report["matched"] == 1
    assert [item["key"] for item in report["mismatched"]] == ["glossary_ref"]


@pytest.mark.parametrize(("key", "shape", "inline_value"), (
    ("intent_ref", "mapping", "unexpected"),
    ("authority_order", "mapping_list", "unexpected"),
))
def test_inline_values_on_allowlisted_key_lines_fail_closed(
    tmp_path,
    capsys,
    key,
    shape,
    inline_value,
):
    """修正RED（AR-P1-001）：許可key行のコロン後の値は宣言形と異なる不正形として拒否する。

    下位の参照対が正しくても、key行に値が同居した時点でfail-closed（exit 5）とし、
    黙って値を捨てて合格させない。
    """

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    if shape == "mapping":
        block = "%s: %s\n  path: docs/intent.md\n  sha256: %s\n" % (
            key,
            inline_value,
            digest,
        )
    else:
        block = "%s: %s\n  - path: docs/intent.md\n    sha256: %s\n" % (
            key,
            inline_value,
            digest,
        )
    document = root / "doc.md"
    document.write_text(_document([block]), encoding="utf-8")
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 5
    assert payload["status"] == "failed"
    report = payload["files"][str(document)]
    assert any(item["key"] == key for item in report["invalid"])


def test_body_references_are_not_extracted(tmp_path, capsys):
    """境界10：front matter終端後の本文にあるpath＋hexは抽出しない（non_scope）。"""

    module = _module()
    root = tmp_path / "root"
    root.mkdir()
    digest = _write_target(root, "docs/intent.md", "intent\n")
    body = (
        "| file | SHA-256 |\n"
        "| --- | --- |\n"
        "| `docs/intent.md` | `%s` |\n" % ("d" * 64)
    )
    document = root / "doc.md"
    document.write_text(
        _document(
            [_mapping_block("intent_ref", "docs/intent.md", digest)],
            body=body,
        ),
        encoding="utf-8",
    )
    allowlist = _write_allowlist(tmp_path)

    exit_code, payload = _run(
        module,
        capsys,
        (document,),
        allowlist=allowlist,
        root=root,
    )

    assert exit_code == 0
    assert payload["totals"]["checked"] == 1
