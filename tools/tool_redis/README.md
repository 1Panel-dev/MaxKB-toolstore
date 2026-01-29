# Redis 数据库查询工具

一个强大的 Redis 数据库查询工具，支持执行各种 Redis 命令，为 MaxKB 智能体平台提供 Redis 查询能力。

## 功能特性

- ✅ 支持 Redis 2.6 及以上版本
- ✅ 支持所有 Redis 命令（GET、SET、HGETALL、KEYS 等）
- ✅ 集成到 MaxKB 智能体平台
- ✅ 简单易用的配置和部署
- ✅ 自动处理字节、列表、集合、哈希等数据类型
- ✅ 支持带引号的参数解析
- ✅ 支持连接超时设置
- ✅ 支持结果数量限制
- ✅ 友好的中文错误提示

## 系统要求

- Redis 2.6 或更高版本
- MaxKB 平台环境

## 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install redis==5.0.1
```

依赖包说明：
- `redis==5.0.1` - Redis Python 客户端

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| host | string | 是 | - | Redis 服务器地址 |
| port | string | 是 | 6379 | 端口号 |
| password | string | 否 | - | 密码，无密码时留空 |
| db | string | 是 | 0 | 数据库索引（0-15） |
| command | string | 是 | - | Redis 命令 |
| timeout | number | 否 | 30 | 连接超时时间(秒) |
| max_results | number | 否 | 1000 | 最大返回结果数，设为0不限制 |

## 使用示例

```python
# 获取单个键值
result = query_redis(
    host="127.0.0.1",
    port="6379",
    password="",
    db="0",
    command="GET mykey"
)

# 查找所有键
result = query_redis(
    host="127.0.0.1",
    port="6379",
    password="your_password",
    db="0",
    command="KEYS *"
)

# 获取哈希表所有字段
result = query_redis(
    host="127.0.0.1",
    port="6379",
    password="your_password",
    db="0",
    command="HGETALL user:1001"
)

# 获取列表元素
result = query_redis(
    host="127.0.0.1",
    port="6379",
    password="",
    db="0",
    command="LRANGE mylist 0 -1"
)

# 带引号参数
result = query_redis(
    host="127.0.0.1",
    port="6379",
    password="",
    db="0",
    command='SET mykey "hello world"'
)
```

## 常用命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| GET | 获取字符串值 | GET key |
| SET | 设置字符串值 | SET key value |
| KEYS | 查找键 | KEYS pattern |
| HGET | 获取哈希字段 | HGET hash field |
| HGETALL | 获取哈希所有字段 | HGETALL hash |
| LRANGE | 获取列表范围 | LRANGE list 0 -1 |
| SMEMBERS | 获取集合所有成员 | SMEMBERS set |
| ZRANGE | 获取有序集合范围 | ZRANGE zset 0 -1 |
| TTL | 获取键过期时间 | TTL key |
| TYPE | 获取键类型 | TYPE key |
| INFO | 获取服务器信息 | INFO |
| DBSIZE | 获取键数量 | DBSIZE |

## 错误处理

工具会返回友好的中文错误提示：

| 错误类型 | 提示信息 |
|----------|----------|
| 连接失败 | 无法连接到 Redis 服务器 {host}:{port}，请检查地址和端口 |
| 认证失败 | 认证失败，请检查密码 |
| 命令错误 | 命令执行错误: {详细信息} |
| 连接超时 | 连接超时，请检查网络或增加 timeout 参数 |

## 返回格式

查询结果以 JSON 格式返回：

```json
{
  "command": "GET mykey",
  "result": "myvalue",
  "type": "bytes"
}
```

列表/集合结果：
```json
{
  "command": "KEYS *",
  "result": ["key1", "key2", "key3"],
  "type": "list"
}
```

哈希结果：
```json
{
  "command": "HGETALL user:1001",
  "result": {
    "name": "张三",
    "age": "25"
  },
  "type": "dict"
}
```

## 注意事项

1. 生产环境建议配置 Redis 密码认证
2. 检查防火墙是否允许 6379 端口访问
3. 建议使用只读账户进行查询操作
4. 大数据量查询时建议设置 max_results 参数限制返回数量
5. KEYS 命令在大数据量时可能影响性能，建议使用 SCAN 替代
