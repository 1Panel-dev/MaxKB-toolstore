# Mem0 记忆

基于本地部署的 Mem0 REST API Server，对其进行添加记忆、检索记忆、获取记忆、更新记忆、重置记忆、删除记忆。

## 一、环境准备

### 1 本地部署 Mem0 REST API Server

**注意:** 基于 mem0-1.0.3 版本源码部署，在 main.py 里默认使用的是 OpenAI 模型且 update_memory 接口的参数 updated_memory 要求 Dict 类型，但实际需要的是 str 类型。基于此问题，将 main.py 文件里修改大语言模型为 vllm，向量模型为 ollama 且 update_memory 接口的入参也修改为 str，以此打成压缩包放至网盘里，需要的自取。

Mem0 REST API Server 服务下载地址：
链接：https://pan.quark.cn/s/9fc0a0232049
提取码：QqXa

```linux
# 解压文件
unzip mem0.zip
tar -xvf server.tar

# 修改模型配置
在 main.py 中指定，服务启动所需的数据库配置、模型配置，目前提供的服务，默认使用的是大语言模型为 vllm，向量模型为 ollama。

# 创建环境配置文件
cd ~/server
touch .env

# 启动服务
cd ~/server
docker-compose -f docker-compose.yaml up -d

# 执行 docker ps -a，可看到 mem0-dev-mem0-1，mem0-dev-postgres-1 以及 mem0-dev-neo4j-1 服务都正常启动，

# 访问 ：http://服务器IP:8888/docs#/，即可打开 Mem0 REST API 页面
```

## 二、工具说明

### 2.1 启动参数

| 参数 | 组件类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `url` | 文本框 | 是 | Mem0 服务地址 |
| `mem_type` | 单选框 | 是 | 记忆类型 |

### 2.2 输入参数

#### 2.2.1 添加记忆

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `user_content` | string | 是 | 引用参数 | 用户发送的消息内容 |
| `assistant_content` | string | 是 | 引用参数 | AI 助手回复的消息内容 |

#### 2.2.2 检索记忆

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `query` | string | 是 | 引用参数 | 用户检索的消息内容 |

#### 2.2.3 获取记忆

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |

#### 2.2.4 获取某个记忆

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `memory_id` | string | 是 | 引用参数 | 单条记忆的唯一标识 |

#### 2.2.5 更新记忆

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `memory_id` | string | 否 | 引用参数 | 单条记忆的唯一标识 |
| `updated_memory` | string | 是 | 引用参数 | 更新内容 |

#### 2.2.6 获取记忆历史

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `memory_id` | string | 是 | 引用参数 | 单条记忆的唯一标识 |

#### 2.2.7 重置记忆

| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `memory_id` | string | 否 | 引用参数 | 单条记忆的唯一标识 |

#### 2.2.8 删除记忆
| 参数名 | 数据类型 | 必填 | 来源 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | string | 是 | 引用参数 | 用户唯一标识符 |
| `agent_id` | string | 否 | 引用参数 |  应用唯一标识 |
| `memory_id` | string | 否 | 引用参数 | 单条记忆的唯一标识 |

