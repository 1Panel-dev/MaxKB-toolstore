# MaxKB RAG-QA技能

面向 AI Agent 的通用 MaxKB RAG Skill。核心采用**统一、渐进式检索链路**，不人为区分简单问题和复杂问题：所有问题优先走 Vector/Blend，只有证据不足时才逐级升级到 Query Rewrite、Paragraph Fallback、Section/Context 和必要的多步检索。

完整使用协议见 [SKILL.md](SKILL.md)。

## 核心能力

- AI Agent 负责理解问题和判断证据是否足够，Skill 负责执行检索与证据获取；
- 默认优先 `search`，避免每个问题都执行完整规划；
- `search` 内部采用 `Blend → Embedding → Query Rewrite → Paragraph Fallback` 的渐进式检索；
- Paragraph Fallback 使用文档名、标题、中文关键词、业务术语和精确编号等确定性信息，解决“知识存在但向量没有搜出来”；
- 支持 `enum_documents`、`get_section`、`context`；
- 证据不足时再进行 Query Rewrite、扩大知识库范围或按缺口执行多步检索；
- 可解释 Evidence Score，不使用独立 Reranker；
- 区分真实无命中与 API/网络/权限错误；
- 仅依赖 Python 标准库。

## 检索原则

```text
原始问题
  ↓
Vector / Blend
  ↓
结果足够？ → 回答
  ↓ 否
Query Rewrite
  ↓
再次 Vector / Blend
  ↓
仍不足？
  ↓
Paragraph Fallback
  ↓
仍不足？
  ↓
Section / Context 或按缺口多步检索
```

复杂问题也使用同一条链路，不单独启动“复杂模式”。

## 运行环境

本 Skill 面向 MaxKB Agent Runtime 运行。MaxKB 当前支持 Python Skill，Skill 内部脚本可以使用 Python 访问 MaxKB API；子进程、系统调用、文件和网络访问受 MaxKB Sandbox / Runtime 限制。

Agent 不需要自行执行 CLI 来调用 Skill；`scripts/*.py` 由 Skill Runtime 负责运行。

独立开发或调试时可以使用 Python CLI 初始化配置，但这属于管理员/开发者操作，不是 Agent 运行时前提。

## 环境要求

- Python 3.7+
- 含 `/admin/api` 管理端和 `hit_test` 接口的 MaxKB 实例
- API Key 与至少一个可访问工作空间

## 初始化（独立开发/调试）

```bash
python scripts/init.py
```

初始化仅需输入 MaxKB 地址和 API Key。地址支持 HTTP 或 HTTPS，例如：

```text
http://maxkb.example.com:50505
https://maxkb.example.com:50505
```

常用命令：

| 命令 | 用途 |
|---|---|
| `python scripts/init.py --status` | 查看连接、工作空间和知识库别名 |
| `python scripts/init.py --workspaces` | 重选工作空间并重选知识库 |
| `python scripts/init.py --knowledge` | 重选知识库 |
| `python scripts/init.py --connection` | 更新地址或 API Key |
| `python scripts/init.py --reset` | 清空本地配置与选库状态 |

### 高层取证封装（answer.py）

`scripts/answer.py` 是 v5.3 新增的一体化取证入口：单次进程内完成「检索 → 枚举 → 定位 → 全文 dump」，避免反复冷启动与重复拉取文档清单。

| 命令 | 用途 |
|---|---|
| `python scripts/answer.py "你的问题"` | 渐进式取证，输出结构化证据（含来源/质量分/缺口） |
| `python scripts/answer.py "问题" --json` | 输出完整 JSON，便于程序解析 |
| `python scripts/answer.py --enum` | 只枚举文档清单（建立答案边界） |
| `python scripts/answer.py --full FM5` | dump 名称含 FM5 的文档全文 |
| `python scripts/answer.py "问题" --refresh` | 清本地缓存后重新取证 |

## v5.2 性能优化

在保持检索正确率不变的前提下，引入三项零风险优化：

- **本地缓存层**：`list_documents` / `get_paragraphs` 的结果按「知识库/文档」缓存到 `.cache/`，默认 TTL 6 小时。仅缓存成功响应，命中失败绝不缓存，数据同源故不影响正确率。
  - 关闭/调参：设 `MAXKB_CACHE_TTL=0` 关闭缓存；在 `.env` 写入 `MAXKB_CACHE_TTL=3600` 改窗口；代码层 `refresh=True` 或 `clear_cache()` 强制重拉。
- **段落兜底并发**：`_paragraph_search` 的逐文档串行 GET 改为线程池并发（默认 `pool=8`），最坏耗时随文档数线性下降，结果集与原逻辑等价。
- **高层 answer.py 封装**：见上表，减少重复冷启动与重复枚举。

实测（开发环境）：`list_documents` 约 6.6x、`get_paragraphs` 约 5.3x 加速，证据完全一致。

## v5.3 沙箱（Sandbox）健壮性

针对 MaxKB Agent Runtime 把 `/skills` **只读挂载**导致写入崩溃的问题（典型报错 `PermissionError: ...Permission denied: '.../skills/..env.xxxx'`），做了根因修复：

- **可写探测 + 运行时目录**：启动时探测技能目录是否可写；只读时把 `state.json` 与 `.cache` 自动改挂到系统临时目录（如 `tempfile.gettempdir()/maxkb_rag_qa_runtime`），配置读取仍优先环境变量注入。
- **`atomic_write` 全程不抛错**：临时文件改在系统临时目录创建，落到只读目标失败则返回 `False`，由调用方降级，不再冒 `PermissionError` 中断 `init.py` 等命令。
- **`save_kbs` / `write_env` 降级**：只读沙箱下返回失败并提示，同时仍把键值注入当前进程环境变量；运行时依赖平台注入的 `MAXKB_DOMAIN` / `MAXKB_TOKEN` / `MAXKB_WS` 与 `load_kbs()` 的动态知识库发现，无需持久化 `state.json`。
- **缓存优化在沙箱内恢复生效**：v5.2 的本地缓存原本写在技能目录、在只读沙箱里静默失效；v5.3 起缓存随运行时目录落到可写位置，提速优化在 MaxKB 上同样有效。

> 结论：`init.py` 等命令在只读沙箱中可安全空跑不中断；真正检索（`search` / `get_section` / 动态发现）不受影响，与本地开发行为一致。

## 基础接口

### Search

```python
from scripts.kbs import search
result = search("系统 A 部署失败如何排查", kb=None, verbose=False)
```

返回：

- `hits`：候选证据；
- `rounds`：实际执行过的检索阶段；
- `failures`：调用失败信息。

### Agent 渐进式编排

```python
from scripts.agentic import agent_retrieve
result = agent_retrieve("系统 A 的 v1 和 v2 在权限与审计方面有什么差异？")
print(result["decision"])
for evidence in result["evidence_pack"]["evidence"]:
    print(evidence["doc"], evidence["content"])
```

`agent_retrieve()` 不是另一套独立检索器，而是对 `search()` 的渐进式编排：首轮正常搜索，证据不足才升级到 Rewrite、范围扩展、Section/Context 或按缺口多步检索。

### 文档枚举

仅在确认“文档名就是业务实体”时使用：

```python
from scripts.kbs import enum_documents
result = enum_documents("角色资料@默认工作空间", verbose=False)
```

### 小节与上下文

```python
from scripts.kbs import get_section, context
sections = get_section("系统文档@默认工作空间", "权限配置", context=1, doc="管理员手册")
blocks = context("系统文档@默认工作空间", "部署要求", radius=1, doc="安装指南")
```

## 目录

```text
maxkb-rag-qa/
├── SKILL.md
├── README.md
├── .env.example
├── state.example.json
└── scripts/
    ├── init.py
    ├── configure.py
    ├── kbs_common.py
    ├── kbs.py
    ├── agentic.py
    ├── answer.py
    └── pick_kb.py
```

> 注：`.env`（含 API Key）与 `state.json`（已选知识库）为本地配置，不随技能包分发；分发时仅提供 `.env.example` / `state.example.json` 模板。`.cache/` 为运行时缓存，亦不纳入包。
