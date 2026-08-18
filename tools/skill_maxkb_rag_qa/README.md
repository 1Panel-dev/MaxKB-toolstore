# 智能MaxKB知识库检索

面向 AI Agent 的通用 MaxKB RAG 检索技能。核心采用**统一、渐进式检索链路**，不人为区分简单问题和复杂问题：所有问题优先走 Vector/Blend，只有证据不足时才逐级升级到 Query Rewrite、Paragraph Fallback、Section/Context 和必要的多步检索。

## 核心能力

- AI Agent 负责理解问题和判断证据是否足够，Skill 负责执行检索与证据获取；
- 默认优先 `search`，避免每个问题都执行完整规划；
- `search` 内部采用 `Blend → Embedding → Query Rewrite → Paragraph Fallback` 的渐进式检索；
- Paragraph Fallback 使用文档名、标题、中文关键词、业务术语和精确编号等确定性信息，解决"知识存在但向量没有搜出来"；
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

复杂问题也使用同一条链路，不单独启动"复杂模式"。

## 运行环境

本 Skill 面向 MaxKB Agent Runtime 运行。MaxKB 支持以 Python 作为 Skill 的脚本语言；Skill 内部脚本使用 Python 访问 MaxKB API。Python、子进程、系统调用、文件和网络访问都处于 MaxKB Runtime / Sandbox 的受控边界内。

Skill 的初始化参数由 MaxKB Runtime 注入环境变量（`MAXKB_DOMAIN`、`MAXKB_TOKEN`、`MAXKB_WS` 等）；本地开发时可以使用 `.env` / `state.json`，但运行时不应把 `state.json` 作为必须存在的持久配置。

## 初始化（独立开发/调试）

```bash
python scripts/init.py
```

初始化仅需输入 MaxKB 地址和 API Key。常用命令：

| 命令 | 用途 |
|---|---|
| `python scripts/init.py --status` | 查看连接、工作空间和知识库别名 |
| `python scripts/init.py --workspaces` | 重选工作空间并重选知识库 |
| `python scripts/init.py --knowledge` | 重选知识库 |
| `python scripts/init.py --connection` | 更新地址或 API Key |
| `python scripts/init.py --reset` | 清空本地配置与选库状态 |

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

### 文档枚举

仅在确认"文档名就是业务实体"时使用：

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
    └── pick_kb.py
```

## 安全与数据边界

- API Key 仅用于访问用户配置的 MaxKB 实例；
- 不向第三方检索服务发送知识库内容；
- 不在回答中暴露 API Key、内部配置或认证信息；
- `failures` 中的认证、权限、网络等错误应区分处理。
