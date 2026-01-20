# CRM 智能查询智能体

## 一、应用描述

本应用专为 Cordys CRM 系统用户设计，依托 AI 自然语言交互能力，简化查询信息的流程。用户无需手动操作系统表单，仅需用自然语言描述要查询的信息，AI 智能体便会调用 MCP 工具在 Cordys CRM 系统中进行查询，降低系统操作门槛，适配销售、客服等岗位的业务需求。

## 二、应用功能

CRM 智能查询智能体应用具有以下功能：
- 查询信息：用户通过自然语言描述要查询的信息，AI 智能体会调用 Cordys CRM MCP 工具进行查询，并将查询结果返回给用户。

## 三、应用构建要素

CRM 智能记录智能体应用构建时涉及的核心要素内容：
- 大模型：deepseek-chat
- MCP ：Cordys CRM MCP: https://cordys.cn/docs/mcp_server/#41-maxkb
- 工具：计算时间


需要涉及到的参数：

| 参数名 | 类型 | 说明                    |
| ------ | ---- | ----------------------- |
| `ak`   | str  | Cordys CRM的 Access Key |
| `sk`   | str  | Cordys CRM的 Secret Key |


- 工作流：

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/intelligent_search.png">

## 四、应用效果

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/intelligent_search.gif">


