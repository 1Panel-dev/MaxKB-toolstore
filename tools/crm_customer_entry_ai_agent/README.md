# CRM 客户关系录入AI智能体

## 一、应用描述

该应用用于使用自然语言描述，在 Cordys CRM 系统中创建线索、客户、联系人、商机等信息，帮助用户更好地使用 Cordys CRM 系统及其智能体。适用于 Cordys CRM 系统用户，需要使用自然语言描述创建信息的情况。

## 二、应用功能

CRM 客户关系录入AI智能体应用主要包含以下几个大功能：
- 线索录入：用户通过自然语言与AI智能体对话，告知需创建的线索相关信息，智能体将引导用户补充完整必填项，校验信息合规性后生成标准化线索数据，再调用 Cordys CRM MCP 工具，将已确认的线索信息精准写入 Cordys CRM 系统，实现线索快速录入。
- 客户录入：支持用户以自然语言描述客户基础信息（如企业名称、行业、区域等），AI智能体逐一向用户确认缺失的必填内容，整合形成规范的客户数据并生成JSON格式文件，经用户最终确认后，调用 Cordys CRM MCP 工具完成客户信息向系统的写入操作。
- 商机录入：用户通过自然语言说明商机名称、关联客户、金额等核心信息，AI智能体对信息进行补全引导，确保商机信息完整可追溯，生成符合系统要求的商机数据，待用户确认无误后，调用 Cordys CRM MCP 工具将商机信息同步至 Cordys CRM 系统，实现商机高效建档。
- 联系人录入：用户以自然语言提供联系人姓名、职务、联系方式、所属客户等信息，AI智能体自动校验信息完整性，针对遗漏的必填项进行循环引导补充，整合信息后生成标准化联系人数据，经用户确认后调用 Cordys CRM MCP 工具，将联系人信息写入系统并关联对应客户。

## 三、应用构建要素

CRM 客户关系录入AI智能体应用构建时涉及的核心要素内容：
- 大模型：deepseek-chat
- MCP ：Cordys CRM MCP: https://cordys.cn/docs/mcp_server/#41-maxkb
- 工具：提取AI内容里面的json
- 子应用：Cordys 查重、获取登录用户信息、Cordys 循环补充线索 

需要涉及到的参数（每个应用都需要）：

| 参数名 | 类型 | 说明                    |
| ------ | ---- | ----------------------- |
| `ak`   | str  | Cordys CRM的 Access Key |
| `sk`   | str  | Cordys CRM的 Secret Key |

### 子应用介绍：

#### （1）Cordys 查重

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/cordys_duplicate_check.png">

#### （2）获取登录用户信息

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/get_logged_user_info.png">

#### （3）Cordys 循环补充线索

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/crm_loop_customer_relationship_supplement.png">

- 工作流：

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/crm_customer_entry_ai_agent.png">

## 四、应用效果

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/crm_customer_entry_ai_agent.gif">

## 五、注意事项

- 嵌套关系是`CRM 客户关系录入AI智能体`调用`Cordys 循环补充线索`和`Cordys 查重`，`Cordys 循环补充线索`调用`获取登录用户信息`
- 应当事先准备好Cordys CRM的 Access Key 和 Secret Key
- 应用会根据用户提供的Access Key 和 Secret Key，判断用户的身份信息。
- 