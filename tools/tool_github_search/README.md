# GitHub API 查询工具

查询 GitHub 仓库信息、Issues、Pull Requests、Releases 和贡献者数据。

## 功能特点

- 仓库基本信息查询
- Issues/PRs 查询
- Releases 查询
- 贡献者查询
- 支持 Token 认证

## 参数说明

**输入参数**: owner, repo, query_type, state, per_page
```python
def query_github_repository(
    owner: str,
    repo: str,
    query_type: str,
    state: str,
    token: Optional[str] = None,
    per_page: int = 10,
    page: int = 1
) -> Dict[str, Any]:
    """查询 GitHub 仓库信息
    
    Args:
        owner: 仓库所有者（用户名或组织名）
        repo: 仓库名称
        token: GitHub Personal Access Token（可选，用于提高速率限制）
        query_type: 查询类型，可选 "info"/"issues"/"pulls"/"releases"/"contributors"
        state: 状态过滤，可选 "open"/"closed"/"all"，默认 "open"
        per_page: 每页结果数，默认 10
        page: 页码，默认 1
    
    Returns:
        Dict[str, Any]: 包含查询结果的字典，结构如下：
            - success (bool): 是否成功
            - data (Dict|None): 查询数据，包含：
                - type (str): 查询类型
                - repository (str): 仓库全名
                - info (Dict|None): 仓库基本信息
                - items (List|None): 结果列表（issues/prs/releases 等）
                - total_count (int): 总数
            - message (str): 结果消息
    
    Raises:
        无异常抛出，所有错误在返回值中处理
    
    Examples:
        >>> result = query_github_repository("1Panel-dev", "MaxKB", query_type="info")
        >>> if result["success"]:
        ...     print(f"Stars: {result['data']['info']['stargazers_count']}")
    """
```
**启动参数**: token (可选)

## 使用说明

无需 Token 即可查询公开仓库，提供 Token 可提高速率限制。
