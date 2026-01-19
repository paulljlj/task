"""
验证脚本：verify_auto_tracking_log_cn.py
用于验证 `自动生成跟踪日志任务（追踪记录与归档）` 的实现。
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO_DIR = Path("repo")
TRACING_PY = REPO_DIR / "src" / "tracing.py"
MAIN_PY = REPO_DIR / "src" / "main.py"
DOC_MD = REPO_DIR / "docs" / "TRACE_LOG.md"
README_MD = REPO_DIR / "README.md"


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"Missing required file: {p.as_posix()}")
    except Exception as e:
        fail(f"Cannot read file {p.as_posix()}: {e}")


def assert_regex(text: str, pattern: str, what: str) -> None:
    if not re.search(pattern, text, flags=re.MULTILINE):
        fail(f"Missing pattern for {what}: /{pattern}/")


def main() -> None:
    if not REPO_DIR.exists():
        fail("Missing repo/ directory")
    ok("repo/ directory exists")

    tracing_src = read_text(TRACING_PY)
    main_src = read_text(MAIN_PY)
    doc_src = read_text(DOC_MD)
    readme_src = read_text(README_MD)

    ok("All required files exist and are readable")

    # tracing.py checks
    assert_regex(tracing_src, r"def\s+init_tracing\s*\(", "tracing.py:init_tracing")
    assert_regex(tracing_src, r"def\s+trace\s*\(", "tracing.py:trace")
    # rotation params
    assert_regex(tracing_src, r"max_bytes", "tracing.py:init_tracing:max_bytes")
    assert_regex(tracing_src, r"backup_count", "tracing.py:init_tracing:backup_count")
    assert_regex(tracing_src, r"json\.dumps\s*\(", "tracing.py:json.dumps")
    assert_regex(tracing_src, r"uuid\.uuid4\s*\(", "tracing.py:uuid4")
    assert_regex(tracing_src, r"open\([^\\n]*['\"]a['\"]", "tracing.py:append open('a')")
    assert_regex(
        tracing_src,
        r"(os\.makedirs\s*\(|Path\([^\\n]*\)\.parent\.mkdir\s*\()",
        "tracing.py:ensure parent dir exists",
    )
    for key in ["timestamp", "trace_id", "span", "event"]:
        if key not in tracing_src:
            fail(f"tracing.py should include required field key '{key}'")
    # level field required
    if "level" not in tracing_src:
        fail("tracing.py should include 'level' field support in trace()")
    ok("tracing.py contains required functions and key behaviors")

    # main.py checks
    if "TRACE_LOG_PATH" not in main_src:
        fail("main.py must reference env var TRACE_LOG_PATH")

    assert_regex(
        main_src,
        r"(from\s+\.\s*tracing\s+import|from\s+src\.tracing\s+import|import\s+src\.tracing|import\s+tracing)",
        "main.py:imports tracing",
    )
    assert_regex(main_src, r"init_tracing\s*\(", "main.py:calls init_tracing")
    assert_regex(main_src, r"trace\s*\([^\\n]*command_start", "main.py:trace command_start")
    assert_regex(main_src, r"trace\s*\([^\\n]*command_end", "main.py:trace command_end")
    assert_regex(main_src, r"command_error", "main.py:trace command_error")
    # CLI dump traces
    assert_regex(main_src, r"--dump-traces", "main.py:--dump-traces flag")
    assert_regex(main_src, r"tail_traces|trace_utils", "main.py:uses trace_utils.tail_traces")

    ok("main.py integrates tracing and emits start/end/error events")

    # docs checks
    for kw in ["JSONL", "TRACE_LOG_PATH", "timestamp", "trace_id", "span", "event"]:
        if kw not in doc_src:
            fail(f"docs/TRACE_LOG.md must mention '{kw}'")
    # docs must mention rotation, level and dump
    for kw in ["轮转", "max_bytes", "backup_count", "level", "--dump-traces"]:
        if kw not in doc_src and kw.lower() not in doc_src.lower():
            fail(f"docs/TRACE_LOG.md must mention '{kw}'")
    ok("docs/TRACE_LOG.md includes required explanations and fields")

    if "TRACE_LOG_PATH" not in readme_src:
        fail("README.md must mention TRACE_LOG_PATH usage")
    ok("README.md updated with TRACE_LOG_PATH")

    print("\nSUCCESS: 本任务的基本要求已满足。")


if __name__ == "__main__":
    main()
