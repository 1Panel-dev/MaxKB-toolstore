# Desearch Web Search for MaxKB

A native MaxKB custom tool that calls `web-search` on the hosted Desearch MCP service at `https://mcp.desearch.ai/mcp`. It returns titles, HTTPS source URLs and snippets. No API or MCP server code is copied into this package.

## Install and run

1. Use a self-hosted MaxKB **v2.10.8-lts** instance. Download the trusted `1.0.0/Desearch.tool` from this directory. MaxKB `.tool` is a Python pickle format; import files only from a trusted source.
2. Open **Tools → Import**, select `Desearch.tool` and open the imported **Desearch Web Search** custom tool. The imported tool starts inactive and contains no credential.
3. **Before supplying any real key**, apply and verify the memory-only executor configuration below, with `INFO` logging. Restart every MaxKB process that can execute tools with these settings. An ordinary disk-backed temporary directory does not meet this integration's credential requirements.
4. Open the tool's debug panel. Supply your Desearch key in the **Desearch API key (runtime only)** password input, set `query` and optionally `max_results`, then run. Get your own key at https://console.desearch.ai/.
5. Pass the key as a runtime `init_params.desearch_api_key` value. Do not save a key into the tool, its code, its default value, a workflow, or exported files. The adapter does not read process environment variables. MaxKB clears the tool subprocess environment.

The tested route is import plus the native custom-tool debug executor on an isolated self-hosted MaxKB v2.10.8-lts instance, with the standard Linux sandbox enabled. MaxKB's native executor embeds runtime arguments in a temporary Python file, including the key. The mandatory tmpfs/no-swap configuration below keeps that file in memory; INFO logging prevents the executor from logging its contents. Persistent credential storage and model-driven workflow configuration are outside this version's validated route. The host receives the key at execution time and sends it only as `x-api-key` to the fixed HTTPS MCP endpoint. No arbitrary endpoint option, subprocess, local storage, direct Desearch API call or retry is included in this adapter.

A Desearch account/key and available search balance are required. Search usage follows your Desearch account plan; this package does not provision billing or promise free usage.

## Required memory-only executor configuration

Apply these options to the existing MaxKB Docker container, preserving its other deployment options. The memory values below match the tested isolated import/debug host; allocate enough RAM for your deployment and keep both values equal to disable container swap. This requires Linux cgroup v2 with enforced swap limits.

```sh
--memory=1536m --memory-swap=1536m --ulimit core=0 \
--tmpfs /run/maxkb-tool-tmp:rw,noexec,nosuid,nodev,size=32m,mode=0700 \
-e TMPDIR=/run/maxkb-tool-tmp \
-e TMP=/run/maxkb-tool-tmp -e TEMP=/run/maxkb-tool-tmp \
-e MAXKB_CONFIG_TYPE=ENV -e MAXKB_LOG_LEVEL=INFO
```

Do not bind-mount this directory or place it on a disk volume. Set these variables before Python starts: Python caches its temporary-directory selection, and can fall back to a disk path if the configured directory is unavailable. Before starting the web executor (and any tool-executing worker), run this preflight in that container and refuse real-key execution unless every check passes:

```sh
set -eu
test "$(findmnt -T "$TMPDIR" -no FSTYPE)" = tmpfs
test "$(cat /sys/fs/cgroup/memory.swap.max)" = 0
python -c 'import tempfile; assert tempfile.gettempdir() == "/run/maxkb-tool-tmp"'
test "$(ulimit -c)" = 0
```

Also verify the web process inherited this configuration using the dummy-canary probe in the QA evidence: while a native debug call is running, its generated `.py` file must reside in this tmpfs, have mode `0600`, and contain the dummy argument; after normal completion **and an execution exception**, that file must be gone. No real key should be used for inspection. The probe also checks the executor's sandbox remains enabled.

The host's `NamedTemporaryFile(delete=True)` cleans up when the executor unwinds normally or handles a tool failure. A forced process/VM termination can leave a file in the RAM mount until the container stops; stopping the container discards the tmpfs. Container swap and core dumps must remain disabled. Do not copy, back up or snapshot this execution-memory mount. INFO logging and runtime-only parameters are required in addition to the memory mount. If these checks cannot be enforced, do not run this integration with a real key.

This uses standard [Python temporary-directory configuration](https://docs.python.org/3.11/library/tempfile.html#tempfile.gettempdir) and [Docker equal memory/swap limits](https://docs.docker.com/engine/containers/resource_constraints/#--memory-swap-details); it requires no MaxKB core change. The QA pack records in-flight success/failure canaries and subsequent native authenticated searches under these settings.

## Parameters

| Name | MaxKB field | Required | Meaning |
| --- | --- | --- | --- |
| `desearch_api_key` | Runtime startup password input | Yes | Caller-supplied Desearch API key. Default is empty. |
| `query` | Referenced string input | Yes | Nonblank search query, at most 2,000 characters. |
| `max_results` | Referenced integer input | No | 1 to 10, default 5; caps parsed results locally. It does not change upstream search usage. |

Example runtime inputs (replace the placeholder only in the runtime password field):

```json
{"query": "Python urllib request documentation", "max_results": 3}
```

The result is a JSON string, so parse it before referencing fields in a later step:

```json
{"success": true, "query": "Python urllib request documentation", "results": [{"title": "Example source title", "url": "https://example.org/source", "snippet": "Example excerpt"}]}
```

An empty results array is valid. The adapter omits non-HTTPS, untitled and duplicate sources. It uses the hosted server's result text or structured content. It initializes MCP, sends the initialized notification and calls `web-search`, handling JSON and SSE responses. Connect timeout is 10 seconds, read timeout is 45 seconds per HTTP request; there are at most three requests per run, with no automatic retry. Responses over 5 MB are rejected.

Failures return `{"success": false, "error": "<code>", "results": []}`. Codes are `missing_api_key`, `invalid_api_key`, `invalid_query`, `invalid_max_results`, `authentication_failed` (HTTP 401/403), `search_rejected` (MCP tool error), `request_timeout`, `connection_failed`, `unsupported_mcp_version`, and `invalid_mcp_response` (including other HTTP/RPC errors). Remote error bodies and request headers are not returned. A key rejected inside an MCP tool result may use `search_rejected`.

## Dependencies and disable

Python 3.11 and `requests` are provided by the tested MaxKB image's sandbox. No extra installation is required. The tool supports negotiated MCP versions 2024-11-05, 2025-03-26 and 2025-06-18. To disable it, stop calling it and leave the imported tool inactive; remove its workflow references before deleting it. No remote setup is created.

## Source and reproducibility

Only `data.yaml`, `logo.png`, this README, `LICENSE` and one versioned `.tool` are included. The source below is exactly the packaged Python function. The binary uses the host's `tools.serializers.tool.ToolInstance` envelope with format version `v2`, pickle protocol 4, a blank credential default and custom-tool input metadata. QA evidence includes a reproducible build script, protocol/error tests and an installed-host test harness. This public package is prepared for review; it has not been submitted to the MaxKB store.

References checked 2026-11-16:

- [Official MaxKB toolstore format](https://github.com/1Panel-dev/MaxKB-toolstore/tree/2fa10771662aad33cc9949aa8194fabcac1e2289).
- [MaxKB v2.10.8-lts](https://github.com/1Panel-dev/MaxKB/tree/792a525c5a78e42bf04b91c251f747a0bc3e8517).
- [Desearch MCP reference](https://github.com/Desearch-ai/mcp-desearch/tree/42bb4ef2312c28976fb295521b6fda20132ef1fc). Logo reused from `public/icon-512.png` at that revision.

```python
def desearch_search(query: str, max_results: int = 5, desearch_api_key: str = ""):
    """Search the public web through the hosted Desearch MCP service."""
    import json
    from urllib.parse import urlsplit

    import requests

    def fail(code):
        return json.dumps({"success": False, "error": code, "results": []})

    if not isinstance(desearch_api_key, str) or not desearch_api_key.strip():
        return fail("missing_api_key")
    key = desearch_api_key.strip()
    if len(key) > 512 or any(ord(char) < 32 or ord(char) > 126 for char in key):
        return fail("invalid_api_key")
    if not isinstance(query, str) or not query.strip() or len(query) > 2000:
        return fail("invalid_query")
    if max_results is None:
        max_results = 5
    if type(max_results) is not int or not 1 <= max_results <= 10:
        return fail("invalid_max_results")
    query = query.strip()
    headers = {
        "x-api-key": key,
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    endpoint = "https://mcp.desearch.ai/mcp"

    def rpc(body):
        with requests.post(
            endpoint, headers=headers, json=body, timeout=(10, 45), allow_redirects=False, stream=True
        ) as response:
            if response.status_code in (401, 403):
                raise PermissionError
            if response.status_code not in (200, 202, 204):
                raise RuntimeError("mcp_http_error")
            session_id = response.headers.get("Mcp-Session-Id")
            if session_id:
                headers["Mcp-Session-Id"] = session_id
            if "id" not in body:
                return None
            chunks = []
            size = 0
            for chunk in response.iter_content(65536):
                size += len(chunk)
                if size > 5_000_000:
                    raise RuntimeError("mcp_response_too_large")
                chunks.append(chunk)
            text = b"".join(chunks).decode("utf-8")
            if "text/event-stream" in response.headers.get("Content-Type", ""):
                frames = []
                for event in text.replace("\r\n", "\n").split("\n\n"):
                    data = "\n".join(line[5:].lstrip(" ") for line in event.splitlines() if line.startswith("data:"))
                    if data:
                        frames.append(json.loads(data))
            else:
                frames = [json.loads(text)]
            replies = [frame for frame in frames if isinstance(frame, dict) and frame.get("id") == body["id"]]
            if not replies:
                raise RuntimeError("invalid_mcp_response")
            reply = replies[-1]
            if "error" in reply:
                raise RuntimeError("mcp_rpc_error")
            if not isinstance(reply.get("result"), dict):
                raise RuntimeError("invalid_mcp_response")
            return reply["result"]

    try:
        initialized = rpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "desearch-maxkb-integration", "version": "1.0.0"},
                },
            }
        )
        version = initialized.get("protocolVersion")
        if version not in ("2024-11-05", "2025-03-26", "2025-06-18"):
            return fail("unsupported_mcp_version")
        headers["MCP-Protocol-Version"] = version
        rpc({"jsonrpc": "2.0", "method": "notifications/initialized"})
        result = rpc(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "web-search",
                    "arguments": {"query": query},
                },
            }
        )
        if result.get("isError"):
            return fail("search_rejected")
        payloads = []
        if isinstance(result.get("structuredContent"), dict):
            payloads.append(result["structuredContent"])
        for content in result.get("content", []):
            if content.get("type") == "text":
                try:
                    payloads.append(json.loads(content["text"]))
                except (ValueError, KeyError, TypeError):
                    pass
        rows = []

        def collect(value, depth=0):
            if depth > 5:
                return
            if isinstance(value, list):
                rows.extend(item for item in value if isinstance(item, dict))
            elif isinstance(value, dict):
                for name in ("data", "organic", "results", "search_results", "items", "search"):
                    if name in value:
                        collect(value[name], depth + 1)

        for payload in payloads:
            collect(payload)
        results = []
        seen = set()
        for row in rows:
            url = row.get("link") or row.get("url") or row.get("href")
            title = row.get("title") or row.get("name")
            if not isinstance(url, str) or not isinstance(title, str) or not title.strip():
                continue
            try:
                parsed = urlsplit(url)
                if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                    continue
            except ValueError:
                continue
            if key in url or url in seen:
                continue
            seen.add(url)
            snippet = row.get("snippet") or row.get("description") or ""
            results.append(
                {
                    "title": title.strip().replace(key, "[redacted]"),
                    "url": url,
                    "snippet": snippet.replace(key, "[redacted]") if isinstance(snippet, str) else "",
                }
            )
            if len(results) >= max_results:
                break
        return json.dumps({"success": True, "query": query, "results": results}, ensure_ascii=False)
    except PermissionError:
        return fail("authentication_failed")
    except requests.exceptions.Timeout:
        return fail("request_timeout")
    except requests.exceptions.RequestException:
        return fail("connection_failed")
    except (ValueError, TypeError, KeyError, AttributeError, RuntimeError):
        return fail("invalid_mcp_response")
```
