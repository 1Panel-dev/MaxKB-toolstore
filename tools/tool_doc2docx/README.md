# Word 文档转 DOCX 工具

## 工具介绍

`zlb-doc转docx` 用于将 MaxKB 中引用的 Word 97-2003 文档（`.doc`）转换为 Office Open XML 文档（`.docx`），并将转换结果上传至 MaxKB 临时对象存储。工具最终返回可在 MaxKB 页面中打开或下载的文件链接。

该工具适用于需要将旧版 Word 文档统一转换为 `.docx` 后，再交由智能体、知识库工作流或其他业务流程继续处理的场景。

## 功能

- 接收 MaxKB 文件引用列表中的首个文档。
- 根据文件引用地址下载源文件。
- 将 `.doc` 文件调用转换服务转换为 `.docx` 文件。
- `.docx` 文件无需转换，直接上传。
- 将结果上传为有效期 120 分钟的 MaxKB 临时文件。
- 返回带有文件名的 HTML 跳转链接，供页面展示和下载。

## 使用说明

1. 在 MaxKB 工作流或智能体编排中添加该自定义工具。
2. 将上游文件上传节点或文件选择节点的输出映射到 `doc_list`。
3. 为 `auth_token` 配置当前 MaxKB 环境可用的认证令牌。
4. 执行工具后，在输出中获取 `.docx` 文件链接，并将其传给后续节点或直接展示给用户。

## 参数说明

### 输入参数

| 参数名 | 类型 | 必填 | 来源 | 说明 |
| --- | --- | --- | --- | --- |
| `doc_list` | `array` | 是 | `reference` | MaxKB 文件引用列表。工具仅处理列表中的第一个文件对象。 |
| `auth_token` | `string` | 是 | `custom` | 当前 MaxKB 环境的认证令牌，用于下载源文件并上传转换结果。 |

#### `doc_list` 文件对象

| 字段名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | `string` | 是 | 源文件名称，例如 `合同模板.doc`。支持 `.doc` 或 `.docx` 文件。 |
| `url` | `string` | 是 | MaxKB 返回的文件相对地址，例如 `./api/oss/file/xxxx`。 |

### 输出参数

| 输出类型 | 说明 |
| --- | --- |
| `string` | 成功时返回 MaxKB 可识别的 HTML 渲染片段，其中包含 `.docx` 文件链接；失败时返回描述下载、转换或上传失败原因的错误字符串。 |

成功结果示例：

```html
<html_rander><a href=" " onclick='jump("https://edu-maxkb2.fit2cloud.cn/admin/api/oss/file/xxxx")'>合同模板.docx</a></html_rander>
```

## 调用方法

工具入口函数为 `process_documents(doc_list, auth_token)`。

1. 工具从 `doc_list` 取得第一个文件的 `name` 和 `url`。
2. 使用 `auth_token` 下载源文件。
3. 当输入为 `.doc` 时，调用 `doc-to-docx` 转换接口；输入为 `.docx` 时跳过转换。
4. 将最终的 `.docx` 文件上传到 MaxKB 临时对象存储。
5. 返回跳转至上传文件的 HTML 链接。

## 调用示例

### MaxKB 节点输入

```json
{
  "doc_list": [
    {
      "name": "合同模板.doc",
      "url": "./api/oss/file/temporary/contract-template.doc"
    }
  ],
  "auth_token": "<MAXKB_AUTH_TOKEN>"
}
```

### Python 调用

```python
result = process_documents(
    doc_list=[
        {
            "name": "合同模板.doc",
            "url": "./api/oss/file/temporary/contract-template.doc"
        }
    ],
    auth_token="<MAXKB_AUTH_TOKEN>"
)
```

## 注意事项

- 工具仅处理 `doc_list` 中的第一个文件；批量转换应在工作流中逐个调用。
- 源文件应为可正常下载的 `.doc` 或 `.docx` 文件，且文件引用 URL 不可为空。
- 转换服务地址、MaxKB 基础地址和认证令牌需与实际部署环境保持一致。
- 上传结果使用 `TEMPORARY_120_MINUTE` 临时存储策略，链接有效期为 120 分钟；需要长期保存时，应改用持久化存储策略。
- 请勿在工具代码、README 或工作流配置中明文提交有效的认证令牌。
- 本文档未引用图片或 GIF。后续如添加图片或 GIF，必须使用 OSS、网盘或其他公网可访问地址，避免使用本地文件路径。
