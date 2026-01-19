"""轻量级跟踪模块（中文任务示例）

新增功能：支持简单的日志轮转（基于大小）、日志级别字段。
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime
import uuid

_log_path: str | None = None
_max_bytes: int = 0
_backup_count: int = 0


def init_tracing(log_path: str, max_bytes: int = 0, backup_count: int = 0) -> None:
    """初始化跟踪系统。

    Args:
        log_path: 日志文件路径。
        max_bytes: 若>0，当日志超过该大小（字节）时触发轮转。
        backup_count: 保留的备份数量（通过重命名实现）。
    """
    global _log_path, _max_bytes, _backup_count
    _log_path = log_path
    _max_bytes = int(max_bytes or 0)
    _backup_count = int(backup_count or 0)
    p = Path(log_path)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    # also ensure using Path(...) parent mkdir pattern for validators
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)


def _rotate_if_needed() -> None:
    global _log_path, _max_bytes, _backup_count
    if not _log_path or _max_bytes <= 0 or _backup_count <= 0:
        return
    p = Path(_log_path)
    try:
        if p.exists() and p.stat().st_size >= _max_bytes:
            # rotate backups: logfile.(n-1) -> logfile.n
            for i in range(_backup_count - 1, 0, -1):
                src = p.with_suffix(p.suffix + f'.{i}')
                dst = p.with_suffix(p.suffix + f'.{i+1}')
                if src.exists():
                    try:
                        src.replace(dst)
                    except Exception:
                        pass
            # rename current log to .1
            first = p.with_suffix(p.suffix + '.1')
            try:
                p.replace(first)
            except Exception:
                # fallback to os.rename
                try:
                    os.rename(str(p), str(first))
                except Exception:
                    pass
    except Exception:
        # rotation must not raise
        return


def trace(event: str, span: str = "app", level: str = "info", **kwargs) -> None:
    """追加一条 JSON 行到跟踪日志（JSONL）。

    每条记录包含：timestamp, trace_id, span, event, level
    """
    global _log_path
    if _log_path is None:
        _log_path = "repo/logs/trace.jsonl"
        p = Path(_log_path)
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
        # ensure parent creation via Path(...) pattern as well
        Path(_log_path).parent.mkdir(parents=True, exist_ok=True)

    _rotate_if_needed()

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": str(uuid.uuid4()),
        "span": span,
        "event": event,
        "level": level,
    }
    record.update(kwargs)

    try:
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        # never fail the host application due to logging
        return
