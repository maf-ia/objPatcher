import sys
import re
#, os, pprint, time

from PyQt4.QtGui import *
from PyQt4 import QtCore
import parse


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("objPatcher")
        
        self.buildInterface()
        self.buildActions() 
        
        self.show()
        
        
    def buildInterface(self):
        self.setCentralWidget(QWidget(self))
        
        self.view = QTreeView()
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setUniformRowHeights(True) 
        
        self.model = parse.TreeDump()
        self.view.setModel(self.model)
        self.view.clicked.connect(self.clickItem)
        
        import HTMLDelegate
        delegate = HTMLDelegate.HTMLDelegate()
        self.view.setItemDelegate(delegate)
               
        self.edit = QLineEdit(self)
        self.edit.setEnabled( False )
        self.saveBtn = QPushButton("Save", self)
        self.saveBtn.setEnabled( False )
        self.saveBtn.clicked.connect(self.saveEdit)
        
        hlay = QHBoxLayout()
        hlay.addWidget( self.edit, 1 )
        hlay.addWidget( self.saveBtn )
        
        mainLayout=QVBoxLayout(self.centralWidget())
        mainLayout.addWidget(self.view)
        mainLayout.addLayout( hlay )
    
    def buildAction( self, label, shortcut, tip, method ):
        action = QAction(label, self)
        action.setShortcut(shortcut)
        action.setStatusTip(tip)
        action.triggered.connect(method)
        
        return action

    def buildActions(self):
        openAction = self.buildAction( "&Open", "Ctrl+O", "Open", self.actionOpen )
        saveAction = self.buildAction( "&Save", "Ctrl+S", "Open", self.actionSave )
        quitAction = self.buildAction( "&Quit", "Ctrl+Q", "Quit", self.actionQuit )
        
        unfoldAction = self.buildAction( "&Unfold ", "Ctrl+U", "Unfold tree", self.actionUnfold )
        foldAction = self.buildAction( "&Fold ", "", "Fold tree", self.actionFold )
        findAction = self.buildAction( "&Find ", "Ctrl+F", "Find", self.actionQuit )
                
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAction)
        
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(unfoldAction)
        editMenu.addAction(foldAction)
        editMenu.addSeparator()
        editMenu.addAction(findAction)
       
    def actionQuit(self):
        #print("Exit")
        sys.exit()
        
    def actionOpen(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '.',"Binary files (*.*)")
        self.loadFile( filename )
        
    def actionSave(self):
        pass
        
    def actionUnfold(self):
        indexes = self.model.match(self.model.index(0,0), QtCore.Qt.DisplayRole, "*", -1, QtCore.Qt.MatchWildcard|QtCore.Qt.MatchRecursive)
        for idx in indexes:
            self.view.expand(idx)
                
    def actionFold(self):
        indexes = self.model.match(self.model.index(0,0), QtCore.Qt.DisplayRole, "*", -1, QtCore.Qt.MatchWildcard|QtCore.Qt.MatchRecursive)
        for idx in indexes:
            self.view.collapse(idx)
        
    def manageClick( self, new, old ):
        print(new,old)

    def loadFile( self, filename ):
        self.setWindowTitle( "objPatcher - " + filename )
        
        self.model.loadFile( filename )   
        for section in self.model.sections :
            self.view.setFirstColumnSpanned( section.row(), self.view.rootIndex(), True)
            for block in section.blocks:
                self.view.setFirstColumnSpanned( block.row(), section.index(), True)
        
        
        self.edit.setEnabled( True )
        self.saveBtn.setEnabled( True )
        
        self.actionUnfold()
        
    

    def clickItem(self,idx):
        item = self.model.itemFromIndex(idx)
        if item.__class__.__name__ == "LineItem":
            self.currentIndex = idx
            self.edit.setText( item.data.getRawHexa() )
            self.edit.setEnabled( True )
            self.saveBtn.setEnabled( True )
        else:
            self.saveBtn.setEnabled( False )
            self.edit.setEnabled( False )
            self.edit.setText( "" )

    def saveEdit(self):
        item = self.model.itemFromIndex(self.currentIndex)
        val = self.edit.text()
        val = val.upper()
        #print(val)
        val = re.sub(r'[^0-9A-F]', '', val)
        #print(val)
        if len(val) % 2 != 0:
            QMessageBox.warning( self, "Bad string data", "Please enter a correct hexa string" )
            return
        if len(val)/2 != len(item.data.binData):
            QMessageBox.warning( self, "Bad string data", "Please keep same data length" )
            return
        newHexa = "".join( [chr(int(val[2*i:2*(i+1)],16)) for i in range( int( len(val) / 2 ) )] )
        
        item.data.setNewData( newHexa )
        #item.setText(item.data.hexa)
        
        
        
        
