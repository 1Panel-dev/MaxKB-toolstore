# PDF转图片

一个用于将 PDF 转 图片 的工具，支持将PDF文件进行切割并上传至MaxKB OSS中。

## 功能特性

- ✅ 支持将 PDF 文本转 图片
- ✅ 可直接应用于“图片理解”节点
- ✅ 无需外部存储，任务纯本地进行


## 应用示例

![CSDN图标](https://notificationoss.microbaton.com/maxkb/wechat_2025-10-22_203234_890.png)

## 安装依赖
在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install PyMuPDF
pip install requests
```
## 参数说明

### 输入参数    
| 参数名称 | 参数类型 | 参数说明 | 默认值 |
| -------- | -------- | -------- | ------ |
| `images` | 字符串     | 应用中开始变量{{文件}} | `{{开始.document}}`|

### 启动参数    
| 参数名称 | 参数类型 | 参数说明 | 默认值 |
| -------- | -------- | -------- | ------ |
| `api_key`   | 字符串   | API-KEY，请参见MaxKB右上角头像中API KEY | 'user-xxxxxxxxxxxx'|
| `base_url` | 字符串   | MaxKB 地址 | `https://<MaxKB_URL>/PORT` |


## 支持

如有有其他文件处理需求或问题，请联系我们：jiangshiwei@microbaton.com