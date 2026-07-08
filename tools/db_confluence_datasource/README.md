# Confluence 数据源工具

## 简介

Confluence 数据源工具是一个专为 MaxKB 平台设计的数据源集成工具，用于从 Confluence 指定页面开始，递归获取该页面及其所有子页面，并导入到 MaxKB 知识库。

## 功能特性

- 适用于 **Confluence Server / Data Center**（REST API v1）。
- 以树形结构展示指定页面及其所有子孙页面，支持手动展开。
- 页面自动以 `storage` 格式获取后转为 Markdown。
- 无附件的页面直接返回 Markdown 文本；有附件的页面打包为 zip 包：`{title}.zip`，包内含 `{title}.md` 和 `assets/` 资源文件夹。
- 页面中的图片、视频、文件附件下载后放入 `assets/`，Markdown 中以 `./assets/文件名` 相对路径引用。

## 系统要求

- MaxKB 平台环境
- 可访问的 Confluence 实例
- 具备读取目标页面及其子页面权限的账号及 PAT

## 配置参数

| 参数名         | 类型   | 必填 | 说明                                                            |
| -------------- | ------ | ---- | --------------------------------------------------------------- |
| base_url       | String | 是   | Confluence 地址，例如 `https://confluence.demo.com`           |
| api_token      | String | 是   | Bearer Token（PAT/Token）                                       |
| parent_page_id | String | 是   | 根页面 ID，例如 `197788905`，作为同步的根页面                 |
| ssl_verify     | String | 是   | SSL 证书校验：`true` 或 `false`，自签名证书建议选 `false` |

### 准备 PAT

1. 在 Confluence 账号设置中生成个人访问令牌（PAT）。
2. `api_token` 填写 PAT。
3. 如果是内网自签名 HTTPS，`ssl_verify` 选择 `false`（跳过证书校验）。

### 选择根节点

- 填写 `parent_page_id`（例如 `197788905`）后，树形选择器会以该页面为根节点，可手动展开查看其子孙页面。

## 使用说明

1. 在 MaxKB 工具商店中添加本工具，并填写上述配置。
2. 进入知识库 → 数据源 → 选择 **Confluence 数据源**。
3. 树形选择器会以根页面为起点，点击节点可展开查看子页面，勾选需要导入的内容。
4. 确认后 MaxKB 会自动下载并解析内容。

## 支持的文件类型

| 类型           | 导出格式 | 说明                                     |
| -------------- | -------- | ---------------------------------------- |
| 页面（无附件） | `.md`  | 纯 Markdown 文本                         |
| 页面（有附件） | `.zip` | 含 `.md` 文档和 `assets/` 附件文件夹 |
