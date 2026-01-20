# HTML 转 PDF 转换工具

基于 PDF API 服务封装的 Python 工具函数，支持将 HTML 内容转换为 PDF 文件。

## 一、项目介绍

### 1.1 核心功能

- **HTML 到 PDF 转换**：支持 HTML 字符串或 HTML 文件路径作为输入，转换为高质量的 PDF 文档。
- **文件上传集成**：转换完成后可自动上传到指定服务器，支持自定义请求头。
- **临时文件管理**：自动生成唯一命名的临时文件，并在处理完成后清理，避免磁盘空间占用。
- **错误处理机制**：完善的异常捕获和错误信息提示，便于问题排查。

### 1.2 适用场景

- **报告生成**：将数据分析结果或报告从 HTML 格式转换为可打印的 PDF 文档。
- **文档归档**：将网页内容或动态生成的 HTML 内容保存为 PDF 进行长期存储。
- **内容分发**：在 Web 应用中提供 PDF 下载功能，增强用户体验。
- **自动化流程**：集成到自动化工作流中，批量处理 HTML 到 PDF 的转换任务。

## 二、环境准备

### 2.1 依赖库

该工具基于 Python 标准库和常用第三方库构建。

| 依赖库     | 版本要求      | 用途说明               |
| :--------- | :------------ | :--------------------- |
| `requests` | ≥ 2.20.0      | 发送 HTTP 请求         |
| `os`       | Python 标准库 | 文件路径操作和系统接口 |
| `uuid`     | Python 标准库 | 生成唯一标识符         |
| `datetime` | Python 标准库 | 时间戳生成             |

### 2.2 安装依赖

通过 `pip` 安装 `requests` 库：

```bash
pip install requests
```

------

## 三、使用说明

### 3.1 部署html-to-pdf服务

镜像下载地址：
链接：https://pan.quark.cn/s/3bba18351775?pwd=S4TF
提取码：S4TF

```linux
# 解压文件
unzip htmltopdf.zip

# 加载镜像
docker load -i html-to-pdf.tar

# 启动
docker run -d -p 6000:6000 --name convertpdf  html-to-pdf
```

### 3.2 参数说明

#### 启动参数

| 参数名           | 类型 | 说明         |
| ---------------- | ---- | ------------ |
| `upload_url`     | str  | 文件上传地址 |
| `upload_headers` | str  | 上传请求头   |
| `api_url`        | str  | API 端点     |

##### 填写要求：

`upload_url`:填写当前使用的 MaxKB 地址。

`upload_headers`：填写 MaxKB 的 API Key。

`api_url`：参照 3.1 使用自己部署的 html-to-pdf 服务

#### 输入参数

| 参数名         | 类型 | 说明                      |
| -------------- | ---- | ------------------------- |
| `html_content` | str  | HTML 字符串内容或文件路径 |
| `filename`     | str  | 输出文件名                |

## 四、注意事项

- **文件清理**：无论转换成功与否，都会自动清理临时生成的 PDF 文件
- **上传认证**：上传功能需要有效的 Bearer Token，请确保 `upload_headers`参数正确
- **字符编码**：处理 HTML 文件时使用 UTF-8 编码，确保中文等特殊字符正确显示
