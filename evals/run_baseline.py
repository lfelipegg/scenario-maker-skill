#!/usr/bin/env python3
"""Capture the fixed Phase 1 baseline. Scoring and human review are separate."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import tarfile
import tempfile
import time
from datetime import datetime, timezone

BASELINE = "5fcc3d0eded83c6a9aaf472a1dc8d5ce24011d9d"
MODEL = "openai-codex/gpt-6-astra"
ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
TOOLS = "read,grep,glob,bash,write"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def capture(case, repetition, snapshot, destination, timeout, scratch):
    evidence = destination / case["id"] / f"attempt-{repetition}"
    evidence.mkdir(parents=True)
    workspace = scratch / case["id"] / f"attempt-{repetition}"
    workspace.mkdir(parents=True)
    # Each attempt has independent script/cache paths. Large immutable CSVs use
    # hardlinks; the selected skill is never an authorized write destination.
    shutil.copytree(snapshot, workspace / "selected-skill", copy_function=os.link)
    for fixture in case["fixtures"]:
        source = EVALS / "fixtures" / fixture
        target = workspace / "fixtures" / fixture
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    prompt = "Use the explicitly selected Scenario Maker skill in ./selected-skill/SKILL.md.\n\n" + case["request"]
    if case["fixtures"]:
        prompt += "\n\nSupplied local fixtures: " + ", ".join("fixtures/" + name for name in case["fixtures"])
    (evidence / "request.txt").write_text(prompt, encoding="utf-8")
    command = ["omp", "--cwd", str(workspace), "--print", "--mode", "json",
               "--model", MODEL, "--thinking", "high", "--no-session", "--no-title",
               "--no-prewalk", "--no-skills", "--no-rules", "--no-extensions",
               "--no-lsp", "--no-pty", "--tools", TOOLS, "--approval-mode", "yolo",
               "--config", str(EVALS / "omp-config.json"),
               "--system-prompt", str(EVALS / "generator-system.txt"),
               "--extension", str(EVALS / "capture.ts"), "--max-time", f"{timeout}s", prompt]
    environment = os.environ.copy()
    environment.update(EVAL_CONTEXT_FILE=str(evidence / "context.jsonl"),
                       EVAL_SYSTEM_FILE=str(EVALS / "generator-system.txt"),
                       PYTHONDONTWRITEBYTECODE="1", TZ="UTC", LC_ALL="C.UTF-8")
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    status, exit_code, error = "error", None, None
    with (evidence / "trace.jsonl").open("wb") as stdout, (evidence / "stderr.txt").open("wb") as stderr:
        try:
            process = subprocess.Popen(command, cwd=workspace, env=environment,
                                       stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                exit_code = process.wait(timeout=timeout + 30)
                status = "completed" if exit_code == 0 else "error"
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                exit_code, status, error = process.returncode, "timeout", "outer capture deadline"
        except OSError as exc:
            error = str(exc)
    events, malformed = [], []
    for index, line in enumerate((evidence / "trace.jsonl").read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            malformed.append(index)
    messages = [event.get("message", {}) for event in events if event.get("type") == "message_end"]
    assistant = [m for m in messages if m.get("role") == "assistant"]
    text_messages = [m for m in assistant if any(c.get("type") == "text" for c in m.get("content", []))
                     and not any(c.get("type") == "toolCall" for c in m.get("content", []))]
    final = [m for m in text_messages if m.get("stopReason") == "stop"]
    output_path, partial_path = None, None
    if final:
        output_path = "output.txt"
        (evidence / output_path).write_text("".join(c["text"] for c in final[-1]["content"] if c.get("type") == "text"), encoding="utf-8")
    elif text_messages:
        partial_path = "partial-output.txt"
        (evidence / partial_path).write_text("".join(c["text"] for c in text_messages[-1]["content"] if c.get("type") == "text"), encoding="utf-8")
    model_errors = [m.get("errorMessage", m.get("stopReason")) for m in assistant
                    if m.get("stopReason") in ("error", "aborted")]
    if model_errors and status == "completed":
        status = "error"
    started_calls = {e.get("toolCallId") for e in events if e.get("type") == "tool_execution_start"}
    ended_calls = {e.get("toolCallId") for e in events if e.get("type") == "tool_execution_end"}
    trace_complete = bool(not malformed and started_calls == ended_calls
                          and any(e.get("type") == "agent_end" and e.get("isTerminal") is True for e in events))
    artifacts = []
    fixture_set = {"fixtures/" + name for name in case["fixtures"]}
    for path in sorted(workspace.rglob("*")):
        relative = path.relative_to(workspace)
        if not path.is_file() or path.is_symlink() or relative.parts[0] in ("selected-skill", ".omp", ".git") or relative.as_posix() in fixture_set:
            continue
        stored = Path("artifacts") / relative
        target = evidence / stored
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        artifacts.append({"path": relative.as_posix(), "stored_path": stored.as_posix(),
                          "sha256": digest(target), "bytes": target.stat().st_size})
    contexts = []
    context_file = evidence / "context.jsonl"
    if context_file.exists():
        for line in context_file.read_text(encoding="utf-8").splitlines():
            contexts.append(json.loads(line))
    actual = [c for c in contexts if c.get("type") == "eval_context"]
    record = {"case_id": case["id"], "attempt": repetition, "revision": BASELINE,
              "started_at": started, "elapsed_seconds": round(time.monotonic() - start, 3),
              "command": command, "cwd": str(workspace),
              "execution": {"status": status, "exit_code": exit_code, "error": error,
                            "model_errors": model_errors, "malformed_trace_lines": malformed},
              "raw": {"output": output_path, "partial_output": partial_path, "trace": "trace.jsonl", "stderr": "stderr.txt",
                      "context": "context.jsonl" if context_file.exists() else None},
              "trace_complete": trace_complete, "artifacts": artifacts,
              "observed_context": actual,
              "raw_checksums": {p.name: digest(p) for p in evidence.iterdir() if p.is_file()}}
    save_json(evidence / "attempt.json", record)
    print(json.dumps({"case": case["id"], "attempt": repetition, "status": status,
                      "output": output_path is not None, "trace_complete": trace_complete}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="New evidence directory; existing paths are refused")
    parser.add_argument("--smoke", action="store_true", help="One separate capture exercise, never baseline acceptance")
    parser.add_argument("--timeout", type=int, default=300, help="OMP deadline per attempt in seconds")
    parser.add_argument("--jobs", type=int, default=3, help="Maximum concurrent fresh OMP sessions")
    args = parser.parse_args()
    if args.timeout < 1 or args.jobs < 1:
        parser.error("timeout and jobs must be positive")
    cases = ([{"id": "capture-smoke", "request": "Read the selected skill and its applicable prompt-type reference. Write one very short still-image prompt about a red cube on a gray surface to outputs/smoke.txt. Report the saved path.", "fixtures": []}]
             if args.smoke else [json.loads(line) for line in (EVALS / "cases.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()])
    if not args.smoke and (len(cases) != 16 or len({c["id"] for c in cases}) != 16):
        parser.error("baseline requires exactly sixteen distinct reviewed cases")
    for case in cases:
        if Path(case["id"]).name != case["id"] or case["id"] in (".", ".."):
            parser.error("unsafe case id")
        for fixture in case["fixtures"]:
            path = Path(fixture)
            if not path.parts or path.is_absolute() or ".." in path.parts:
                parser.error("fixtures must be inside evals/fixtures")
    destination = args.out.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    version = subprocess.run(["omp", "--help"], text=True, capture_output=True, check=True).stdout.splitlines()[0]
    provenance_files = ["generator-system.txt", "omp-config.json", "capture.ts", "run_baseline.py"]
    if not args.smoke:
        provenance_files += ["cases.jsonl", "rubric.md", "evaluate.py"]
    manifest = {"kind": "capture-smoke" if args.smoke else "original-phase-one-baseline",
                "created_at": datetime.now(timezone.utc).isoformat(), "baseline_revision": BASELINE,
                "candidate_revision": None, "omp_version": version, "model_requested": MODEL,
                "reasoning_requested": "high", "resolved_immutable_snapshot": None,
                "unknown_metadata": ["immutable provider snapshot", "provider seed", "system fingerprint", "hidden provider instructions"],
                "tools_requested": TOOLS.split(","), "permissions": "auto-approved local tools; not an OS sandbox",
                "environment": {"platform": platform.platform(), "python": platform.python_version(), "TZ": "UTC", "LC_ALL": "C.UTF-8"},
                "timeout_seconds": args.timeout, "jobs": args.jobs,
                "scheduling": "case-major submission, repetition ascending; completion order may differ",
                "attempts_per_case": 1 if args.smoke else 3,
                "evaluation_files": {name: digest(EVALS / name) for name in provenance_files},
                "fixtures": {name: digest(EVALS / "fixtures" / name) for c in cases for name in c["fixtures"]},
                "redactions": [], "trace_boundary": "OMP client JSON events and allowlisted provider request body fields; no headers/credentials"}
    save_json(destination / "manifest.json", manifest)
    with tempfile.TemporaryDirectory(prefix="scenario-maker-eval-") as temp:
        scratch = Path(temp)
        snapshot = scratch / "snapshot"
        snapshot.mkdir()
        archive = scratch / "baseline.tar"
        with archive.open("wb") as stream:
            subprocess.run(["git", "archive", BASELINE, "SKILL.md", "references", "scripts", "docs/danbooru_tags"],
                           cwd=ROOT, stdout=stream, check=True)
        with tarfile.open(archive) as bundle:
            bundle.extractall(snapshot, filter="data")
        archive.unlink()
        source_manifest = {p.relative_to(snapshot).as_posix(): digest(p) for p in sorted(snapshot.rglob("*")) if p.is_file()}
        save_json(destination / "selected-skill-files.json", source_manifest)
        for path in snapshot.rglob("*"):
            if path.is_file():
                path.chmod(0o444)
        records = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(capture, case, repetition, snapshot, destination, args.timeout, scratch)
                       for case in cases for repetition in range(1, 2 if args.smoke else 4)]
            for future in concurrent.futures.as_completed(futures):
                records.append(future.result())
        save_json(destination / "execution-summary.json", {
            "attempts": len(records), "completed": sum(r["execution"]["status"] == "completed" for r in records),
            "errors": sum(r["execution"]["status"] == "error" for r in records),
            "timeouts": sum(r["execution"]["status"] == "timeout" for r in records),
            "outputs": sum(r["raw"]["output"] is not None for r in records),
            "trace_complete": sum(r["trace_complete"] for r in records),
            "semantic_review": "not-run", "acceptance": "not assessed"})


if __name__ == "__main__":
    main()
