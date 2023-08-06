from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl
from .core import Vars
from .core.view import MainWidget, ToolBar, MenuBar
from .core.control import HtmlPage
from .core.control import MenuBarControl


class QMarkdownEditor(QMainWindow):
    def __init__(self):
        super(QMarkdownEditor, self).__init__()
        Vars.MarkEditor = self
        
        
        # MenuBar :
        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)
        MenuBarControl.activate()
        
        
        # tool bar :
        self.toolbar = ToolBar()
        Vars.toolBar = self.toolbar
        self.toolbar.activate()
        
        # MainWidget :
        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)
        
        
        # html :
        self.html = HtmlPage()
        
        # SaveButton :
        Vars.saveButton = self.toolbar.save
        self.saveButton = self.toolbar.save
        
        Vars.cancelButton = self.toolbar.cancel
        
        with open(f'{Vars.abs_path}\\view\\style\\style.qss','r') as f:
            self.setStyleSheet(f.read())
        
        #size:
        self.resize(700,500)
                
    def toHtml(self):
        return self.html.toHtml(self.toMarkdown())
    
    def toMarkdown(self):
        return Vars.textArea.toPlainText()
    
    def setText(self,text):
        Vars.textArea.setText(text)

    def refresh(self):
        Vars.view.setHtml(self.toHtml(), QUrl.fromLocalFile(Vars.css_dir))
        
        
        
    