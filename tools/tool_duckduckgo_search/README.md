# DuckDuckGo 搜索工具

基于 `duckduckgo_search` 库实现的搜索工具，支持文字搜索和图片搜索。无需API密钥，开箱即用，可集成到MaxKB知识库系统中。

## 一、功能说明

- **文字搜索**：获取最新的网络信息和数据
- **图片搜索**：搜索并获取图片资源
- **隐私保护**：DuckDuckGo不跟踪用户搜索记录
- **免费使用**：无需API密钥，完全免费

## 二、参数说明

### 2.1 输入参数

| 参数名 | 数据类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `query` | string | 是 | - | 搜索关键词 |
| `max_results` | int | 否 | `10` | 返回的最大结果数量 |
| `search_type` | string | 否 | `text` | 搜索类型：`text`(文字搜索) 或 `image`(图片搜索) |

---

## 三、工具内容（Python）

```python
from ddgs import DDGS
import json


def duckduckgo_search(query, max_results=10, search_type='text'):
    """
    使用 DuckDuckGo 进行搜索（统一入口函数）

    参数:
        query: 搜索关键词
        max_results: 返回的最大结果数量，默认10条
        search_type: 搜索类型，'text'(文字搜索) 或 'image'(图片搜索)，默认'text'

    返回:
        JSON格式的搜索结果列表
    """
    try:
        # 确保 max_results 在合理范围内
        max_results = int(max_results)
        if max_results < 1:
            max_results = 1
        if max_results > 20:
            max_results = 20
        # 创建 DDGS 实例并执行搜索
        with DDGS() as ddgs:
            if search_type == 'image':
                results = list(ddgs.images(
                    keywords=query,
                    max_results=max_results
                ))
            else:
                results = list(ddgs.text(
                    keywords=query,
                    max_results=max_results
                ))

        # 返回 JSON 格式的结果
        return json.dumps(results, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "error": str(e),
            "message": f"{search_type}搜索失败，请检查网络连接或稍后重试"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)
```

---

## 四、使用示例

### 文字搜索

```python
# 基本搜索
result = duckduckgo_search(query='Python编程')

# 指定返回结果数量
result = duckduckgo_search(query='AI新闻', max_results=5)

# 明确指定文字搜索
result = duckduckgo_search(query='Python编程', max_results=10, search_type='text')
```

### 图片搜索

```python
# 基本图片搜索
images = duckduckgo_search(query='风景', search_type='image')

# 指定返回结果数量
images = duckduckgo_search(query='猫', max_results=20, search_type='image')
```

---

## 五、依赖库

| 依赖库 | 版本要求 | 用途说明 |
| :--- | :--- | :--- |
| `ddgs` | ≥ 9.10.0 | DuckDuckGo搜索核心库 |

安装命令：

```bash
pip install ddgs
```

---

## 六、注意事项

- 确保网络连接正常
- 遵守DuckDuckGo使用条款
- 建议合理控制搜索频率，避免被限流
- 搜索结果的准确性需要人工验证
