# MemOS 记忆管理工具

基于 MemOS 记忆存储系统 API 封装的 Python 记忆管理工具函数，支持记忆检索、消息添加、记忆获取等功能。MemOS 会自动解析消息并处理记忆，召回包括事实记忆、偏好记忆、工具记忆三类，让 AI 拥有持续记忆与成长能力。

## 一、项目介绍

### 1.1 核心功能

- **记忆检索（search_memory）**：根据查询文本检索指定用户的记忆，返回与查询内容最相关的事实记忆、偏好记忆和工具记忆片段。
- **消息添加（add_message）**：将会话消息批量写入 MemOS，支持多角色（user/assistant/system/tool）、多类型内容，MemOS 会自动解析并生成记忆。
- **记忆获取（get_memory）**：获取某个用户的全量记忆数据，支持分页查询，包含事实记忆、偏好记忆与工具记忆。

### 1.2 适用场景

- **用户画像构建**：通过持续积累用户对话记忆，自动生成用户偏好与行为画像。
- **个性化推荐**：基于用户历史记忆数据，提供更贴合用户需求的回答和推荐。
- **聊天历史管理**：将对话消息持久化存储，支持跨会话的上下文回忆。
- **用户行为跟踪**：记录用户交互行为，支持后续的数据分析与洞察。
- **智能客服增强**：结合历史记忆为用户提供连贯、个性化的客服体验。

---

## 二、环境准备

### 2.1 获取 API Key

使用前需在 MemOS 控制台获取 API Key：

1. 登录 MemOS 平台
2. 进入 **API 控制台** > **接口密钥**
3. 创建或复制已有的 API Key

### 2.2 基础地址

```
https://memos.memtensor.cn/api/openmem/v1
```

### 2.3 认证方式

所有请求需在 Header 中携带 Token 认证：

```
Authorization: Token YOUR_API_KEY
Content-Type: application/json
```

---

## 三、使用说明

本工具包含以下三个函数：

### 3.1 search_memory — 检索记忆

**接口**：`POST /search/memory`

该接口用于检索指定用户的记忆，返回与查询内容最相关的记忆片段供 Agent 使用。召回包括事实记忆、偏好记忆、工具记忆三类。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 用户唯一标识符 |
| `query` | string | 是 | 查询文本内容（token 上限 20k） |
| `conversation_id` | string | 否 | 会话唯一标识符 |
| `filter` | object | 否 | 记忆过滤条件，支持逻辑/比较运算符 |
| `knowledgebase_ids` | string[] | 否 | 可访问知识库范围（默认空） |
| `memory_limit_number` | number | 否 | 事实记忆返回条数（默认 6，最大 25） |
| `include_preference` | boolean | 否 | 是否召回偏好记忆（默认 true） |
| `preference_limit_number` | number | 否 | 偏好记忆条数（默认 6，最大 25） |
| `include_tool_memory` | boolean | 否 | 是否召回工具记忆（默认 false） |
| `tool_memory_limit_number` | number | 否 | 工具记忆条数（默认 6，最大 25） |
| `include_skill` | boolean | 否 | 是否召回技能（默认 false） |
| `skill_limit_number` | number | 否 | 技能条数（默认 6，最大 25） |

**请求示例：**

```python
import requests, json, os

data = {
    "query": "我国庆想出去玩，帮我推荐个没去过的城市",
    "user_id": "memos_user_123",
    "conversation_id": "0928"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}

res = requests.post(
    url=f"{os.environ['MEMOS_BASE_URL']}/search/memory",
    headers=headers,
    data=json.dumps(data)
)
print(res.json())
```

**响应示例：**

```json
{
  "code": 0,
  "data": {
    "memory_detail_list": [
      {
        "id": "mem_123",
        "memory_key": "出行偏好",
        "memory_value": "用户喜欢自驾游",
        "memory_type": "LongTermMemory",
        "confidence": 0.95,
        "relativity": 0.87,
        "tags": ["旅游", "偏好"],
        "status": "activated"
      }
    ],
    "preference_detail_list": [
      {
        "id": "pref_456",
        "preference_type": "explicit_preference",
        "preference": "倾向选择南方城市",
        "reasoning": "历史对话中多次提及"
      }
    ],
    "tool_memory_detail_list": [],
    "skill_detail_list": []
  },
  "message": "success"
}
```

---

### 3.2 add_message — 添加消息

**接口**：`POST /add/message`

该接口用于添加会话消息，支持多类型内容、批量添加。MemOS 会自动解析消息并处理记忆。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 消息关联的用户唯一标识符 |
| `conversation_id` | string | 是 | 消息关联的会话唯一标识符 |
| `messages` | array | 是 | 消息对象数组（总 token 上限 20k） |
| `agent_id` | string | 否 | Agent 唯一标识符 |
| `app_id` | string | 否 | 应用唯一标识符 |
| `tags` | array | 否 | 自定义标签列表 |
| `info` | object | 否 | 自定义元信息字段 |
| `allow_public` | boolean | 否 | 记忆是否允许写入公共库（默认 false） |
| `allow_knowledgebase_ids` | array | 否 | 允许写入的知识库范围 |
| `async_mode` | boolean | 否 | 是否异步添加记忆（默认 true） |

**消息对象字段：**

| 字段 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `role` | string | 是 | 消息角色：user / assistant / system / tool |
| `content` | string / object[] | 是 | 消息内容文本 |
| `chat_time` | string | 否 | 对话时间（结构化或中文描述） |

**请求示例：**

```python
import requests, json, os

data = {
    "user_id": "memos_user_123",
    "conversation_id": "0610",
    "messages": [
        {"role": "user", "content": "我暑假定好去广州旅游"},
        {"role": "assistant", "content": "您可以考虑【七天、全季、希尔顿】"}
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}

res = requests.post(
    url=f"{os.environ['MEMOS_BASE_URL']}/add/message",
    headers=headers,
    data=json.dumps(data)
)
print(res.json())
```

**响应示例：**

```json
{
  "code": 0,
  "data": {
    "success": true,
    "task_id": "task_abc123",
    "status": "running"
  },
  "message": "ok"
}
```

---

### 3.3 get_memory — 获取记忆

**接口**：`POST /get/memory`

该接口用于获取某个用户的记忆，包含事实记忆、偏好记忆与工具记忆，支持分页查询。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 获取的记忆所关联的用户唯一标识符 |
| `page` | number | 否 | 分页页码（默认 1） |
| `size` | number | 否 | 每类记忆当前页返回条目数量（默认 10，最大 50） |
| `filter` | object | 否 | 记忆过滤条件，支持 agent_id、app_id、create_time、update_time 及 info 中的字段 |
| `include_preference` | boolean | 否 | 是否返回偏好记忆（默认 true） |
| `include_tool_memory` | boolean | 否 | 是否返回工具记忆（默认 true） |

**请求示例：**

```python
import requests, json, os

data = {
    "user_id": "memos_user_123"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}

res = requests.post(
    url=f"{os.environ['MEMOS_BASE_URL']}/get/memory",
    headers=headers,
    data=json.dumps(data)
)
print(res.json())
```

**响应示例：**

```json
{
  "code": 0,
  "data": {
    "memory_detail_list": [
      {
        "id": "mem_123",
        "memory_key": "出行偏好",
        "memory_value": "用户喜欢自驾游",
        "memory_type": "LongTermMemory",
        "confidence": 0.95,
        "tags": ["旅游"],
        "status": "activated"
      }
    ],
    "preference_detail_list": [],
    "tool_memory_detail_list": [],
    "total": 1,
    "size": 10,
    "current": 1,
    "pages": 1
  },
  "message": "success"
}
```

**分页字段说明：**

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `total` | number | 各类记忆总数中的最大值 |
| `size` | number | 每类记忆当前页返回的条目数量 |
| `current` | number | 当前页码 |
| `pages` | number | 总页数 |

---
