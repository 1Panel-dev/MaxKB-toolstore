# Elasticsearch 数据库查询工具

一个强大的 Elasticsearch 8.x 只读查询工具，支持执行各种 ES 查询操作，为 MaxKB 智能体平台提供 Elasticsearch 查询能力。

## 功能特性

- ✅ 支持 Elasticsearch 8.x 版本
- ✅ 支持文档搜索、聚合分析、集群信息查询
- ✅ 集成到 MaxKB 智能体平台
- ✅ 简单易用的配置和部署
- ✅ 支持灵活的查询 DSL
- ✅ 支持多索引搜索和批量文档获取
- ✅ 安全的白名单验证机制
- ✅ 支持 HTTPS 连接和 SSL 证书验证
- ✅ 友好的中文错误提示

## 系统要求

- Elasticsearch 8.x 集群
- MaxKB 平台环境
- Python 3.7+

## 安装依赖

在使用此工具之前，需要先安装所需的依赖包：

```bash
pip install elasticsearch>=8.0.0,<9.0.0
```

依赖包说明：
- `elasticsearch>=8.0.0,<9.0.0` - Elasticsearch Python 客户端（8.x 版本）

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| host | string | 是 | - | Elasticsearch 服务器地址 |
| port | string | 是 | 9200 | Elasticsearch 端口 |
| user | string | 是 | - | 认证用户名 |
| password | string | 是 | - | 认证密码 |
| use_ssl | boolean | 否 | true | 是否使用 HTTPS 连接 |
| verify_certs | boolean | 否 | true | 是否验证 SSL 证书 |
| api_path | string | 是 | - | ES API 路径（如: index_name/_search） |
| query_dsl | string | 否 | - | 查询 DSL JSON 字符串（可选） |
| timeout | number | 否 | 30 | 连接超时时间(秒) |

## 支持的 API

### 搜索类 API
- `_search` - 搜索文档
- `_mget` - 批量获取多个文档
- `_count` - 统计文档数量
- `_validate/query` - 验证查询语法

### 信息类 API
- `_get` 或 `_doc/{id}` - 获取单个文档
- `_cat/*` - 集群信息查询（indices, aliases, health, nodes 等）
- `_cluster/health` - 集群健康状态
- `_cluster/state` - 集群状态
- `_aliases` - 索引别名信息
- `_mapping` - 索引映射信息
- `_settings` - 索引设置

## 使用示例

### 基础搜索

```python
# 搜索所有文档
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="my_index/_search",
    query_dsl='{"query": {"match_all": {}}}'
)

# 条件搜索
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="my_index/_search",
    query_dsl='{"query": {"match": {"title": "搜索关键词"}}}'
)
```

### 获取单个文档

```python
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="my_index/_doc/123"
)
```

### 批量获取多个文档

```python
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="_mget",
    query_dsl='{"docs": [{"_index": "my_index", "_id": "1"}, {"_index": "my_index", "_id": "2"}]}'
)
```

### 多索引搜索

```python
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="index1,index2/_search",
    query_dsl='{"query": {"match_all": {}}}'
)
```

### 聚合查询

```python
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="my_index/_search",
    query_dsl='{"size": 0, "aggs": {"avg_price": {"avg": {"field": "price"}}}}'
)
```

### 集群信息查询

```python
# 集群健康状态
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="_cluster/health"
)

# 索引列表
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="_cat/indices"
)

# 索引映射
result = query_elasticsearch(
    host="localhost",
    port="9200",
    user="elastic",
    password="changeme",
    api_path="my_index/_mapping"
)
```

## 错误处理

工具会返回友好的中文错误提示：

| 错误类型 | 提示信息 |
|----------|----------|
| 连接失败 | 无法连接到 Elasticsearch 服务器 {host}:{port}，请检查地址和端口 |
| 认证失败 | 认证失败，请检查用户名和密码 |
| SSL 错误 | SSL 证书验证失败，请检查证书或设置 verify_certs=False |
| 权限不足 | 权限不足，请检查用户是否有相应的查询权限 |
| 索引不存在 | 索引 {index_name} 不存在 |
| 查询语法错误 | 查询语法错误: {详细信息} |
| 超时 | 连接超时，请检查网络或增加 timeout 参数 |
| 不支持的 API | 不允许的 API 路径: {api_path}。此工具只支持只读查询操作 |
| 不支持的 HTTP 方法 | 不支持的 HTTP 方法: {method}。只允许 GET 和 HEAD 请求 |

## 安全验证

工具实现了双重安全验证机制：

1. **白名单路径验证**: 只允许预定义的只读 API 路径
2. **HTTP 方法验证**: 只允许 GET 和 HEAD 请求

这确保了工具只能执行只读查询操作，防止误操作导致数据修改或删除。

## 注意事项

1. 生产环境建议使用专用只读账户
2. 建议在 ES 集群配置中启用安全认证和 HTTPS
3. 不要在日志中记录敏感信息（如密码）
4. 检查防火墙是否允许 ES 端口访问
5. 大数据量查询时建议在 query_dsl 中添加分页参数（from, size）
6. 避免使用高开销的查询（如通配符查询、正则查询）在大数据集上
7. 建议设置合理的 timeout 参数，避免长时间等待

## 测试说明

### 本地测试

在提交工具前，建议进行以下测试：

1. **参数验证测试**
```python
from elasticsearch_query import query_elasticsearch

# 测试缺少必填参数
result = query_elasticsearch(host="", port="9200", user="elastic", password="changeme", api_path="test/_search")
print(result)  # 应返回参数错误

# 测试无效的 API 路径
result = query_elasticsearch(host="localhost", port="9200", user="elastic", password="changeme", api_path="test/_delete")
print(result)  # 应返回不允许的 API 路径错误
```

2. **连接测试**
```python
# 测试基础搜索（需要实际 ES 环境）
result = query_elasticsearch(
 host="localhost",
 port="9200",
 user="elastic",
 password="changeme",
 api_path="_cat/indices"
)
print(result)  # 应返回索引列表或认证失败错误
```

3. **查询 DSL 测试**
```python
# 测试无效的 JSON
result = query_elasticsearch(
 host="localhost",
 port="9200",
 user="elastic",
 password="changeme",
 api_path="test_index/_search",
 query_dsl="{invalid json}"
)
print(result)  # 应返回 JSON 解析错误
```

### 集成测试

在 MaxKB 平台中测试：

1. 上传工具到平台
2. 配置连接参数
3. 测试各种 API 路径：
 - `_cat/indices` - 获取索引列表
 - `index_name/_search` - 搜索文档
 - `_cluster/health` - 集群健康状态
4. 验证错误处理是否返回友好的中文提示
