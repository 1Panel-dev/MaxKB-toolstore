# MemOS 记忆检索工具

基于 MemOS 记忆存储系统 API 封装的记忆检索工具，根据查询文本检索指定用户的记忆，返回与查询内容最相关的事实记忆、偏好记忆片段供 Agent 使用。

## 一、功能说明

- 根据查询文本在记忆库中搜索最相关的记忆片段
- 支持召回事实记忆、偏好记忆两类
- 可自定义返回的记忆项数量

## 二、参数说明

### 2.1 启动参数

| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `access_key` | 密码框 | 是 | MemOS API Key，在 API 控制台 > 接口密钥中获取 |

### 2.2 输入参数

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `query` | string | 是 | 引用参数 | 查询文本内容（token 上限 20k） |
| `conversation_id` | string | 否 | 引用参数 | 会话唯一标识符 |
| `memory_limit_number` | int | 否 | 引用参数 | 事实记忆返回条数（默认 6，最大 25） |

> **参数获取说明**：
> - `user_id`：MaxKB 中使用系统变量 `{{user_id}}`，建议添加前缀如 `maxkb_{{user_id}}`
> - `conversation_id`：MaxKB 中使用系统变量 `{{chat_id}}`

---

## 三、工具内容（Python）

```python
import requests


def search_memory(user_id: str, query: str, conversation_id: str = "", memory_limit_number: int = 6, access_key: str = ""):
    """
    MemOS 记忆检索

    参数类型（根据官方API文档）：
    - user_id: string, 必填, 用户唯一标识符
    - query: string, 必填, 查询文本内容（token上限20k）
    - conversation_id: string, 可选, 会话唯一标识符
    - memory_limit_number: number, 可选, 事实记忆返回条数（默认6，最大25）
    - access_key: string, 必填, API密钥
    """
    http_session = requests.Session()
    try:
        data = {
            "user_id": user_id,
            "query": query,
            "include_preference": True,
            "memory_limit_number": memory_limit_number
        }
        if conversation_id:
            data["conversation_id"] = conversation_id

        rep = http_session.post(
            url="https://memos.memtensor.cn/api/openmem/v1/search/memory",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {access_key}"
            },
            json=data
        ).json()

        if rep.get("code") == 0:
            result_parts = []
            memory_list = rep.get("data", {}).get("memory_detail_list", [])
            preference_list = rep.get("data", {}).get("preference_detail_list", [])

            if memory_list:
                result_parts.append("【事实记忆】")
                for mem in memory_list:
                    result_parts.append(f"- {mem.get('memory_key', '')}: {mem.get('memory_value', '')}")

            if preference_list:
                result_parts.append("【偏好记忆】")
                for pref in preference_list:
                    result_parts.append(f"- {pref.get('preference', '')}")

            if result_parts:
                return "\n".join(result_parts)
            else:
                return "未找到相关记忆"
        else:
            return f"错误：记忆检索失败：{rep.get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"错误：记忆检索时发生网络错误: {e}"
    except Exception as e:
        return f"错误：处理记忆检索响应时发生错误: {e}"
```

---
