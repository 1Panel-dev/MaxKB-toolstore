# OFD 文件提取

针对原生 OFD 文件，提取相关文件内容，并以 json 格式返回，扫描版 OFD 暂时还不支持。

说明：原生 OFD，即将 OFD 文件解压后，Pages 目录下的 Content.xml 基本都是 TextObject 
元素来表示内容，否则如果没有 TextObject，而是使用 ImageObject元素，则表示是扫描版 OFD。

## 智能体设计样例

## 参数说明

### 启动参数    

启动参数需要根据环境自行输入。

| 参数名称 | 参数类型   | 参数说明 | 默认值 |
| -------- |--------| -------- | ------ |
| `base_url` | string | MaxKB 地址 | `https://<MaxKB_URL>/PORT` |


### 输入参数    
| 参数名称 | 参数类型 | 参数说明                                 | 默认值 |
| -------- |------|--------------------------------------| ------ |
| `file_info` | dict | MaxKB 工作流应用中开其他文件（{{开始.other}}）的一个元素 | |

说明：可以使用循环体来对上传的多个 OFD 文件进行提取。


## 返回说明
返回 json,样式如下： 
{
    "file_name": "xxxx.ofd",
    "document_custom_datas": [
        {
          "Name": "xxxx",
          "Content": "xxx"
        },
    ]
    "pages": [
        {
            "page_id": "Page_0",
            "text_content": "text_content"	
        }	
    ]
}

