# Webhook 请求工具

一个安全、可靠且功能完善的 Python HTTP 客户端模块，专为发送 Webhook 请求而设计。它提供了简单的 API、内置的安全防护（如 SSRF 防御）以及完善的错误处理机制，适用于生产环境。

## 一、项目介绍

### 1.1 核心功能
- **安全可靠**：内置 SSRF（服务端请求伪造）防护，禁止访问私有 IP 和危险端口，默认强制使用 HTTPS。
- **功能全面**：支持常见的 HTTP 方法（GET, POST, PUT, DELETE, PATCH），可自定义请求头、查询参数和多种格式的请求体（JSON/字符串）。
- **容错性强**：具备连接超时控制、自动重试（针对特定方法和状态码）以及统一的异常捕获机制。
- **易于集成**：返回标准化的结果字典，包含状态码、内容、响应头、耗时及明确的错误信息，无需处理底层异常。

### 1.2 适用场景
- 向第三方服务发送 Webhook 通知（如支付回调、状态更新）。
- 作为微服务间轻量级的 HTTP 通信客户端。
- 需要高安全性和稳定性的外部 API 调用。
- 快速构建需要 HTTP 请求功能的脚本或工具。

## 二、环境准备

### 2.1 依赖库
- **Python**: 3.7+
- **requests**: >= 2.25.0

### 2.2 安装依赖
```bash
pip install requests
```

## 三、快速开始

### 3.1 基础使用示例
以下示例展示了如何发送一个简单的 POST 请求到 Webhook 端点。

```python
# 导入函数
from your_module import send_webhook_request

# 定义目标 URL 和请求数据
webhook_url = "https://api.example.com/webhook"
payload = {"event": "user_created", "user_id": 12345}

# 发送请求
result = send_webhook_request(
    url=webhook_url,
    method="POST",
    body=payload,
    headers={"Content-Type": "application/json", "X-Signature": "your_signature"}
)

# 检查请求结果
if result["success"]:
    print(f"✅ 请求成功！状态码: {result['status_code']}")
    print(f"响应内容: {result['content']}")
    print(f"耗时: {result['elapsed']} 秒")
else:
    print(f"❌ 请求失败！")
    print(f"错误信息: {result['error']}")
    print(f"HTTP状态码: {result['status_code']}")

# 预期输出（成功时）:
# ✅ 请求成功！状态码: 200
# 响应内容: {'status': 'ok', 'received': True}
# 耗时: 0.356 秒
```

## 四、使用说明

### 4.1 函数定义
```python
def send_webhook_request(
    url: str,
    method: str = "POST",
    headers: Optional[dict[str, str]] = None,
    body: Optional[dict[str, Any] | list[Any] | str] = None,
    params: Optional[dict[str, str]] = None,
    timeout: int = 30,
    max_retries: int = 3,
    verify_ssl: bool = True,
    auth: Optional[tuple[str, str]] = None,
    allow_http: bool = False,
) -> dict[str, Any]:
```

### 4.2 参数说明

| 参数名 | 类型 | 必需 | 默认值 | 描述 | 有效值/范围 | 示例 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `url` | `str` | 是 | 无 | 目标 URL 地址。 | 有效的 HTTP/HTTPS URL 字符串。 | `"https://api.example.com/event"` |
| `method` | `str` | 否 | `"POST"` | HTTP 请求方法。 | `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, `"PATCH"` | `"GET"` |
| `headers` | `dict` | 否 | `None` | 自定义 HTTP 请求头。键和值会自动转换为字符串。 | 任意字典，如 `{"Key": "Value"}`。 | `{"Content-Type": "application/json"}` |
| `body` | `dict`, `list`, `str` | 否 | `None` | HTTP 请求体。<br>1. **`dict/list`**: 自动序列化为 JSON。<br>2. **`str`**: 作为原始字符串发送。 | 字典、列表或字符串。 | `{"data": "test"}` |
| `params` | `dict` | 否 | `None` | URL 查询参数字典。会自动附加到 URL 后。键和值会自动转换为字符串。 | 任意字典。 | `{"page": "1", "limit": "10"}` |
| `timeout` | `int` | 否 | `30` | 请求超时时间（秒）。 | `1` 到 `300` 之间的整数。 | `10` |
| `max_retries` | `int` | 否 | `3` | 最大重试次数。仅对幂等方法（GET, PUT, DELETE等）和特定错误状态码有效。 | `0` 到 `5` 之间的整数。 | `2` |
| `verify_ssl` | `bool` | 否 | `True` | 是否验证服务器的 SSL 证书。**生产环境建议保持 `True`**。 | `True` 或 `False` | `False` （仅用于测试） |
| `auth` | `tuple` | 否 | `None` | HTTP 基础认证凭据，格式为 `(username, password)`。 | 包含两个字符串的元组。 | `("admin", "secret")` |
| `allow_http` | `bool` | 否 | `False` | 是否允许使用不安全的 HTTP 协议。**出于安全考虑，默认为 `False`**。 | `True` 或 `False` | `True` |

#### 参数关系与注意事项：
1. **`body` 与 `headers['Content-Type']`**：
    - 当 `body` 为 `dict` 或 `list` 时，如果没有指定 `Content-Type` 头，函数会自动添加 `Content-Type: application/json`。
    - 当 `body` 为 `str` 时，请务必手动设置正确的 `Content-Type`（如 `text/plain`）。

2. **`allow_http` 与 `url` 协议**：
    - 当 `allow_http=False`（默认）时，如果 `url` 以 `http://` 开头，函数将返回错误。
    - 仅在测试或可信的内部网络环境中，才应设置 `allow_http=True`。

3. **`max_retries` 的重试策略**：
    - 仅对 `method` 为 `"GET"`, `"PUT"`, `"DELETE"` 等幂等方法生效。
    - 仅对 HTTP 状态码为 `429`, `500`, `502`, `503`, `504` 的响应进行重试。
    - `POST` 方法默认**不会**自动重试，以避免重复提交。

### 4.3 返回值说明
函数总是返回一个字典，结构如下：
```python
{
    "status_code": Optional[int],   # HTTP响应状态码，失败时为None
    "content": Optional[Union[str, dict]], # 响应内容。如果是JSON，已解析为字典。
    "response_headers": Optional[dict], # 响应头字典
    "elapsed": float,                # 请求总耗时（秒），保留3位小数
    "error": Optional[str],          # 错误信息。成功时为None。
    "success": bool                  # 请求是否成功（HTTP状态码为2xx）
}
```

**判断请求结果的正确方式：**
```python
result = send_webhook_request(...)
if result["success"]:
    # 处理成功响应
    data = result["content"]
else:
    # 处理失败，`error`字段会告诉你原因
    log_error(result["error"], result["status_code"])
```
