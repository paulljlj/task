"""示例 CLI - 中文任务仓库入口"""

from __future__ import annotations

import os
import sys
import argparse

try:
    from .tracing import init_tracing, trace
    from .trace_utils import tail_traces
except Exception:
    from src.tracing import init_tracing, trace
    from src.trace_utils import tail_traces


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(prog="sample-cli-cn")
    parser.add_argument("--dump-traces", type=int, help="打印最近 N 条 trace 后退出")
    subparsers = parser.add_subparsers(dest="command")

    greet = subparsers.add_parser("greet")
    greet.add_argument("--name", required=True)

    args = parser.parse_args(argv)

    trace_path = os.environ.get("TRACE_LOG_PATH", "repo/logs/trace.jsonl")
    # 初始化时不指定轮转参数（可由调用者扩展）
    init_tracing(trace_path)

    # 支持快速查看最近 N 条 trace
    if getattr(args, "dump_traces", None):
        n = int(getattr(args, "dump_traces"))
        items = tail_traces(trace_path, n)
        for it in items:
            print(it)
        return 0

    try:
        trace("command_start", span="cli", command=args.command or "", name=getattr(args, "name", ""))
        if args.command == "greet":
            print(f"你好, {args.name}!")
        trace("command_end", span="cli", command=args.command or "", name=getattr(args, "name", ""))
    except Exception as e:
        trace("command_error", span="cli", command=getattr(args, "command", ""), error=str(e), level="error")
        raise

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
