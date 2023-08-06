from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtCore
from ...core import Vars
from ...core.control import TextAreaControl


class TextArea(QTextEdit):
    keyPressed = QtCore.pyqtSignal(int)
    def __init__(self):
        super(TextArea, self).__init__()
        self.setObjectName('TextArea')
        
        Vars.textArea = self
        TextAreaControl.activate()
        

        
    def keyPressEvent(self, event):
        self.keyPressed.emit(event.key())
        super().keyPressEvent(event)
        