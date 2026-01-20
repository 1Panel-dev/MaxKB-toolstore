# HTML 转 PDF 工具

支持 HTML 快速转 PDF 工具，最终返回 pdf 下载地址。

## 1 部署服务

使用夸克网盘下载镜像：
链接：https://pan.quark.cn/s/b44c6edc2a07?pwd=pg8f
提取码：pg8f


```linux

# 解压文件
unzip html-to-pdf.zip

# 加载镜像
docker load < html-to-pdf.tar

# 启动
docker-compose -f docker-compose.yml up -d

```


## 2 参数说明

### 2.1 安装依赖
进到 maxkb 容器里，安装 requests 库即可

```linux

pip install requests
```

### 2.2 启动参数


| 参数名           | 类型 | 说明         |
| ---------------- | ---- | ------------ |
| `ip`             | str  | 服务器IP   |
| `port`           | str  | 端口 |
| `protocol`       | str  | 请求协议     |

#### 填写要求：

`ip`: 部署镜像服务的服务器IP。

`port`: 镜像服务的端口(默认是30060)。

`protocol`：请求协议(http或https)

### 2.3 输入参数

| 参数名         | 类型 | 说明                      |
| -------------- | ---- | ------------------------- |
| `html_content` | str  | 要转成 pdf 的 html 内容 |
| `pdf_name` | str  | 生成的pdf名称  |

## 3 注意事项

- **网络问题**： 确保 MaxKB 服务和 镜像服务网络连接正常
- **html格式**：若 html 里链接本地图片，将图片放到 /opt/test-pdf/convert_files/images 即可。
在 html 里格式 ```<img src="file:///tmp/convert_files/images/stream.png">```
