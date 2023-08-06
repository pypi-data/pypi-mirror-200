from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import uic
from ...core import Vars
from ...core.control import TextAreaControl
from .text_area import TextArea


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()


        # add a layout :
        self.main_layout = QHBoxLayout(self)
        self.mainsplitter = QSplitter()
        
        # text area 
        self.textArea = TextArea()
        self.mainsplitter.addWidget(self.textArea)
        
        # text area 
        self.view = QWebEngineView()
        self.view.setMinimumWidth(200)
        self.mainsplitter.addWidget(self.view)
        
        # add splitter :
        self.main_layout.addWidget(self.mainsplitter)

        # add control to textArea && view :
        Vars.view = self.view

        
        
        
        
        
        
        
        
        
        
        
        
        