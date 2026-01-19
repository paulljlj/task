# 示例仓库 - 自动跟踪日志（中文版）

该仓库包含用于演示自动生成跟踪日志的最小示例代码。

运行示例：

python -m src.main greet --name 张三

启用跟踪日志：设置环境变量 `TRACE_LOG_PATH`，例如：

Windows:

$env:TRACE_LOG_PATH = 'repo/logs/trace.jsonl'

详见 `docs/TRACE_LOG.md`。
