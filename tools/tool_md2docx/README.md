# Markdown 转 DOCX 工具

一个用于将 Markdown 转 DOCX 的工具，支持将 AI 生成的 Markdown 格式文本转化成 DOCX ，并提供预览和下载。

## 功能特性

- ✅ 支持将 Markdown 文本转 DOCX
- ✅ 支持预览文档内容
- ✅ 支持下载文档


## 环境准备

### 1.1 Kodbox 安装

在使用此工具之前，需要先安装 Kodbox 。
Kodbox 是一个开源的在线文件管理器，提供了方便的文件浏览、上传、下载和共享功能。它可以让您通过 web 浏览器访问和管理您的文件，无论是个人使用还是团队协作都非常便捷。

推荐使用 1panel 安装 Kodbox ，安装步骤如下：

1. 安装 1panel，参考 1panel 官方文档：https://1panel.cn/docs/v2/installation/online_installation/
2. 在 1panel 控制面板中，点击“应用商店”，搜索“Kodbox”，点击“安装”
3. 安装完成后，在 1panel 控制面板中，点击“应用”，找到“Kodbox”，点击“访问”

### 1.2 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install requests python-docx
```

## 参数说明

### 启动参数    
| 参数名称 | 参数类型 | 参数说明 | 默认值 |
| -------- | -------- | -------- | ------ |
| `server_url` | 字符串     | Kodbox 服务地址 | `http://<Kodbox_URL>`|
| `username`   | 字符串   | Kodbox 用户名 | `<username>` |
| `password`   | 字符串   | Kodbox 密码  | `<password>` |

### 输入参数    
| 参数名称 | 参数类型 | 参数说明 | 默认值 |
| -------- | -------- | -------- | ------ |
| `content` | 字符串     | Markdown 文本| |
| `file_name`   | 字符串   | DOCX 文件名 | |
| `base_image_url` | 字符串   | MaxKB 知识库中图片地址前缀 | `https://<MaxKB_URL>/admin/` |
