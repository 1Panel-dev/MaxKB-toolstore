# MinerU 离线 PDF 转 Markdown

## 📖 简介

**MinerU 离线 PDF 转 Markdown** 用于在 MaxKB 工作流中调用**本地离线部署**的 MinerU（Gradio 服务）解析 PDF，并**直接返回 Markdown 文本**，方便后续执行“文档分段 / 入库 / RAG”等处理。

与 ZIP 结果流不同，本工具不进行 ZIP 打包、不上传 OSS，输出更轻量。

## ✅ 前置条件

1. 已离线部署 MinerU（Gradio 服务）

参考：
https://opendatalab.github.io/MinerU/zh/quick_start/docker_deployment/

2. MaxKB v2.4+ 建议配置（按需）

修改 `/opt/maxkb/conf/maxkb.env`：

```bash
MAXKB_SANDBOX_TMP_DIR_ENABLED=1
MAXKB_SANDBOX_PYTHON_ALLOW_SUBPROCESS=1
MAXKB_SANDBOX_PYTHON_PROCESS_LIMIT_MEM_MB=521
```

重启：

```bash
docker restart maxkb
```

3. 依赖安装

在 maxkb 容器内安装：

```bash
pip install gradio_client
# 如果存在 huggingface-hub 版本冲突
pip install gradio_client huggingface-hub==0.34.0
```

## 🧩 参数说明

### 输入参数

| 参数名 (`Key`) | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| `file_input` | Array / Object | ✅ | MaxKB 文件对象（通常是上游节点输出的文件列表/字典） | `{{start.file_list}}` |

### 启动参数

| 参数名 (`Key`) | 类型 | 必填 | 说明 | 默认值 |
| --- | --- | --- | --- | --- |
| `url_prefix` | String | ✅ | MaxKB 管理端前缀，用于拼接下载地址 | `http://<ip>:8080/admin` |
| `mineru_gradio_url` | String | ✅ | MinerU Gradio 服务地址 | `http://localhost:7860/` |
| `enable_ocr` | Boolean | ❌ | 是否启用 OCR | `true` |
| `enable_formula` | Boolean | ❌ | 是否启用公式识别 | `true` |
| `enable_table` | Boolean | ❌ | 是否启用表格识别 | `true` |
| `language` | String | ❌ | 语言选项 | `ch (Chinese, English, Chinese Traditional)` |
| `backend` | String | ❌ | 解析引擎 | `vlm-auto-engine` |
| `max_convert_pages` | Integer | ❌ | 最大解析页数 | `500` |
| `download_dir` | String | ❌ | 临时下载目录（为空时自动探测可写目录） | 空字符串 |
| `gradio_retry_count` | Integer | ❌ | Gradio 调用失败重试次数 | `2` |
| `timeout` | Integer | ❌ | 下载与解析超时（秒） | `600` |

## 📤 输出结果

工具执行成功后返回 `Array[Object]`（长度为 1），示例：

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

- `content`：推荐使用的 Markdown 文本（下游分段节点通常用这个）
- `markdown_raw`：MinerU 渲染版 Markdown（便于排查格式问题）

## 🔧 使用建议

- 如果下游节点只认 `content`，请优先使用 `content`
- 如果遇到权限问题（临时目录 / HuggingFace cache），请确保容器内 `/tmp` 可写
