from markdown import markdown
from bs4 import BeautifulSoup
import os.path as op
class BeautifulOfMD():
    def __init__(self, output_arg = 'html5',format_arg='html.parser',exten_arg=['extra'],head_tag = ''):
        '''默认参数规整'html5','html.parser',['extra']'''
        self.output_arg = output_arg#转化模板
        self.format_arg = format_arg#美化模板
        self.exten_arg = exten_arg#拓展，默认只开启```识别
        self.head_tag = head_tag #这是用来附加CSS样式的

    def convert_to_HTML(self,infile,*func_arg,source = 'DB',outfile=None,en_code = 'utf8'):
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
        rawhtml = self.head_tag + markdown(markdownText, output_format=self.output_arg, extensions=self.exten_arg)
        html_obj = BeautifulSoup(rawhtml, self.format_arg)
        for func in func_arg:
            func(html_obj)


        prethtml = html_obj.prettify()

        #不同状况下的输出
        if source == 'FILE':
            with open(outfile, 'w', encoding=en_code) as f:
                f.write(prethtml)
        else:
            return prethtml


def modify_image_tag(article_id = None):
    def inner_func(raw_html):
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
    return inner_func



html = BeautifulOfMD()
html.convert_to_HTML('E:\\GITHUB\\function_tool\\md_to_HTML\\test.md',modify_image_tag(3),source = 'FILE')