import markdown
from bs4 import BeautifulSoup

markdownText = '''
如今已经习惯了利用MarkDown编写使用文档和博文。大多数博客编辑网站也都支持MarkDown。如今想将文档快速导出为HTML，以方便建站使用，比如现在看到的这个文章。
## 思路规整
- 将MarkDown转为HTML模板
- 根据不同的模块（表格、图片、列表）。修改HTML模板，以适应现有的样式表（这一点涉及面其实不多，我们主要美化HTML模板的方法还是利用CSS样式表，可以看到很多在线MarkDown编辑器也没有着重于这一点。）
- 引用至主站
- 解决附档和图片随MarkDown上传的问题（因为没有想做在线编辑器，当然主要是没有思路。投机取巧）
## 模板转化
熟悉了MarkDown写作的，大致也能猜到转化方法：按行匹配并附加上HTML标签即可。但是，既然是小工具，我们得先看下有没有可以利用的包。

### 前置工作
包[markdown](https://pypi.org/project/Markdown/)是一个非常优秀的MarkDown文本处理工具用以规整MarkDown的输入和输出，暂时我们也只需要其中一个功能：MarkDown转HTML

测试结果
```
<h1>测试</h1>
<hr>
<table>
<thead>
<tr>
<th>a</th>
<th>b</th>
<th>c</th>
</tr>
</thead>
<tbody>
<tr>
<td>s</td>
<td>d</td>
<td>v</td>
</tr>
</tbody>
</table>
```
讲解下两个要点
- 通过output_format指定输出格式，因为这里只是利用此包转化MarkDown文档
- extensions属于拓展模块，MarkDown如果有特殊标准可以利用此导入拓展。extra是为了解析```代码块```，看到这时这个代码块已经被解析的，其实这是三个反引号包裹的代码块。
'''

perser_HTML = markdown.markdown(markdownText, output_format='html5', extensions=['extra'])
brautiful_HTML = BeautifulSoup(perser_HTML, 'html.parser').prettify()
print(brautiful_HTML)