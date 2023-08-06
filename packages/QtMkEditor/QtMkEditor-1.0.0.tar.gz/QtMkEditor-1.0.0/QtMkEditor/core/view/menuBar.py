from PyQt5.QtWidgets import QMenuBar, QMenu
from .toolBar import Action
from ...core import Vars
import os

class MenuBar(QMenuBar):
    def __init__(self):
        super(MenuBar, self).__init__()
        Vars.MenuBar = self
                
        
        # File Menu :
        
        self.file = QMenu('File', self)
        
        
        self.open = Action('Open', self)
        self.open.addIcon('open.png')
        self.file.addAction(self.open)
        
        self.addMenu(self.file)
        
        # Edit Menu :
        
        self.edit = QMenu('Edit', self)
        
        self.addMenu(self.edit)
        
        # Help Menu :
        
        self.help = QMenu('Help', self)
        
        self.addMenu(self.help)
        
        
        with open(os.path.join(Vars.abs_path, 'view/style/menubar.qss'),'r') as f:
            self.setStyleSheet(f.read())
        
        