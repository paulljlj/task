"""日志工具：读取并解析 JSONL 跟踪日志的尾部记录"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict


def tail_traces(path: str, limit: int = 10) -> List[Dict]:
    """读取日志文件的最后若干行并返回解码后的 JSON 对象列表。

    如果某行无法解析为 JSON，则忽略。
    """
    p = Path(path)
    if not p.exists():
        return []

    try:
        with p.open("rb") as f:
            # Read file in binary and splitlines for robustness
            data = f.read()
    except Exception:
        return []

    lines = data.splitlines()
    results: List[Dict] = []
    for line in lines[-limit:]:
        try:
            text = line.decode("utf-8")
            obj = json.loads(text)
            if isinstance(obj, dict):
                results.append(obj)
        except Exception:
            continue

    return results
