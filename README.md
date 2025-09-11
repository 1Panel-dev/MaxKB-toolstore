# MaxKB Appstore

MaxKB 应用商店 - 强大易用的开源企业级智能体平台应用集合

## 📖 项目简介

MaxKB Appstore 是 MaxKB 智能体平台的官方应用商店，提供各类工具应用来扩展 MaxKB 的功能。通过这些应用，您可以轻松地为 MaxKB 添加联网搜索、数据库查询等能力。

## 🚀 现有应用

### 联网搜索类
- **秘塔AI搜索** - 强大的AI驱动搜索引擎，提供准确的联网搜索能力

### 数据库查询类  
- **MongoDB 查询** - 支持 MongoDB 4.x 以上版本的数据库查询操作

## 📁 项目结构

```
MaxKB-appstore/
├── README.md              # 项目说明文档
├── apps/                  # 应用目录
│   ├── data.yaml         # 应用商店配置
│   ├── logo.png          # 商店图标
│   ├── metaso/           # 秘塔AI搜索应用
│   │   ├── data.yaml     # 应用配置
│   │   ├── logo.png      # 应用图标
│   │   ├── README.md     # 应用说明
│   │   └── 1.0.0/        # 版本目录
│   └── mongo/            # MongoDB查询应用
│       ├── data.yaml     # 应用配置
│       ├── logo.png      # 应用图标
│       ├── README.md     # 应用说明
│       ├── requirements.txt # 依赖文件
│       └── 1.0.0/        # 版本目录
```

## 🔧 如何使用

1. 在 MaxKB 平台中访问应用商店
2. 浏览并选择所需的应用
3. 点击安装并按照说明进行配置
4. 开始使用扩展功能

## 🤝 贡献指南

如果您想为 MaxKB Appstore 贡献新的应用，请参考：
[如何提交自己想要的应用](./如何提交应用.md)

### 应用开发规范

- 每个应用需要包含 `data.yaml` 配置文件
- 提供清晰的应用说明文档
- 包含适当的图标和版本管理
- 遵循 MaxKB 平台的开发规范


## 📞 联系我们

- 项目地址：https://github.com/1panel-dev/MaxKB-appstore
- 问题反馈：请在 GitHub Issues 中提交
- 文档支持：参考 MaxKB 官方文档

