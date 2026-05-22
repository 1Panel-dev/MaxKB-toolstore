# MaxKB OSS 通用文件上传工具

上传服务器已有文件或传入文本内容至 MaxKB OSS，返回结构化结果及下载链接，便于在工作流中做条件分支。

## 一、功能说明

- **file_path 模式**：上传服务器上已存在的文件（支持所有类型）
- **file_content 模式**：传入文本内容，自动生成临时文件再上传
- 返回结构化 `dict`，包含 `status`、`message`、`file_id`、`file_name`、`download_url`

## 二、参数说明

### 2.1 启动参数（初始化参数）

| 参数 | 组件类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `upload_url` | 文本框 | 是 | — | MaxKB 服务器地址，如 `http://x.x.x.x:8080` |
| `upload_headers` | 文本框 | 是 | — | API 鉴权 Token（不带 Bearer 前缀） |
| `source_type` | 文本框 | 否 | `TEMPORARY_30_MINUTE` | 文件生命周期类型，详见下方说明 |
| `source_id` | 文本框 | 否 | 与 `source_type` 相同 | 文件归属 ID |

**`source_type` 可选值说明：**

`source_type` 决定文件的归属和生命周期，`source_id` 为对应业务对象的 ID。

| 类型 | 说明 |
| :--- | :--- |
| `KNOWLEDGE` | 知识库文件，跟随知识库删除，`source_id` 为知识库 ID |
| `APPLICATION` | 应用文件，跟随应用删除，`source_id` 为应用 ID |
| `TOOL` | 工具文件，跟随工具删除，`source_id` 为工具 ID |
| `DOCUMENT` | 文档文件，`source_id` 为文档 ID |
| `CHAT` | 对话文件，`source_id` 为对话 ID |
| `SYSTEM` | 系统文件 |
| `TEMPORARY_30_MINUTE` | 临时文件，30 分钟后自动清理 |
| `TEMPORARY_120_MINUTE` | 临时文件，120 分钟后自动清理 |
| `TEMPORARY_1_DAY` | 临时文件，1 天后自动清理 |

**常用场景推荐：**
- 智能体生成文件供用户下载 → `TEMPORARY_1_DAY`
- 文件需跟随业务对象删除 → 使用对应类型（`KNOWLEDGE` / `APPLICATION` / `TOOL` 等）
- 仅临时使用 → `TEMPORARY_30_MINUTE` 或 `TEMPORARY_120_MINUTE`

### 2.2 输入参数

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `file_path` | string | 二选一 | 引用参数 | 服务器文件路径（优先级高），提供此参数则忽略 `file_content` |
| `file_content` | string | 二选一 | 引用参数 | 文件文本内容（`file_path` 为空时使用） |
| `filename` | string | 否 | 引用参数 | 文件名（不含扩展名），留空默认 `文件` |
| `extension` | string | 否 | 自定义参数 | 文件扩展名，如 `.html`、`.md`、`.txt`、`.pdf` |

> **参数获取说明**：
> - `upload_url`：填写你的 MaxKB 服务地址（含端口）
> - `upload_headers`：在 MaxKB 后台生成 API Token 后填写，格式为 Token 值本身（不含 `Bearer` 前缀）
> - `file_path` / `file_content`：使用 MaxKB 系统变量如 `{{file_path}}` 引用上游输出

## 三、返回结果

返回一个 `dict`，结构如下：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | string | `success` / `failed` / `warning` |
| `message` | string | 结果描述信息 |
| `file_id` | string | OSS 文件 ID |
| `file_name` | string | 上传的文件名 |
| `download_url` | string | 文件下载链接 |

## 四、工具内容（Python）

```python
"""
通用文件上传工具（MaxKB 自定义工具）

两种用法：
  1. file_path 模式 — 上传服务器上已存在的文件（支持所有类型）
  2. file_content 模式 — 传入文本内容，自动生成临时文件再上传

返回结构化 dict，便于工作流做条件分支。
"""
import os
import io
import re
import requests
from datetime import datetime
from mimetypes import guess_type


# ── 辅助函数 ──

def _plain(value) -> str:
    """健壮取值：兼容 str / dict / 对象 / None"""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ["value", "content", "text", "result", "data"]:
            if key in value:
                return _plain(value[key])
        return str(value).strip()
    for attr in ["value", "content", "text", "result", "data"]:
        if hasattr(value, attr):
            try:
                return _plain(getattr(value, attr))
            except Exception:
                pass
    return str(value).strip()


def _cfg(name: str, value: str = "", default: str = "") -> str:
    """环境变量兜底：传入值 > 环境变量 > 默认值"""
    value = _plain(value)
    return value or _plain(os.getenv(name)) or _plain(os.getenv(name.upper())) or default


def _result(status: str, message: str, file_name: str = "",
            download_url: str = "", file_id: str = "", extra=None) -> dict:
    """统一构造返回 dict"""
    result = {
        "status": status,
        "message": _plain(message),
        "file_id": file_id,
        "file_name": _plain(file_name),
        "download_url": download_url,
    }
    if extra is not None:
        result["extra"] = extra
    return result


def _extract_file_id(resp_json) -> str:
    """从响应中提取 file_id，兼容多种返回格式"""
    def pick(text) -> str:
        text = _plain(text)
        if not text:
            return ""
        match = re.search(r"/oss/file/([^/]+)/?", text)
        if match:
            return match.group(1)
        if "/" not in text and "." not in text:
            return text
        return ""

    if not isinstance(resp_json, dict):
        return ""

    for key in ["file_id", "id", "oss_id", "uuid"]:
        if resp_json.get(key):
            return _plain(resp_json[key])

    for key in ["url", "path", "download_url", "file_url"]:
        fid = pick(resp_json.get(key))
        if fid:
            return fid

    data = resp_json.get("data")
    if isinstance(data, str):
        return pick(data)
    if isinstance(data, dict):
        for key in ["file_id", "id", "oss_id", "uuid"]:
            if data.get(key):
                return _plain(data[key])
        for key in ["url", "path", "download_url", "file_url"]:
            fid = pick(data.get(key))
            if fid:
                return fid

    return ""


def main(
    file_path: str = "",
    file_content: str = "",
    filename: str = "",
    extension: str = "",
    upload_url: str = "",
    upload_headers: str = "",
    source_type: str = "",
    source_id: str = "",
) -> dict:
    """
    通用文件上传工具

    :param file_path:     服务器文件路径（优先），提供此参数则忽略 file_content
    :param file_content:  文件内容文本（file_path 为空时使用）
    :param filename:      文件名（不含扩展名），留空默认 "文件"
    :param extension:     文件扩展名，如 .html .md .txt .pdf
    :param upload_url:    MaxKB 服务器地址，如 http://x.x.x.x:8080
    :param upload_headers: Authorization: Bearer xxx 的 Token
    :param source_type:   生命周期，默认 TEMPORARY_30_MINUTE
    :param source_id:     归属 ID，留空自动使用 source_type
    :return: dict { status, message, file_id, file_name, download_url }
    """
    # ── 参数规整化 ──
    file_path = _plain(file_path)
    file_content = _plain(file_content)
    filename = _plain(filename)
    extension = _plain(extension)
    if extension and not extension.startswith('.'):
        extension = '.' + extension
    upload_url = _cfg("upload_url", upload_url)
    upload_headers = _cfg("upload_headers", upload_headers)
    source_type = _cfg("source_type", source_type, "TEMPORARY_30_MINUTE")
    source_id = _cfg("source_id", source_id, source_type)

    # ── 校验 ──
    if not upload_url:
        return _result("failed", "缺少 upload_url，请配置 MaxKB 服务地址")

    if not upload_headers:
        return _result("failed", "缺少 upload_headers，请配置 API Token")

    if not file_path and not file_content:
        return _result("failed", "file_path 和 file_content 都为空，请至少提供一个")

    # ── 获取文件名 + 数据 ──
    if file_path:
        basename = os.path.basename(file_path) if '/' in file_path or '\\' in file_path else file_path
        if not filename:
            filename, auto_ext = os.path.splitext(basename)
        else:
            auto_ext = ""
        ext = extension or auto_ext
        basename = f"{filename}{ext}"
        try:
            with open(file_path, 'rb') as f:
                data_bytes = f.read()
        except Exception as e:
            return _result("failed", f"读取文件失败：{e}",
                           extra={"file_path": file_path})
    else:
        if not filename:
            filename = "文件"
        ext = extension or ".txt"
        basename = f"{filename}{ext}"
        data_bytes = file_content.encode('utf-8')

    # ── 上传到 OSS ──
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    upload_name = f"{filename}_{timestamp}{ext}"
    api_url = upload_url.rstrip('/') + "/chat/api/oss/file"

    headers = {}
    if upload_headers:
        headers["Authorization"] = f"Bearer {upload_headers}"

    form_data = {"source_type": source_type, "source_id": source_id}
    buf = io.BytesIO(data_bytes)
    mime_type, _ = guess_type(upload_name)
    files = {"file": (upload_name, buf, mime_type) if mime_type else (upload_name, buf)}

    try:
        resp = requests.post(api_url, headers=headers, data=form_data,
                             files=files, timeout=120)
    except Exception as e:
        return _result("failed", f"上传请求异常：{e}", filename,
                       extra={"upload_url": api_url})

    if resp.status_code < 200 or resp.status_code >= 300:
        return _result("failed", "上传失败", filename,
                       extra={"status_code": resp.status_code,
                              "response": resp.text[:500]})

    try:
        resp_json = resp.json()
    except Exception:
        return _result("failed", "服务端返回非 JSON", filename,
                       extra={"response": resp.text[:500]})

    file_id = _extract_file_id(resp_json)
    if not file_id:
        return _result("warning", "上传成功但未解析到 file_id", filename,
                       extra={"response": resp_json})

    download_url = f"{upload_url.rstrip('/')}/chat/oss/file/{file_id}/"

    return _result("success", "上传成功", basename, download_url, file_id)
```

---

## 五、使用示例

**示例 1：上传服务器文件**

```json
{
  "file_path": "/tmp/report.pdf",
  "extension": ".pdf",
  "upload_url": "http://your-maxkb-server:8080",
  "upload_headers": "your-api-token"
}
```

**示例 2：上传文本内容**

```json
{
  "file_content": "# 标题\n\n这是内容",
  "filename": "报告",
  "extension": ".md",
  "upload_url": "http://your-maxkb-server:8080",
  "upload_headers": "your-api-token"
}
```
