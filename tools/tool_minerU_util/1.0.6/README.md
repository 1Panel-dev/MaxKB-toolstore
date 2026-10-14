## 1.0.6 版本说明

**注意**：当前适用的 MaxKB 版本为 v2.10.5-lts 及以上版本，MinerU（本地 Gradio 服务）版本为 3.4.4。

## 配置参数

需在 `/opt/maxkb/conf/maxkb.env` 中额外添加以下参数（用于关闭文件访问鉴权，使工具能正常下载/读取待解析的文件），修改后重启 maxkb 容器生效：

```bash
MAXKB_FILE_AUTH=0
```

## 注意事项

- 仅支持**离线部署**的 MinerU，且解析服务需以 Gradio 形式暴露（默认 `http://<MinerU 服务 ip>:7860/`）
- 1.0.6 起容器内**无需**再安装 `gradio_client`；若此前按 1.0.5 的文档装过，保留即可、不必卸载
