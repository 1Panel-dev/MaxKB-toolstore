# JSON 路径处理工具
一个基于 `jsonpath_ng` 的安全、高效的 JSON 数据路径查询与操作工具库。它封装了标准的 jsonpath 语法，提供数据查询、更新、删除等核心操作，并内置缓存机制以提升性能。

## 一、项目介绍

### 1.1 核心功能
- **精准查询**: 使用标准的 jsonpath 表达式从复杂的嵌套 JSON 结构中提取数据。
- **数据更新**: 定位并修改 JSON 数据中指定路径节点的值。
- **节点删除**: 安全地删除 JSON 数据中符合路径表达式的节点。
- **健壮性保障**: 全面的输入验证和异常捕获，所有错误以字符串形式返回，避免程序崩溃。
- **性能优化**: 内置路径表达式编译缓存，对重复查询场景性能提升显著。

### 1.2 适用场景
- 从 API 响应或配置文件中提取特定字段。
- 批量修改或清理 JSON 数据结构（如日志、数据记录）。
- 在数据处理流水线中，作为 JSON 内容转换的中间件。
- 开发需要动态解析和操作 JSON 的脚本或工具。

## 二、环境准备

### 2.1 依赖库
- **Python**: 3.7 或更高版本。
- **jsonpath_ng**: >= 1.5.0 (核心依赖，提供 JSONPath 解析能力)。
- **json**: Python 标准库，无需单独安装。

### 2.2 安装依赖
使用 pip 安装必需的第三方库：
```bash
pip install jsonpath_ng>=1.5.0
```

## 三、使用说明

### 3.1 函数定义
核心函数为 `execute_jsonpath_operation`，位于 `jsonpath_util.py` 文件中。
```python
from jsonpath_util import execute_jsonpath_operation
```

### 3.2 参数说明

| 参数名 | 类型 | 必需 | 默认值 | 描述 | 有效值/范围 | 示例 |
|--------|------|------|--------|------|------------|------|
| `json_content` | `str` | 是 | 无 | 待处理的 JSON 数据字符串。必须是有效的 JSON 格式。 | 任意有效的 JSON 字符串 | `‘{“name”: “Test”}’` |
| `path_expression` | `str` | 是 | 无 | 用于定位数据的 jsonpath 表达式。 | 标准 JSONPath 语法 | ``$.store.book[*].title`` |
| `operation_type` | `str` | 否 | `”query”` | 指定要执行的操作类型。 | `”query”`, `”update”`, `”delete”` | `”update”` |
| `new_value` | `Any` | 否 | `None` | 当 `operation_type=”update”` 时，用于替换匹配节点的新值。 | 任何 Python 可 JSON 序列化的数据类型 | `30`, `”new”`, `[1,2]` |

**参数关系说明**:
- `new_value` 仅在 `operation_type=”update”` 时为有效参数，否则会被忽略。
- `path_expression` 支持标准 JSONPath 语法，包括根节点 (`$`)、子节点 (`.`/`[]`)、递归下降 (`..`)、通配符 (`*`)、数组索引/切片 (`[n]`, `[start:end]`)、过滤表达式 (`?(expression)`)。

### 3.3 代码示例

#### 示例 1：基础查询操作
**场景**：从一个在线书店的库存 JSON 中提取所有书籍的标题。

```python
import json
from jsonpath_util import execute_jsonpath_operation

# 原始 JSON 数据字符串
json_str = """
{
  "store": {
    "book": [
      {"category": "reference", "author": "Nigel Rees", "title": "Sayings of the Century", "price": 8.95},
      {"category": "fiction", "author": "J. R. R. Tolkien", "title": "The Lord of the Rings", "price": 22.99},
      {"category": "fiction", "author": "Herman Melville", "title": "Moby Dick", "isbn": "0-553-21311-3", "price": 8.99}
    ],
    "bicycle": {"color": "red", "price": 19.95}
  }
}
"""

# 1. 使用 jsonpath 表达式查找所有书籍标题
result = execute_jsonpath_operation(json_str, "$.store.book[*].title", "query")

# 2. 打印结果
print("所有书籍标题：")
for title in result:
    print(f"- {title}")

# 预期输出:
# 所有书籍标题：
# - Sayings of the Century
# - The Lord of the Rings
# - Moby Dick
```

#### 示例 2：更新操作
**场景**：更新用户配置文件中特定字段的值。

```python
from jsonpath_util import execute_jsonpath_operation

# 用户配置 JSON
user_config = '{"username": "zhangsan", "settings": {"theme": "light", "notifications": true, "language": "zh-CN"}}'

# 将主题从 “light” 更新为 “dark”
updated_config = execute_jsonpath_operation(
    json_content=user_config,
    path_expression="$.settings.theme",  # 定位到 theme 字段
    operation_type="update",
    new_value="dark"  # 新的值
)

print("更新后的配置：")
print(json.dumps(updated_config, indent=2, ensure_ascii=False))  # 美化输出

# 预期输出（格式化后）:
# {
#   “username”: “zhangsan”，
#   “settings”: {
#     “theme”: “dark”，
#     “notifications”: true,
#     “language”: “zh-CN”
#   }
# }
```

#### 示例 3：删除操作
**场景**：从数据记录中移除敏感信息（如身份证号）。

```python
from jsonpath_util import execute_jsonpath_operation

# 包含敏感信息的记录
data_record = ‘{“id”: 101， “name”: “李四”， “id_card”: “110101199001011234”， “department”: “技术部”}’

# 删除 id_card 字段
cleaned_record = execute_jsonpath_operation(
    json_content=data_record,
    path_expression="$.id_card",  # 定位到要删除的字段
    operation_type="delete"
)

print(“脱敏后的记录：”)
print(json.dumps(cleaned_record， indent=2， ensure_ascii=False))

# 预期输出:
# {
#   “id”: 101，
#   “name”: “李四”，
#   “department”: “技术部”
# }
```
