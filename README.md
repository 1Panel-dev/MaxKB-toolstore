# MaxKB Toolstore

MaxKB 工具商店 - 强大易用的开源企业级智能体平台工具集合

## 📖 项目简介

MaxKB Toolstore 是 MaxKB 智能体平台的官方工具商店，提供各类工具工具来扩展 MaxKB 的功能。通过这些工具，您可以轻松地为 MaxKB 添加联网搜索、数据库查询等能力。

## 🚀 现有工具

### 联网搜索类
- **秘塔AI搜索** - 强大的AI驱动搜索引擎，提供准确的联网搜索能力

### 数据库查询类  
- **MongoDB 查询** - 支持 MongoDB 4.x 以上版本的数据库查询操作

## 📁 项目结构

```
MaxKB-toolstore/
├── README.md             # 项目说明文档
├── tools/                # 模板目录(所有内容都放到此目录下面)
│   ├── tool_xxx_xxx/     # 工具命名规范，使用tool开头
│   │   ├── data.yaml     # 配置
│   │   ├── logo.png      # 图标
│   │   ├── README.md     # 说明
│   │   └── 1.0.0/        # 版本目录 
│   └── app_xxx/          # 智能体模板命名规范，使用app开头
│   │   ├── data.yaml     # 配置
│   │   ├── logo.png      # 图标
│   │   ├── README.md     # 说明
│   │   └── 1.0.0/        # 版本目录
│   └── db_xxx/           # 数据源命名规范，使用db开头
│   │   ├── data.yaml     # 配置
│   │   ├── logo.png      # 图标
│   │   ├── README.md     # 说明
│   │   └── 1.0.0/        # 版本目录
│   └── kbwf_xxx/         # 知识库工作流命名规范，使用kbwf开头
│   │   ├── data.yaml     # 配置
│   │   ├── logo.png      # 图标
│   │   ├── README.md     # 说明
│   │   └── 1.0.0/        # 版本目录
```
## 🛠️ 注意事项
1. 必须包含 data.yaml、logo.png、README.md 以及至少一个版本目录（如 1.0.0）。如果有多个版本，则需创建相应数量的版本目录，例如 1.0.0、1.0.1 等。
2. README.md 文件应详细描述工具信息，包括但不限于工具介绍、功能、使用说明、参数说明及调用示例。其中引用的所有图片或 GIF 需托管于公网地址上（例如 OSS 或网盘）以便正确显示。
3. 对于工具类模板，务必在 README.md 中明确记录输入输出参数及其调用方法；对于智能体类，若存在父子嵌套结构，需在 README.md 中清晰描述其调用关系，并确保被调用的子智能体文件也存储于公网地址（如 OSS 或网盘）。
4. 在 data.yaml 文件中：
   - name: 工具名称，例如“合同审核智能体”。
   - tags: 与 tools 下的 data.yaml 中保持一致，例如 ["智能体模板"]。可参考https://apps.fit2cloud.com/maxkb 分类标签，切勿写错字。
   - title: 在工具商店展示的简短描述，例如“用于审核合同内容并提供智能建议的应用。”
   - description: 导入到 MaxKB 的详细描述，可以与 title 相同。
```
name: 合同审核智能体
tags:
  - 智能体模板
title: 用于审核合同内容并提供智能建议的应用。
description: 用于审核合同内容并提供智能建议的应用。
```
[详细说明文档](https://my.feishu.cn/wiki/J8M0w8N6jiPm4akwrpQcdjCCnCg)
## 🔧 如何使用

1. 在 MaxKB 平台中访问工具商店
2. 浏览并选择所需的工具
3. 点击安装并按照说明进行配置
4. 开始使用扩展功能

## 🤝 贡献指南

如果您想为 MaxKB Toolstore 贡献新的工具，请参考：
[如何提交自己想要的工具](./如何提交工具.md)

### 工具开发规范

- 每个工具需要包含 `data.yaml` 配置文件
- 提供清晰的工具说明文档
- 包含适当的图标和版本管理
- 遵循 MaxKB 平台的开发规范


## 📞 联系我们

- 项目地址：https://github.com/1panel-dev/MaxKB-toolstore
- 问题反馈：请在 GitHub Issues 中提交
- 文档支持：参考 MaxKB 官方文档

