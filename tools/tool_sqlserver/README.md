# Microsoft SQL Server 数据库查询工具

一个强大的 Microsoft SQL Server 数据库查询工具，支持对接 SQL Server 2012 及以上版本，为 MaxKB 智能体平台提供数据库查询能力。

## 功能特性

- ✅ 支持 SQL Server 2012 及以上版本
- ✅ 提供完整的数据库查询操作
- ✅ 集成到 MaxKB 智能体平台
- ✅ 简单易用的配置和部署
- ✅ 自动处理日期、Decimal、UUID、timedelta 等数据类型
- ✅ 支持无列名查询结果
- ✅ 支持连接超时设置
- ✅ 支持结果集行数限制
- ✅ 友好的中文错误提示

## 系统要求

- Microsoft SQL Server 2012 或更高版本
- MaxKB 平台环境

## 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install pymssql==2.3.2
```

依赖包说明：
- `pymssql==2.3.2` - Microsoft SQL Server Python 驱动程序

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| host | string | 是 | - | 数据库服务器地址 |
| port | string | 是 | 1433 | 端口号 |
| user | string | 是 | - | 用户名 |
| password | string | 是 | - | 密码 |
| database | string | 是 | - | 数据库名称 |
| query | string | 是 | - | SQL 查询语句 |
| timeout | number | 否 | 30 | 连接超时时间(秒) |
| max_rows | number | 否 | 1000 | 最大返回行数，设为0不限制 |

## 使用示例

```python
# 基础查询
result = query_sqlserver(
    host="10.1.12.86",
    port="1433",
    user="sa",
    password="your_password",
    database="master",
    query="SELECT * FROM sys.tables"
)

# 带超时和行数限制的查询
result = query_sqlserver(
    host="10.1.12.86",
    port="1433",
    user="sa",
    password="your_password",
    database="master",
    query="SELECT * FROM sys.objects",
    timeout=60,
    max_rows=500
)
```

## 错误处理

工具会返回友好的中文错误提示：

| 错误类型 | 提示信息 |
|----------|----------|
| 连接失败 | 无法连接到数据库服务器 {host}:{port}，请检查地址和端口 |
| 认证失败 | 认证失败，请检查用户名和密码 |
| 数据库不存在 | 数据库 '{database}' 不存在或无权访问 |
| SQL语法错误 | SQL语法错误: {详细信息} |
| 连接超时 | 连接超时，请检查网络或增加 timeout 参数 |

## 返回格式

查询结果以 JSON 格式返回：

```json
[
  {"column1": "value1", "column2": "value2"},
  {"column1": "value3", "column2": "value4"}
]
```

## 注意事项

1. 确保 SQL Server 已启用 TCP/IP 协议
2. 检查防火墙是否允许 1433 端口访问
3. 建议使用只读账户进行查询操作
4. 大数据量查询时建议设置 max_rows 参数限制返回行数
