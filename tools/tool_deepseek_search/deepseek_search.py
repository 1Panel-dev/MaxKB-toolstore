# -*- coding: utf-8 -*-
# =============================================================================
# MaxKB 脚本工具：DeepSeek 联网搜索（Search API）
# 接口文档：https://api-docs.deepseek.com/zh-cn/guides/search
#
# MaxKB 工具规范要点（照抄即可生效）：
#   1. 代码里必须有一个 main() 作为入口，参数名/顺序须与工具「参数」面板完全一致；
#   2. MaxKB 内部以 main(**keywords) 的关键字方式调用，参数名不一致会直接 TypeError；
#   3. main() 必须写在代码的【最后】，MaxKB 取「最后一个定义的对象」作为入口函数；
#   4. 返回值需可 JSON 序列化，建议统一返回 dict（success / results / markdown / error）；
#   5. 不要在此文件里调用 main()，也不要写 `if __name__ == '__main__'`。
# =============================================================================
import json

SEARCH_URL = "https://api.deepseek.com/v1/tools/search"
TIMEOUT = 30          # 秒；MaxKB 函数执行默认超时为 3600s，这里只限制单次 HTTP
MAX_CONTENT_CHARS = 1500   # 单条正文截断长度，避免把上下文塞爆

STATUS_HINT = {
    400: "请求参数不合法（检查 query 长度 1~128 字符、count 在 1~50 之间）",
    401: "API Key 缺失或无效，请检查工具参数中的 api_key",
    402: "DeepSeek 账户余额不足，请充值后重试",
    429: "触发 QPS 限速（Search 每账号 5 QPS），请稍后重试",
    500: "DeepSeek 服务端内部错误，建议稍后重试",
    504: "DeepSeek 下游请求超时，建议稍后重试",
}


def _to_int(value, default):
    """把模型传进来的 "5" / 5.0 / None 统一成 int。"""
    try:
        return int(float(str(value).strip()))
    except Exception:
        return default


def _to_bool(value):
    """把 "true" / 1 / True 统一成 bool。"""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "y", "on")


def _http_post_json(url, headers, payload, timeout=TIMEOUT):
    """POST JSON，返回 (status_code, text)。优先 requests，缺失时回退 urllib。"""
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


def _build_markdown(items):
    """把结构化结果拼成给模型看的 Markdown，减少模型二次解析成本。"""
    if not items:
        return "未检索到相关网页。可尝试更换关键词、放宽 site:/after: 等限定条件。"

    blocks = []
    for i, it in enumerate(items, 1):
        lines = ["### %d. %s" % (i, it.get("title") or "(无标题)")]
        meta = []
        if it.get("site_name"):
            meta.append("站点：%s" % it["site_name"])
        if it.get("date"):
            meta.append("时间：%s" % it["date"])
        if it.get("authority") is not None:
            meta.append("权威性：%s/4" % it["authority"])
        if it.get("rerank_score") is not None:
            meta.append("相关度：%s/3" % it["rerank_score"])
        if meta:
            lines.append("- " + " ｜ ".join(meta))
        lines.append("- 链接：%s" % (it.get("url") or ""))
        summary = it.get("summary") or it.get("snippet") or ""
        if summary:
            lines.append("")
            lines.append(summary.strip())
        content = (it.get("content") or "").strip()
        if content:
            if len(content) > MAX_CONTENT_CHARS:
                content = content[:MAX_CONTENT_CHARS] + "……（正文已截断）"
            lines.append("")
            lines.append("> " + content.replace("\n", "\n> "))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def main(api_key, query, count=10, need_content="false", ori_question=""):
    """DeepSeek 网页搜索：返回结构化结果 + 可直接喂给大模型的 Markdown。"""
    api_key = (api_key or "").strip()
    query = (query or "").strip()
    ori_question = (ori_question or "").strip()

    # ---------- 参数校验 ----------
    if not api_key:
        return {
            "success": False,
            "error": "缺少 api_key：请在工具参数中填入 DeepSeek API Key",
            "results": [],
            "count": 0,
            "markdown": "",
        }
    if not query:
        return {
            "success": False,
            "error": "query 不能为空：请把用户问题提炼成 1~128 字符的搜索词",
            "results": [],
            "count": 0,
            "markdown": "",
        }

    count = _to_int(count, 10)
    count = max(1, min(50, count))

    payload = {"query": query[:128], "count": count}
    if _to_bool(need_content):
        payload["need_content"] = True
    if ori_question:
        payload["ori_question"] = ori_question[:128]

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # ---------- 调用接口 ----------
    try:
        status, text = _http_post_json(SEARCH_URL, headers, payload)
    except Exception as e:
        return {
            "success": False,
            "error": "请求异常：%s" % e,
            "hint": "检查 MaxKB 容器到 api.deepseek.com 的网络连通性（出网/代理/防火墙）",
            "results": [],
            "count": 0,
            "markdown": "",
        }

    try:
        data = json.loads(text) if text else {}
    except Exception:
        return {
            "success": False,
            "status": status,
            "error": "响应不是合法 JSON：%s" % (text or "")[:300],
            "results": [],
            "count": 0,
            "markdown": "",
        }

    # ---------- 错误处理 ----------
    if status != 200:
        err = data.get("error") or {}
        message = err.get("message") or data.get("message") or ("HTTP %s" % status)
        return {
            "success": False,
            "status": status,
            "error": message,
            "hint": STATUS_HINT.get(status, "未预期状态码，请对照官方文档排查"),
            "results": [],
            "count": 0,
            "markdown": "",
        }

    # ---------- 结果整形 ----------
    raw_items = data.get("results") or []
    items = []
    for r in raw_items:
        items.append({
            "title": r.get("title") or "",
            "url": r.get("url") or "",
            "snippet": r.get("snippet") or "",
            "summary": r.get("summary") or "",
            "content": r.get("content") or "",
            "site_name": r.get("site_name"),
            "date": r.get("date"),
            "authority": r.get("authority"),
            "rerank_score": r.get("rerank_score"),
        })

    return {
        "success": True,
        "query": payload["query"],
        "count": len(items),
        "results": items,
        "markdown": _build_markdown(items),
        "notice": "" if items else "搜索正常结束但无匹配结果（本次不计费）",
    }
