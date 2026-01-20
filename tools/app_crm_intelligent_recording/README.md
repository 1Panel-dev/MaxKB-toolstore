# CRM 智能记录智能体

## 一、应用描述

本应用专为 Cordys CRM 系统用户设计，依托 AI 自然语言交互能力，简化线索、商机跟进记录的录入流程。用户无需手动操作系统表单，仅需用自然语言描述待录入信息，AI 智能体便会主动引导补充必填项、校验信息规范性，生成标准化数据并同步至 Cordys CRM 系统，大幅提升信息录入效率与准确性，降低系统操作门槛，适配销售、客服等岗位快速建档的业务需求。

## 二、应用功能

CRM 智能记录智能体应用主要包含以下几个大功能：
- 线索跟进记录录入：用户通过自然语言与 AI 智能体对话，告知跟进相关信息，智能体将引导用户补充完整必填项，校验信息合规性后生成标准化数据，再调用 Cordys CRM MCP 工具，将已确认的 JSON 信息精准写入 Cordys CRM 系统，实现线索跟进记录的快速录入。
- 商机跟进记录录入：支持用户以自然语言描述客户的跟进基础信息，AI智能体逐一向用户确认缺失的必填内容，整合形成规范的数据并生成 JSON 格式文件，经用户最终确认后，调用 Cordys CRM MCP 工具完成客户跟进记录向系统的写入操作。

## 三、应用构建要素

CRM 智能记录智能体应用构建时涉及的核心要素内容：
- 大模型：deepseek-chat
- MCP ：Cordys CRM MCP: https://cordys.cn/docs/mcp_server/#41-maxkb
- 工具：提取AI内容里面的json
- 子应用：Cordys 查重、获取登录用户信息 

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

- 工作流：

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/intelligent_recording.png">

## 四、应用效果

<img src="https://maxkb-apps-1323865188.cos.ap-shanghai.myqcloud.com/intelligent_recording.gif">

## 五、注意事项

- 嵌套关系明确：`CRM 智能记录智能体` 调用 `Cordys 查重` 与 `获取登录用户信息` 子应用
- 身份校验规则：应用通过用户提供的 ak 和 sk 校验身份权限，保障系统数据安全性与合规性。
- 信息合规提示：录入的跟进信息需真实有效，避免填写虚假数据，同时需遵守企业客户信息保密制度，严禁泄露敏感信息。