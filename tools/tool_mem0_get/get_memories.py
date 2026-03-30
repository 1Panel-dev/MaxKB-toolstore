import json
import requests


def get_memories(user_id: str = "", agent_id: str = "", app_id: str = "", run_id: str = "", api_key: str = "", base_url: str = "https://api.mem0.ai"):
    try:
        if not api_key:
            return json.dumps({"success": False, "message": "api_key 不能为空", "error": "missing_api_key"}, ensure_ascii=False)
        if not any([user_id, agent_id, app_id, run_id]):
            return json.dumps({
                "success": False,
                "message": "user_id、agent_id、app_id、run_id 至少需要提供一个",
                "error": "missing_scope_filter"
            }, ensure_ascii=False)

        filters = []
        if user_id:
            filters.append({"user_id": user_id})
        if agent_id:
            filters.append({"agent_id": agent_id})
        if app_id:
            filters.append({"app_id": app_id})
        if run_id:
            filters.append({"run_id": run_id})

        payload = {
            "version": "v2"
        }
        if len(filters) == 1:
            payload["filters"] = filters[0]
        else:
            payload["filters"] = {"OR": filters}

        rep = requests.post(
            url=f"{base_url.rstrip('/')}/v2/memories/",
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
        return json.dumps({"success": True, "message": "记忆获取成功", "data": data}, ensure_ascii=False)
    except requests.exceptions.HTTPError as e:
        detail = None
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text if e.response is not None else str(e)
        return json.dumps({
            "success": False,
            "message": "获取记忆失败",
            "error": str(e),
            "status_code": e.response.status_code if e.response is not None else None,
            "details": detail
        }, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return json.dumps({"success": False, "message": "获取记忆请求失败", "error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "message": "处理获取记忆响应时发生错误", "error": str(e)}, ensure_ascii=False)
