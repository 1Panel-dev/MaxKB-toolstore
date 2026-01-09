# CRM 客户关系录入AI智能体

## 一、应用描述

该应用用于使用自然语言描述，在 Cordys CRM 系统中创建线索、客户、联系人、商机等信息，帮助用户更好地使用 Cordys CRM 系统及其智能体。适用于 Cordys CRM 系统用户，需要使用自然语言描述创建信息的情况。

## 二、应用功能

CRM 客户关系录入AI智能体应用主要包含以下几个大功能：
- 线索录入：与 AI 对话，生成线索信息，并调用 Cordys CRM MCP 工具将线索信息写入 Cordys CRM 系统。
- 客户录入：与 AI 对话，生成客户信息，并调用 Cordys CRM MCP 工具将客户信息写入 Cordys CRM 系统。
- 商机录入：与 AI 对话，生成商机信息，并调用 Cordys CRM MCP 工具将商机信息写入 Cordys CRM 系统。
- 联系人录入：与 AI 对话，生成联系人信息，并调用 Cordys CRM MCP 工具将联系人信息写入 Cordys CRM 系统。
能够使用自然语言描述创建线索、客户、联系人、商机等信息：用户可以输入要创建的线索名/商机名/联系人/客户名的信息，应用将逐步引导用户补充必填信息，信息完整后生成json数据，待用户确认后即调用mcp工具写入 Cordys CRM 系统。

## 三、应用构建要素

CRM 客户关系录入AI智能体应用构建时涉及的核心要素内容：
- 大模型：deepseek-chat
- MCP 与工具：Cordys CRM MCP: https://cordys.cn/docs/mcp_server/#41-maxkb，提取AI内容里面的json
- 子应用：Cordys 查重、获取登录用户信息、Cordys 循环补充线索 

需要涉及到的参数（每个应用都需要）：

| 参数名 | 类型 | 说明                    |
| ------ | ---- | ----------------------- |
| `ak`   | str  | Cordys CRM的 Access Key |
| `sk`   | str  | Cordys CRM的 Secret Key |

### 子应用介绍：

#### （1）Cordys 查重

- 工作流：部分截图

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/cordys_duplicate_check.png">

#### （2）获取登录用户信息

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/get_logged_user_info.png">

#### （3）Cordys 循环补充线索

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/crm_loop_customer_relationship_supplement.png">

- 工作流：部分截图

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/crm_customer_entry_ai_agent.png">

## 四、应用效果

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/crm_customer_entry_ai_agent.gif">

## 五、注意事项

- 嵌套关系是`CRM 客户关系录入AI智能体`调用`Cordys 循环补充线索`和`Cordys 查重`，`Cordys 循环补充线索`调用`获取登录用户信息`
- 应当事先准备好Cordys CRM的 Access Key 和 Secret Key
- 应用会根据用户提供的Access Key 和 Secret Key，判断用户的身份信息。
- 