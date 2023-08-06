from bs4 import BeautifulSoup
import markdown as md
from ...core import Vars
import re
import os


class HtmlPage(BeautifulSoup):
    
    html_base = f'''
    <html>
        <head>
        <link rel="stylesheet" type="text/css" href="{Vars.css_path}">
            </head>
        <body> 
        ksjdksj     
            </body>
    </html>
    
    '''
    python_keywords = ['False', 'class', 'from', 'or', 'None', 'continue', 'global',
     'pass', 'True', 'def', 'if', 'raise', 'and', 'del', 'import', 'return', 'as', 
     'elif', 'in', 'try', 'assert', 'else', 'is', 'while', 'async', 'except', 'lambda',
      'with', 'await', 'finally', 'nonlocal', 'yield', 'break', 'for', 'not']

    
    def __init__(self):
        super(HtmlPage, self).__init__(self.html_base, 'html.parser')
        
    def clear(self):
        self.body.clear()
        
    def toHtml(self, text):
        
        self.clear()
        extensions = ['fenced_code','tables']
        mark_text = md.markdown(text, extensions = extensions)
        htmt_code = BeautifulSoup(mark_text,'html.parser')
        self.body.append(htmt_code)
        
        self.pythonHighlight()

        return self.prettify()

    def pythonHighlight(self):
        pythonCode = re.compile(r'\b(' + '|'.join(self.python_keywords) + r')\b')

        for code in self.find_all("code",  {"class": 'language-python'}):
            new_code = pythonCode.sub(r'<span class = "python-words">\1</span>', code.text)

            code.replace_with(BeautifulSoup(f'<code class = "language-python">{new_code}</code>','html.parser'))








