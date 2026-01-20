# 大单网招标信息查询API文档

## 功能介绍

该API用于查询大单网（dadan.vip）上的招标采购信息。通过指定关键词、地区、时间范围、金额等条件，可以精确检索相关的招标公告、中标公告等信息。

此接口支持多种筛选条件：
- 关键词搜索与排除词过滤
- 地区筛选（省、市、区县）
- 时间范围限定
- 金额区间筛选
- 单位信息筛选
- 公告类型筛选
- 分页查询

## 参数说明

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| api_token | str | 是 | API认证令牌 |
| keywords | List[str] | 是 | 搜索关键词列表 |
| exclude_words | Optional[List[str]] | 否 | 排除关键词列表 |
| provinces | Optional[List[str]] | 否 | 省份列表 |
| cities | Optional[List[str]] | 否 | 城市列表 |
| districts | Optional[List[str]] | 否 | 区县列表 |
| start_date | Optional[str] | 否 | 开始日期 (格式: yyyy-MM-dd) |
| end_date | Optional[str] | 否 | 结束日期 (格式: yyyy-MM-dd) |
| min_amount | Optional[float] | 否 | 最小金额 |
| max_amount | Optional[float] | 否 | 最大金额 |
| channels | Optional[List[int]] | 否 | 公告类型ID列表 |
| tenderee | Optional[str] | 否 | 招标单位 |
| win_tenderer | Optional[str] | 否 | 中标单位 |
| agency | Optional[str] | 否 | 代理单位 |
| page_no | int | 否 | 页码，默认为1 |
| page_size | int | 否 | 每页大小，默认为20 |

### 公告类型(channels)参考值：

- 101: 招标公告
- 118: 中标候选人公示
- 119: 中标结果公告
- 120: 废标公告
- 121: 流标公告
- 122: 更正公告
- 102: 采购公告
- 51: 成交公告
- 103: 邀请公告
- 105: 竞争性谈判公告
- 104: 询价公告
- 115: 单一来源采购公示
- 116: 资格预审公告
- 117: 其他公告
- 52: 结果公告
- 303: 合同公示

## 返回值说明

返回一个包含查询结果的字典对象，主要字段包括：

- data: 查询到的数据列表
- `total`: 总记录数
- `pageNo`: 当前页码
- `pageSize`: 每页大小
- `success`: 请求是否成功标识

每个数据项通常包含以下信息：
- 标题(title)
- 公告类型(channel)
- 发布时间(publishTime)
- 项目金额(projectAmount)
- 招标单位(tenderee)
- 中标单位(winTenderer)
- 代理机构(agency)
- 详情链接(url)

## 调用示例

### Python调用示例
基本查询示例
```python

from typing import List, Dict, Any import http.client import json
response = query_big_orders( api_token="your_api_token_here", keywords=["服务器", "采购"], provinces=["广东省"], cities=["深圳市"], start_date="2024-01-01", end_date="2024-12-31", min_amount=100000.0, max_amount=1000000.0, channels=[101, 119], # 招标公告和中标结果公告 page_no=1, page_size=20 )
print(json.dumps(response, ensure_ascii=False, indent=2))
```
### 使用排除词示例
使用排除词过滤不相关的结果
```python
response = query_big_orders( api_token="your_api_token_here", keywords=["软件开发"], exclude_words=["维护", "运维"], provinces=["北京市", "上海市"], channels=[101] )

```
### 按单位查询示例
根据特定招标单位或中标单位查询

```python
response = query_big_orders( api_token="your_api_token_here", keywords=["信息化"], tenderee="中国电信", win_tenderer="华为技术有限公司" )
```
## 注意事项说明

1. **API权限**：使用此API需要有效的api_token，请确保token未过期且具有相应权限。

2. **时间范围**：如果未指定start_date和end_date，系统默认查询最近三个月的数据。

3. **分页机制**：默认每页显示20条记录，可通过page_no和page_size参数控制分页。

4. **地区筛选**：地区筛选支持省、市、区三级筛选，可单独使用也可组合使用。

5. **关键词逻辑**：多个关键词之间是"与"的关系，即必须同时满足所有关键词条件。

6. **错误处理**：当请求发生异常时，函数会返回包含错误信息的字典，包含`error: True`和`message`字段。

7. **编码问题**：请求体已正确处理中文字符编码，确保中文参数能正常传递。

8. **请求限制**：请注意API可能存在的访问频率限制，避免短时间内大量请求。

9. **数据时效性**：API返回的数据更新可能存在一定延迟，请以官方平台为准。

10. **安全提醒**：在生产环境中，请妥善保管您的api_token，避免泄露。
