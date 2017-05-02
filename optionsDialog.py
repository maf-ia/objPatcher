
from PyQt5.QtWidgets import *

class OptionsDialog(QDialog):
    
    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self.setWindowTitle( "Options" )

        layV = QVBoxLayout()

        formLayout = QFormLayout()
        self.syntaxBox = QCheckBox("Use AT&&T syntax", self)
        formLayout.addRow("Syntax : ", self.syntaxBox)
        
        layV.addLayout(formLayout)
        
        dialButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        dialButtons.accepted.connect( self.accept )
        dialButtons.rejected.connect( self.reject )
        
        layV.addWidget( dialButtons )
        self.setLayout(layV)
        
    def isATTSyntax( self ):
        return self.syntaxBox.isChecked()
            
        
