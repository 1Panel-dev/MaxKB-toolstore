import json
import requests


def search_memory(query: str, user_id: str = "", agent_id: str = "", top_k: int = 5, api_key: str = "", base_url: str = "https://api.mem0.ai"):
    try:
        if not query:
            return json.dumps({"success": False, "message": "query 不能为空", "error": "missing_query"}, ensure_ascii=False)
        if not api_key:
            return json.dumps({"success": False, "message": "api_key 不能为空", "error": "missing_api_key"}, ensure_ascii=False)

        payload = {
            "query": query,
            "version": "v2",
            "top_k": top_k
        }

        filters = []
        if user_id:
            filters.append({"user_id": user_id})
        if agent_id:
            filters.append({"agent_id": agent_id})

        if len(filters) == 1:
            payload["filters"] = filters[0]
        elif len(filters) > 1:
            payload["filters"] = {"OR": filters}

        rep = requests.post(
            url=f"{base_url.rstrip('/')}/v2/memories/search/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {api_key}",
                "Accept": "application/json"
            },
            json=payload,
            timeout=30
        )
        rep.raise_for_status()
        data = rep.json()
        return json.dumps({"success": True, "message": "记忆检索成功", "data": data}, ensure_ascii=False)
    except requests.exceptions.HTTPError as e:
        detail = None
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text if e.response is not None else str(e)
        return json.dumps({
            "success": False,
            "message": "记忆检索失败",
            "error": str(e),
            "status_code": e.response.status_code if e.response is not None else None,
            "details": detail
        }, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return json.dumps({"success": False, "message": "记忆检索请求失败", "error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "message": "处理记忆检索响应时发生错误", "error": str(e)}, ensure_ascii=False)
