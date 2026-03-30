# Tavily 搜索工具

基于 Tavily Search API 封装的联网搜索工具，执行搜索查询并返回原始 JSON 结果，适合在工作流中继续处理。

## 一、功能说明

- 使用 Tavily Search API 执行联网搜索
- 返回原始 JSON 结果，包含标题、链接、摘要、相关性评分等字段
- 支持主题分类（general / news / finance）
- 支持搜索深度控制（basic / advanced / fast / ultra-fast）
- 支持返回数量、LLM 答案、正文内容等可选增强

## 二、参数说明

### 2.1 启动参数

| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `tavily_api_key` | 密码框 | 是 | Tavily API Key，在 https://app.tavily.com 获取 |

### 2.2 输入参数

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `query` | string | 是 | 引用参数 | 搜索关键词 |
| `topic` | string | 否 | 引用参数 | 搜索主题，支持 `general`（默认）/ `news` / `finance` |
| `search_depth` | string | 否 | 引用参数 | 搜索深度，支持 `basic`（默认）/ `advanced` / `fast` / `ultra-fast` |
| `max_results` | int | 否 | 自定义参数 | 最大返回结果数，默认 5，范围 0-20 |
| `include_answer` | string | 否 | 引用参数 | 是否包含 LLM 生成的答案，支持 `false`（默认）/ `true` / `basic` / `advanced` |
| `include_raw_content` | string | 否 | 引用参数 | 是否包含正文内容，支持 `false`（默认）/ `true` / `markdown` / `text` |

> **参数获取说明**：
> - `query`：直接输入搜索关键词，或使用 MaxKB 系统变量如 `{{query}}`
> - `max_results`：建议使用自定义参数，设置为 5-10 之间

## 三、工具内容（Python）

```python
import json
import requests


def tavily_search(query: str, topic: str = "general", search_depth: str = "basic", max_results: int = 5, include_answer: str = "false", include_raw_content: str = "false", tavily_api_key: str = ""):
    """
    Tavily 搜索

    参数类型：
    - query: string, 必填，搜索关键词
    - topic: string, 可选，搜索主题（general/news/finance），默认 general
    - search_depth: string, 可选，搜索深度（basic/advanced/fast/ultra-fast），默认 basic
    - max_results: int, 可选，最大返回结果数，默认 5，范围 0-20
    - include_answer: string/bool, 可选，是否包含 LLM 生成的答案
    - include_raw_content: string/bool, 可选，是否包含正文内容
    - tavily_api_key: string, 必填，Tavily API Key
    """
    try:
        if not query:
            return json.dumps({"success": False, "message": "query 不能为空", "error": "missing_query"}, ensure_ascii=False)
        if not tavily_api_key:
            return json.dumps({"success": False, "message": "tavily_api_key 不能为空", "error": "missing_tavily_api_key"}, ensure_ascii=False)

        def normalize_bool_or_mode(value):
            if isinstance(value, bool):
                return value
            text = str(value).strip().lower()
            if text in ["true", "basic", "advanced", "markdown", "text"]:
                if text == "true":
                    return True
                return text
            return False

        payload = {
            "query": query,
            "topic": topic or "general",
            "search_depth": search_depth or "basic",
            "max_results": max_results
        }

        answer_value = normalize_bool_or_mode(include_answer)
        raw_value = normalize_bool_or_mode(include_raw_content)
        if answer_value is not False:
            payload["include_answer"] = answer_value
        if raw_value is not False:
            payload["include_raw_content"] = raw_value

        rep = requests.post(
            url="https://api.tavily.com/search",
            headers={
                "Content-Type": "application/json"
            },
            json={**payload, "api_key": tavily_api_key},
            timeout=30
        )
        rep.raise_for_status()
        data = rep.json()
        return json.dumps({"success": True, "message": "Tavily 搜索成功", "data": data}, ensure_ascii=False)
    except requests.exceptions.HTTPError as e:
        detail = None
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text if e.response is not None else str(e)
        return json.dumps({
            "success": False,
            "message": "Tavily 搜索失败",
            "error": str(e),
            "status_code": e.response.status_code if e.response is not None else None,
            "details": detail
        }, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return json.dumps({"success": False, "message": "Tavily 搜索请求失败", "error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "message": "处理 Tavily 搜索响应时发生错误", "error": str(e)}, ensure_ascii=False)
```

---
