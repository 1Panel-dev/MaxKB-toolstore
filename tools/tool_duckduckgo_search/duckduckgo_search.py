from ddgs import DDGS
import json


def duckduckgo_search(query, max_results=10, search_type="text", region="cn-zh"):
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
        ddgs = DDGS()
        if search_type == "image":
            results = list(
                ddgs.images(
                    query=query,
                    max_results=max_results,
                    region=region,
                    safesearch="off",
                )
            )
        else:
            results = list(
                ddgs.text(
                    query=query,
                    max_results=max_results,
                    region=region,
                    safesearch="off",
                )
            )

        # 返回 JSON 格式的结果
        return json.dumps(results, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "error": str(e),
            "message": f"{search_type}搜索失败，请检查网络连接或稍后重试",
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)
