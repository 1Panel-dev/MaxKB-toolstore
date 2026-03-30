import json
import requests


def add_memory(user_id: str, content: str, role: str = "user", agent_id: str = "", metadata: str = "", api_key: str = "", base_url: str = "https://api.mem0.ai/v1"):
    try:
        if not user_id:
            return json.dumps({"success": False, "message": "user_id 不能为空", "error": "missing_user_id"}, ensure_ascii=False)
        if not content:
            return json.dumps({"success": False, "message": "content 不能为空", "error": "missing_content"}, ensure_ascii=False)
        if not api_key:
            return json.dumps({"success": False, "message": "api_key 不能为空", "error": "missing_api_key"}, ensure_ascii=False)

        payload = {
            "messages": [{"role": role or "user", "content": content}],
            "user_id": user_id,
            "infer": True,
            "version": "v2"
        }
        if agent_id:
            payload["agent_id"] = agent_id
        if metadata:
            try:
                payload["metadata"] = json.loads(metadata)
            except Exception:
                return json.dumps({"success": False, "message": "metadata 必须是合法 JSON 字符串", "error": "invalid_metadata_json"}, ensure_ascii=False)

        rep = requests.post(
            url=f"{base_url.rstrip('/')}/memories/",
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
        return json.dumps({"success": True, "message": "记忆添加成功", "data": data}, ensure_ascii=False)
    except requests.exceptions.HTTPError as e:
        detail = None
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text if e.response is not None else str(e)
        return json.dumps({
            "success": False,
            "message": "添加记忆失败",
            "error": str(e),
            "status_code": e.response.status_code if e.response is not None else None,
            "details": detail
        }, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return json.dumps({"success": False, "message": "添加记忆请求失败", "error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "message": "处理添加记忆响应时发生错误", "error": str(e)}, ensure_ascii=False)
