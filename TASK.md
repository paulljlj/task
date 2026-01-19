tool: github
name: "自动生成跟踪日志任务（追踪记录与归档）"
category: auto_tracking_log_cn

description: |
  你将获得一个从 GitHub 导出的仓库物料（位于 `repo/` 目录）。请在该仓库内实现自动生成跟踪日志的能力，并补齐相应代码与文档。

  注意仓库结构：
  - 核心代码位于 `repo/src/`，入口为 `repo/src/main.py`（可通过 `python -m src.main ...` 运行）。

  请严格按路径创建或修改以下内容：
  1) 在 `repo/src/trace_utils.py` 中新增读取工具，要求：
     - 提供 `tail_traces(path: str, limit: int = 10) -> list[dict]`，能解析并返回日志文件的最后若干行 JSON 对象；
     - 对无法解析的行应安全忽略，不中断读取流程。

  2) 在 `repo/docs/TRACE_LOG.md` 中新增文档，要求说明：
     - 日志格式为 JSONL，并列出必备字段含义；
     - `TRACE_LOG_PATH` 的使用方法；
     - 轮转（`max_bytes` / `backup_count`）策略说明与示例；
     - `level` 字段含义（info/warn/error/debug）和示例；
     - `--dump-traces` 的使用示例；
     - 包含至少一条示例日志记录（包含 `timestamp/trace_id/span/event/level` 字段）。

  3) 更新 `repo/README.md`：增加一小节说明如何开启/查看跟踪日志（提到 `TRACE_LOG_PATH` 与 `--dump-traces`）。

  4) 在 `repo/src/tracing.py` 中实现跟踪模块，要求：
     - 提供 `init_tracing(log_path: str, max_bytes: int = 0, backup_count: int = 0) -> None`，用于初始化日志路径与可选的轮转配置；
     - 提供 `trace(event: str, span: str = "app", level: str = "info", **kwargs) -> None`，向日志文件追加一行 JSON（JSONL）；
     - 每条日志必须至少包含字段：`timestamp`（ISO8601）、`trace_id`（uuid4）、`span`、`event`、`level`；
     - 文件写入模式为追加（append），在父目录不存在时自动创建；
     - 当 `max_bytes>0` 且日志大小超过阈值时，按 `backup_count` 做简单的文件轮转（通过重命名备份实现），不得使用第三方库；
     - 仅允许使用 Python 标准库实现。

  5) 在 `repo/src/main.py` 中集成 tracing，要求：
     - 支持通过环境变量 `TRACE_LOG_PATH` 指定日志路径，默认 `repo/logs/trace.jsonl`；
     - 在命令开始时写入 `command_start`，成功结束时写入 `command_end`，出现异常时写入 `command_error`（并包含 `error` 字段）；
     - `trace` 中应记录命令名及关键参数（例如 `greet` 的 `name`）；
     - 增加可选 CLI 参数 `--dump-traces N`：若提供，则打印最近 N 条 trace（使用 `repo/src/trace_utils.py` 的 `tail_traces`）后退出。

  6) 验证脚本要求：
     - 验证 `tracing.py` 中存在 `init_tracing` 与 `trace`，并支持 `max_bytes` / `backup_count` / `level`；
     - 验证 `trace_utils.tail_traces` 存在且能读取 JSONL 的最后若干条记录；
     - 验证 `main.py` 引用了 `TRACE_LOG_PATH`、调用了 `init_tracing`、并支持 `--dump-traces`；
     - 验证 `docs/TRACE_LOG.md` 中包含 JSONL、`TRACE_LOG_PATH`、轮转参数、级别与 `--dump-traces` 的说明。

  输出要求：
  - 保持代码可读、注释清晰；
  - 不要进行大量与任务无关的重构；
  - 所有新增/修改文件路径必须与本任务描述一致。

