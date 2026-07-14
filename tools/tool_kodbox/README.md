# Kodbox 文件上传与分享

## 简介

连接 Kodbox 网盘，批量上传文件并生成分享链接。

## 启动参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | 是 | Kodbox 服务地址 |
| `user` | string | 是 | 登录用户名 |
| `password` | string | 是 | 登录密码 |

## 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `path_list` | list | 是 | - | 本地文件路径列表 |
| `upload_path` | string | 否 | `/` | 远程目标目录 |

## 输出结果

返回 Markdown 格式的分享链接列表：

```
## 在线预览
- 文件名1 [https://xxx/#s/xxx](https://xxx/#s/xxx)
- 文件名2 [https://xxx/#s/xxx](https://xxx/#s/xxx)
```

上传失败的文件会显示对应错误信息。
