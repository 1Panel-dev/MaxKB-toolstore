# Jina Reader 工具

使用 Jina AI Reader 将 URL 转换为 LLM 友好的 Markdown 格式。

## 功能特点

- URL 转 Markdown
- 智能内容提取
- 自动清理噪音
- 支持中文优化

## 参数说明

**输入参数**: url, return_format
```python
def read_url_with_jina(
    url: str,
    return_format: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """使用 Jina Reader 读取 URL 内容
    
    Args:
        url: 要读取的网页 URL
        api_key: Jina API 密钥 (可选)
        return_format: 返回格式 markdown/html
    
    Returns:
        Dict[str, Any]: 包含读取结果的字典
    """
```
**启动参数**: api_key (可选)

## 使用示例

```
url: https://example.com/article
return_format: markdown
```
