from .markdownToHtml import HtmlPage
from PyQt5.QtCore import QUrl
from ...core import Vars
import os

class TextAreaControl:
    
    @staticmethod
    def activate():
            
        # event when text changed :
        Vars.textArea.keyPressed.connect(lambda : TextAreaControl.text_Changed())
                
        # HtmlPage  :
        TextAreaControl.html_page = HtmlPage()
        
        
        # Action Buttons :
        Vars.toolBar.bold.triggered.connect(lambda: TextAreaControl.setBold())
        Vars.toolBar.italic.triggered.connect(lambda: TextAreaControl.setItalic())
        Vars.toolBar.underline.triggered.connect(lambda: TextAreaControl.setUnderline())
        
        
        Vars.toolBar.code.triggered.connect(lambda: TextAreaControl.addCode())
        Vars.toolBar.link.triggered.connect(lambda: TextAreaControl.addLink())
        Vars.toolBar.image.triggered.connect(lambda: TextAreaControl.addImage())
        
    @staticmethod
    def delimiter(sub = '', suff = ''):
        cursor = Vars.textArea.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text=='':
            selected_text = ' '
        
        cursor.insertText(''.join([sub,selected_text,suff]))
        
        cursor.setPosition(cursor.position())
        Vars.textArea.setTextCursor(cursor)
        
    @staticmethod
    def setBold():
        TextAreaControl.delimiter('**','**')
    
    @staticmethod
    def setItalic():
        TextAreaControl.delimiter('*','*')
        
    @staticmethod
    def setUnderline():
        TextAreaControl.delimiter('<u>','</u>')

    @staticmethod
    def addCode():
        Vars.textArea.insertPlainText('\n``` python\n\n```')
        
    @staticmethod
    def addLink():
        Vars.textArea.insertPlainText(' []()')
        
    @staticmethod
    def addImage():
        Vars.textArea.insertPlainText('\n![]()')
    
    @staticmethod 
    def text_Changed():
        
        full_text = Vars.textArea.toPlainText()
        
        Vars.view.setHtml(TextAreaControl.html_page.toHtml(full_text), QUrl.fromLocalFile(Vars.css_dir))
        
        

        
        
    