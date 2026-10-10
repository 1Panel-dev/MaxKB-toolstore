## 1.0.7 版本说明

**注意**：当前适用的 MaxKB 版本为 v2.10.5-lts 及以上版本，MinerU（本地 Gradio 服务）版本为 **v4**。

本版本将工具适配到 **MinerU v4**，工具内显示名为 `MinerU-v4 解析pdf`。v4 与 v3 的 Gradio 接口不兼容，若你的 MinerU 服务仍是 3.x，请继续使用 1.0.6。

## 与 1.0.6（MinerU v3）的主要差异

- **解析接口变更**：v3 调用 `/convert_to_markdown_stream`（10 个参数、输出 6 项），v4 改为调用 `/convert_handler`（4 个参数：`file`、`tier`、`page_range`、`force_ocr`，输出 16 项）。
- **无 zip 输出**：v4 不再返回打包的 zip，工具改为从解析结果的 HTML 中提取 `<img>` 的完整图片 URL 并逐张下载，再上传至 OSS。
- **新增解析档位 `tier`**：v4 通过 `tier`（0~3 档）决定解析引擎、语言与识别能力，本工具默认使用**档位 2**。
- **v3 旧参数在 v4 中已无对应**：`enable_formula`、`language`、`enable_table`、`backend`、`backend_server_url`、`max_convert_pages` 等启动参数在 v4 接口中不再起作用，工具签名予以保留以兼容旧配置，但**运行时会被忽略**（实际能力由 `tier` 决定）。

## 注意事项

- 仅支持**离线部署**的 MinerU v4，且解析服务需以 Gradio 形式暴露（默认 `http://<MinerU 服务 ip>:7860/`）。
- 与 1.0.6 一样，容器内**无需**安装 `gradio_client`（直连 MinerU Gradio 的 HTTP API）。
- 若需切换解析档位（`tier`），请在工具代码中修改 `tier` 的默认值。
