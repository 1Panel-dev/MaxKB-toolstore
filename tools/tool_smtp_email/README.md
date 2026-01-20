# SMTP 邮件通知工具

基于 Python `smtplib` 和 `email` 库封装的邮件通知工具函数，支持发送文本邮件、添加收件人和抄送人、支持 SSL/TLS 加密，适用于告警通知、自动化运维、业务消息推送等场景。

## 一、项目介绍

### 1.1 核心功能

- **文本邮件发送**：通过 SMTP 协议发送自定义文本邮件，支持多行文本和特殊字符。
- **收件人和抄送人支持**：支持指定多个收件人和抄送人，确保消息触达相关人员。
- **SSL/TLS 加密支持**：支持通过 SSL 或 TLS 协议加密邮件传输，确保通信安全。
- **智能错误处理**：捕获 SMTP 服务器连接失败、认证错误、收件人无效等异常，输出清晰的错误提示。
- **简洁接口设计**：通过单一函数整合 SMTP 配置和邮件发送，降低集成成本。

### 1.2 适用场景

- **系统告警通知**：服务器异常、接口报错、磁盘空间不足等告警信息通过邮件实时通知。
- **自动化运维**：定时任务执行结果、脚本运行日志、数据备份状态等通知。
- **业务消息提醒**：订单状态变更、用户注册通知、数据统计报表等业务消息推送。
- **CI/CD 集成**：构建成功/失败通知、部署进度提醒、代码审查消息等。
- **日报周报推送**：定时发送团队工作总结、数据分析报告等。

---

## 二、环境准备

### 2.1 依赖库

该工具基于 Python 标准库构建，无需额外安装第三方库。

### 2.2 SMTP 配置准备

使用前需获取 SMTP 服务器相关配置信息：

1. **获取 SMTP 配置**：
    - 确定 SMTP 服务器的 `host` 和 `port`（常见 SMTP 服务器配置如下）：
        - Gmail: `smtp.gmail.com`, Port: 587 (TLS) 或 465 (SSL)
        - Outlook: `smtp-mail.outlook.com`, Port: 587 (TLS)
        - QQ 邮箱: `smtp.qq.com`, Port: 465 (SSL) 或 587 (TLS)
    - 获取发送账户的邮箱地址和密码（或应用专用密码）。
    - 确认是否使用 SSL 或 TLS 加密。

2. **启用 SMTP 服务**：
    - 对于 Gmail、QQ 邮箱等服务，需在账户设置中启用 SMTP 服务并生成应用专用密码：
        - Gmail: 开启“两步验证”后生成“应用专用密码”。
        - QQ 邮箱: 在“设置” → “账户” → “POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务”中启用 SMTP 并生成授权码。
    - 参考各邮箱服务商的官方文档。

3. **安全配置**（推荐）：
    - 使用应用专用密码而非账户主密码。
    - 配置防火墙以允许 SMTP 端口（465 或 587）访问。

> **注意**：SMTP 服务器可能有发送频率限制（如 Gmail 每日 500 封），建议控制发送频率以避免被限制。

---

## 三、使用说明

### 3.1 函数定义

```python
def smtp_email(host, port, username, password, use_ssl, use_tls, subject, message, recipients, cc_recipients):
    """
    SMTP 邮件通知方法，支持发送文本邮件，包含收件人和抄送人。
 
    Args:
        host (str): SMTP 服务器地址
        port (int): SMTP 服务器端口
        username (str): 发送者邮箱账户
        password (str): 发送者邮箱密码或应用专用密码
        use_ssl (bool): 是否使用 SSL 加密
        use_tls (bool): 是否使用 TLS 加密
        subject (str): 邮件主题
        message (str): 邮件正文内容
        recipients (str): 逗号分隔的收件人邮箱地址
        cc_recipients (str, optional): 逗号分隔的抄送人邮箱地址，默认为空
 
    Returns:
        str: 邮件发送结果状态信息
    """
```

---

### 3.2 参数说明

#### 必需参数

| 参数名         | 类型 | 说明                                   | 示例                                       |
| :------------- | :--- | :------------------------------------- | :----------------------------------------- |
| `host`         | str  | SMTP 服务器地址                       | `'smtp.gmail.com'`                        |
| `port`         | int  | SMTP 服务器端口                       | `587` (TLS) 或 `465` (SSL)                |
| `username`     | str  | 发送者邮箱账户                       | `'user@gmail.com'`                        |
| `password`     | str  | 发送者邮箱密码或应用专用密码          | `'your_app_specific_password'`            |
| `use_ssl`      | bool | 是否使用 SSL 加密                    | `True` 或 `False`                         |
| `use_tls`      | bool | 是否使用 TLS 加密                    | `True` 或 `False`                         |
| `subject`      | str  | 邮件主题                             | `'服务器告警通知'`                        |
| `message`      | str  | 邮件正文内容                         | `'服务器 CPU 使用率超过 80%'`             |
| `recipients`   | str  | 逗号分隔的收件人邮箱地址             | `'recipient1@example.com,recipient2@example.com'` |

#### 可选参数

| 参数名         | 类型 | 默认值 | 说明                                   |
| :------------- | :--- | :----- | :------------------------------------- |
| `cc_recipients`| str  | `''`   | 逗号分隔的抄送人邮箱地址              |

#### 参数组合说明

- **SSL/TLS 配置**：
    - 如果 `use_ssl=True`，使用 SSL 连接（通常端口为 465）。
    - 如果 `use_tls=True`，使用 TLS 连接（通常端口为 587）。
    - 如果两者均为 `False`，使用非加密连接（不推荐）。
    - **注意**：`use_ssl` 和 `use_tls` 不可同时为 `True`。

- **收件人和抄送人**：
    - `recipients` 必须包含至少一个有效邮箱地址。
    - `cc_recipients` 可为空，表示无抄送人。
    - 邮箱地址需为有效格式（如 `user@example.com`）。

---