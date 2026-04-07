# MinerU 离线 PDF 转 Markdown

## 简介

**MinerU 离线 PDF 转 Markdown** 用于在 MaxKB 工作流中调用本地离线部署的 MinerU（Gradio 服务）解析 PDF，并直接返回 Markdown 文本，方便后续执行文档分段、入库、RAG 等处理。

与 ZIP 结果流不同，本工具不进行 ZIP 打包、不上传 OSS，输出更轻量，适合内网环境或仅需文本结果的场景。

## 核心能力

- 调用本地离线部署的 MinerU 服务解析 PDF
- 直接输出 Markdown 文本，便于下游节点继续处理
- 支持配置重试次数、最大处理页数与超时时间

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

## 参数说明

### 输入参数

| 参数名 (`Key`) | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| `file_input` | Array / Object | ✅ | MaxKB 文件对象，通常为上游节点输出的文件列表或字典 | `{{start.file_list}}` |

### 启动参数

| 参数名 (`Key`) | 类型 | 必填 | 说明 | 默认值 |
| --- | --- | --- | --- | --- |
| `url_prefix` | String | ✅ | MaxKB 基础地址前缀，用于拼接文件下载地址 | `http://192.168.11.114:8080/admin` |
| `mineru_gradio_url` | String | ✅ | 本地 MinerU Gradio 服务地址 | `http://192.168.11.114:7860/` |
| `gradio_retry_count` | Integer | ❌ | Gradio 调用失败时的重试次数 | `2` |
| `max_convert_pages` | Integer | ❌ | 最大处理页数，用于限制单次解析范围 | `500` |
| `timeout` | Integer | ❌ | 下载与解析超时时间，单位秒 | `600` |

## 输出结果

工具执行成功后返回 `Array[Object]`，长度为 1。示例：

```json
[
  {
    "status": "completed",
    "task_id": "local-xxxxxxxxxxxx",
    "name": "xxx.pdf",
    "size": 12345,
    "uid": 1775184,
    "content": "# Markdown...",
    "markdown_raw": "# Markdown(rendered)..."
  }
]
```

字段说明：

- `content`：推荐给下游节点使用的 Markdown 文本
- `markdown_raw`：MinerU 渲染版 Markdown，便于排查格式问题

## 使用建议

- 如果下游节点只识别 `content`，优先使用 `content`
- 如果 PDF 页数很多，建议显式设置 `max_convert_pages`
- 如果网络或本地服务偶发不稳定，可适当调大 `gradio_retry_count`
- 如果大文件处理耗时较长，建议调大 `timeout`

## 适用场景

- 内网环境下的 PDF 转 Markdown 解析
- 文档预处理后直接进入知识库分段
- 工作流中需要轻量文本输出，不需要图片上传与 OSS 回填
