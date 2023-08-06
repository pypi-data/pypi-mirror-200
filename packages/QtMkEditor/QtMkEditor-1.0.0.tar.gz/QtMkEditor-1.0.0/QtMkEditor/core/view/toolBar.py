from PyQt5.QtWidgets import QAction, QToolBar
from ...core import Vars
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import QSize, Qt
import os

class Action(QAction):
    def __init__(self, text='', parent = Vars.MarkEditor):
        super(Action,self).__init__(text,parent )
        
    def addIcon(self, icon_path):
        self.setIcon(QIcon(os.path.join(Vars.abs_path, 'view\\icons', icon_path)))
        
        

class ToolBar:
    def activate(self):
    
    # Text ToolBar :
        self.textToolBar = QToolBar('Text Tool Bar')
        Vars.MarkEditor.addToolBar(Qt.LeftToolBarArea ,self.textToolBar)
        self.textToolBar.setIconSize(QSize(14,14))
        
        self.bold = Action('Bold')
        self.bold.addIcon('bold.png')
        
        self.italic = Action('italic')
        self.italic.addIcon('italic.png')
        
        self.underline = Action('underline')
        self.underline.addIcon('underline.png')
                
        
        self.textToolBar.addActions([self.bold,self.italic, self.underline,
                                     ])
        
    
    # Tools :
        self.toolsToolBar = QToolBar('Tools ToolBar')
        Vars.MarkEditor.addToolBar(Qt.LeftToolBarArea ,self.toolsToolBar)
        self.toolsToolBar.setIconSize(QSize(16,16))
        
        self.code = Action('Code')
        self.code.addIcon('code.png')
        
        self.table = Action('Table')
        self.table.addIcon('table.png')
        
        self.image = Action('Image')
        self.image.addIcon('image.png')
        
        self.link = Action('Link')
        self.link.addIcon('link.png')
        
        self.toolsToolBar.addActions([
            self.code, self.table, self.image, self.link
        ])
    
    
    # Save ToolBar :
        self.opeartionToolBar = QToolBar('Operations Tool Bar')
        Vars.MarkEditor.addToolBar(Qt.LeftToolBarArea ,self.opeartionToolBar)
        self.opeartionToolBar.setIconSize(QSize(16,16))
        
        self.save = Action("Save")
        self.save.setShortcut("Ctrl+S")
        self.save.addIcon('save.png')
        
        self.cancel = Action("Cancel")
        self.cancel.setShortcut("Ctrl+W")
        self.cancel.addIcon('cancel.png')
        
        
        self.opeartionToolBar.addActions([self.save,self.cancel])
        
        
        
        
        
        
        
        
        
