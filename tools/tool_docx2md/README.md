# DOCX 转 Markdown 工具

本工具用于实现单个 DOCX 文件转 Markdown 转换，内置 EMF 矢量图转 PNG 图片处理能力。可以将此工具加到工作流知识库中，输出处理后的文件信息。

## 功能特性

- ✅ 支持将 DOCX 文本转 Markdown
- ✅ 支持将 EMF 矢量图转 PNG 图片


## 环境准备

### 1.1 unoserver 安装

在使用此工具之前，需要先安装 unoserver 。
unoserver 是一个文档转换工具‌，这里使用它来转换 EMF 图片。

安装步骤如下：

```bash
docker run -d -p 2003:2003 --name unoserver-service ghcr.io/unoconv/unoserver-docker
```
### 1.2 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
docker exec -it maxkb pip install unoserver==3.4
```

## 参数说明

### 启动参数

| 参数名称 | 参数类型 | 参数说明                | 默认值                        |
| -------- | -------- |---------------------|----------------------------|
| `base_url` | 字符串     | MaxKB 服务地址          | `http://192.XX.XX.17:8080` |
| `APIKey`   | 字符串   | MaxKB 系统用户的 APIKey  | `user-XXXXXXXX` |
| `unoserver_host`   | 字符串   | unoserver 服务的 ip 地址 | `192.XX.XX.17` |

### 输入参数

| 参数名称             | 参数类型 | 参数说明      | 参数示例 |
|------------------|----|-----------|------|
| `source_id`        | 字符串 | 知识库 id    |      |
| `file_info`      | 字典 | 知识库上传文件信息 | 见下表  |

#### 格式参数说明（`file_info` 字段）

`file_info` 参数是一个字典，数据来源于 知识库工作流【文本文件】-【文件列表】的单个文件信息

| 参数名称                   | 类型  | 说明    | 
|------------------------|-----|-------|    
| `1784191412795`             | 数值  | 时间戳   | 
| `name`             | 字符串 | 文件名称  |  
| `size`          | 数值  | 文件大小  | 
| `status`      | 字符串 | 状态    | 
| `file_id`            | 字符串 | 文件 id | 

**完整 `file_info` 参数示例：**

```json
{
  "uid": 1784191412795,
  "name": "测试文档.docx",
  "size": 239520,
  "status": "success",
  "file_id": "019f6a18-6add-7132-bd5a-fbe1509cbe1b"
}
```
### 输出参数

| 参数名称             | 参数类型 | 参数说明             | 
|------------------|------|------------------|
| `content`        | 字符串  | 转换后的 Markdown 文本 |
| `id`      | 字符串  | 源文件 file_id      |
| `name`    | 字符串 | 文件名称             |

**响应示例：**

```json
{
  "content": "#### 技术标文件\n# 一、项目概述\n本项目旨在建设一套高效、稳定的信息化系统，以满足企业日益增长的业务需求。\n项目将采用先进的技术架构，确保系统的可扩展性、安全性和可靠性。\n![image.png](./oss/file/019f6e2d-ed1d-7df2-83b3-4be05980dd15)\n",
  "id": "019f6a18-6add-7132-bd5a-fbe1509cbe1b",
  "name": "测试文档.docx"
}
```
**知识库工作流使用示例**

链接: https://pan.baidu.com/s/1nEzb8f0BtjdRSpUqoC3E0Q?pwd=7mta 提取码: 7mta