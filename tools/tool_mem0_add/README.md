# Mem0 记忆添加工具

基于 mem0 API 的单入口工具，用于向指定用户写入一条记忆。

## 功能说明
- 添加一条用户或助手消息到 Mem0
- 支持 metadata
- 支持可选 agent_id
- 使用官方 `POST /v1/memories/` 接口
- 注意：Mem0 默认异步处理，写入后可能需要等待 2-3 秒再检索

## 参数说明
### 启动参数
| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `api_key` | 密码框 | 是 | Mem0 API Key |
| `base_url` | 文本框 | 否 | API 地址，默认 `https://api.mem0.ai/v1` |

### 输入参数
| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识 |
| `content` | string | 是 | 引用参数 | 要写入的记忆内容 |
| `role` | string | 否 | 引用参数 | 角色，默认 `user` |
| `agent_id` | string | 否 | 引用参数 | agent 唯一标识 |
| `metadata` | string | 否 | 引用参数 | JSON 字符串格式的元数据 |
