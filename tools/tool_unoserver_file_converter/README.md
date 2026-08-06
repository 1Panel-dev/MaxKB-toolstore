# unoserver 文档类型转换工具

 本工具借助 Unoserver 达到文件类型转换的功能，并将转换后的文件上传至 MaxKB，返回上传响应信息。
 
## 功能特性

- ✅ 支持 DOC->DOCX 文件转换
- ✅ 支持 WPS->DOCX 文件转换
- ✅ 支持 PPT->PPTX 文件转换


## 环境准备

### 1.1 Unoserver 安装

Unoserver 是基于 LibreOffice UNO 接口的‌客户端 - 服务器架构文档转换服务,支持 LibreOffice 兼容的所有格式（如 docx/odt/xlsx/pptx 等）互转. 

安装步骤如下：

```
docker run -d -p 2003:2003 --name unoserver-service ghcr.io/unoconv/unoserver-docker
```

### 1.2 安装依赖

```
docker exec -it maxkb pip install unoserver==3.4
```

## 参数说明

### 启动参数    
| 参数名称             | 参数类型 | 参数说明                 | 默认值                       |
|------------------|------|----------------------|---------------------------|
| `unoserver_host`        | 字符串  | unoserver 部署服务 ip 地址 |                           |
| `api_base_url`      | 字符串  | MaxKB 服务地址           | `http://xxx.x.xx.xx:8080` |
| `api_auth_token` | 字符串  | MaxKB 用户的 APIKey     | `user-XXXXX`              |

### 输入参数
| 参数名称 | 参数类型 | 参数说明                                                                                                                     | 默认值          |
| -------- |------|--------------------------------------------------------------------------------------------------------------------------|--------------|
| `username`   | 字符串  | MaxKB 用户登录名                                                                                                              | `<username>` |
| `password`   | 字符串  | MaxKB 密码                                                                                                                 | `<password>` |
| `file_info`   | 字典   | MaxKB 文件上传信息                                                                                                             |              |
| `source_type`   | 字符串  | 文件资源上传类型（类型候选[KNOWLEDGE,APPLICATION,TOOL,DOCUMENT,CHAT,SYSTEM,TEMPORARY_30_MINUTE,TEMPORARY_120_MINUTE,TEMPORARY_1_DAY]） |              |
| `source_id`   | 字符串  | 资源 id ,如果 source_type 为[TEMPORARY_30_MINUTE,TEMPORARY_120_MINUTE,TEMPORARY_1_DAY,SYSTEM] 其他的需要为对应资源的id                   | |

**知识库工作流使用示例**
链接: https://pan.baidu.com/s/1_F84cUXaIuI20WaW4l1XMg?pwd=cn5y 提取码: cn5y
