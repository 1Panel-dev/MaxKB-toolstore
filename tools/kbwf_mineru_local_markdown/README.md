# MinerU 本地 PDF 入库工作流模板

## 简介

**MinerU 本地 PDF 入库工作流模板** 是一个面向知识库构建场景的工作流模板。它调用本地离线部署的 MinerU（Gradio 服务）解析用户上传的 PDF，直接获取 Markdown 文本，并在 MaxKB 内继续完成文档分段和知识库入库。

该模板适合无法访问公网 API、需要本地私有化部署、或者只需要文本入库而不要求图片上传 OSS 的场景。

## 工作流能力

- 接收用户上传的 PDF 文件
- 调用本地 MinerU 服务完成 PDF 转 Markdown
- 直接使用 Markdown 文本进入文档分段节点
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

## 关键参数

### MinerU 工具节点输入参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `file_input` | Array / Object | ✅ | 开始节点传入的文件对象 |
| `url_prefix` | String | ✅ | MaxKB 基础地址前缀，用于拼接文件下载地址 |
| `mineru_gradio_url` | String | ✅ | 本地 MinerU Gradio 服务地址 |
| `gradio_retry_count` | Integer | ❌ | Gradio 调用失败时的重试次数 |
| `max_convert_pages` | Integer | ❌ | 最大处理页数 |
| `timeout` | Integer | ❌ | 下载与解析超时时间，单位秒 |

### 启动参数示例

| 参数名 | 示例值 |
| --- | --- |
| `url_prefix` | `http://192.168.11.114:8080/admin` |
| `mineru_gradio_url` | `http://192.168.11.114:7860/` |
| `gradio_retry_count` | `2` |
| `max_convert_pages` | `500` |
| `timeout` | `600` |

## 使用说明

1. 导入该 `kbwf` 模板到 MaxKB
2. 确认工具节点中的 `url_prefix` 与 `mineru_gradio_url` 填写正确
3. 按需设置 `gradio_retry_count`、`max_convert_pages`、`timeout`
4. 上传测试 PDF 文件
5. 检查工具节点输出中的 `content`
6. 确认文档分段与知识库写入结果正常

## 注意事项

- 该模板依赖本地 MinerU 服务可访问，不能直接替代在线 MinerU API 工作流
- 该模板输出以 Markdown 文本为主，不包含图片上传 OSS 的处理链路
- 如果 PDF 文件较大或内容复杂，建议调大 `timeout` 并确认容器临时目录可写

## 关联工具

- `tool_mineru_local_markdown`：本工作流依赖的核心工具
