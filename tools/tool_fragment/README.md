# 代码片段提取工具

## 简介
代码片段提取工具是一个专门用于从 Markdown 格式文本中提取特定语言代码块的 Python 函数。

## 功能特性
- **精准提取**：使用正则表达式精准匹配 Markdown 代码块
- **格式保持**：完整保留代码块内部的格式和缩进
- **多语言支持**：支持提取任意编程语言的代码片段
- **简单易用**：清晰的 API 接口，一行代码即可完成提取

## 核心函数

```python
def main(input_str: str, split_str: str) -> str | None:
    """
    从 Markdown 文本中提取指定语言的代码块内容
    
    Args:
        input_str: 输入的 Markdown 格式文本
        split_str: 要提取的代码块语言标识
        
    Returns:
        成功时返回提取的代码内容，未找到匹配时返回 None
    """
    pattern = r'```'+split_str+'\s*\n(.*?)\n\s*```'
    match = re.search(pattern, input_str, re.DOTALL)
    if match:
        content = match.group(1).strip('\n')
        return content
    return None

```

# 使用示例
示例 1：提取 json 数据

提取前：
```json
{
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "server": {
        "port": 8080,
        "debug": true
    },
    "features": ["auth", "upload", "api"]
}
```

提取后：
去掉了 ```json ```  的标识，方便后续接口传参

{
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "server": {
        "port": 8080,
        "debug": true
    },
    "features": ["auth", "upload", "api"]
}

示例 2：提取 sql 语句

提取前:

```sql    
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(o.id) as order_count
FROM 
    users u
LEFT JOIN 
    orders o ON u.id = o.user_id
WHERE 
    u.created_at >= '2024-01-01'
    AND u.status = 'active'
GROUP BY 
    u.id, u.username, u.email
HAVING 
    COUNT(o.id) > 5
ORDER BY 
    order_count DESC
LIMIT 10;
```

提取后：

去掉了 ```sql ```  的标识，后面直接对接sql函数查询即可。

SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(o.id) as order_count
FROM 
    users u
LEFT JOIN 
    orders o ON u.id = o.user_id
WHERE 
    u.created_at >= '2024-01-01'
    AND u.status = 'active'
GROUP BY 
    u.id, u.username, u.email
HAVING 
    COUNT(o.id) > 5
ORDER BY 
    order_count DESC
LIMIT 10;



