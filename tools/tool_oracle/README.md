# Oracle 数据库查询工具

一个面向 MaxKB 智能体平台的 Oracle 数据库查询工具，支持使用 Service Name 或 SID 连接 Oracle 12.1 及以上版本。

## 功能特性

- 支持 Service Name 和 SID 两种连接方式
- 同时填写时优先使用 Service Name
- 使用 python-oracledb Thin 模式，无需安装 Oracle Client
- 自动处理日期、Decimal、LOB、字节等数据类型
- 支持连接超时设置
- 支持结果集行数限制
- 返回 JSON 格式查询结果和中文错误信息

## 系统要求

- Oracle Database 12.1 或更高版本
- MaxKB 平台环境

## 安装依赖

```bash
pip install oracledb==3.4.2
```

依赖包说明：

- `oracledb==3.4.2` - Oracle 官方 Python 数据库驱动

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| host | string | 是 | - | 数据库服务器地址 |
| port | string | 是 | 1521 | 监听端口 |
| user | string | 是 | - | 用户名 |
| password | string | 是 | - | 密码 |
| service_name | string | 否 | - | Service Name；与 SID 同时填写时优先使用 |
| sid | string | 否 | - | SID；Service Name 为空时使用 |
| query | string | 是 | - | SQL 查询语句 |
| timeout | number | 否 | 30 | 连接超时时间（秒） |
| max_rows | number | 否 | 1000 | 最大返回行数，设为 0 不限制 |

`service_name` 和 `sid` 均不单独必填，但至少需要填写一个。

## 使用示例

### 使用 Service Name

```python
result = query_oracle(
    host="10.1.12.86",
    port="1521",
    user="system",
    password="your_password",
    service_name="ORCLPDB1",
    query="SELECT * FROM v$version"
)
```

### 使用 SID

```python
result = query_oracle(
    host="10.1.12.86",
    port="1521",
    user="system",
    password="your_password",
    sid="ORCLCDB",
    query="SELECT instance_name FROM v$instance"
)
```

## 错误处理

| 错误类型 | 提示信息 |
|----------|----------|
| 连接标识缺失 | Service Name 和 SID 至少填写一个 |
| 认证失败 | 认证失败，请检查用户名和密码 |
| 服务不存在 | 无法连接到指定的 Service Name 或 SID |
| 监听不可用 | 无法连接到数据库服务器，请检查地址、端口和监听状态 |
| SQL 执行失败 | SQL 执行错误及 Oracle 返回的详细信息 |

## 返回格式

查询结果以 JSON 格式返回：

```json
[
  {"COLUMN1": "value1", "COLUMN2": "value2"},
  {"COLUMN1": "value3", "COLUMN2": "value4"}
]
```

## 注意事项

1. 确保 Oracle Listener 已启动，并允许 MaxKB 所在主机访问监听端口。
2. Service Name 与 SID 同时填写时，工具优先使用 Service Name。
3. 建议使用仅具备所需查询权限的数据库账户。
4. 大数据量查询建议保留 `max_rows` 限制。
