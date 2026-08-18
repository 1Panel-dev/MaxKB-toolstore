## 2.3.0 版本说明

**注意**: 当前适用的 MaxKB 版本为 v2.10.4-lts 及以上版本

- 适配 MinerU 3.4.4

## MinerU 离线 PDF 转换 Markdown 工具

**注意**: 离线的 mineru 使用版本为 3.4.4

启动参数
 - MaxKB 基础地址前缀： MaxKB 的访问地址 (https://maxkb访问地址/admin)
 - 本地 MinerU Gradio 地址：本地 minerU_Gradio 访问地址(http://minerU_Gradio访问地址:7860/)
 - 上传 Token：用于 MaxKB OSS 接口鉴权的 Token(user-74xxx)
 - 解析引擎：MinerU 的处理引擎模式(pipeline、hybrid-auto-engine、vlm-auto-engine等)
 - 知识库id：当前工作流知识库的id
 - 用户名：MaxKB 登录用户名
 - 密码：MaxKB 登录密码

输入参数:
 - file_input：MaxKB 传入的文件列表

输出结果:
 - 列表({"id":"文件id","name":"文件名字","content":"提取的 markdown 结果"})
