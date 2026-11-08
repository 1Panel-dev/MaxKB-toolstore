# LinkDigest 社交链接转文本

把一条社交媒体链接变成大模型能读的文本。支持小红书、抖音、B站、微博、微信公众号、小宇宙、TikTok、YouTube、X、Instagram；直接贴 App 里「分享 → 复制链接」出来的整段文案也行，工具会取出里面的链接。

> 说明：本工具由 LinkDigest 的作者提交，调用的是 LinkDigest 的托管服务（https://linkdigest.dev），需要一个 LinkDigest API Key。工具代码完整公开在本目录的 `linkdigest_reader.py`，与 `.tool` 文件中的代码一致。

## 功能

- **视频**：带秒数的口播文案（语音转写）、画面上的字（花字、字幕条）、要点
- **图文笔记**：正文、逐图文字、要点
- **小红书**：分享页上展示的几条热评（不是全部评论）
- 不登录、不用 Cookie、不碰任何账号；只读公开页面，不发布任何内容
- 读不到的内容（已删除、仅自己可见、平台拒绝）会说明原因，不扣积分

## 参数说明

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | string | 是 | 链接或整段分享文案 |
| `depth` | string | 否 | 留空 = 完整读取（口播 + 画面文字 + 要点）；`transcript` = 逐字稿优先；`script` = 只要口播文案（最便宜） |
| `max_chars` | int | 否 | `content` 的最大字符数，默认 12000，超出截断 |

**启动参数**

| 参数 | 说明 |
|---|---|
| `api_key` | LinkDigest API Key，形如 `ld_live_...`。注册后在 https://linkdigest.dev/app/keys 获取 |

**输出（dict）**

| 字段 | 说明 |
|---|---|
| `success` | 是否成功 |
| `platform` / `title` / `author` / `url` | 平台、标题、作者、原链接 |
| `transcript` | 口播文案（每段一行） |
| `on_screen_text` | 画面上的字 |
| `key_points` | 要点列表 |
| `top_comments` | 小红书分享页上的热评 |
| `content` | 整篇 Markdown（可直接交给大模型） |
| `credits` / `credits_left` / `cached` | 本次扣的积分、剩余积分（免费账号）、是否命中缓存 |
| `error` / `error_code` / `hint` | 失败时的原因和处理建议；积分不够时还会带购买链接 |

## 调用方式

接口：`POST https://linkdigest.dev/api/v1/digest`，请求头 `Authorization: Bearer <api_key>`，请求体 `{"url": "...", "depth": "script"}`。视频通常要 30–90 秒，接口约 25 秒内先返回 `pending`；本工具会自动重发同样的请求（同一条只扣一次费），最多等约 100 秒。

## 使用示例

```
url: 7.32 复制打开抖音，看看【…的作品】… https://v.douyin.com/xxxxxxx/
depth: script
max_chars: 8000
```

返回（节选）：

```json
{
  "success": true,
  "platform": "douyin",
  "title": "拖地机器人全自动扫地机家用一拖净干湿两用拖把智能懒人擦洗地机",
  "transcript": "快来看看这款超实用的拖地机器人,加水开机就行,它边走边湿拖……",
  "key_points": ["产品为一款超实用的拖地机器人。", "操作简便，只需加水并开机即可使用。"],
  "credits": 0,
  "cached": true
}
```

## 费用

按读取量扣积分，任何人读过的同一条链接再读不扣积分：

- 图文笔记：一般 1 积分（每 6 张图 1 积分）
- 视频完整读取：1 积分 + 每分钟 1 积分；`transcript`：1 积分 + 每 2 分钟 1 积分；`script`：每 2 分钟 1 积分
- 注册送 10 积分；之后支付宝 ¥9.9 = 50 积分、¥36 = 250 积分（一次性，不订阅、不过期），也可用银行卡

## 链接

- 官网：https://linkdigest.dev
- 中文文档：https://linkdigest.dev/zh/docs
- 开源 SDK / MCP：https://github.com/jcaiagent7143-ui/linkdigest-mcp
- 联系：support@linkdigest.dev
