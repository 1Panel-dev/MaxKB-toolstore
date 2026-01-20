# ECharts 图表 HTML 转 SVG 工具

支持 ECharts 图表 HTML 转 SVG 工具，最终可以在浏览器上访问 SVG 图。

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
| `echart_html` | str  | ehcart图的html  |

## 3 注意事项

- **网络问题**： 确保 MaxKB 服务和 镜像服务网络连接正常
- **html格式**：ECharts 图表 HTML 格式请参考 https://pan.quark.cn/s/3d69a9bb4ea6?pwd=x6Bc
- **内网环境**：无法访问在线的 echart.min.js，将 echart.min.js 放到 /opt/test-pdf/echart_files 即可
