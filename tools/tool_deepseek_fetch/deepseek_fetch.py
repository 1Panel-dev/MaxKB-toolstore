# -*- coding: utf-8 -*-
# =============================================================================
# MaxKB 脚本工具：DeepSeek 网页正文抓取（Fetch API）
# 接口文档：https://api-docs.deepseek.com/zh-cn/guides/search
# 规范同上：main() 必须放在最后，参数名与工具面板一致，返回 dict。
# =============================================================================
import json

FETCH_URL = "https://api.deepseek.com/v1/tools/fetch"
TIMEOUT = 40
MAX_CHARS = 8000

STATUS_HINT = {
    400: "url 不合法（必须为含 host 的 http/https 地址，不带账号密码，长度 ≤ 8192）",
    401: "API Key 缺失或无效",
    402: "DeepSeek 账户余额不足",
    403: "Fetch 被安全策略拒绝（目标站点不允许抓取）",
    404: "未能获取可用网页内容（URL 失效/被站点拦截/无可提取正文）",
    429: "触发 QPS 限速（Fetch 每账号 5 QPS，且按目标域名单独限速）",
}


def _http_post_json(url, headers, payload, timeout=TIMEOUT):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    try:
        import requests
    except Exception:
        requests = None

    if requests is not None:
        resp = requests.post(url, headers=headers, data=body, timeout=timeout)
        return resp.status_code, resp.text

    import urllib.request
    import urllib.error

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main(api_key, url, max_chars=8000):
    api_key = (api_key or "").strip()
    url = (url or "").strip()

    if not api_key:
        return {"success": False, "error": "缺少 api_key", "title": "", "content": ""}
    if not url:
        return {"success": False, "error": "缺少 url", "title": "", "content": ""}

    body = {"url": url[:8192]}
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        status, text = _http_post_json(FETCH_URL, headers, body)
    except Exception as e:
        return {
            "success": False,
            "error": "请求异常：%s" % e,
            "hint": "检查 MaxKB 容器到 api.deepseek.com 的网络连通性",
            "title": "",
            "content": "",
        }

    try:
        data = json.loads(text) if text else {}
    except Exception:
        return {"success": False, "status": status, "error": (text or "")[:300], "title": "", "content": ""}

    if status != 200:
        err = data.get("error") or {}
        return {
            "success": False,
            "status": status,
            "error": err.get("message") or ("HTTP %s" % status),
            "hint": STATUS_HINT.get(status, "未预期状态码，请对照官方文档排查"),
            "title": "",
            "content": "",
        }

    title = data.get("title") or ""
    content = data.get("content") or ""
    try:
        limit = int(float(str(max_chars)))
    except Exception:
        limit = MAX_CHARS
    truncated = len(content) > limit
    if truncated:
        content = content[:limit] + "\n\n……（正文已截断）"

    return {
        "success": True,
        "title": title,
        "url": url,
        "chars": len(content),
        "truncated": truncated,
        "content": content,
        "markdown": ("# %s\n\n来源：%s\n\n%s" % (title or url, url, content)).strip(),
    }
