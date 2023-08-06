from ...core import Vars
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class MenuBarControl:
    
    @staticmethod
    def activate():
        
        Vars.MenuBar.open.triggered.connect(lambda: MenuBarControl.load())
        
    @staticmethod
    def load():
        
        fileName  = QFileDialog.getOpenFileName(Vars.MarkEditor, 'Open file', 
                                'c:\\',"Markdown File (*.md *.txt)")
        if fileName[0] != '':
            if Vars.textArea.toPlainText().replace(' ', '') != '':
                ans = QMessageBox.question(Vars.MarkEditor, 'Open', "Are you sure to clear Text ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            else:
                ans = QMessageBox.Yes
        
            if ans == QMessageBox.Yes:
                with open(fileName[0],'r') as f:
                    Vars.textArea.setText(f.read())

                Vars.MarkEditor.refresh()
        
