import json
import subprocess


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

        payload = {}
        if len(filters) == 1:
            payload["filters"] = filters[0]
        else:
            payload["filters"] = {"OR": filters}

        curl_cmd = [
            "curl",
            "-sS",
            "-X",
            "POST",
            f"{base_url.rstrip('/')}/v2/memories/",
            "-H",
            f"Authorization: Token {api_key}",
            "-H",
            "Content-Type: application/json",
            "-H",
            "Accept: application/json",
            "--data",
            json.dumps(payload, ensure_ascii=False),
            "--max-time",
            "30"
        ]
        rep = subprocess.run(curl_cmd, capture_output=True, text=True)
        if rep.returncode != 0:
            return json.dumps({
                "success": False,
                "message": "获取记忆请求失败",
                "error": rep.stderr.strip() or f"curl exited with code {rep.returncode}"
            }, ensure_ascii=False)

        raw = rep.stdout.strip()
        try:
            data = json.loads(raw) if raw else []
        except Exception:
            return json.dumps({
                "success": False,
                "message": "处理获取记忆响应时发生错误",
                "error": "invalid_json_response",
                "raw_response": raw
            }, ensure_ascii=False)

        return json.dumps({"success": True, "message": "记忆获取成功", "data": data}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "message": "处理获取记忆响应时发生错误", "error": str(e)}, ensure_ascii=False)
