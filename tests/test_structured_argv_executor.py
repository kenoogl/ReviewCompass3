"""読み取り専用argv executor最小sliceのAcceptance Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-implement-read-only-argv-executor-slice.md
承認：DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001

承認範囲は次だけである。

- shell文字列を使わず、argv配列のまま読み取り専用操作を起動する経路。
- 実行templateは`git status --porcelain`だけ。`--`の後ろにpathspecを0個以上置ける。
- inventory／preflight／receiptは既存の`operation_routing`をそのまま使う。

このTestは実processを起動しない。runnerをfakeへ差し替え、呼出し回数、受け取ったargv、cwdを観測する。
"""

import importlib
import json
from pathlib import Path

import pytest


TEMPLATE = ["git", "status", "--porcelain"]
GRANTED_NONE = {"granted_permissions": []}


@pytest.fixture
def executor():
    return importlib.import_module("tools.development.structured_argv_executor")


@pytest.fixture
def routing():
    return importlib.import_module("tools.development.operation_routing")


class _FakeRunner:
    """呼出し回数、argv、cwdを記録する。報告文を根拠にしない。"""

    def __init__(self, returncode=0, stdout="", stderr=""):
        self.calls = []
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def __call__(self, argv, *, cwd):
        self.calls.append({"argv": argv, "cwd": cwd})
        return {
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def _operation(operation_id, argv, classification="read_only", summary="作業状態を読む"):
    return {
        "operation_id": operation_id,
        "classification": classification,
        "argv": list(argv),
        "summary": summary,
    }


def _inventory(routing, operations, inventory_id="OPINV-ARGV-001"):
    return routing.build_operation_inventory(
        inventory_id=inventory_id, inventory_version=1, operations=operations
    )


def _workspace(tmp_path):
    root = tmp_path / "project"
    (root / "records").mkdir(parents=True)
    (root / "records" / "keep.md").write_text("keep\n", encoding="utf-8")
    return root


def _run(executor, *, inventory, runner, project_root, cwd=".", attestation=None):
    return executor.run_read_only_operations(
        inventory=inventory,
        host_attestation=attestation or GRANTED_NONE,
        project_root=project_root,
        cwd=cwd,
        runner=runner,
    )


def _reject(executor, *, inventory, runner, project_root, cwd=".", attestation=None):
    with pytest.raises(executor.StructuredArgvExecutorError) as error:
        _run(
            executor, inventory=inventory, runner=runner,
            project_root=project_root, cwd=cwd, attestation=attestation,
        )
    assert runner.calls == [], "停止時にrunnerを一度も呼ばない"
    return error.value.code


# ------------------------------------------------------------------ 1. 正常例


def test_argv_reaches_the_runner_as_a_list_without_reshaping(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    pathspecs = [
        "records/keep.md",
        "path with space.md",
        'quote".md',
        "single'.md",
        "back`tick.md",
        "$HOME/var.md",
        "glob*.md",
        "日本語.md",
        "",
    ]
    argv = TEMPLATE + ["--"] + pathspecs
    inventory = _inventory(routing, [_operation("OP-001", argv)])
    runner = _FakeRunner(stdout=" M records/keep.md\n")

    receipt = _run(executor, inventory=inventory, runner=runner, project_root=root)

    assert len(runner.calls) == 1
    call = runner.calls[0]
    assert call["argv"] == argv, "文字列へ結合・展開・分割されない"
    assert isinstance(call["argv"], list)
    assert all(isinstance(item, str) for item in call["argv"])
    assert call["cwd"] == root.resolve()

    assert routing.validate_execution_receipt(receipt, inventory=inventory) is True
    assert [item["operation_id"] for item in receipt["results"]] == ["OP-001"]
    assert receipt["results"][0]["status"] == "completed"


def test_template_without_pathspec_is_accepted(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    inventory = _inventory(routing, [_operation("OP-001", TEMPLATE)])
    runner = _FakeRunner()

    receipt = _run(executor, inventory=inventory, runner=runner, project_root=root)

    assert [call["argv"] for call in runner.calls] == [TEMPLATE]
    assert routing.validate_execution_receipt(receipt, inventory=inventory) is True


def test_separator_with_no_pathspec_is_accepted(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    argv = TEMPLATE + ["--"]
    inventory = _inventory(routing, [_operation("OP-001", argv)])
    runner = _FakeRunner()

    _run(executor, inventory=inventory, runner=runner, project_root=root)

    assert [call["argv"] for call in runner.calls] == [argv]


# ------------------------------------------------------------------ 2. template外


def test_operations_outside_the_template_are_rejected(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    outside = {
        "別のsubcommand": ["git", "log", "--porcelain"],
        "前置option": ["git", "-C", "other", "status", "--porcelain"],
        "区切り前の余分な引数": ["git", "status", "--porcelain", "--short"],
        "区切り無しのpathspec": ["git", "status", "--porcelain", "records/keep.md"],
        "porcelain無し": ["git", "status"],
        "git以外": ["ls", "status", "--porcelain"],
        "区切りが二重": ["git", "status", "--porcelain", "--", "--", "x"],
    }
    for label, argv in outside.items():
        inventory = _inventory(routing, [_operation("OP-001", argv)])
        runner = _FakeRunner()
        assert _reject(
            executor, inventory=inventory, runner=runner, project_root=root
        ) == "template_mismatch", label


# ------------------------------------------------------------------ 3. 分類境界


def test_non_read_only_inventories_are_rejected(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    for classification in (
        "project_artifact_write", "git_metadata_write", "external", "unknown",
    ):
        inventory = _inventory(
            routing,
            [
                _operation("OP-001", TEMPLATE),
                _operation("OP-002", TEMPLATE, classification=classification),
            ],
        )
        runner = _FakeRunner()
        assert _reject(
            executor, inventory=inventory, runner=runner, project_root=root,
            attestation={
                "granted_permissions": ["git_metadata_write", "project_artifact_write"]
            },
        ) == "inventory_not_read_only", classification


# ------------------------------------------------------------------ 4. argv境界


def test_argv_shape_problems_are_rejected(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    inventory = _inventory(routing, [_operation("OP-001", TEMPLATE)])

    def _tampered(argv):
        document = json.loads(json.dumps(inventory))
        document["operations"][0]["argv"] = argv
        document["content_digest"] = routing.canonical_digest(document)
        return document

    # 空listと非文字列要素は、先に走るinventory validatorが拒否する。
    for label, argv in {
        "空list": [],
        "非文字列要素": ["git", 1, "--porcelain"],
    }.items():
        runner = _FakeRunner()
        assert _reject(
            executor, inventory=_tampered(argv), runner=runner, project_root=root
        ) == "inventory_invalid", label

    # 空文字列の実行fileはinventory validatorを通るため、executorが拒否する。
    runner = _FakeRunner()
    assert _reject(
        executor, inventory=_tampered(["", "status", "--porcelain"]), runner=runner,
        project_root=root,
    ) == "argv_invalid"

    # 空文字列のpathspecは有効な引数としてそのまま渡す。
    argv = TEMPLATE + ["--", ""]
    good = _inventory(routing, [_operation("OP-001", argv)])
    runner = _FakeRunner()
    _run(executor, inventory=good, runner=runner, project_root=root)
    assert runner.calls[0]["argv"] == argv


# ------------------------------------------------------------------ 5. cwd境界


def test_cwd_boundaries_are_enforced(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    inventory = _inventory(routing, [_operation("OP-001", TEMPLATE)])

    (root / "linked").symlink_to(root / "records")
    (root / "records" / "file.md").write_text("x\n", encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()

    for label, cwd in {
        "絶対path": str(root),
        "親への脱出": "..",
        "親経由の脱出": "records/../../outside",
        "symlink": "linked",
        "不在": "records/absent",
        "通常fileへの指定": "records/file.md",
    }.items():
        runner = _FakeRunner()
        assert _reject(
            executor, inventory=inventory, runner=runner, project_root=root, cwd=cwd
        ) == "cwd_invalid", label

    for accepted in (".", "records"):
        runner = _FakeRunner()
        _run(executor, inventory=inventory, runner=runner, project_root=root, cwd=accepted)
        assert runner.calls[0]["cwd"] == (root / accepted).resolve()


# ------------------------------------------------------------------ 6. preflight境界


def test_preflight_failures_never_reach_the_runner(executor, routing, tmp_path):
    root = _workspace(tmp_path)

    # inventoryのidentityが壊れていれば起動しない。
    inventory = _inventory(routing, [_operation("OP-001", TEMPLATE)])
    broken = dict(inventory, content_digest="0" * 64)
    runner = _FakeRunner()
    assert _reject(
        executor, inventory=broken, runner=runner, project_root=root
    ) == "inventory_digest_mismatch"

    # host attestationの語彙外は起動しない。
    runner = _FakeRunner()
    assert _reject(
        executor, inventory=inventory, runner=runner, project_root=root,
        attestation={"granted_permissions": ["superuser"]},
    ) == "host_attestation_invalid"


def test_executor_does_not_grant_or_reclassify_permissions(executor, routing, tmp_path):
    """read_onlyだけのinventoryは必要権限が空である。executorは権限を足さない。"""

    root = _workspace(tmp_path)
    inventory = _inventory(routing, [_operation("OP-001", TEMPLATE)])
    runner = _FakeRunner()

    receipt = _run(executor, inventory=inventory, runner=runner, project_root=root)

    assert receipt["preflight_ref"]["required_permissions"] == []
    assert receipt["preflight_ref"]["granted_permissions"] == []
    assert receipt["preflight_ref"]["verdict"] == "granted"
    assert receipt["preflight_ref"]["attestation_source"] == "host"


# ------------------------------------------------------------------ 7. 実行失敗


def test_process_failure_is_recorded_not_raised(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    inventory = _inventory(routing, [_operation("OP-001", TEMPLATE)])
    runner = _FakeRunner(returncode=128, stderr="fatal: not a repository\n")

    receipt = _run(executor, inventory=inventory, runner=runner, project_root=root)

    assert len(runner.calls) == 1
    assert receipt["results"][0]["status"] == "failed"
    assert "128" in receipt["results"][0]["detail"]
    assert routing.validate_execution_receipt(receipt, inventory=inventory) is True


def test_input_failure_and_process_failure_are_not_confused(executor, routing, tmp_path):
    root = _workspace(tmp_path)
    inventory = _inventory(routing, [_operation("OP-001", ["git", "log"])])
    runner = _FakeRunner(returncode=1)

    # 入力検証の失敗は例外であり、receiptを作らない。
    assert _reject(
        executor, inventory=inventory, runner=runner, project_root=root
    ) == "template_mismatch"

    # process結果の失敗は例外にせず、receiptへ記録する。
    good = _inventory(routing, [_operation("OP-001", TEMPLATE)])
    failing = _FakeRunner(returncode=1)
    receipt = _run(executor, inventory=good, runner=failing, project_root=root)
    assert receipt["results"][0]["status"] == "failed"


# ------------------------------------------------------------------ 8. source inspection


def test_module_never_builds_a_shell_string(executor):
    text = Path(executor.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "shell=True", "os.system", '" ".join(argv', "' '.join(argv",
        "shlex.join", "subprocess.getoutput",
    ):
        assert forbidden not in text


def test_module_declares_its_stop_codes(executor):
    for code in (
        "inventory_not_read_only", "template_mismatch", "argv_invalid", "cwd_invalid",
    ):
        assert code in executor.STOP_CODES
    assert executor.READ_ONLY_TEMPLATE == tuple(TEMPLATE)
