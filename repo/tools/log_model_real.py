"""模板：调用真实模型并把响应写入 trace（不包含密钥）

说明：
- 不要在仓库中提交任何 API key；脚本从环境变量读取 `MODEL_API_URL` 和 `MODEL_API_KEY`。
- 根据你使用的模型服务替换请求逻辑（示例使用 `requests`）。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# 确保能导入 repo/src 包
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tracing import init_tracing, trace

import json
import requests


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    out_dir = repo / "tmp_verify_traces"
    out_dir.mkdir(parents=True, exist_ok=True)
    trace_path = out_dir / "trace.jsonl"

    # 初始化 tracing（按需调整 max_bytes/backup_count）
    init_tracing(str(trace_path), max_bytes=0, backup_count=0)

    trace("command_start", span="cli", command="call_real_model")

    api_url = os.environ.get("MODEL_API_URL")
    api_key = os.environ.get("MODEL_API_KEY")
    if not api_url or not api_key:
        trace("command_error", span="cli", command="call_real_model", error="missing api config", level="error")
        print("Missing MODEL_API_URL or MODEL_API_KEY environment variables")
        return

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # 简单示例 payload — 根据实际模型 API 调整
    payload = {"prompt": "请输出一句简短的问候语。", "max_tokens": 64}

    try:
        resp = requests.post(api_url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        text = resp.text
    except Exception as e:
        trace("command_error", span="cli", command="call_real_model", error=str(e), level="error")
        print(f"Model request failed: {e}")
        return

    # 将模型响应写入 trace
    trace("model_response", span="model", model="real-model", response=text)

    trace("command_end", span="cli", command="call_real_model")


if __name__ == "__main__":
    main()
