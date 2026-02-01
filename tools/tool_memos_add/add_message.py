import requests


def add_message(user_id: str, conversation_id: str, user_message: str, assistant_message: str, access_key: str = ""):
    """
    MemOS 消息添加

    参数类型（根据官方API文档）：
    - user_id: string, 必填, 消息关联的用户唯一标识符
    - conversation_id: string, 必填, 消息关联的会话唯一标识符
    - user_message: string, 必填, 用户消息内容（对应 messages[].content）
    - assistant_message: string, 必填, 助手消息内容（对应 messages[].content）
    - access_key: string, 必填, API密钥

    原始API messages数组字段：
    - role: string, 必填, 消息角色（user/assistant/system/tool）
    - content: string, 必填, 消息内容文本
    - chat_time: string, 可选, 对话时间
    """
    http_session = requests.Session()
    try:
        messages = []
        if user_message:
            messages.append({"role": "user", "content": user_message})
        if assistant_message:
            messages.append({"role": "assistant", "content": assistant_message})

        if not messages:
            return "错误：消息内容不能为空"

        data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": messages
        }

        rep = http_session.post(
            url="https://memos.memtensor.cn/api/openmem/v1/add/message",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {access_key}"
            },
            json=data
        ).json()

        if rep.get("code") == 0:
            task_id = rep.get("data", {}).get("task_id", "")
            return f"信息：消息添加成功，任务ID: {task_id}"
        else:
            return f"错误：消息添加失败：{rep.get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"错误：添加消息时发生网络错误: {e}"
    except Exception as e:
        return f"错误：处理消息添加响应时发生错误: {e}"
