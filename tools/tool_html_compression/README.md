# HTML内容处理工具 - 使用说明

## 一、项目介绍
这是一个用于HTML内容清理和压缩的Python工具，能够自动处理HTML代码，移除不必要的标签、注释和空白字符，输出干净、紧凑的HTML格式。

## 二、核心功能
- **自动清理标签**：移除最外层的`<html_rander>`包装标签
- **智能压缩**：删除HTML注释，压缩多余空格和换行
- **格式优化**：保持HTML结构的同时最小化代码体积
- **保留内容**：不改变原始文本内容和标签属性

## 三、入参说明
### 函数定义
```python
def process_html_content(html_content: str) -> str
```
## 参数详细说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| `html_content` | `str` | 是 | 无 | 需要处理的原始HTML内容，可以包含或不包含 `<html_rander>` 标签 | `<html_rander><div>内容</div></html_rander>` 或 `<div>内容</div>` |

### 支持的输入格式：
- 包含 `<html_rander>` 标签的完整内容
- 普通 HTML 片段
- 带有多余空格、换行和注释的 HTML
- 任意合法的 HTML 字符串


## 四、出参说明

### 返回结果
| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| 返回值 | `str` | 处理后的压缩HTML字符串 | `<div class="test"><p>内容</p></div>` |


## 五、使用示例
### 示例1：基础用法
```python
from html_processor import process_html_content

# 输入HTML
html_input = '''
<html_rander>
    <div class="container">
        <p>Hello World</p>
    </div>
</html_rander>
'''

# 处理HTML
result = process_html_content(html_input)
print(result)
# 输出：<div class="container"><p>Hello World</p></div>
```
### 示例2：处理带注释的HTML
```python
html_input = '''
<html_rander>
    <!-- 这是注释 -->
    <section>
        <h1>标题</h1>
        <p>内容    段落</p>
    </section>
</html_rander>
'''

result = process_html_content(html_input)
print(result)
# 输出：<section><h1>标题</h1><p>内容 段落</p></section>
```
### 示例3：处理带多余空格和换行的HTML
```python

html_input = '''
<div>
    <ul>
        <li>项目1</li>
        <li>项目2</li>
    </ul>
</div>
'''

result = process_html_content(html_input)
print(result)
# 输出：<div><ul><li>项目1</li><li>项目2</li></ul></div>

```
### 示例4：处理带属性的HTML
```python
html_input = '''
<html_rander>
    <article id="post-123">
        <header>
            <h2 class="title">文章标题</h2>
            <time>2024-01-01</time>
        </header>
        <div class="content">
            <p>第一段文字。</p>
            <p>第二段  文字。</p>
            <!-- 广告位 -->
            <div class="ad"></div>
        </div>
    </article>
</html_rander>
'''
result = process_html_content(html_input)
print(result)
# 输出：<article id="post-123"><header><h2 class="title">文章标题</h2><time>2024-01-01</time></header><div class="content"><p>第一段文字。</p><p>第二段 文字。</p><div class="ad"></div></div></article>
```