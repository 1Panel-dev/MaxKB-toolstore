# OfficeCLI 技能

让 AI 智能体完全掌控 Word、Excel 和 PowerPoint——只需一行命令。OfficeCLI 是全球首个专为 AI 智能体设计的 Office 套件，开源免费，单一可执行文件，无需安装 Office，全平台运行。

开源地址：[https://github.com/iOfficeAI/OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)

## 一、功能说明

**OfficeCLI 能做什么：**

- **创建** 文档 -- 空白文档或带内容的文档
- **读取** 文本、结构、样式、公式 -- 纯文本或结构化 JSON
- **分析** 格式问题、样式不一致和结构缺陷
- **修改** 任意元素 -- 文本、字体、颜色、布局、公式、图表、图片
- **重组** 内容 -- 添加、删除、移动、复制跨文档元素

| 格式 | 读取 | 修改 | 创建 |
|------|------|------|------|
| Word (.docx) | ✅ | ✅ | ✅ |
| Excel (.xlsx) | ✅ | ✅ | ✅ |
| PowerPoint (.pptx) | ✅ | ✅ | ✅ |

**Word** — i18n 与 RTL 支持（按脚本字体槽位、按脚本 BCP-47 语言标签 `lang.latin/ea/cs`、复杂脚本粗体/斜体/字号、`direction=rtl` 在段落/文本片段/节/表格/样式/页眉/页脚/docDefaults 间级联、`rtlGutter` + `pgBorders` 简写、印地语/阿拉伯语/泰语/中日韩本地化页码）、段落、文本片段、表格、样式、页眉/页脚、图片（PNG/JPG/GIF/SVG）、公式、批注、脚注、水印、书签、目录、图表、超链接、节、表单域、内容控件 (SDT)、域（22 种零参数 + MERGEFIELD / REF / PAGEREF / SEQ / STYLEREF / DOCPROPERTY / IF）、OLE 对象、文档属性

**Excel** — 单元格（添加时支持音标/振假名）、公式（内置 350+ 函数自动求值，可溢出的动态数组自动加 `_xlfn.` 前缀，含财务/债券与统计函数族）、工作表（visible/hidden/veryHidden、打印边距、printTitleRows/Cols、RTL `sheetView`、级联感知的工作表重命名）、表格、排序（工作表/区域、多键、附属感知）、条件格式、图表（含箱线图、帕累托图自动排序 + 累计百分比、对数轴）、数据透视表（多字段、日期分组、showDataAs、排序、总计、分类汇总、紧凑/大纲/表格布局、重复项目标签、空白行、计算字段）、切片器、命名范围、数据验证、图片（PNG/JPG/GIF/SVG，双重表示回退）、迷你图、批注（RTL）、自动筛选、形状、OLE 对象、CSV/TSV 导入、`$Sheet:A1` 单元格寻址

**PowerPoint** — 幻灯片（页眉/页脚/日期/页码切换、隐藏）、形状（图案填充、模糊效果、超链接提示 + 跳转幻灯片链接）、图片（PNG/JPG/GIF/SVG，填充模式：stretch/contain/cover/tile，亮度/对比度/发光/阴影）、表格、图表、动画、morph 过渡、3D 模型（.glb）、幻灯片缩放、公式、主题、连接线、视频/音频、组合、备注（RTL、lang）、批注（RTL）、OLE 对象、占位符（按 phType 添加/设置）

## 二、工作流程

1. **初始化**：运行初始化脚本清理残留文件，如有附件则下载到临时目录
2. **操作文档**：打开文档 → 读取/修改/分析 → 关闭文档
3. **交付**：运行交付脚本获取下载链接

## 三、参数说明

| 参数 | 说明 | 用途 |
|------|------|------|
| `BASE_URL` | MaxKB API 服务地址 | 指定 MaxKB 后端服务地址 |
| `API_KEY` | API 认证密钥 | 用于 API 调用鉴权 |

## 四、注意事项

以下环境变量必须设置，否则功能无法正常运行：

| 环境变量 | 值 | 说明 |
|----------|-----|------|
| `MAXKB_SANDBOX_TMP_DIR_ENABLED` | `1` | 启用临时目录沙箱，允许 `/tmp` 读写 |
| `MAXKB_SANDBOX_PYTHON_ALLOW_SUBPROCESS` | `1` | 允许 Python 脚本调用 officecli 子进程 |
| `MAXKB_LANGCHAIN_GRAPH_RECURSION_LIMIT` | `500` | 提高工具调用次数上限，防止复杂文档操作超限 |



