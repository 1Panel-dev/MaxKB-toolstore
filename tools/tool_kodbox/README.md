# Kodbox 文件上传与分享

## 简介

本工具可连接 Kodbox 服务，将本地文件批量上传至指定目录并生成免登录分享链接。用户点击链接即可在线预览 Word、Excel、PPT、PDF 等文档，以及图片、视频等文件，无需下载或安装任何软件，方便快速分发和协作。

## 启动参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | 是 | Kodbox 服务地址 |
| `user` | string | 是 | 登录用户名 |
| `password` | string | 是 | 登录密码 |

## 输入参数（使用工具时显示）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `path_list` | list | 是 | - | 本地文件路径列表，如 ['/tmp/a.txt', '/tmp/myfile/test.docx'] |
| `upload_path` | string | 否 | `{source:7}/` | kodbox远程目标目录，默认 {source:7}/ 为 /个人空间/我的文档 |

## 输出结果

返回 Markdown 格式的分享链接列表：

```
## 在线预览
- 文件名1 [https://xxx/#s/xxx](https://xxx/#s/xxx)
- 文件名2 [https://xxx/#s/xxx](https://xxx/#s/xxx)
```

上传失败的文件会显示对应错误信息。
