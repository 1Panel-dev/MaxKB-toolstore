# MinerU 在线 API PDF 解析 ZIP 获取工具

## 📖 简介 

**MinerU 在线 API PDF 解析 ZIP 获取** 是 PDF 解析 RAG 工作流的核心前置工具。它负责将 MaxKB 传入的 **单个** PDF 文件提交至 MinerU 解析服务，并持续轮询任务状态，最终获取包含高保真解析结果（Markdown、公式、图片）的 ZIP 压缩包下载链接。

本工具作为 ETL 流程的“生产者”，为后续的解压清洗与知识库入库提供标准化的数据源。

---

## ✨ 核心功能

* **自动化任务提交**：一键将 MaxKB 文件流对接至 MinerU API，支持 VLM 高精度模式。
* **智能轮询机制**：内置指数退避与状态检测，自动处理任务排队、进行中、完成及失败状态。
* **回调链接生成**：自动生成 MaxKB 的公网回调地址，确保 MinerU 服务器能够正确读取源文件。
* **异常处理**：能够识别并反馈 MinerU 服务端的错误信息（如解析失败、超时等）。

---

## 🛠️ 使用说明 

### 1. 前置条件

* **MinerU API Token**：需要有效的 MinerU API 令牌（可在 [MinerU 官网](https://mineru.net/) 申请）。
* **公网可访问的 MaxKB**：MaxKB 实例必须具备公网 IP 或域名，且 `maxkb_base_url` 能够被外部网络（MinerU 服务器）访问。

### 2. 参数配置

在工作流节点中，请按照以下说明配置输入参数：

| 参数名 (`Key`) | 类型 | 必填 | 说明 | 示例值                                      |
| :--- | :--- | :--- | :--- |:-----------------------------------------|
| `pdf_file` | Array | ✅ | MaxKB 传入的文件对象列表。通常引用上游“开始”节点的输出。 | `{{start.file_list}}`                    |
| `mineru_api_token` | String | ✅ | MinerU 平台的 API 认证令牌。 | `eyJhbGciOiJIUzI1Ni...`                  |
| `maxkb_base_url` | String | ✅ | MaxKB 的**公网访问域名**。MinerU 将通过此地址下载源 PDF。**注意：不能填 localhost 或内网 IP**。 | `https://kb.yourdomain.com/admin`        |
| `mineru_api_url` | String | ✅ | MinerU 任务提交接口地址。 | `https://mineru.net/api/v4/extract/task` |
| `max_retries` | Integer | ❌ | 轮询重试次数。每次间隔 3 秒。默认 120 次（约 6 分钟）。**大文件建议调大此值**。 | `200`                                    |

### 3. 输出结果

工具执行成功后，将返回一个 JSON 对象，包含以下关键信息：

* `task_id`: MinerU 任务的唯一标识符。
* `full_zip_url`: 解析完成后生成的 ZIP 包下载直链（有效期通常有限，需尽快处理）。
* `file_name`: 原始文件名。
* `status`: 任务最终状态 (`completed`)。

---

## ⚠️ 注意事项

1.  **网络连通性**：最常见的问题是 **"Download failed"**。请务必检查 `maxkb_base_url` 是否正确，并且您的 MaxKB 服务器防火墙允许外部访问。
2.  **超时设置**：对于超过 50MB 的 PDF，解析时间可能超过 5 分钟。请适当增加 `max_retries` 参数（例如设为 300），并确保 MaxKB 容器的 `MAXKB_SANDBOX_PYTHON_PROCESS_LIMIT_TIMEOUT_SECONDS` 环境变量足够大。
3.  **API 配额**：请关注您的 MinerU 账户余额或调用次数限制。
4. **解析文件数**：目前只支持**单个**文件上传解析。