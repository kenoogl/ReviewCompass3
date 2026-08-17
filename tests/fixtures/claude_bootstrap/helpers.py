import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import subprocess
import types


_REAL_SUBPROCESS = types.SimpleNamespace(run=subprocess.run)
FIXTURE_ROOT = Path(__file__).parent
CONTRACT = json.loads(
    (FIXTURE_ROOT / "contract-v1.json").read_text(encoding="utf-8")
)
SUCCESS_RESULT = json.loads(
    (FIXTURE_ROOT / "success-result-v1.json").read_text(encoding="utf-8")
)
ERROR_RESULTS = [
    json.loads(path.read_text(encoding="utf-8"))
    for path in sorted(FIXTURE_ROOT.glob("error-*-v1.json"))
]
APPROVAL_ID = "RC3-CB-APPROVAL-20260811-TEST"
STORE_IDENTITY = "store-11111111-1111-4111-8111-111111111111"
PROJECT_ID = "reviewcompass3-bootstrap-test"
COMPLETION_REVIEW_ID = "RC3-CB-COMPLETION-REVIEW-TEST"
COMPLETION_REVIEW_RELATIVE_PATH = (
    "records/development/claude-bootstrap-completion-review-v1.json"
)


def canonical_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def write_json(path, value, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))
    if mode is not None:
        path.chmod(mode)


def run_git(repository, *arguments):
    return _REAL_SUBPROCESS.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )


class FakeCompletedProcess:
    def __init__(self, *, args, returncode=0, stdout="", stderr=""):
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FakeClaudeProcess:
    def __init__(self):
        self.calls = []
        self.payload_results = []
        self.trusted_transport_missing = False
        self.trusted_transport_ready = True
        self.fail_first_payload = False
        self.response_models = ["claude-fable-5", "claude-fable-5"]
        self.result_text_wrappers = ["raw", "raw"]
        self.result_outer_updates = [{}, {}]
        self.payload_stderr = ["", ""]

    @property
    def payload_calls(self):
        return [call for call in self.calls if "--print" in call["args"]]

    @property
    def preflight_calls(self):
        return [call for call in self.calls if "--print" not in call["args"]]

    def __call__(self, args, **kwargs):
        call = {
            "args": list(args),
            "cwd": kwargs.get("cwd"),
            "env": copy.deepcopy(kwargs.get("env")),
            "input": kwargs.get("input"),
            "shell": kwargs.get("shell", False),
        }
        self.calls.append(call)
        if call["shell"]:
            raise AssertionError("shell must remain disabled")
        if not isinstance(args, (list, tuple)):
            raise AssertionError("argv must be a structured sequence")
        if list(args) == [
            "/usr/local/libexec/reviewcompass/trusted-review-send",
            "--capabilities",
        ]:
            if self.trusted_transport_missing:
                raise FileNotFoundError("missing trusted sender")
            roles = {}
            if self.trusted_transport_ready:
                roles["claude_session_bootstrap"] = {
                    "model": "claude-fable-5",
                    "purpose": "codex-pilot-no-tool-claude-bootstrap",
                    "topology": "same_session_two_payload",
                }
            return FakeCompletedProcess(
                args=args,
                stdout=json.dumps(
                    {
                        "status": "capabilities",
                        "schema_version": "trusted-review-send-v1",
                        "roles": roles,
                    }
                ),
            )
        if "--version" in args:
            return FakeCompletedProcess(
                args=args,
                stdout="2.1.224 (Claude Code)\n",
            )
        if "auth" in args and "status" in args:
            return FakeCompletedProcess(
                args=args,
                stdout=json.dumps(
                    {
                        "loggedIn": True,
                        "authMethod": "claude.ai",
                        "apiProvider": "firstParty",
                    }
                ),
            )
        if "--print" not in args:
            raise AssertionError(f"unexpected process: {args}")
        if self.fail_first_payload and len(self.payload_calls) == 1:
            result = copy.deepcopy(ERROR_RESULTS[0])
            self.payload_results.append(result)
            return FakeCompletedProcess(args=args, returncode=1, stdout=json.dumps(result))
        result = copy.deepcopy(SUCCESS_RESULT)
        payload_index = len(self.payload_calls) - 1
        response_model = self.response_models[payload_index]
        usage = next(iter(result["modelUsage"].values()))
        result["modelUsage"] = {response_model: usage}
        if "--resume" in args:
            session_id = args[args.index("--resume") + 1]
            result["session_id"] = session_id
            result["uuid"] = "22222222-2222-4222-8222-222222222222"
            result["result"] = json.dumps(
                {
                    "protocol": "codex-pilot-claude-bootstrap-v1",
                    "continued": True,
                    "nonce": "RC3-CPC-20260811-A",
                    "reinvoke": False,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
        else:
            session_id = args[args.index("--session-id") + 1]
            result["session_id"] = session_id
        wrapper = self.result_text_wrappers[payload_index]
        if wrapper == "json_fence":
            result["result"] = f"```json\n{result['result']}\n```"
        elif wrapper == "prefixed":
            result["result"] = f"result follows\n{result['result']}"
        elif wrapper == "fenced_with_prefix":
            result["result"] = f"result follows\n```json\n{result['result']}\n```"
        elif wrapper == "double_fence":
            result["result"] = (
                f"```json\n```json\n{result['result']}\n```\n```"
            )
        result.update(self.result_outer_updates[payload_index])
        self.payload_results.append(result)
        return FakeCompletedProcess(
            args=args,
            stdout=json.dumps(result),
            stderr=self.payload_stderr[payload_index],
        )


class BootstrapScenario:
    def __init__(self, *, repository, home, runtime_root, manifest_path,
                 completion_review_path, decision_path, token_path, store_root,
                 work_directory, manifest_digest, target_commit, fake_process):
        self.repository = repository
        self.home = home
        self.runtime_root = runtime_root
        self.manifest_path = manifest_path
        self.completion_review_path = completion_review_path
        self.decision_path = decision_path
        self.token_path = token_path
        self.store_root = store_root
        self.work_directory = work_directory
        self.manifest_digest = manifest_digest
        self.target_commit = target_commit
        self.approval_id = APPROVAL_ID
        self.fake_process = fake_process

    def module(self):
        return importlib.import_module("tools.development.claude_bootstrap")

    def run(self):
        module = self.module()
        return module.run_approved_no_tool_bootstrap(
            self.manifest_digest,
            self.approval_id,
        )


def _manifest():
    return {
        "schema_version": 1,
        "record_kind": "approved_no_tool_claude_bootstrap_manifest",
        "purpose": CONTRACT["purpose"],
        "provider": CONTRACT["provider"],
        "model": CONTRACT["model"],
        "allowed_response_models": CONTRACT["allowed_response_models"],
        "claude_code_version": CONTRACT["claude_code_version"],
        "claude_executable_sha256": CONTRACT["claude_executable_sha256"],
        "payloads": CONTRACT["payloads"],
        "ordered_payload_sha256": CONTRACT["ordered_payload_sha256"],
        "material_policy": CONTRACT["material_policy"],
    }


def create_scenario(tmp_path, monkeypatch):
    tmp_path.mkdir(parents=True, exist_ok=True)
    repository = tmp_path / "repository"
    home = tmp_path / "home"
    repository.mkdir()
    home.mkdir()
    run_git(repository, "init", "-q")
    run_git(repository, "config", "user.email", "fixture@example.invalid")
    run_git(repository, "config", "user.name", "Fixture")

    project_manifest = repository / ".reviewcompass/project-manifest.json"
    write_json(
        project_manifest,
        {
            "schema_version": 1,
            "project_id": PROJECT_ID,
            "artifact_roots": {},
            "document_links": [],
        },
    )
    manifest_path = (
        repository
        / "records/development/claude-bootstrap-send-manifest-v1.json"
    )
    write_json(manifest_path, _manifest())
    manifest_digest = sha256_bytes(manifest_path.read_bytes())
    run_git(repository, "add", ".reviewcompass/project-manifest.json")
    run_git(
        repository,
        "add",
        "records/development/claude-bootstrap-send-manifest-v1.json",
    )
    run_git(repository, "commit", "-q", "-m", "fixture target")
    target_commit = run_git(repository, "rev-parse", "HEAD").stdout.strip()

    runtime_root = home / ".reviewcompass3"
    profile_root = runtime_root / "projects" / PROJECT_ID / "development"
    state_root = profile_root / "state"
    sensitive_root = profile_root / "sensitive"
    data_root = profile_root / "data"
    store_root = state_root / "claude-bootstrap" / "approval-store"
    work_directory = data_root / "claude-bootstrap" / "work"
    result_root = sensitive_root / "claude-bootstrap" / "runs" / APPROVAL_ID
    for path in (
        store_root / "pending",
        store_root / "claimed",
        store_root / "consumed",
        work_directory,
        result_root,
    ):
        path.mkdir(parents=True, exist_ok=True)
        path.chmod(0o700)
    store_root.chmod(0o700)
    write_json(
        store_root / "store.json",
        {
            "schema_version": 1,
            "store_identity": STORE_IDENTITY,
        },
        mode=0o600,
    )

    completion_review_path = repository / COMPLETION_REVIEW_RELATIVE_PATH
    completion_review = {
        "schema_version": 1,
        "record_kind": "claude_bootstrap_completion_review",
        "review_id": COMPLETION_REVIEW_ID,
        "status": "verified",
        "target_commit": target_commit,
        "manifest_sha256": manifest_digest,
        "ordered_payload_sha256": CONTRACT["ordered_payload_sha256"],
        "blocking_finding_count": 0,
    }
    write_json(completion_review_path, completion_review)
    decision_path = (
        repository
        / "records/development/claude-bootstrap-human-decision-v1.json"
    )
    decision = {
        "schema_version": 1,
        "record_kind": "human_claude_bootstrap_send_approval",
        "approved_by": "user",
        "approval_id": APPROVAL_ID,
        "store_identity": STORE_IDENTITY,
        "purpose": CONTRACT["purpose"],
        "provider": CONTRACT["provider"],
        "model": CONTRACT["model"],
        "allowed_response_models": CONTRACT["allowed_response_models"],
        "manifest_sha256": manifest_digest,
        "ordered_payload_sha256": CONTRACT["ordered_payload_sha256"],
        "claude_executable_sha256": CONTRACT["claude_executable_sha256"],
        "expires_at": "2999-12-31T23:59:59Z",
        "material_policy": CONTRACT["material_policy"],
        "result_root_identity": sha256_bytes(str(result_root).encode("utf-8")),
        "completion_review_id": COMPLETION_REVIEW_ID,
        "completion_review_path": COMPLETION_REVIEW_RELATIVE_PATH,
        "completion_review_sha256": sha256_bytes(
            completion_review_path.read_bytes()
        ),
        "completion_review_target_commit": target_commit,
    }
    write_json(decision_path, decision)
    token_path = store_root / "pending" / f"{APPROVAL_ID}.json"
    write_json(
        token_path,
        {
            "schema_version": 1,
            "approval_id": APPROVAL_ID,
            "decision_sha256": sha256_bytes(decision_path.read_bytes()),
            "store_identity": STORE_IDENTITY,
            "manifest_sha256": manifest_digest,
            "ordered_payload_sha256": CONTRACT["ordered_payload_sha256"],
            "provider": CONTRACT["provider"],
            "model": CONTRACT["model"],
            "allowed_response_models": CONTRACT["allowed_response_models"],
            "purpose": CONTRACT["purpose"],
            "claude_executable_sha256": CONTRACT["claude_executable_sha256"],
            "expires_at": "2999-12-31T23:59:59Z",
        },
        mode=0o600,
    )
    run_git(repository, "add", COMPLETION_REVIEW_RELATIVE_PATH)
    run_git(repository, "add", "records/development/claude-bootstrap-human-decision-v1.json")
    run_git(repository, "commit", "-q", "-m", "fixture approval")

    monkeypatch.chdir(repository)
    monkeypatch.setenv("HOME", str(home))
    for name in (
        "REVIEWCOMPASS3_RUNTIME_ROOT",
        "REVIEWCOMPASS3_STATE_ROOT",
        "REVIEWCOMPASS3_SENSITIVE_ROOT",
        "REVIEWCOMPASS3_DATA_ROOT",
    ):
        monkeypatch.delenv(name, raising=False)
    fake_process = FakeClaudeProcess()
    return BootstrapScenario(
        repository=repository,
        home=home,
        runtime_root=runtime_root,
        manifest_path=manifest_path,
        completion_review_path=completion_review_path,
        decision_path=decision_path,
        token_path=token_path,
        store_root=store_root,
        work_directory=work_directory,
        manifest_digest=manifest_digest,
        target_commit=target_commit,
        fake_process=fake_process,
    )


def install_fake_process(monkeypatch, scenario):
    module = scenario.module()
    monkeypatch.setattr(module.subprocess, "run", scenario.fake_process)
    return module


def rebind_manifest(scenario, mutator):
    manifest = json.loads(scenario.manifest_path.read_text(encoding="utf-8"))
    mutator(manifest)
    write_json(scenario.manifest_path, manifest)
    scenario.manifest_digest = sha256_bytes(scenario.manifest_path.read_bytes())
    completion_review = json.loads(
        scenario.completion_review_path.read_text(encoding="utf-8")
    )
    completion_review["manifest_sha256"] = scenario.manifest_digest
    write_json(scenario.completion_review_path, completion_review)
    decision = json.loads(scenario.decision_path.read_text(encoding="utf-8"))
    decision["manifest_sha256"] = scenario.manifest_digest
    decision["model"] = manifest["model"]
    decision["allowed_response_models"] = manifest["allowed_response_models"]
    decision["completion_review_sha256"] = sha256_bytes(
        scenario.completion_review_path.read_bytes()
    )
    write_json(scenario.decision_path, decision)
    token = json.loads(scenario.token_path.read_text(encoding="utf-8"))
    token["manifest_sha256"] = scenario.manifest_digest
    token["model"] = manifest["model"]
    token["allowed_response_models"] = manifest["allowed_response_models"]
    token["decision_sha256"] = sha256_bytes(scenario.decision_path.read_bytes())
    write_json(scenario.token_path, token, mode=0o600)
    for path in (
        scenario.manifest_path,
        scenario.completion_review_path,
        scenario.decision_path,
    ):
        run_git(scenario.repository, "add", str(path.relative_to(scenario.repository)))
    run_git(scenario.repository, "commit", "-q", "-m", "rebind fixture")


def rebind_completion_review(scenario, mutator):
    review = json.loads(
        scenario.completion_review_path.read_text(encoding="utf-8")
    )
    mutator(review)
    write_json(scenario.completion_review_path, review)
    decision = json.loads(scenario.decision_path.read_text(encoding="utf-8"))
    decision["completion_review_sha256"] = sha256_bytes(
        scenario.completion_review_path.read_bytes()
    )
    write_json(scenario.decision_path, decision)
    token = json.loads(scenario.token_path.read_text(encoding="utf-8"))
    token["decision_sha256"] = sha256_bytes(scenario.decision_path.read_bytes())
    write_json(scenario.token_path, token, mode=0o600)
    run_git(
        scenario.repository,
        "add",
        str(scenario.completion_review_path.relative_to(scenario.repository)),
    )
    run_git(
        scenario.repository,
        "add",
        str(scenario.decision_path.relative_to(scenario.repository)),
    )
    run_git(scenario.repository, "commit", "-q", "-m", "rebind review")


def rebind_decision(scenario, mutator):
    decision = json.loads(scenario.decision_path.read_text(encoding="utf-8"))
    mutator(decision)
    write_json(scenario.decision_path, decision)
    token = json.loads(scenario.token_path.read_text(encoding="utf-8"))
    token["decision_sha256"] = sha256_bytes(scenario.decision_path.read_bytes())
    write_json(scenario.token_path, token, mode=0o600)
    run_git(
        scenario.repository,
        "add",
        str(scenario.decision_path.relative_to(scenario.repository)),
    )
    run_git(scenario.repository, "commit", "-q", "-m", "rebind decision")


def assert_stop(result, code, scenario):
    assert result["schema_version"] == 1
    assert result["result"] == "stopped"
    assert result["stop_code"] == code
    assert result["payload_process_count"] == 0
    assert result["preflight_process_count"] >= 0
    assert result["approval_state"] in {"pending", "claimed", "consumed"}
    assert isinstance(result["recovery"], str) and result["recovery"]
    assert scenario.fake_process.payload_calls == []


def all_managed_paths(repository):
    output = run_git(repository, "ls-files").stdout
    return {line for line in output.splitlines() if line}


def assert_private_mode(path):
    assert stat.S_IMODE(path.stat().st_mode) in {0o600, 0o700}
