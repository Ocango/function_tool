如今已经习惯了利用MarkDown编写使用文档和博文。大多数博客编辑网站也都支持MarkDown。如今想将文档快速导出为HTML，以方便建站使用，比如现在看到的这个文章。

项目关联GIT[]()
## 思路规整
- 将MarkDown转为HTML模板
- 根据不同的模块（表格、图片、列表）。修改HTML模板，以适应现有的样式表（这一点涉及面其实不多，我们主要美化HTML模板的方法还是利用CSS样式表，可以看到很多在线MarkDown编辑器也没有着重于这一点。）
- 引用至主站
- 解决附档和图片随MarkDown上传的问题（因为没有想做在线编辑器，当然主要是没有思路。投机取巧）
## 模板转化
熟悉了MarkDown写作的，大致也能猜到转化方法：按行匹配并附加上HTML标签即可。但是，既然是小工具，我们得先看下有没有可以利用的包。

### 前置工作
包[markdown](https://pypi.org/project/Markdown/)是一个非常优秀的MarkDown文本处理工具用以规整MarkDown的输入和输出，暂时我们也只需要其中一个功能：MarkDown转HTML

测试
```
import markdown

markdownText = '''# 测试
----------
a|b|c
-|-|-
s|d|v
'''

print(markdown.markdown(markdownText, output_format='html5', extensions=['extra']))
```
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
### 美化HTML
[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)，这个包较为常见于爬虫，用来解析HTML文档并转化为字典。这里用来格式化文本（其实上一步已经成了，画蛇添足下），大材小用下。
```
from bs4 import BeautifulSoup
perser_HTML = markdown.markdown(markdownText, output_format='html5', extensions=['extra'])
brautiful_HTML = BeautifulSoup(perser_HTML, 'html.parser').prettify()
print(brautiful_HTML)
```
这里用**html.parser**主要是因为这是python自带的HTML格式化包。后期如果想规整HTML，并附加一些功能，**BeautifulSoup4**也会提供很多帮助。
### 工具规整与实现
1. 需求规整

这边鱼就只以个人需求为出发点进行分析了，因为需求难点已经解决了。

因为网站使用的jinja2模板设计HTML，所以只需要留置参数，将转化好的HTML页面显示出来即可。又因为写MarkDown需要上传后才需要显示，所以预计将转换设计在MarkDown上传的时候。

2. 实现功能类

首先为了方便，我们需要剥离逻辑，用类包装功能
```
from markdown import markdown
from bs4 import BeautifulSoup
import os.path as op
class BeautifulOfMD():
    def __init__(self, output_arg = 'html5',format_arg='html.parser',exten_arg=['extra'],head_tag = None):
        '''默认参数规整'html5','html.parser',['extra']'''
        self.output_arg = output_arg#转化模板
        self.format_arg = format_arg#美化模板
        self.exten_arg = exten_arg#拓展，默认只开启```识别
        self.head_tag = head_tag #这是用来附加CSS样式的

    def convert_to_HTML(self,infile,source = 'DB',outfile=None,en_code = 'utf8',beautiful_flag = False):
        '''
        当source为'DB'，将会直接将inflie当做MarkDown文档，return作为输出
        当source为'FILE',则直接输入文件并输出到指定文件/同名同目录下
        其他来源则默认与DB处理方式相同
        '''
```

3. 实现功能函数
    - 将MarkDown文档转置为HTML
```
    def convert_to_HTML(self,infile,source = 'DB',outfile=None,en_code = 'utf8',beautiful_flag = False):
        '''
        当source为'DB'，将会直接将inflie当做MarkDown文档，return作为输出
        当source为'FILE',则直接输入文件并输出到指定文件/同名同目录下
        其他来源则默认与DB处理方式相同
        '''
        #不同状态下的输入
        if source == 'FILE':

            if not op.isfile(infile):
                return {
                    'message':'请输入正确的 markdown 文件路径！',
                    'result':None
                }
            if outfile is None:
                outfile = op.splitext(infile)[0] + '.html'
            with open(infile, 'r', encoding=en_code) as f:
                markdownText = f.read()
        else:
            markdownText = infile
        
        #转档处理
        rawhtml = self.headTag + markdown.markdown(markdownText, output_format=self.output_arg, extensions=self.exten_arg)

        if beautiful_flag:
            rawhtml = BeautifulSoup(rawhtml, self.format_arg).prettify()

        #不同状况下的输出
        if source == 'FILE':
            with open(outfile, 'w', encoding=en_code) as f:
                f.write(rawhtml)
        else:
            return rawhtml
```
4. 测试
最简单的测试方法：直接转化当前的MarkDown说明档案
```
(tool_env) PS E:\GITHUB\function_tool> python
Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from md_to_HTML.beautifulofmd import BeautifulOfMD
>>> my_md = BeautifulOfMD()
>>> my_md.convert_to_HTML('E:\\GITHUB\\function_tool\\md_to_HTML\\ReadMe.md',source = 'FILE')
```
此时目录下的ReadMe.html即转档后的档案。
### 附加的设计
#### 修改HTML文档
单纯的转档不一定能直接符合实际的转档需求，根据当前的情况，有一个特殊点需要你做出改变：```<image></image>```中的内容需要写成修改成以下的格式，这有这样才能符合目前CSS针对**image**标签的设定4
```
<span class="image main"><img src="/static/images/2/DD428E54-AC60-4342-B9B4-DF6CD096D8D0.png" alt="晒个大脸" /></span>
#src的格式为：/static/images/<int:文档编号>/图片名
```
思路：之前借用过**BeautifulSoup**用来格式化HTML文本，而用过爬虫的都知道之所以爬虫会使用**BeautifulSoup**却是因为他能解析HTML文档并转化为字典，有利于我们对HTML文档进行处理，就不需要采用**遍历匹配**的方法了。

解决方案：[用BeautifulSoup修改HTML](https://www.jb51.net/article/109619.htm)

实际操作：
```
def convert_to_HTML(self,infile,*func_arg,source = 'DB',outfile=None,en_code = 'utf8',beautiful_flag = False):
    for func in func_arg:
        func(html_obj)
def modify_image_tag(raw_html):
'''拓展：修改<img>为<span class="image main"><img></span>'''
    producer_image = raw_html.find_all('img')
    for image in producer_image:
        image['src'] = '/static/image/3/' + image['src']
        new_span_tag = raw_html.new_tag('span')
        new_span_tag['class'] = "image main"
        image.wrap(new_span_tag)
```
实际还可以针对要求，添加拓展方法func_arg，其实用list更好，因人而异。

此时可能还有人会想，如果我要传参呢？**函数嵌套**。比如这里需要额外修饰src，串上一个额外的参数。
```
def asd(article_id = None):
    def modify_image_tag(raw_html):
        producer_image = raw_html.find_all('img')
        for image in producer_image:
            if article_id :
                image_src = '/static/image/' + str(article_id) + '/'
            else:
                image_src = '/static/image/'
            image['src'] = image_src + image['src']
            new_span_tag = raw_html.new_tag('span')
            new_span_tag['class'] = "image main"
            image.wrap(new_span_tag)
    return modify_image_tag
```
接下来调用我们就可以利用这个额外的参数了
```
html = BeautifulOfMD()
html.convert_to_HTML('E:\\GITHUB\\function_tool\\md_to_HTML\\test.md',asd(3),source = 'FILE')
```
如此大多数情况我们就都解决了。接下来OcanGo要将他移植到网页上去了，以方便个人书写文章并转档。大家各去所需吧
#### 可能今后有所补充