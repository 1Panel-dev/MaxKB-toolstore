# DeepSeek 网页抓取工具

基于 DeepSeek 官方 Fetch API（<https://api-docs.deepseek.com/zh-cn/guides/search>）封装的网页抓取工具，输入 URL，返回页面标题与 Markdown 格式正文。

## 一、功能说明

- **单页抓取**：调用 `https://api.deepseek.com/v1/tools/fetch`，将目标网页转换为 Markdown 正文
- **长度可控**：`max_chars` 参数控制返回正文的字符上限，超出自动截断并标注，避免撑爆模型上下文
- **结构化输出**：同时返回 `title` / `content` / `markdown`（标题 + 来源 + 正文拼装）与截断标记
- **降级友好**：任何失败统一返回 `success: false` 而非抛异常，并附带 `error` 与中文 `hint`
- **与搜索配套**：配合「DeepSeek 联网搜索」工具（`tool_deepseek_search`）可组成"搜索 → 抓正文 → 生成回答"的完整链路

## 二、参数说明

### 2.1 启动参数

| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `api_key` | 密码框 | 是 | DeepSeek API Key，在 <https://platform.deepseek.com/api_keys> 获取 |

### 2.2 输入参数

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `url` | string | 是 | 引用参数 | 目标网页地址，必须为含 host 的 http/https URL，不能带用户名密码，长度不超过 8192 |
| `max_chars` | int | 否 | 自定义参数 | 返回正文的最大字符数，默认 8000，超出部分截断 |

### 2.3 输出参数

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `success` | bool | 是否成功 |
| `title` | string | 页面标题，缺失时为空串 |
| `url` | string | 实际抓取的地址 |
| `chars` | int | 返回正文长度 |
| `truncated` | bool | 正文是否被截断 |
| `content` | string | Markdown 正文 |
| `markdown` | string | `# 标题 + 来源链接 + 正文` 的拼装结果 |
| `error` / `hint` / `status` | string / string / int | 失败时的错误信息、排查建议与原样状态码 |

## 三、工具内容（Python）

完整源码见本目录下 `deepseek_fetch.py`（同时内嵌于 `1.0.0/DeepSeek网页抓取.tool`）。

```python
def main(api_key, url, max_chars=8000):
    # 1. 参数校验：api_key / url 必填
    # 2. POST https://api.deepseek.com/v1/tools/fetch  {"url": ...}
    #    headers: Authorization: Bearer <key>, Content-Type: application/json
    # 3. 状态码分级：400/401/402/403/404/429 分别给出排查提示
    # 4. 正文按 max_chars 截断，拼装 markdown
    return {"success": True, "title": ..., "content": ..., "markdown": ...}
```

编写时遵守的三条 MaxKB 规范：

1. 入口函数名必须是 `main`，形参名与工具面板中的参数名逐字一致（MaxKB 以 `main(**keywords)` 调用）
2. `main` 必须位于代码末尾（MaxKB 取最后一个定义的对象作为入口）
3. 返回值需可 JSON 序列化；`print` 会被重定向到 devnull，不要依赖它调试

## 四、调用示例

### 4.1 与搜索工具串联（推荐编排）

```
开始(question)
  → DeepSeek 联网搜索(query={{question}}, count=5)
  → AI 对话(从搜索结果中选出最相关的 1~2 条 url)
  → DeepSeek 网页抓取(url={{AI选出的url}}, max_chars=6000)
  → AI 对话(基于正文生成带引用的回答)
```

### 4.2 直接调用（Python）

```python
from deepseek_fetch import main

r = main(api_key="sk-xxxxxxxx", url="https://example.com/article", max_chars=6000)
print(r["title"])
print(r["markdown"][:500])
```

### 4.3 典型返回

```json
{
  "success": true,
  "title": "Example article",
  "url": "https://example.com/article",
  "chars": 5210,
  "truncated": false,
  "content": "# Example article\n\nArticle content...",
  "markdown": "# Example article\n\n来源：https://example.com/article\n\n# Example article..."
}
```

## 五、错误处理

| 现象 | 原因 | 处理 |
| :--- | :--- | :--- |
| `HTTP 400` | URL 不合法（无 host / 带账号密码 / 超 8192） | 检查 url 格式 |
| `HTTP 401` | Key 错误或失效 | 检查启动参数中的 `api_key` |
| `HTTP 402` | 账户余额不足 | 充值后重试 |
| `HTTP 403` | 被 DeepSeek 安全策略拒绝 | 目标站点不允许抓取，更换来源 |
| `HTTP 404` | 无法获取可用网页内容 | URL 失效/被站点拦截/无可提取正文，属正常业务失败 |
| `HTTP 429` | 超过 QPS 限制（账号级 5 QPS + 目标域名单独限速） | 稍后重试 |
| 请求异常 / 超时 | MaxKB 容器无出网权限 | 在容器内执行 `curl -I https://api.deepseek.com` 验证 |
| `ModuleNotFoundError: requests` | 精简镜像缺包 | 代码已内置 urllib 回退，通常无需安装 |

注意：`403`/`404` 多数情况是目标站点策略所致，属预期业务结果，编排中应把 `success=false` 视为"跳过该链接继续"，而非流程报错。

## 六、计费与限速

- 计费：Fetch 按成功请求计费，**5 元 / 1000 次**；失败、超时不计费（必须返回网页正文才计费）
- 限速：账号级 **5 QPS**，另外对目标域名有独立 QPS 限制，超限同样返回 429

## 七、版本记录

| 版本 | 日期 | 说明 |
| :--- | :--- | :--- |
| 1.0.0 | 2026-10-19 | 首发：Fetch 接口封装，支持 max_chars 截断、markdown 拼装与分级错误处理 |
