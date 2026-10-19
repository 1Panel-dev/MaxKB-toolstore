# DeepSeek 联网搜索工具

基于 DeepSeek 官方 Search API（<https://api-docs.deepseek.com/zh-cn/guides/search>）封装的联网搜索工具，为 MaxKB 智能体提供实时网页检索能力。

## 一、功能说明

- **实时检索**：调用 `https://api.deepseek.com/v1/tools/search`，返回标题、链接、短摘要、长摘要、站点名、发布时间、权威性与重排分数
- **搜索语法**：支持 `site:` / `-site:` / `"精确短语"` / `-关键词` / `lang:` / `after:` / `before:`，可在一次 query 中组合使用
- **正文可选**：`need_content=true` 时额外返回网页正文，适合需要深读的场景；默认关闭以节省上下文
- **双形态返回**：同时给出结构化 `results` 数组与拼装好的 `markdown`，后者带链接与来源标注，模型可直接用于回答
- **降级友好**：任何失败都返回 `success: false` 而非抛异常，工作流可据此决定是否退化为"不联网回答"

## 二、参数说明

### 2.1 启动参数

| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `api_key` | 密码框 | 是 | DeepSeek API Key，在 <https://platform.deepseek.com/api_keys> 获取 |

> 启动参数与输入参数分离，工作流中只需关注 `query`，可避免 Key 在编排界面反复暴露。

### 2.2 输入参数

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `query` | string | 是 | 引用参数 | 搜索关键词，1～128 个字符，不能全为空白 |
| `count` | int | 否 | 自定义参数 | 返回条数，默认 10，范围 1～50，越界自动夹逼 |
| `need_content` | string | 否 | 引用参数 | 是否返回网页正文，`false`（默认）/ `true` |
| `ori_question` | string | 否 | 引用参数 | 用户原始问题，有助于搜索意图理解，可留空 |

### 2.3 输出参数

返回一个 dict（已可 JSON 序列化）：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `success` | bool | 是否成功 |
| `query` | string | 实际发出的搜索词 |
| `count` | int | 实际返回条数 |
| `results` | array | 结果数组，元素字段见下 |
| `markdown` | string | 拼装好的 Markdown，含序号、站点、时间、权威性、链接与摘要 |
| `notice` | string | 无结果时的提示信息 |
| `error` / `hint` / `status` | string / string / int | 失败时的错误信息、排查建议与原样状态码 |

`results` 元素字段：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `title` | string | 标题 |
| `url` | string | 结果链接 |
| `snippet` | string | 短摘要（100～200 字符），适合前端展示 |
| `summary` | string | 长摘要（600～800 字符），适合给模型阅读 |
| `content` | string | 网页正文，`need_content=false` 时为空串 |
| `site_name` | string / null | 站点名称 |
| `date` | string / null | 发布时间，UTC RFC 3339 |
| `authority` | int | 权威性 0～4，`≥3` 为极权威，`-1` 表示未知 |
| `rerank_score` | number | 相关度 0～3，`≥1.5` 为优质结果 |

## 三、工具内容（Python）

完整源码见本目录下 `deepseek_search.py`（同时内嵌于 `1.0.0/DeepSeek联网搜索.tool`）。

核心实现约 200 行，结构如下：

```python
def main(api_key, query, count=10, need_content="false", ori_question=""):
    # 1. 参数校验：api_key / query 必填，count 夹逼到 1~50
    # 2. POST https://api.deepseek.com/v1/tools/search
    #    headers: Authorization: Bearer <key>, Content-Type: application/json
    # 3. 状态码分级：400/401/402/429/500/504 分别给出排查提示
    # 4. 结果整形：抽取字段 + 拼接 Markdown
    return {"success": True, "query": ..., "count": ..., "results": [...], "markdown": "..."}
```

编写时遵守的三条 MaxKB 规范：

1. 入口函数名必须是 `main`，形参名与工具面板中的参数名逐字一致（MaxKB 以 `main(**keywords)` 调用）
2. `main` 必须位于代码末尾（MaxKB 取最后一个定义的对象作为入口）
3. 返回值需可 JSON 序列化；`print` 会被重定向到 devnull，不要依赖它调试

## 四、调用示例

### 4.1 工作流节点调用

工具节点参数配置：

| 节点参数 | 取值 |
| :--- | :--- |
| `api_key` | 启动参数中已配置，无需重复填写 |
| `query` | 引用「开始」节点的 `question` |
| `count` | 5 |
| `need_content` | false |

下游 AI 对话节点提示词中加入：

```
参考资料：
{{搜索节点.markdown}}
```

### 4.2 直接调用（Python）

```python
from deepseek_search import main

r = main(
    api_key="sk-xxxxxxxx",
    query="DeepSeek 模型 site:github.com lang:zh after:2025",
    count=5,
    need_content="false",
)
print(r["markdown"])
```

### 4.3 典型返回

```json
{
  "success": true,
  "query": "DeepSeek V4 模型 发布",
  "count": 2,
  "results": [
    {
      "title": "DeepSeek V4 模型发布",
      "url": "https://example.com/deepseek-v4",
      "snippet": "DeepSeek V4 已上线，支持工具调用与长上下文。",
      "summary": "DeepSeek 发布了 V4 模型。此次发布改进了工具调用与长上下文能力，适合 Agent 工作流。",
      "content": "",
      "site_name": "Example News",
      "date": "2026-06-01T00:00:00+00:00",
      "authority": 3,
      "rerank_score": 2.4
    }
  ],
  "markdown": "### 1. DeepSeek V4 模型发布\n- 站点：Example News ｜ 时间：2026-06-01T00:00:00+00:00 ｜ 权威性：3/4 ｜ 相关度：2.4/3\n- 链接：https://example.com/deepseek-v4\n\n长摘要..."
}
```

## 五、错误处理

| 现象 | 原因 | 处理 |
| :--- | :--- | :--- |
| `HTTP 401 Authentication Fails` | Key 错误或失效 | 检查启动参数中的 `api_key`，去掉首尾空格 |
| `HTTP 402` | 账户余额不足 | 充值后重试 |
| `HTTP 429` | 超过账号级 QPS（Search 5 QPS） | 稍后重试，或在编排中增加延时 |
| `HTTP 400` | query 或 count 不合法 | 检查 query 长度与 count 范围 |
| `HTTP 5xx` | 服务端错误或下游超时 | 稍后重试 |
| 请求异常 / 超时 | MaxKB 容器无出网权限 | 在容器内执行 `curl -I https://api.deepseek.com` 验证 |
| `ModuleNotFoundError: requests` | 精简镜像缺包 | `docker exec -it maxkb pip install requests`（代码已内置 urllib 回退，通常无需安装） |

## 六、计费与限速

- 计费：Search 按成功请求计费，**5 元 / 1000 次**；`count` 不影响单价；请求失败、无结果、超时不计费
- 限速：每个账号独立 **5 QPS**，与模型并发限制互不影响

## 七、版本记录

| 版本 | 日期 | 说明 |
| :--- | :--- | :--- |
| 1.0.0 | 2026-10-19 | 首发：Search 接口封装，支持搜索语法、可选正文、Markdown 输出与分级错误处理 |
