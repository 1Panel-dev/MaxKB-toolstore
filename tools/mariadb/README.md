# MariaDB 数据库查询工具

一个强大的 MariaDB 数据库查询工具，支持对接 MariaDB 10.x 及以上版本，为 MaxKB 智能体平台提供数据库查询能力。

## 功能特性

- ✅ 支持 MariaDB 10.x 及以上版本
- ✅ 兼容 MySQL 5.7 及以上版本
- ✅ 提供完整的数据库查询操作
- ✅ 集成到 MaxKB 智能体平台
- ✅ 简单易用的配置和部署
- ✅ 自动处理日期、Decimal、UUID、timedelta 等数据类型
- ✅ 支持 utf8mb4 字符集（完整 Unicode 支持）
- ✅ 支持连接超时设置
- ✅ 支持结果集行数限制
- ✅ 支持 SSL 加密连接
- ✅ 友好的中文错误提示

## 系统要求

- MariaDB 10.x 或更高版本（或 MySQL 5.7+）
- MaxKB 平台环境

## 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install pymysql==1.1.1
```

依赖包说明：
- `pymysql==1.1.1` - MariaDB/MySQL Python 驱动程序

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| host | string | 是 | - | 数据库服务器地址 |
| port | string | 是 | 3306 | 端口号 |
| user | string | 是 | - | 用户名 |
| password | string | 是 | - | 密码 |
| database | string | 是 | - | 数据库名称 |
| query | string | 是 | - | SQL 查询语句 |
| timeout | number | 否 | 30 | 连接超时时间(秒) |
| max_rows | number | 否 | 1000 | 最大返回行数，设为0不限制 |
| use_ssl | boolean | 否 | false | 是否使用 SSL 加密连接 |

## 使用示例

```python
# 基础查询
result = query_mariadb(
    host="192.168.1.100",
    port="3306",
    user="root",
    password="your_password",
    database="test_db",
    query="SELECT * FROM users"
)

# 带超时和行数限制的查询
result = query_mariadb(
    host="192.168.1.100",
    port="3306",
    user="root",
    password="your_password",
    database="test_db",
    query="SELECT * FROM large_table",
    timeout=60,
    max_rows=500
)

# 使用 SSL 加密连接
result = query_mariadb(
    host="192.168.1.100",
    port="3306",
    user="root",
    password="your_password",
    database="test_db",
    query="SELECT * FROM users",
    use_ssl=True
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
| 连接超时 | 连接超时，请检查网络或增加 timeout 参数 |

## 返回格式

查询结果以 JSON 格式返回：

```json
[
  {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
  {"id": 2, "name": "李四", "email": "lisi@example.com"}
]
```

## 注意事项

1. 确保 MariaDB/MySQL 服务已启动并允许远程连接
2. 检查防火墙是否允许 3306 端口访问
3. 建议使用只读账户进行查询操作
4. 大数据量查询时建议设置 max_rows 参数限制返回行数
5. 生产环境建议启用 SSL 加密连接（use_ssl=True）
6. 默认使用 utf8mb4 字符集，支持完整 Unicode 字符（包括 emoji）
