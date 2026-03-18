# Mem0 记忆检索工具

基于 mem0 API 的单入口工具，用于按语义搜索指定范围内的相关记忆。

## 功能说明
- 基于 query 搜索相关记忆
- 支持 user_id / agent_id 范围限制
- 当同时提供 user_id 和 agent_id 时，内部使用 `OR` 过滤，避免官方文档提到的空结果问题
- 使用官方 `POST /v2/memories/search/` 接口

## 参数说明
### 启动参数
| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `api_key` | 密码框 | 是 | Mem0 API Key |
| `base_url` | 文本框 | 否 | API 地址，默认 `https://api.mem0.ai` |

### 输入参数
| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `query` | string | 是 | 引用参数 | 搜索语句 |
| `user_id` | string | 否 | 引用参数 | 用户唯一标识 |
| `agent_id` | string | 否 | 引用参数 | agent 唯一标识 |
| `top_k` | int | 否 | 自定义参数 | 返回数量，默认 5 |
