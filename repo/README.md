# 示例仓库 - 自动跟踪日志（中文版）

该仓库包含用于演示自动生成跟踪日志的最小示例代码。

运行示例：

python -m src.main greet --name 张三

启用跟踪日志：设置环境变量 `TRACE_LOG_PATH`，例如：

Windows:

$env:TRACE_LOG_PATH = 'repo/logs/trace.jsonl'

详见 `docs/TRACE_LOG.md`。

使用真实模型（模板）：

1. 将模型服务地址与密钥设置为环境变量：

Windows PowerShell:

$env:MODEL_API_URL = 'https://api.example.com/v1/generate'
$env:MODEL_API_KEY = 'YOUR_KEY'

2. 安装依赖并运行示例模型调用脚本（脚本不会把密钥写入仓库）：

pip install -r requirements.txt
python tools/log_model_real.py

执行后，模型响应会以 `model_response` 事件写入到 `repo/tmp_verify_traces/trace.jsonl`，随后可以运行仓根的验证脚本并启用动态验证来检查 trace。
