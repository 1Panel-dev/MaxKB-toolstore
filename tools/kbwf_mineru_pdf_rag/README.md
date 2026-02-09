# PDF 解析 RAG 工作流 (PDF Parsing RAG Workflow)

## 📖 简介 (Introduction)

**PDF 解析 RAG 工作流** 是一个专为 **检索增强生成 (RAG)** 场景设计的高性能文档处理模板。它基于 **MinerU** 强大的解析能力，能够将复杂的 PDF 文档（包含公式、表格、多栏排版及高清图片）深度结构化为 Markdown 格式，并自动将提取的图片资源上传至 MaxKB 对象存储，实现真正的“图文并茂”知识库构建。

---

## ✨ 核心功能 (Features)

* **MinerU 深度解析**：利用 VLM 模型精准还原 PDF 中的布局、表格、数学公式及代码块。
* **图文混排 Markdown**：自动提取文档中的图片，上传至 MaxKB 存储，并在 Markdown 中回填远程链接，保留完整的视觉上下文。
* **高性能 ETL 管道**：
    * **背压控制**：通过 `queue_size` 动态调节内存缓冲区，防止生产速度过快导致内存爆炸。
    * **多线程并发**：支持多线程并行上传图片，最大化利用网络带宽。
    * **智能下载**：优先使用磁盘缓存下载大文件，仅在必要时降级为内存模式。
* **高度可配置**：支持动态调整并发数与队列大小，适应从 256MB 到 1GB+ 的不同运行环境。

---

## 🛠️ 使用说明 (Usage)

### 1. 前置准备

在运行本工作流之前，请确保您已拥有以下服务的访问权限：

* **MaxKB 实例**：用于托管工作流及存储解析后的知识库。
* **MinerU API Token**：用于调用 MinerU 的 PDF 解析服务。可前往 [MinerU 官网](https://mineru.net/) 获取。

### 2. 工作流概览 (Workflow Overview)

本工作流由四个主要节点组成，形成了一个完整的文档处理闭环：


1.  **开始节点 (Start)**：接收用户上传的 PDF 文件。
2.  **MinerU 任务提取 (MinerU Task Submitter)**：将 PDF 提交至 MinerU 平台，并轮询等待解析完成，获取 ZIP 包下载链接。
3.  **解压文件上传与资源清洗 (Unzip & Upload Pipeline)**：下载 ZIP 包，流式解压图片并上传至 MaxKB，最终输出包含远程图片链接的 Markdown 文本。
4.  **文档分段 & 知识库写入 (Chunking & Indexing)**：将清洗后的 Markdown 文本进行分段处理，并写入向量数据库，完成 RAG 索引构建。

---

### 3. 详细参数配置 (Configuration)

#### 🟢 节点 1：MinerU 任务提取 (MinerU Task Submitter)

此节点负责与 MinerU API 交互，是解析流程的入口。

**输入参数 (Input Parameters):**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `pdf_file` | Array | ✅ | - | MaxKB 传入的文件列表（通常引用于 **开始节点** 的输出）。 |
| `mineru_api_token` | String | ✅ | - | MinerU 平台的 API 认证令牌。建议在全局变量中配置。 |
| `maxkb_base_url` | String | ✅ | - | MaxKB 的公网访问域名（例如 `http://kb.example.com`），用于生成回调链接供 MinerU 下载文件。 |
| `mineru_api_url` | String | ❌ | `https://mineru.net/api/v4/extract/task` | MinerU 的任务提交接口地址。 |
| `max_retries` | Integer | ❌ | `120` | 轮询结果的最大重试次数。每次间隔 3 秒，默认总等待时间约 6 分钟。 |

**输出结果 (Output):**

* `result`: JSON 对象，包含 `task_id`、`full_zip_url` (ZIP 包地址) 等。

#### 🔵 节点 2：解压文件上传与资源清洗 (Unzip & Upload Pipeline)

此节点是整个 ETL 流程的核心，负责数据清洗与迁移。

**输入参数 (Input Parameters):**

| 参数名 | 类型 | 必填 | 默认值 | 说明                                                                                             |
| :--- | :--- | :--- | :--- |:-----------------------------------------------------------------------------------------------|
| `miner_data` | Dict | ✅ | - | 引用 **节点 1** 的输出结果 (`MinerU任务提取 > 结果`)。                                                         |
| `kb_id` | String | ✅ | - | 目标知识库 ID，用于标记图片资源的归属。                                                                          |
| `maxkb_api_token` | String | ✅ | - | MaxKB 的 API Token，用于鉴权图片上传接口。                                                                  |
| `maxkb_base_url` | String | ✅ | - | MaxKB 的公网访问域名（同节点 1）。                                                                          |
| `concurrency` | Integer | ❌ | `4` | **并发线程数**。并行上传图片的线程数量。建议值：<br>• 低配环境：`2-4`<br>• 高配环境：`8-16`                                    |
| `queue_size` | Integer | ❌ | `10` | **内存队列缓冲大小**。控制解压后待上传图片的积压数量。<br>• **256MB 内存**：强烈建议填 `8`。<br>• **1GB+ 内存**：建议填 `30` 以上以提升吞吐量。 |

**输出结果 (Output):**

* `result`: JSON 对象，包含最终处理完成的 Markdown 文本 (`content`) 及统计信息。

#### 🟡 节点 3 & 4：文档分段与写入 (Chunking & Indexing)

这两个节点使用 MaxKB 原生组件，负责将 Markdown 内容转化为向量索引。

* **文档分段**：
    * **输入内容**：引用 **节点 2** 的输出 (`解压文件上传... > 结果 > content`)。
    * **分段标识符**：建议使用换行符 `\n` 或 Markdown 标题 `#`。
    * **分段最大长度**：建议 `500-1000` 字符。
* **知识库写入**：
    * **输入内容**：引用 **文档分段** 节点的输出列表。

---

## 💻 核心代码逻辑 (Core Logic)

为了确保在受限资源下稳定运行，**解压文件上传与资源清洗** 节点采用了高度优化的 Python 实现。

### 关键优化点

1.  **智能存储策略**：
    * `download_source` 函数会自动探测 `/dev/shm`（内存盘）和 `/tmp`（磁盘）。对于大文件，优先写入磁盘以节省内存；仅在磁盘不可用时降级为内存流。
2.  **背压机制 (Backpressure)**：
    * 使用 `queue.Queue(maxsize=queue_size)` 连接解压线程（生产者）与上传线程（消费者）。
    * 当队列满时，解压线程会被阻塞，从而物理上限制了内存中积压的图片数量，彻底根治 OOM 问题。
3.  **资源自动释放**：
    * 采用 `tempfile` 管理临时文件，并在流程结束或异常时自动清理。
    * 显式调用 `gc.collect()` 确保大对象（如 ZIP 解压缓冲区）及时回收。

### 完整代码

*(此处省略具体 Python 代码，请参考 workflow 文件中的脚本节点内容)*

---

## ⚠️ 注意事项 (Notes)

1.  **超时设置 (Timeout)**：
    * 对于超过 50MB 的大文件，PDF 解析与图片上传耗时较长。请务必检查 MaxKB 容器环境变量 `MAXKB_SANDBOX_PYTHON_PROCESS_LIMIT_TIMEOUT_SECONDS`，建议设置为 `3600` (1小时) 或更高，防止任务因执行时间过长而被强制终止。

2.  **内存限制 (Memory Limit)**：
    * MaxKB 沙箱默认内存限制为 **256MB** (`MAXKB_SANDBOX_PYTHON_PROCESS_LIMIT_MEM_MB=256`)。
    * **建议优化**：如果您需要处理高清多图的 PDF 或希望提高 `queue_size` 以获得更快的解析速度，强烈建议将此环境变量修改为 `1024` (1GB) 或更高。

3.  **网络连通性 (Connectivity)**：
    * MaxKB 服务器必须能够访问公网（连接 MinerU API）。
    * MinerU 服务器必须能够访问 MaxKB 的 `maxkb_base_url`（下载源 PDF）。请确保该地址是公网可达的。

4.  **低配环境配置**：
    * 如果您的 MaxKB 容器必须运行在默认的 256MB 内存限制下，请务必严格遵守以下参数配置，否则极易发生 OOM (Out Of Memory) 错误：
        * `concurrency`: **4**
        * `queue_size`: **8**