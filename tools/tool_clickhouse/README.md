# ClickHouse 数据库查询工具

一个强大的 ClickHouse 列式数据库查询工具，支持对接 ClickHouse 20.x 及以上版本，为 MaxKB 智能体平台提供数据库查询能力。

## 功能特性

- ✅ 支持 ClickHouse 20.x ~ 25.x (推荐 21.8+)
- ✅ 提供完整的数据库查询操作
- ✅ 集成到 MaxKB 智能体平台
- ✅ 简单易用的配置和部署
- ✅ 自动处理日期、Decimal、UUID、IPv4/IPv6 等数据类型
- ✅ 支持 Array、Tuple、Nested 等复杂数据类型
- ✅ 支持连接超时设置
- ✅ 支持结果集行数限制（自动添加 LIMIT）
- ✅ 支持 HTTP/HTTPS 连接
- ✅ 友好的中文错误提示

## 系统要求

- ClickHouse Server 20.x 或更高版本（推荐 21.8+）
- MaxKB 平台环境

## 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install clickhouse-connect>=0.6.0
```

依赖包说明：
- `clickhouse-connect>=0.6.0` - ClickHouse 官方推荐的 Python 驱动程序

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| host | string | 是 | - | 数据库服务器地址 |
| port | string | 是 | 8123 | HTTP 端口号（HTTPS 默认 8443） |
| user | string | 是 | - | 用户名 |
| password | string | 是 | - | 密码 |
| database | string | 是 | - | 数据库名称 |
| query | string | 是 | - | SQL 查询语句 |
| timeout | number | 否 | 30 | 连接超时时间(秒) |
| max_rows | number | 否 | 1000 | 最大返回行数，设为0不限制 |
| use_https | boolean | 否 | False | 是否使用 HTTPS 连接 |

## 使用示例

```python
# 基础查询
result = query_clickhouse(
    host="192.168.1.100",
    port="8123",
    user="default",
    password="your_password",
    database="test_db",
    query="SELECT * FROM system.tables LIMIT 10"
)

# 带超时和行数限制的查询
result = query_clickhouse(
    host="192.168.1.100",
    port="8123",
    user="default",
    password="your_password",
    database="test_db",
    query="SELECT * FROM your_table",
    timeout=60,
    max_rows=500
)

# 使用 HTTPS 连接
result = query_clickhouse(
    host="192.168.1.100",
    port="8443",
    user="default",
    password="your_password",
    database="test_db",
    query="SELECT version()",
    use_https=True
)
```

## 错误处理

工具会返回友好的中文错误提示：

| 错误类型 | 提示信息 |
|----------|----------|
| 连接失败 | 无法连接到数据库服务器 {host}:{port}，请检查地址和端口 |
| 认证失败 | 认证失败，请检查用户名和密码 |
| 数据库不存在 | 数据库 '{database}' 不存在 |
| SQL语法错误 | SQL语法错误: {详细信息} |

## 返回格式

查询结果以 JSON 格式返回：

```json
[
  {"column1": "value1", "column2": "value2"},
  {"column1": "value3", "column2": "value4"}
]
```

## 支持的数据类型

| ClickHouse 类型 | 转换结果 |
|-----------------|----------|
| DateTime/Date | ISO 8601 格式字符串 |
| Decimal | 浮点数 |
| UUID | 字符串 |
| IPv4/IPv6 | 字符串 |
| Array | JSON 数组 |
| Tuple | JSON 数组 |
| Nested | JSON 对象 |
| FixedString/String | 字符串 |

## 注意事项

1. 默认使用 HTTP 协议（端口 8123），如需 HTTPS 请设置 `use_https=True` 并使用端口 8443
2. 检查防火墙是否允许 8123/8443 端口访问
3. 建议使用只读账户进行查询操作
4. 大数据量查询时建议设置 max_rows 参数限制返回行数
5. 如果查询语句没有 LIMIT，工具会自动添加 max_rows 限制
