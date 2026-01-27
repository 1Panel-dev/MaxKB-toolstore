# 调用本地 MinerU 解析 PDF 工具

一个调用本地 MinerU 解析 PDF 的工具，支持解析 PDF 中的普通文本、图片中的文字

注意：只支持离线部署的 MinerU

## 离线部署 MinerU

离线部署 MinerU 操作步骤链接如下:

https://mineru.site/%E7%96%91%E9%9A%BE%E6%9D%82%E7%97%87/2025/05/22/1fa9e6fa-6062-8065-82db-cc0cf9818496

### 配置参数
MaxKB v2.4 及以上版本，需修改配置文件 `/opt/maxkb/conf/maxkb.env`

```bash
MAXKB_SANDBOX_TMP_DIR_ENABLED=1
MAXKB_SANDBOX_PYTHON_ALLOW_SUBPROCESS=1
MAXKB_SANDBOX_PYTHON_PROCESS_LIMIT_MEM_MB=521
```
重启 maxkb 容器
```bash
docker restart maxkb
```

### 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

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

### 启动参数
| 参数名称                    | 参数类型     | 参数说明                                          | 默认值                                                         |
|-------------------------|--------------|--------------------------------------------------|-------------------------------------------------------------|
| `enable_formula`        | 开关           | 控制是否提取文件中的数学公式                             | True                                                        |
| `language`              | 字符串          | 指定文件内容的主要语言（影响 OCR 识别准确率）              | `ch`                                                        |
| `enable_table`          | 开关           | 控制是否提取文件中的表格结构并转换为 Markdown 表格          | True                                                        |
| `download_dir`          | 字符串          | 存储下载的原始文件和解析临时文件的目录路径                  | `/tmp`                                                      |
| `upload_url`            | 字符串          | 图片上传至 OSS 存储的接口地址                           | `http://MaxKB 服务器 ip:MaxKB 服务端口(默认8080)/admin/api/oss/file` |
| `upload_token`          | 字符串          | 在 MaxKB 的 API Key 管理中创建的 API Key              | API Key                                                     |
| `url_prefix`            | 字符串          | 拼接 file_input 中相对路径的前缀，生成完整文件下载 URL      | `http://MaxKB 服务器 ip:MaxKB 服务端口(默认8080)/admin`              |
| `enable_ocr`            | 开关           | 控制是否启用 OCR 功能（识别图片类文件或文件中的图片内容）      | True                                                        |
| `gradio_retry_count`    | 整数           | Gradio OCR 接口调用失败后的重试次数                      | 2                                                           |
| `img_upload_batch_size` | 整数           | 异步批量上传图片的最大并发数                              | 10                                                          |
| `max_convert_pages`     | 整数           | 限制单个文件的最大解析页数（避免超长文件耗时过久）              | 500                                                         |
| `mineru_gradio_url`     | 字符串          | MinerU 的 Gradio OCR 服务的访问地址（核心解析服务）         | `http://Gradio OCR 服务 ip:端口(默认7860)/`                       |
| `backend_server_url`    | 字符串          | MinerU 为 pipeline 解析引擎提供底层支持的后端服务地址        | `http://后端服务 ip:端口(默认30000)`                                |

### 输入参数
| 参数名称       | 参数类型   | 参数说明           | 默认值                                             |
|--------------|----------|-------------------|-------------------------------------------------|
| `file_input` | 输入源     | 需要解析的文件数据源  | 在 MaxKB 应用中开启文件上传后，file_input 为上传文档  |
