import hashlib
import importlib
import json
from pathlib import Path
import stat
import types


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _module():
    return importlib.import_module(
        "tools.deployment.installed.trusted_review_send_dispatch"
    )


def test_capabilities_add_only_fixed_claude_bootstrap_role():
    module = _module()
    base = {
        "status": "capabilities",
        "schema_version": "trusted-review-send-v1",
        "roles": {
            "post_write_small": {
                "model": "gpt-5.6-terra",
                "purpose": "post_write_small_independent",
                "topology": "post_write_independent_single",
            }
        },
    }

    result = module.with_claude_capability(base)

    assert result["roles"]["post_write_small"] == base["roles"]["post_write_small"]
    assert result["roles"]["claude_session_bootstrap"] == {
        "model": "claude-fable-5",
        "purpose": "codex-pilot-no-tool-claude-bootstrap",
        "topology": "same_session_two_payload",
    }
    assert result["roles"]["claude_implementation_executor"] == {
        "model": "from-approved-launch",
        "purpose": "claude_implementation_executor",
        "topology": "same_session_test_then_implementation",
    }
    assert base["roles"].get("claude_session_bootstrap") is None
    assert base["roles"].get("claude_implementation_executor") is None


def test_dispatch_accepts_only_fixed_claude_inputs(monkeypatch, capsys):
    module = _module()
    calls = []
    fake_bootstrap = types.SimpleNamespace(
        run_approved_no_tool_bootstrap=lambda digest, approval_id: calls.append(
            (digest, approval_id)
        )
        or {
            "schema_version": 1,
            "result": "succeeded",
        }
    )
    monkeypatch.setattr(module, "_load_bootstrap", lambda root: fake_bootstrap)

    exit_code = module.main(
        [
            "claude-bootstrap",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--manifest-digest",
            "a" * 64,
            "--approval-id",
            "RC3-CB-APPROVAL-TEST",
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    assert exit_code == 0
    assert calls == [("a" * 64, "RC3-CB-APPROVAL-TEST")]
    assert json.loads(capsys.readouterr().out)["result"] == "succeeded"

    calls.clear()
    exit_code = module.main(
        [
            "claude-bootstrap",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--manifest-digest",
            "a" * 64,
            "--approval-id",
            "RC3-CB-APPROVAL-TEST",
            "--model",
            "other",
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    assert exit_code == 2
    assert calls == []


def test_workspace_project_identity_mismatch_stops_before_loading(tmp_path):
    module = _module()
    workspace = tmp_path / "workspace"
    manifest = workspace / ".reviewcompass/project-manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps({"project_id": "other-project"}),
        encoding="utf-8",
    )

    try:
        module._validate_workspace(workspace)
    except ValueError as error:
        assert str(error) == "trusted workspace invalid"
    else:
        raise AssertionError("other project must be rejected")


def test_non_claude_commands_remain_owned_by_existing_trusted_sender():
    module = _module()
    calls = []

    exit_code = module.main(
        ["--manifest", "existing.yaml", "--dry-run"],
        base_main=lambda argv: calls.append(tuple(argv)) or 7,
        base_capabilities=lambda: {},
    )

    assert exit_code == 7
    assert calls == [("--manifest", "existing.yaml", "--dry-run")]


def test_dispatch_records_fixed_claude_implementation_inputs(
    tmp_path, monkeypatch, capsys
):
    module = _module()
    calls = []
    outcome = {"schema_version": 1, "run_id": "run-001", "state": "recorded"}
    fake_route = types.SimpleNamespace(
        record_turn=lambda *arguments: calls.append(arguments) or outcome
    )
    monkeypatch.setattr(module, "_load_implementation", lambda root: fake_route)
    repository = tmp_path / "repository"
    private_root = tmp_path / "private"
    launch = tmp_path / "launch.json"
    raw = tmp_path / "raw.json"

    exit_code = module.main(
        [
            "claude-implementation-record",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--repository",
            str(repository),
            "--private-root",
            str(private_root),
            "--run-id",
            "run-001",
            "--turn",
            "implementation",
            "--launch-record",
            str(launch),
            "--raw-file",
            str(raw),
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert captured.out.count("\n") == 1
    assert json.loads(captured.out) == outcome
    assert calls == [
        (
            repository,
            private_root,
            "run-001",
            "implementation",
            launch,
            raw,
        )
    ]


def test_dispatch_executes_one_fixed_claude_implementation_turn(
    tmp_path, monkeypatch, capsys
):
    module = _module()
    calls = []
    outcome = {
        "schema_version": 1,
        "run_id": "run-001",
        "state": "ready_for_implementation_turn",
    }
    fake_executor = types.SimpleNamespace(
        execute_turn=lambda *arguments: calls.append(arguments) or outcome
    )
    monkeypatch.setattr(module, "_load_executor", lambda root: fake_executor)
    repository = tmp_path / "repository"
    private_root = tmp_path / "private"

    exit_code = module.main(
        [
            "claude-implementation-execute",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--repository",
            str(repository),
            "--private-root",
            str(private_root),
            "--run-id",
            "run-001",
            "--turn",
            "test",
            "--approval-id",
            "RC3-CD-SEND-APPROVAL-001",
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert captured.out.count("\n") == 1
    assert json.loads(captured.out) == outcome
    assert calls == [
        (
            repository,
            private_root,
            "run-001",
            "test",
            "RC3-CD-SEND-APPROVAL-001",
        )
    ]


def test_dispatch_blocks_invalid_execute_arguments_before_loading(
    tmp_path, monkeypatch, capsys
):
    module = _module()
    loaded = []
    monkeypatch.setattr(
        module,
        "_load_executor",
        lambda root: loaded.append(root),
        raising=False,
    )

    exit_code = module.main(
        [
            "claude-implementation-execute",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--repository",
            "relative/repository",
            "--private-root",
            str(tmp_path / "private"),
            "--run-id",
            "run-001",
            "--turn",
            "review",
            "--approval-id",
            "RC3-CD-SEND-APPROVAL-001",
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    assert exit_code == 2
    assert loaded == []
    assert json.loads(capsys.readouterr().out) == {
        "schema_version": 1,
        "result": "stopped",
        "stop_code": "trusted_transport_unavailable",
    }


def test_dispatch_blocks_invalid_implementation_arguments_before_loading(
    tmp_path, monkeypatch, capsys
):
    module = _module()
    loaded = []
    monkeypatch.setattr(
        module,
        "_load_implementation",
        lambda root: loaded.append(root),
    )

    exit_code = module.main(
        [
            "claude-implementation-record",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--repository",
            "relative/repository",
            "--private-root",
            str(tmp_path / "private"),
            "--run-id",
            "run-001",
            "--turn",
            "review",
            "--launch-record",
            str(tmp_path / "launch.json"),
            "--raw-file",
            str(tmp_path / "raw.json"),
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    assert exit_code == 2
    assert loaded == []
    assert json.loads(capsys.readouterr().out) == {
        "schema_version": 1,
        "result": "stopped",
        "stop_code": "trusted_transport_unavailable",
    }


def test_dispatch_blocks_implementation_stop_and_exception_without_detail(
    tmp_path, monkeypatch, capsys
):
    module = _module()

    class FakeStop(Exception):
        pass

    arguments = [
        "claude-implementation-record",
        "--workspace-root",
        str(PROJECT_ROOT),
        "--repository",
        str(tmp_path / "repository"),
        "--private-root",
        str(tmp_path / "private"),
        "--run-id",
        "run-001",
        "--turn",
        "test",
        "--launch-record",
        str(tmp_path / "launch.json"),
        "--raw-file",
        str(tmp_path / "raw.json"),
    ]
    for error in (FakeStop("secret-one"), RuntimeError("secret-two")):
        fake_route = types.SimpleNamespace(
            RouteStop=FakeStop,
            record_turn=lambda *values, current=error: (_ for _ in ()).throw(current),
        )
        monkeypatch.setattr(
            module,
            "_load_implementation",
            lambda root, current=fake_route: current,
        )

        exit_code = module.main(
            arguments,
            base_main=lambda argv: 99,
            base_capabilities=lambda: {},
        )
        output = capsys.readouterr().out

        assert exit_code == 2
        assert "secret" not in output
        assert json.loads(output)["stop_code"] == "trusted_transport_unavailable"


def test_administrator_install_is_fixed_backed_up_and_post_verified(
    tmp_path, monkeypatch
):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    source_dispatch = (
        source_root
        / "tools/deployment/installed/trusted_review_send_dispatch.py"
    )
    source_wrapper = (
        source_root / "tools/deployment/installed/trusted-review-send"
    )
    target_dispatch = (
        install_root
        / "tools/api_providers/trusted_review_send_dispatch.py"
    )
    target_base = (
        install_root / "tools/api_providers/trusted_review_send.py"
    )
    target_wrapper = install_root / "trusted-review-send"
    for path, content in (
        (source_dispatch, b"approved dispatch\n"),
        (source_wrapper, b"approved wrapper\n"),
        (target_base, b"existing trusted sender\n"),
        (target_wrapper, b"legacy wrapper\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    for relative in installer.TRUSTED_RUNTIME_FILES:
        path = source_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"approved {relative}\n".encode("utf-8"))
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(target_base.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(target_wrapper.read_bytes()).hexdigest(),
    )

    before = installer.deployment_status(
        install_root=install_root,
        source_root=source_root,
    )
    result = installer.install_trusted_transport(
        install_root=install_root,
        source_root=source_root,
        effective_user_id=0,
    )
    after = installer.deployment_status(
        install_root=install_root,
        source_root=source_root,
    )

    assert before["state"] == "claude_capability_missing"
    assert result["state"] == "ready"
    assert after["state"] == "ready"
    assert target_dispatch.read_bytes() == source_dispatch.read_bytes()
    assert target_wrapper.read_bytes() == source_wrapper.read_bytes()
    for relative in installer.TRUSTED_RUNTIME_FILES:
        assert (install_root / relative).read_bytes() == (
            source_root / relative
        ).read_bytes()
    assert (
        install_root / "trusted-review-send.pre-claude-bootstrap-v1"
    ).read_bytes() == b"legacy wrapper\n"
    assert stat.S_IMODE(target_dispatch.stat().st_mode) == 0o644
    assert stat.S_IMODE(target_wrapper.stat().st_mode) == 0o755


def _runtime_upgrade_fixture(tmp_path, monkeypatch, *, unknown=False):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    source_dispatch = (
        source_root
        / "tools/deployment/installed/trusted_review_send_dispatch.py"
    )
    source_wrapper = (
        source_root / "tools/deployment/installed/trusted-review-send"
    )
    target_dispatch = (
        install_root
        / "tools/api_providers/trusted_review_send_dispatch.py"
    )
    target_base = (
        install_root / "tools/api_providers/trusted_review_send.py"
    )
    target_wrapper = install_root / "trusted-review-send"
    backup_wrapper = (
        install_root / "trusted-review-send.pre-claude-bootstrap-v1"
    )
    for path, content in (
        (source_dispatch, b"approved dispatch\n"),
        (source_wrapper, b"approved wrapper\n"),
        (target_dispatch, b"approved dispatch\n"),
        (target_base, b"existing trusted sender\n"),
        (target_wrapper, b"approved wrapper\n"),
        (backup_wrapper, b"legacy wrapper\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    prior_digests = {}
    for index, relative in enumerate(installer.TRUSTED_RUNTIME_FILES):
        source = source_root / relative
        target = install_root / relative
        source.parent.mkdir(parents=True, exist_ok=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(f"approved {relative}\n".encode("utf-8"))
        prior = f"prior {relative}\n".encode("utf-8")
        target.write_bytes(
            b"unknown runtime\n" if unknown and index == 0 else prior
        )
        prior_digests[relative] = hashlib.sha256(prior).hexdigest()
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(target_base.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(backup_wrapper.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_PRIOR_RUNTIME_SHA256",
        prior_digests,
        raising=False,
    )
    return types.SimpleNamespace(
        installer=installer,
        source_root=source_root,
        install_root=install_root,
        backup_wrapper=backup_wrapper,
        first_runtime=install_root / installer.TRUSTED_RUNTIME_FILES[0],
    )


def test_administrator_install_updates_only_exact_pinned_prior_runtime(
    tmp_path, monkeypatch
):
    fixture = _runtime_upgrade_fixture(tmp_path, monkeypatch)

    before = fixture.installer.deployment_status(
        install_root=fixture.install_root,
        source_root=fixture.source_root,
    )
    result = fixture.installer.install_trusted_transport(
        install_root=fixture.install_root,
        source_root=fixture.source_root,
        effective_user_id=0,
    )

    assert result["state"] == "ready"
    for relative in fixture.installer.TRUSTED_RUNTIME_FILES:
        assert (fixture.install_root / relative).read_bytes() == (
            fixture.source_root / relative
        ).read_bytes()
    assert fixture.backup_wrapper.read_bytes() == b"legacy wrapper\n"


def test_new_implementation_runtime_and_exact_prior_dispatch_are_upgraded(
    tmp_path, monkeypatch
):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    assert installer.EXPECTED_PRIOR_DISPATCH_SHA256 == (
        "ee6bf62f8c5e57f1c262176cc92dabffae3f487debcfd04e2f1283b88a362ef7"
    )
    assert Path("tools/development/claude_implementation_route.py") in (
        installer.TRUSTED_RUNTIME_FILES
    )
    assert Path("tools/development/claude_implementation_executor.py") in (
        installer.TRUSTED_RUNTIME_FILES
    )
    assert Path("tools/bootstrap/immutable_result_store.py") in (
        installer.TRUSTED_RUNTIME_FILES
    )

    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    source_dispatch = source_root / installer._SOURCE_DISPATCH
    source_wrapper = source_root / installer._SOURCE_WRAPPER
    target_dispatch = install_root / installer._TARGET_DISPATCH
    target_base = install_root / installer._TARGET_BASE
    target_wrapper = install_root / installer._TARGET_WRAPPER
    backup_wrapper = install_root / installer._BACKUP_WRAPPER
    prior_dispatch = b"exact prior dispatch\n"
    for path, content in (
        (source_dispatch, b"new dispatch\n"),
        (source_wrapper, b"current wrapper\n"),
        (target_dispatch, prior_dispatch),
        (target_base, b"base\n"),
        (target_wrapper, b"current wrapper\n"),
        (backup_wrapper, b"legacy wrapper\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    new_runtime = {
        Path("tools/development/claude_implementation_route.py"),
        Path("tools/development/claude_implementation_executor.py"),
        Path("tools/bootstrap/immutable_result_store.py"),
    }
    prior_digests = {}
    for relative in installer.TRUSTED_RUNTIME_FILES:
        source = source_root / relative
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(f"new {relative}\n".encode())
        if relative not in new_runtime:
            target = install_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            prior = f"prior {relative}\n".encode()
            target.write_bytes(prior)
            prior_digests[relative] = hashlib.sha256(prior).hexdigest()
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(b"base\n").hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(b"legacy wrapper\n").hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_PRIOR_DISPATCH_SHA256",
        hashlib.sha256(prior_dispatch).hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_PRIOR_RUNTIME_SHA256",
        prior_digests,
    )

    before = installer.deployment_status(
        install_root=install_root,
        source_root=source_root,
    )
    assert before["state"] == "trusted_runtime_update_required"
    result = installer.install_trusted_transport(
        install_root=install_root,
        source_root=source_root,
        effective_user_id=0,
    )

    assert result["state"] == "ready"
    assert target_dispatch.read_bytes() == b"new dispatch\n"
    for relative in installer.TRUSTED_RUNTIME_FILES:
        assert (install_root / relative).read_bytes() == (
            source_root / relative
        ).read_bytes()


def test_install_refuses_unknown_existing_runtime(tmp_path, monkeypatch):
    fixture = _runtime_upgrade_fixture(tmp_path, monkeypatch, unknown=True)

    try:
        fixture.installer.install_trusted_transport(
            install_root=fixture.install_root,
            source_root=fixture.source_root,
            effective_user_id=0,
        )
    except ValueError as error:
        assert str(error) == "installed trusted entry mismatch"
    else:
        raise AssertionError("unknown installed runtime must not be overwritten")

    assert fixture.first_runtime.read_bytes() == b"unknown runtime\n"


def test_install_refuses_dangling_runtime_symlink_without_writing_backup(
    tmp_path, monkeypatch
):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    paths = {
        source_root
        / "tools/deployment/installed/trusted_review_send_dispatch.py": b"dispatch\n",
        source_root / "tools/deployment/installed/trusted-review-send": b"wrapper\n",
        install_root
        / "tools/api_providers/trusted_review_send.py": b"base\n",
        install_root / "trusted-review-send": b"legacy wrapper\n",
    }
    for path, content in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    for relative in installer.TRUSTED_RUNTIME_FILES:
        source = source_root / relative
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(f"approved {relative}\n".encode("utf-8"))
    dangling = install_root / installer.TRUSTED_RUNTIME_FILES[0]
    dangling.parent.mkdir(parents=True, exist_ok=True)
    dangling.symlink_to(tmp_path / "missing-runtime")
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(b"base\n").hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(b"legacy wrapper\n").hexdigest(),
    )
    backup = install_root / "trusted-review-send.pre-claude-bootstrap-v1"

    before = installer.deployment_status(
        install_root=install_root,
        source_root=source_root,
    )
    try:
        installer.install_trusted_transport(
            install_root=install_root,
            source_root=source_root,
            effective_user_id=0,
        )
    except ValueError as error:
        assert str(error) == "installed trusted entry mismatch"
    else:
        raise AssertionError("dangling runtime symlink must be rejected")

    assert before["state"] == "installed_mismatch"
    assert dangling.is_symlink()
    assert not backup.exists()


def test_install_refuses_unreviewed_existing_entry(tmp_path, monkeypatch):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    paths = {
        source_root
        / "tools/deployment/installed/trusted_review_send_dispatch.py": b"dispatch\n",
        source_root / "tools/deployment/installed/trusted-review-send": b"wrapper\n",
        install_root
        / "tools/api_providers/trusted_review_send.py": b"base\n",
        install_root / "trusted-review-send": b"unknown wrapper\n",
    }
    for path, content in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    for relative in installer.TRUSTED_RUNTIME_FILES:
        path = source_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"approved {relative}\n".encode("utf-8"))
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(b"base\n").hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(b"different wrapper\n").hexdigest(),
    )

    try:
        installer.install_trusted_transport(
            install_root=install_root,
            source_root=source_root,
            effective_user_id=0,
        )
    except ValueError as error:
        assert str(error) == "installed trusted entry mismatch"
    else:
        raise AssertionError("unknown installed entry must not be overwritten")

    assert (install_root / "trusted-review-send").read_bytes() == b"unknown wrapper\n"


def test_transport_status_and_install_have_one_public_command_entry():
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert (
        'reviewcompass3-trusted-transport = '
        '"tools.deployment.trusted_claude_transport:main"'
    ) in pyproject
