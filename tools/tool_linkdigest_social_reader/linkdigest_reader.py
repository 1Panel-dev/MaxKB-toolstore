# -*- coding: utf-8 -*-
# =============================================================================
# MaxKB 脚本工具：LinkDigest 社交链接转文本
# 接口文档：https://linkdigest.dev/zh/docs  （REST：POST /api/v1/digest）
# 一条小红书 / 抖音 / B站 / 微博 / 公众号 / 小宇宙 / TikTok / YouTube / X / Instagram
# 链接（或整段分享文案）→ 正文、带时间的口播文案、画面文字、要点、热评。
# 不登录、不用 Cookie；LinkDigest 在自己的服务器上读公开页面。
# 规范：main() 放在最后，参数名与工具面板一致，返回 dict。
# =============================================================================
import json
import time

API_URL = "https://linkdigest.dev/api/v1/digest"
TIMEOUT = 60
# 视频要读 30–90 秒；接口约 25 秒内先返回 pending，同样的请求再发一次只扣一次费。
WAIT_SECONDS = 100
MAX_CHARS = 12000

STATUS_HINT = {
    400: "链接无法识别：请贴完整的分享链接或整段分享文案",
    401: "API Key 缺失或无效（https://linkdigest.dev/app/keys 获取，形如 ld_live_...）",
    402: "积分不够，或视频超过当前套餐的时长上限：见返回里的购买链接（支付宝 / 银行卡，一次性、不订阅）",
    422: "平台没有给出这条内容（已删除、仅自己可见或需要 App 打开），不扣积分",
    429: "请求太频繁，稍后再试",
    503: "平台暂时拒绝了服务器读取，不扣积分；稍后再试，或按返回里的 how_to_read_now 处理",
}


def _post_json(url, headers, payload, timeout=TIMEOUT):
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


def _lines(items, key="text"):
    out = []
    for it in items or []:
        if isinstance(it, dict):
            text = str(it.get(key) or "").strip()
        else:
            text = str(it or "").strip()
        if text:
            out.append(text)
    return out


def main(api_key, url, depth="", max_chars=12000):
    api_key = (api_key or "").strip()
    url = (url or "").strip()
    depth = (depth or "").strip().lower()

    if not api_key:
        return {"success": False, "error": "缺少 api_key", "content": ""}
    if not url:
        return {"success": False, "error": "缺少 url", "content": ""}

    payload = {"url": url[:4000]}
    # full（默认，口播 + 画面文字 + 要点）/ transcript（逐字稿优先）/ script（只要口播文案，最便宜）
    if depth in ("transcript", "script"):
        payload["depth"] = depth

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
        "User-Agent": "LinkDigest-MaxKB-tool/1.0",
    }

    started = time.time()
    status, text = _post_json(API_URL, headers, payload)
    while status == 202 and time.time() - started < WAIT_SECONDS:
        time.sleep(10)
        status, text = _post_json(API_URL, headers, payload)

    try:
        data = json.loads(text or "{}")
    except Exception:
        data = {}

    if status == 202:
        return {
            "success": False,
            "pending": True,
            "error": "还在读（长视频）。稍后用同样的参数再调用一次即可拿到结果，只扣一次积分。",
            "content": "",
        }

    if status != 200:
        out = {
            "success": False,
            "status": status,
            "error": data.get("error") or ("HTTP %s" % status),
            "error_code": data.get("error_code") or "",
            "hint": STATUS_HINT.get(status, "未预期状态码，请对照 https://linkdigest.dev/zh/docs 排查"),
            "content": "",
        }
        for k in ("starter_url", "buy_url", "subscribe_url", "offer_zh", "how_to_read_now"):
            if data.get(k):
                out[k] = data[k]
        return out

    transcript = _lines(data.get("transcript"))
    on_screen = _lines(data.get("on_screen"))
    key_points = _lines(data.get("key_points"))
    comments = _lines(data.get("comments"))
    content = data.get("raw_markdown") or ""

    try:
        limit = int(float(str(max_chars)))
    except Exception:
        limit = MAX_CHARS
    truncated = len(content) > limit
    if truncated:
        content = content[:limit] + "\n\n……（已截断）"

    return {
        "success": True,
        "platform": data.get("platform") or "",
        "title": data.get("title") or "",
        "author": data.get("author") or "",
        "url": data.get("source_url") or url,
        "transcript": "\n".join(transcript),
        "on_screen_text": "\n".join(on_screen),
        "key_points": key_points,
        "top_comments": comments,
        "credits": data.get("credits"),
        "credits_left": data.get("credits_left"),
        "cached": data.get("cached"),
        "truncated": truncated,
        "content": content,
    }
