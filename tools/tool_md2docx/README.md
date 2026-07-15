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
pip install requests python-docx Pillow
```

### 配置参数
MaxKB v2.4 及以上版本，需修改配置文件 `/opt/maxkb/maxkb.env` 

```bash
MAXKB_SANDBOX_TMP_DIR_ENABLED=1
MAXKB_SANDBOX_PYTHON_ALLOW_SUBPROCESS=1
```

## 参数说明

### 启动参数    
| 参数名称 | 参数类型 | 参数说明 | 默认值 |
| -------- | -------- | -------- | ------ |
| `server_url` | 字符串     | Kodbox 服务地址 | `http://<Kodbox_URL>`|
| `username`   | 字符串   | Kodbox 用户名 | `<username>` DOCX
| `password`   | 字符串   | Kodbox 密码  | `<password>` |

### 输入参数    
| 参数名称             | 参数类型 | 参数说明                                 | 默认值                                                                                                                                                                                                                                                                                                                          |
|------------------|------|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `content`        | 字符串  | Markdown 文本                          |                                                                                                                                                                                                                                                                                                                              |
| `file_name`      | 字符串  | DOCX 文件名                             |                                                                                                                                                                                                                                                                                                                              |
| `base_image_url` | 字符串  | MaxKB 知识库中图片地址前缀                     | `https://<MaxKB_URL>/admin/`                                                                                                                                                                                                                                                                                                 |
| `format`         | 字典   | 文档格式配置（详见下方格式参数说明） | 见下表 |

#### 格式参数说明（`format` 字段）

`format` 参数是一个字典，用于精细控制生成 DOCX 文档的排版样式。各字段说明如下：

| 参数名称                   | 类型 | 说明 | 可选值/示例                                         | 默认值      |
|------------------------| --- | ---- |------------------------------------------------|----------|
| **正文样式**               | | |                                                |          |
| `fontName`             | 字符串 | 正文字体 | 如：宋体、仿宋                                        | `宋体`     |
| `fontSize`             | 字符串 | 正文字号 | 数字，单位为磅（pt），如：`12` 对应小四                        | `12`     |
| `lineSpacing`          | 字符串 | 正文行距 | 倍数，如：`1.0`、`1.5`                               | `1.5`    |
| `firstLineIndent`      | 字符串 | 正文首行缩进 | 字符数，如：`2` 表示缩进 2 个字符                           | `2`      |
| `alignment`            | 字符串 | 正文对齐方式 | `left`（左对齐）、`center`（居中）、`right`（右对齐）、`justify`（两端对齐） | `left`   |
| **表格样式**               | | |                                                |          |
| `tableFontName`        | 字符串 | 表格字体 | 同正文字体                                          | `宋体`     |
| `tableFontSize`        | 字符串 | 表格字体大小 | 数字，单位为磅（pt）                                    | `12`     |
| `tableFirstLineIndent` | 字符串 | 表格内文字首行缩进 | 字符数                                            | `0`      |
| `tableAlignment`       | 字符串 | 表格对齐方式 | `left`、`center`、`right`、`justify`              | `center` |
| `tableLineSpacing`     | 字符串 | 表格行距 | 倍数                                             | `1.0`    |
| **页面设置**               | | |                                                |          |
| `topSection`           | 字符串 | 上页边距 | 数字，单位为厘米（cm），如：`2.5`                           | `2`      |
| `bottomSection`        | 字符串 | 下页边距 | 数字，单位为厘米（cm）                                   | `2`      |
| `leftSection`          | 字符串 | 左页边距 | 数字，单位为厘米（cm）                                   | `2`      |
| `rightSection`         | 字符串 | 右页边距 | 数字，单位为厘米（cm）                                   | `2`      |
| **图片样式**               | | |                                                |          |
| `imageLineSpacing`     | 字符串 | 图片行距 | 倍数                                             | `1.0`    |

**完整 `format` 参数示例：**

```json
{
  "fontName": "宋体",
  "fontSize": "12",
  "lineSpacing": "1.5",
  "firstLineIndent": "2",
  "alignment": "left",
  "tableFontName": "宋体",
  "tableFontSize": "12",
  "tableFirstLineIndent": "2",
  "tableAlignment": "center",
  "tableLineSpacing": "1.0",
  "topSection": "2.5",
  "bottomSection": "2",
  "leftSection": "2",
  "rightSection": "2",
  "imageLineSpacing": "1.0"
}
```
**智能体工作流使用示例**

<img src="https://kaibo-1251506367.cos.ap-beijing.myqcloud.com/maxkb/appstoreImages/tool_md2docx_format.png">