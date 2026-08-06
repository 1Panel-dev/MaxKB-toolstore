## 1.0.0 版本说明

- 支持 DOC->DOCX 文件转换
- 支持 WPS->DOCX 文件转换
- 支持 PPT->PPTX 文件转换

## unoserver 文档类型转换工具

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


### 输出结果:
转换文件后上传至 MaxKB 的成功响应，如：
```
{
  "code": 200,
  "message": "成功",
  "data": "./oss/file/019fd683-f9b6-7e71-b22f-14cd2ab21557"
}
```
