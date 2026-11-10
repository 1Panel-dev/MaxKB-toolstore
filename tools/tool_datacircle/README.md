## Datacircle GTM API 评测

**Author:** Datacircle
**Version:** 2.0.0
**Type:** tool
**Website:** https://datacircle.dev

## Introduction

Find the best GTM APIs. We benchmark all the GTM APIs and we put the results on our website, https://datacircle.dev.

This tool calls our API, free and open, with no key: list every API, see who is best for each and search every plan, at https://api.datacircle.dev/v1 (its spec: https://api.datacircle.dev/v1/openapi.json). Each plan comes with its score out of 100, and the best come first, as on the sheet.

## Setup

None: no key, no account. Add the tool from the Tool Store and enable it. At most 60 calls a minute from one address.

## Parameters

| Name | Type | Required | Meaning |
|---|---|---|---|
| `action` | string | yes | `apis`, `best` (the default), `plans` or `provider` |
| `api` | string | for `best` | the API's slug, as `apis` lists them, e.g. `email-finder`, `linkedin-profile`; for `plans`, the API to search in |
| `query` | string | no | for `plans`: words that must all appear in the provider's or the plan's name, e.g. `hunter` |
| `provider` | string | for `provider` | the provider's slug: its name in lowercase, e.g. `hunter`, `apollo` |
| `limit` | int | no | how many plans to give, 1 to 50; 5 when left out |

## Actions and the calls they make

| `action` | Call | Answer |
|---|---|---|
| `apis` | `GET /apis` | every API on our sheet: its slug, how many plans and providers, its best plan and its pages |
| `best` | `GET /apis/{api}/best` | who is best for one API: its top plans, best first |
| `plans` | `GET /plans` | plans by API, provider or plan name, best first |
| `provider` | `GET /providers/{provider}` | one provider on every API: its rank on each and its top plans |

Each plan in the answer: `provider`, `plan`, `api`, `call`, `score`, `rank`, `perThousand` (what 1,000 results cost, in USD), `notFoundPerThousand`, `monthlyFee`, `billing`, `page` (its page on datacircle.dev), `pricingPage` and `docs`. An unknown slug answers its error, with the slugs there are.

## 中文说明

找到最好的 GTM API。我们对所有 GTM API 做基准测试，并把结果放在我们的网站 https://datacircle.dev 上。

本工具调用我们免费开放的 API（https://api.datacircle.dev/v1），无需 Key，无需注册：

1. 在 MaxKB 工具商店添加本工具，启用即可。每个地址每分钟最多 60 次调用。
2. 参数：`action`（`apis` 列出每个 API；`best` 默认，某个 API 谁最好；`plans` 按 API、服务商或套餐名搜索套餐；`provider` 某个服务商在每个 API 上的排名与套餐）；`api`（API 的 slug，如 `email-finder`）；`query`（服务商或套餐名中的词）；`provider`（服务商的 slug，如 `hunter`）；`limit`（返回几个套餐，1 到 50，默认 5）。
3. 每个套餐都带有得分（满分 100）与每 1,000 条结果的价格（美元），最好的排在前面，与 https://datacircle.dev 上的表格一致。

## Links

- Website: https://datacircle.dev
- API: https://api.datacircle.dev/v1
- Spec: https://api.datacircle.dev/v1/openapi.json
