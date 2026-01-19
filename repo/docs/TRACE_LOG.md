# 跟踪日志说明（TRACE_LOG）

本文件说明仓库中自动生成的跟踪日志的格式与使用方式。

日志格式：
- 使用 JSONL（每行一个 JSON 对象）。
- 每条记录至少包含：`timestamp`（ISO8601）、`trace_id`（uuid4）、`span`、`event`。

配置：
- 使用环境变量 `TRACE_LOG_PATH` 指定日志文件路径，默认 `repo/logs/trace.jsonl`。

示例：

{
  "timestamp": "2026-01-19T12:00:00.000Z",
  "trace_id": "11111111-2222-3333-4444-555555555555",
  "span": "cli",
  "event": "command_start",
  "command": "greet",
  "name": "张三"
}

请确保父目录不存在时自动创建，并以追加方式写入日志文件。

轮转与大小限制：
- `init_tracing(log_path, max_bytes=0, backup_count=0)` 支持简单的基于大小的轮转策略。若 `max_bytes>0` 且文件超过该大小，则会把当前日志重命名为备份（.1/.2 ...），并保留 `backup_count` 个备份。

日志级别：
- 每条记录包含 `level` 字段（例如 `info`/`warn`/`error`/`debug`）。使用 `trace(..., level="warn")` 可以记录不同级别的事件。

快速查看：
- CLI 支持 `--dump-traces N` 参数，会打印最近 N 条 trace（使用 `repo/src/trace_utils.py` 中的 `tail_traces`）。

示例（轮转/级别）：

{
  "timestamp": "2026-01-19T12:00:00.000Z",
  "trace_id": "11111111-2222-3333-4444-555555555555",
  "span": "cli",
  "event": "command_start",
  "level": "info",
  "command": "greet",
  "name": "张三"
}