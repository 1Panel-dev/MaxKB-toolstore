# MemOS 记忆添加工具

基于 MemOS 记忆存储系统 API 封装的记忆添加工具，将会话消息写入 MemOS，系统会自动解析消息并生成记忆，让 AI 拥有持续记忆与成长能力。

## 一、功能说明

- 将对话消息批量写入 MemOS 记忆存储
- 支持多角色消息（user / assistant）
- MemOS 会自动解析消息内容并生成事实记忆、偏好记忆

## 二、参数说明

### 2.1 启动参数

| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `access_key` | 密码框 | 是 | MemOS API Key，在 API 控制台 > 接口密钥中获取 |

### 2.2 输入参数

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 消息关联的用户唯一标识符 |
| `conversation_id` | string | 是 | 引用参数 | 消息关联的会话唯一标识符 |
| `user_message` | string | 是 | 引用参数 | 用户发送的消息内容 |
| `assistant_message` | string | 是 | 引用参数 | AI 助手回复的消息内容 |

> **参数获取说明**：
> - `user_id`：MaxKB 中使用系统变量 `{{user_id}}`，建议添加前缀如 `maxkb_{{user_id}}`
> - `conversation_id`：MaxKB 中使用系统变量 `{{chat_id}}`

---

## 三、工具内容（Python）

```python
import requests


def add_message(user_id: str, conversation_id: str, user_message: str, assistant_message: str, access_key: str = ""):
    """
    MemOS 消息添加

    参数类型（根据官方API文档）：
    - user_id: string, 必填, 消息关联的用户唯一标识符
    - conversation_id: string, 必填, 消息关联的会话唯一标识符
    - user_message: string, 必填, 用户消息内容（对应 messages[].content）
    - assistant_message: string, 必填, 助手消息内容（对应 messages[].content）
    - access_key: string, 必填, API密钥

    原始API messages数组字段：
    - role: string, 必填, 消息角色（user/assistant/system/tool）
    - content: string, 必填, 消息内容文本
    - chat_time: string, 可选, 对话时间
    """
    http_session = requests.Session()
    try:
        messages = []
        if user_message:
            messages.append({"role": "user", "content": user_message})
        if assistant_message:
            messages.append({"role": "assistant", "content": assistant_message})

        if not messages:
            return "错误：消息内容不能为空"

        data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": messages
        }

        rep = http_session.post(
            url="https://memos.memtensor.cn/api/openmem/v1/add/message",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {access_key}"
            },
            json=data
        ).json()

        if rep.get("code") == 0:
            task_id = rep.get("data", {}).get("task_id", "")
            return f"信息：消息添加成功，任务ID: {task_id}"
        else:
            return f"错误：消息添加失败：{rep.get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"错误：添加消息时发生网络错误: {e}"
    except Exception as e:
        return f"错误：处理消息添加响应时发生错误: {e}"
```

---
