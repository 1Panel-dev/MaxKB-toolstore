## 1.0.7 版本说明

**注意**：当前适用的 MaxKB 版本为 v2.10.5-lts 及以上版本，MinerU（本地 Gradio 服务）版本为 4.0.10。


## 配置参数

需在 `/opt/maxkb/conf/maxkb.env` 中额外添加以下参数（用于关闭文件访问鉴权，使工具能正常下载/读取待解析的文件），修改后重启 maxkb 容器生效：

```bash
MAXKB_FILE_AUTH=0
```

## 启动参数说明

| 参数名称                  | 参数类型 | 参数说明                                              | 默认值                                                   |
|-----------------------|----------|-------------------------------------------------------|--------------------------------------------------------|
| `mineru_gradio_url`   | 字符串     | 离线 MinerU（Gradio）解析服务的访问地址：ip:web 端口号   | `http://<MinerU 服务 ip>:7860/`                        |
| `download_dir`        | 字符串     | 存储下载原始文件与解析临时文件的目录                     | `/tmp`                                                  |
| `upload_url`          | 字符串     | 解析出的图片上传到的接口地址（一般上传到 MaxKB 以便引用） | `http://<MaxKB 服务器 ip>:8080/admin/api/oss/file`      |
| `upload_token`        | 字符串     | MaxKB 的 API Key（替换为实际值）                        | API Key                                                 |
| `url_prefix`          | 字符串     | 拼接 `file_input` 相对路径、生成完整文件 URL 的前缀       | `http://<MaxKB 服务器 ip>:8080/admin`                   |
| `enable_ocr`          | 开关       | 是否启用 OCR（启用则解析文件中的图片文字）               | True                                                    |
| `tier`                | 整数       | v4 解析档位（0~3），数字越大越精细                       | 2                                                       |
| `gradio_retry_count`  | 整数       | Gradio 接口调用失败后的重试次数                          | 2                                                       |
| `img_upload_batch_size` | 整数     | 图片批量上传的并发大小                                   | 10                                                      |

> 输入参数：`file_input`（数组，格式 `["文件url", ...]`），即需要解析的文件数据源。

