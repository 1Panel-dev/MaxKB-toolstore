## datacircle_linkedin_profile

**Author:** Datacircle
**Version:** 1.0.0
**Type:** tool

## Introduction

Datacircle is a data co-op. Query your favorite B2B data APIs through us. Same request, same price, no markup. Every morning, you get the flat file of your data plus everyone else's.

This tool looks up a LinkedIn profile by its URL through us. Each request goes to the provider and gets the profile as it is today.

Right now we have 3 live LinkedIn profile APIs that we trust: Up2Data, HarvestAPI and Fetchin.

## Offer

Sign up at datacircle.dev with your work email: a $5 credit, that's 2,105 LinkedIn profiles at $2.375 per 1,000.

## Setup

1. Log in at [datacircle.dev/login](https://datacircle.dev/login) with your work email. Your API key is on the page once you're in.
2. In MaxKB, add this tool from the Tool Store, paste the key into **API Key**, and enable it.

## Parameters

| Name | Required | Meaning |
|---|---|---|
| `linkedin_url` | yes | the profile's LinkedIn URL, e.g. `https://www.linkedin.com/in/williamhgates` |
| `provider` | no | `up2data` (the default), `harvestapi` or `fetchin` |

The answer is the provider's own JSON, plus `datacircle_meta`: `cost_usd` (what this call cost) and `balance_usd` (what you have left). A call your balance can't cover answers 402. Add funds, from $5, on your dashboard.

## Prices

$2.375 per 1,000 through Up2Data (a profile it can't find is free), $3.70 per 1,000 through HarvestAPI.
$1.485 per 1,000 through Fetchin, a profile it can't find billed the same.

Today's prices: [docs.datacircle.dev/pricing](https://docs.datacircle.dev/pricing).

## 中文说明

Datacircle 是一个数据合作社。通过我们调用你常用的 B2B 数据 API：同样的请求，同样的价格，零加价。本工具按 URL 实时查询领英（LinkedIn）个人档案，经 Up2Data（默认）、HarvestAPI 或 Fetchin。

1. 在 [datacircle.dev/login](https://datacircle.dev/login) 用工作邮箱登录，页面上即有 API Key（注册赠送 $5 额度，即 2,105 条领英档案，每 1,000 条 $2.375）。
2. 在 MaxKB 工具商店添加本工具，在 **API Key** 中填入，启用即可。
3. 参数：`linkedin_url`（必填，领英个人档案 URL）；`provider`（选填，`up2data` 默认，`harvestapi` 或 `fetchin`）。

## Links

- Docs: https://docs.datacircle.dev
- Website: https://datacircle.dev
- Contact: wayne@datacircle.dev
