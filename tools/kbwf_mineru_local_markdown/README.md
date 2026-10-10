# MinerU 本地 PDF 入库工作流模板

## 版本说明

**当前版本**：2.4.0

- 适用于 MaxKB v2.10.4-lts 及以上版本
- 适配 MinerU（API 服务）3.4.4

## 简介

**MinerU 本地 PDF 入库工作流模板** 是一个面向知识库构建场景的工作流模板。它调用本地 MinerU API 服务解析用户上传的文档，直接获取 Markdown 文本，并在 MaxKB 内继续完成文档分段和知识库入库。

## 工作流能力

- 接收用户上传的多种文件：PDF / Word(docx) / PPT(pptx) / Excel(xlsx) / 图片
- 调用 MinerU API（`http://<mineru-ip>:9000`）完成文档转 Markdown
- 可选开启 **Word 转 PDF** 开关：`word_pdf_enable=true` 时先经 unoserver 转换，`false` 时直接透传解析
- 将分段结果写入指定知识库，完成 RAG 入库

## 前置条件

1. 已部署可访问的 MinerU API 服务（支持 `/tasks` 接口，默认 `http://<mineru-ip>:9000`）
2. 若开启 Word 转 PDF 开关，需已部署可访问的 **unoserver** 服务（默认 `http://<unoserver-ip>:2003`）；部署参考：[unoserver 文档类型转换工具](https://apps.fit2cloud.com/maxkb/tool-unoserver-file-converter)

## 工作流结构

本模板把「本地文档 → 知识库入库」串成 5 个节点，数据依次流转：

1. **本地文件（数据源）**：接收用户上传的文件列表，得到 `file_list`（每项含 `file_id`、`name`）。
2. **Word转PDF（工具节点）**：按 `word_pdf_enable` 开关分流——开启时经 unoserver 把 Word 转成 PDF 并回传；关闭时原样透传。
3. **MinerU 解析（工具节点）**：把文件提交给本地 MinerU API（`/tasks`），轮询至解析完成后下载结果，得到 Markdown（含图片，图片上传至 MaxKB OSS 后路径被替换为可访问链接）。
4. **文档分段**：按 Markdown 的标题层级切分文本。
5. **知识库写入**：把切分结果写入指定知识库，完成 RAG 入库。

一句话概括：**上传文件 →（可选）Word 转 PDF → MinerU 解析为 Markdown → 分段 → 入库**。

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

### MinerU 解析工具节点启动参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `mineru_api_base_url` | String | ✅ | MinerU API 服务地址，如 `http://<mineru-ip>:9000` |
| `url_prefix` | String | ✅ | MaxKB 基础地址前缀，用于拼接文件下载地址，如 `http://<maxkb-ip>:8080/admin` |
| `upload_token` | String | ✅ | MaxKB 用户 API Token（`user-xxx`），用于 OSS 接口鉴权 |
| `username` | String | ✅ | MaxKB 登录用户名 |
| `password` | String | ✅ | MaxKB 登录密码 |
| `knowledge_id` | String | ✅ | 当前工作流知识库 ID，用于图片上传归属 |
| `backend` | String | ✅ | MinerU 处理引擎，如 `pipeline`、`hybrid-engine` |
| `parse_method` | String | ✅ | 解析方式，如 `auto`、`txt`、`ocr` |
| `effort` | String | ✅ | 解析力度，如 `medium`、`high` |
| `formula_enable` | Boolean | ✅ | 是否解析公式 |
| `table_enable` | Boolean | ✅ | 是否解析表格 |
| `image_analysis` | Boolean | ✅ | 是否进行图片/图表分析 |

## LLM 标题增强说明

### MinerU llm-aided config

建议在 MinerU 中开启 `llm-aided config`，以保证转换出的 Markdown 标题层级仍然清晰规范。
`llm-aided config` 是 MinerU 中 `mineru.json` 配置文件的一部分，用于配置并启用大模型辅助识别和优化 PDF 文档中的标题层级。开启后，MinerU 在解析复杂 PDF 时会利用大模型智能识别文档中的标题，划分多级标题层级（H1、H2、H3 等），让转换出的 Markdown 结构更清晰规范。

## 使用说明

1. 导入该 `kbwf` 模板到 MaxKB
2. 确认 `unoserver_url`、`api_base_url`、`mineru_api_base_url`、`url_prefix` 填写正确
3. 填写两个工具节点的 `api_auth_token`、`username`、`password`、`knowledge_id` / `source_id`
4. 按需设置 MinerU 的 `backend`、`parse_method` 等
5. 上传测试文件
6. 按需开启 / 关闭 `word_pdf_enable` 开关
7. 检查工具节点输出中的 `content`
8. 确认文档分段与知识库写入结果正常

## 注意事项

- 若在 ON 状态混入非 Word 文件，Word转PDF 节点会因「不支持的文件格式」报错——请按文件类型分开上传
- MinerU 3.4.4 原生支持 docx / pptx / xlsx / 图片，无需必经 Word 转 PDF
- 若不使用 unoserver（即不开启 `word_pdf_enable`）：无需在 MaxKB 的 unoserver 文档转换工具（Word转PDF 节点）中设置任何启动参数，也不必打开 Word 转 PDF 开关。

## 为什么需要 LibreOffice 先转 PDF

LibreOffice（经 unoserver 封装）把 Word 转成 PDF，目的不是「换格式」，而是让 MinerU 改走能识别标题的链路。

MaxKB 采用**结构化分块**——按 Markdown 标题层级切分文档，因此分块质量取决于解析出的文本有没有正确的标题层级。而 MinerU 解析 Word（docx）时走 Office 原生解析链路、**不经过 OCR**，拿不到标题层级：非标准样式的 Word 常用「把字号放大」冒充标题，原生解析出的 Markdown 因此没有结构，MaxKB 只能按长度硬切，导致块碎、语义不完整、召回效果差。

经 LibreOffice 转成 PDF 后，MinerU 改走 **PDF 链路、可以走 OCR**，视觉模型能识别出「字号更大 / 加粗」的标题，输出正确的 `#` 层级，MaxKB 的结构化分块随之恢复正常，切块效果大幅提升；若再搭配 MinerU 的 `llm-aided config`（见「LLM 标题增强说明」），标题识别的效果会更精准。

代价是多一步转换（需额外部署 unoserver），且开关开启时不能混入非 Word 文件。

> **说明**：在线版 MinerU 处理 Word 时，本身就是「**先把 Word 转成 PDF、再对 PDF 走 OCR**」；本方案借鉴这条链路，用 LibreOffice 承担其中「Word → PDF」这一步，让本地 MinerU 也能走「转 PDF → OCR」的同一条链路，从而获得与在线版一致的标题/结构识别效果。

## 关联工具

- `tool_unoserver_file_converter`：Word 转 PDF 工具（依赖 unoserver 服务）
- `mineru-parser`（MinerU API 批量解析）：调用本地 MinerU `/tasks` 接口解析
