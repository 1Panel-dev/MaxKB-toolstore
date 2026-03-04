# 数据写入 EXCEL 工具

支持将数据写入 EXCEL 文件并提供下载链接。

## 1 参数说明

### 1.1 安装依赖
进到 maxkb 容器里，安装 requests 库即可

```linux
pip install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 1.2 启动参数

| 参数名           | 类型 | 说明         |
| ---------------- | ---- | ------------|
| `base_url`       | str  | MaxKB 地址   |
| `api_key`        | str  | 用户的api-key|

### 1.3 输入参数

| 参数名         | 类型 | 说明                      |
| -------------- | ---- | ------------------------- |
| `data_list` | array  | 要写入excel的数据  |
| `headers` | array  | excel的表头  |
| `sheet_name` | str  | sheet页名称  |
| `excel_name` | str  | excel文件名称  |

#### 填写示例：

`headers`: excel的表头，如 ["状态", "记忆","内容","标签","更新时间","响应","错误信息"]

`data_list`: 要写入excel的数据，如
```
[
    {
        "status": "未完成",
        "memory": "test_0001",
        "content": "我是AI智能体",
        "tags": "AI,智能体",
        "update_time": "20260304",
        "response": "AI真牛",
        "error_msg": "无"
    }
]
```

`sheet_name`：sheet 页名称，如"记录状态信息表"

`excel_name`：excel 文件名称，如 "test" 或者 "test.xlsx"

## 2 响应

返回包含下载链接的 HTML 字符串，如

```
<html_rander>
  <a href="..." download="...">文件名.xlsx</a>
</html_rander>
```
