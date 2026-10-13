## 2.5.0 版本说明

**注意**：当前适用的 MaxKB 版本为 v2.10.4-lts 及以上版本，MinerU（本地解析服务）版本为 **v4**。若仍在使用 MinerU API 3.4.4，请使用 2.4.0 模板。

本版本较 2.4.0 的主要变化：

- 解析节点由 `mineru-parser`（MinerU 3.4.4，`/tasks` 异步批量接口）升级为 **`mineru-v4-parser`（本地 MinerU v4 解析服务）**
- 解析参数由 3.4.4 的 `backend` / `parse_method` / `effort` / `formula_enable` / `table_enable` / `image_analysis` 6 项，精简为单一选择 **`tier`（解析档位）**：`flash` 快速本地文本抽取 / `basic` 基础解析 / `standard` 标准（默认）/ `advanced` 复杂文档高精度
- MinerU 服务默认端口由 `9000` 调整为 **`8001`**
- 新增轮询参数：**`max_wait_seconds`**（解析任务最长等待秒数，默认 1800）、**`poll_interval`**（轮询间隔秒数，默认 2）
- Word 转 PDF 开关（`word_pdf_enable`）与 unoserver 转换节点保持不变

## 简介

**MinerU 本地 PDF 入库工作流模板（2.5.0）** 是一个面向知识库构建场景的工作流模板。它调用本地 MinerU v4 解析服务解析用户上传的文档，直接获取 Markdown 文本，并在 MaxKB 内继续完成文档分段和知识库入库。

## 工作流能力

- 接收用户上传的多种文件：PDF / Word(docx) / PPT(pptx) / Excel(xlsx) / 图片
- 调用 MinerU v4 解析服务（`http://<mineru-ip>:8001`）完成文档转 Markdown
- 可选开启 **Word 转 PDF** 开关：`word_pdf_enable=true` 时先经 unoserver 转换，`false` 时直接透传解析
- 将分段结果写入指定知识库，完成 RAG 入库

## 前置条件

1. 已部署可访问的 MinerU v4 解析服务（默认 `http://<mineru-ip>:8001`）
2. 若开启 Word 转 PDF 开关，需已部署可访问的 **unoserver** 服务（默认 `http://<unoserver-ip>:2003`）

## 工作流结构

该模板包含以下核心节点：

1. **本地文件**（数据源）：接收用户上传的文件列表
2. **Word转PDF**（工具节点）：按 `word_pdf_enable` 开关决定「转 PDF」还是「透传原文件」
3. **MinerU v4 解析**（工具节点）：调用 MinerU v4 服务解析为 Markdown（按 `poll_interval` 轮询，最长等待 `max_wait_seconds`）
4. **文档分段**：对 Markdown 文本进行切分
5. **知识库写入**：将切分结果写入知识库

## 关键参数

### 开关（工作流全局参数）

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `word_pdf_enable` | Boolean | ❌ | Word 转 PDF 开关；`true` 先转 PDF 再解析，`false` 透传原文件直接解析 |

### Word转PDF 工具节点启动参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `unoserver_url` | String | ✅ | unoserver 服务地址，如 `http://<unoserver-ip>:2003` |
| `api_base_url` | String | ✅ | MaxKB 访问地址，如 `http://<maxkb-ip>:8080/` |
| `api_auth_token` | String | ✅ | MaxKB 用户 API Token（`user-xxx`） |
| `username` | String | ✅ | MaxKB 登录用户名，用于获取文件下载 Cookie |
| `password` | String | ✅ | MaxKB 登录密码 |
| `source_id` | String | ✅ | 知识库 ID，用于上传归属（防止转出的 PDF 被临时清理） |

### MinerU v4 解析工具节点启动参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `mineru_api_base_url` | String | ✅ | MinerU v4 API 服务地址，如 `http://<mineru-ip>:8001` |
| `tier` | String | ✅ | 解析档位，单选：`flash` 快速本地文本抽取 / `basic` 基础解析 / `standard` 标准（默认）/ `advanced` 复杂文档高精度 |
| `url_prefix` | String | ✅ | MaxKB 基础地址前缀，用于拼接文件下载地址，如 `http://<maxkb-ip>:8080/admin` |
| `upload_token` | String | ✅ | MaxKB 用户 API Token（`user-xxx`），用于 OSS 接口鉴权 |
| `username` | String | ✅ | MaxKB 登录用户名 |
| `password` | String | ✅ | MaxKB 登录密码 |
| `knowledge_id` | String | ✅ | 当前工作流知识库 ID，用于图片上传归属 |
| `max_wait_seconds` | Integer | ❌ | 解析任务最长等待秒数，默认 `1800` |
| `poll_interval` | Integer | ❌ | 轮询间隔（秒），默认 `2` |

## 使用说明

1. 导入该 `kbwf` 模板到 MaxKB
2. 确认 `mineru_api_base_url`、`url_prefix`、`unoserver_url`、`api_base_url` 填写正确
3. 填写两个工具节点的 `upload_token` / `api_auth_token`、`username`、`password`、`knowledge_id` / `source_id`
4. 按需选择 MinerU 解析档位 `tier`（默认 `standard`），必要时调整 `max_wait_seconds`、`poll_interval`
5. 上传测试文件
6. 按需开启 / 关闭 `word_pdf_enable` 开关
7. 检查工具节点输出中的 `content`
8. 确认文档分段与知识库写入结果正常

## 注意事项

- 本模板适配 **MinerU v4**；若解析服务仍为 MinerU API 3.4.4，请使用 2.4.0 模板
- 若在 ON 状态混入非 Word 文件，Word转PDF 节点会因「不支持的文件格式」报错——请按文件类型分开上传
- MinerU v4 原生支持 docx / pptx / xlsx / 图片，无需必经 Word 转 PDF
- **无 GPU 建议**：没有 GPU 时建议开启 `word_pdf_enable`，开启后可达与 GPU 相同的解析效果。

## 关联工具

- `tool_unoserver_file_converter`：Word 转 PDF 工具（依赖 unoserver 服务）
- `mineru-v4-parser`（MinerU v4 解析）：调用本地 MinerU v4 解析服务并轮询取回结果
