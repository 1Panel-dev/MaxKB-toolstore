import json
import requests


def tavily_search(query: str, topic: str = "general", search_depth: str = "basic", max_results: int = 5, include_answer: str = "false", include_raw_content: str = "false", tavily_api_key: str = ""):
    try:
        if not query:
            return json.dumps({"success": False, "message": "query 不能为空", "error": "missing_query"}, ensure_ascii=False)
        if not tavily_api_key:
            return json.dumps({"success": False, "message": "tavily_api_key 不能为空", "error": "missing_tavily_api_key"}, ensure_ascii=False)

        def normalize_bool_or_mode(value):
            if isinstance(value, bool):
                return value
            text = str(value).strip().lower()
            if text in ["true", "basic", "advanced", "markdown", "text"]:
                if text == "true":
                    return True
                return text
            return False

        payload = {
            "query": query,
            "topic": topic or "general",
            "search_depth": search_depth or "basic",
            "max_results": max_results
        }

        answer_value = normalize_bool_or_mode(include_answer)
        raw_value = normalize_bool_or_mode(include_raw_content)
        if answer_value is not False:
            payload["include_answer"] = answer_value
        if raw_value is not False:
            payload["include_raw_content"] = raw_value

        rep = requests.post(
            url="https://api.tavily.com/search",
            headers={
                "Content-Type": "application/json"
            },
            json={**payload, "api_key": tavily_api_key},
            timeout=30
        )
        rep.raise_for_status()
        data = rep.json()
        return json.dumps({"success": True, "message": "Tavily 搜索成功", "data": data}, ensure_ascii=False)
    except requests.exceptions.HTTPError as e:
        detail = None
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text if e.response is not None else str(e)
        return json.dumps({
            "success": False,
            "message": "Tavily 搜索失败",
            "error": str(e),
            "status_code": e.response.status_code if e.response is not None else None,
            "details": detail
        }, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return json.dumps({"success": False, "message": "Tavily 搜索请求失败", "error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "message": "处理 Tavily 搜索响应时发生错误", "error": str(e)}, ensure_ascii=False)
