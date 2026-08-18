# MinerU 本地 PDF 入库工作流模板

## 版本说明

**当前版本**：2.3.0

- 适用于 MaxKB v2.10.4-lts 及以上版本
- 本地 MinerU 版本为 3.4.4

## 简介

**MinerU 本地 PDF 入库工作流模板** 是一个面向知识库构建场景的工作流模板。它调用本地离线部署的 MinerU（Gradio 服务）解析用户上传的 PDF，直接获取 Markdown 文本，并在 MaxKB 内继续完成文档分段和知识库入库。

该模板适合无法访问公网 API、需要本地私有化部署、或者只需要文本入库而不要求图片上传 OSS 的场景。

## 工作流能力

- 接收用户上传的 PDF 文件
- 调用本地 MinerU 服务完成 PDF 转 Markdown
- 可选开启 LLM 标题增强，由大模型修正标题层级后再分段入库
- 将分段结果写入指定知识库，完成 RAG 入库

## 前置条件

1. 已离线部署 MinerU（Gradio 服务）

参考：
https://opendatalab.github.io/MinerU/zh/quick_start/docker_deployment/

2. 在 MaxKB 容器内安装依赖并授权临时目录

```bash
# 到 maxkb 容器内安装 gradio_client
docker exec -it maxkb bash
pip install gradio_client

# 如果安装 gradio_client 提示 huggingface-hub 版本冲突，则使用 pip 的兼容性模式，同时安装兼容版本
pip install gradio_client huggingface-hub==0.34.0

# 授权 tmp 目录的访问操作权限
chmod 777 /tmp
```

## 工作流结构

该模板通常包含以下几个核心节点：

1. 开始节点：接收用户上传的 PDF 文件
2. MinerU 离线 PDF 转 Markdown 工具：调用本地 MinerU 解析文档
3. 文档分段节点：对 Markdown 文本进行切分
4. 知识库写入节点：将切分后的结果写入知识库

开启 `enable_llm_enhancement` 后，MinerU 工具与文档分段之间会增加标题提取、AI 对话和标题替换节点，由大模型修正标题层级后再入库。

## 关键参数

### MinerU 工具节点输入参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `file_input` | Array / Object | ✅ | 开始节点传入的文件对象 |

### MinerU 工具节点启动参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `url_prefix` | String | ✅ | MaxKB 基础地址前缀，用于拼接文件下载地址，如 `http://<maxkb-ip>:8080/admin` |
| `mineru_gradio_url` | String | ✅ | 本地 MinerU Gradio 服务地址，如 `http://<mineru-ip>:7860/` |
| `upload_token` | String | ✅ | MaxKB 用户 API Token（`user-xxx`），用于 OSS 接口鉴权 |
| `backend` | String | ✅ | MinerU 处理引擎模式，如 `pipeline`、`hybrid-auto-engine`、`vlm-auto-engine` |
| `knowledge_id` | String | ✅ | 当前工作流知识库 ID，用于图片上传归属，保证图片永久保留 |
| `username` | String | ✅ | MaxKB 登录用户名，用于获取文件下载鉴权 Cookie |
| `password` | String | ✅ | MaxKB 登录密码 |

### 工作流全局参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `enable_llm_enhancement` | Boolean | ❌ | 是否启用 LLM 标题增强；关闭时转换后直接分段入库，开启时由大模型修正标题层级后再入库 |

### 启动参数示例

| 参数名 | 示例值 |
| --- | --- |
| `url_prefix` | `http://192.168.1.100:8080/admin` |
| `mineru_gradio_url` | `http://192.168.1.100:7860/` |
| `upload_token` | `user-74xxxxxx` |
| `backend` | `pipeline` |
| `knowledge_id` | 工作流绑定的知识库 ID |
| `username` | `admin` |
| `password` | `********` |

## LLM 标题增强说明

### MinerU llm-aided config

`llm-aided config` 是 MinerU 中 `mineru.json` 配置文件的一部分，用于配置并启用大模型辅助识别和优化 PDF 文档中的标题层级。开启后，MinerU 在解析复杂 PDF 时会利用大模型智能识别文档中的标题，划分多级标题层级（H1、H2、H3 等），让转换出的 Markdown 结构更清晰规范。

### enable_llm_enhancement

`enable_llm_enhancement` 是 MaxKB 工作流编排层的业务开关。开启后，工作流会通过后半段的 `ai-chat-node`（大模型对话节点）配合 Prompt，对 MinerU 提取出的标题进行结构化纠错，再按修正后的层级进行文档分段和知识库入库。

### 使用建议

建议在 MinerU 中开启 `llm-aided config`，以保证转换出的 Markdown 标题层级仍然清晰规范。若无法开启，建议使用工作流中的  `enable_llm_enhancement`。

## 使用说明

1. 导入该 `kbwf` 模板到 MaxKB
2. 确认工具节点中的 `url_prefix` 与 `mineru_gradio_url` 填写正确
3. 填写 `upload_token`、`knowledge_id`、`username`、`password`
4. 按需设置 `backend` 解析引擎
5. 上传测试 PDF 文件
6. 按需开启 `enable_llm_enhancement`
7. 检查工具节点输出中的 `content`
8. 确认文档分段与知识库写入结果正常

## 注意事项

- 该模板依赖本地 MinerU 服务可访问，不能直接替代在线 MinerU API 工作流
- 2.3.0 版本使用 `/convert_to_markdown_stream` 接口，适用于 MaxKB v2.10.4-lts 及以上版本
- 如果 PDF 文件较大或内容复杂，建议确认容器临时目录可写，并为任务预留足够的超时时间

## 关联工具

- `tool_mineru_local_markdown`：本工作流依赖的核心工具
