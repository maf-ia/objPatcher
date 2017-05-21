import os
import sys
import re
import tempfile

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import parse
import optionsDialog

class CommandBuilder:
    def __init__(self):
        self.isATTSyntax = True
        
    def getParseCommand( self, filename ):
        if self.isATTSyntax:
            return "objdump -d " + str(filename)
        else:
            return "objdump -d -M intel " + str(filename)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.currentDir = '.'
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("objPatcher")
        
        self.commandBuilder = CommandBuilder()
        
        self.buildInterface()
        self.buildActions()
        
        self.readSettings() 
        
        self.show()
        
        
    def buildInterface(self):
        self.setCentralWidget(QWidget(self))
        
        self.view = QTreeView()
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setUniformRowHeights(True) 
        
        self.model = parse.TreeDump(self.commandBuilder)
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
        reloadAction = self.buildAction( "&Reload", "Ctrl+R", "Reload", self.actionReload )
        optionAction = self.buildAction( "O&ptions", "", "Options", self.actionOption )
        quitAction = self.buildAction( "&Quit", "Ctrl+Q", "Quit", self.actionQuit )
        
        unfoldAction = self.buildAction( "&Unfold ", "Ctrl+U", "Unfold tree", self.actionUnfold )
        foldAction = self.buildAction( "&Fold ", "", "Fold tree", self.actionFold )
        findAction = self.buildAction( "&Find ", "Ctrl+F", "Find", self.actionQuit )
                
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(reloadAction)
        fileMenu.addAction(optionAction)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAction)
        
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(unfoldAction)
        editMenu.addAction(foldAction)
        editMenu.addSeparator()
        editMenu.addAction(findAction)
       
    def actionQuit(self):
        sys.exit()
        
    def actionOpen(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', self.currentDir,"Binary files (*)")
        if filename[0] != '':
            self.loadFile( filename[0] )
        
    def actionSave(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file', self.currentDir,"Binary files (*)")
        if filename[0] != '':
            self.saveFile( filename[0] )
        
    def actionReload(self):
        index = self.view.currentIndex()
        print(index)
        isIndex = index.isValid()
        if isIndex:
            item = self.model.itemFromIndex(index)
        
        tempFilename = tempfile.mktemp()
        self.saveFile( tempFilename )
        self.loadFile( tempFilename )
        
        if isIndex:
            index = self.model.findItemIndex( item )
            self.view.setCurrentIndex(index)    
                
        os.system( "rm " + tempFilename )
        
    def actionOption(self):
        option = optionsDialog.OptionsDialog()
        settings = QtCore.QSettings()
        settings.beginGroup("Objdump")
        option.syntaxBox.setChecked( bool(settings.value("isATTSyntax", True )) )
        settings.endGroup()
        if option.exec_() == QDialog.Accepted:
            settings.beginGroup("Objdump")
            settings.setValue("isATTSyntax", option.isATTSyntax())
            self.commandBuilder.isATTSyntax = option.isATTSyntax()
            settings.endGroup();

                
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
        self.currentDir = "/".join( filename.split( "/" )[:-1] )
        
        self.model.loadFile( filename )   
        for section in self.model.sections :
            self.view.setFirstColumnSpanned( section.row(), self.view.rootIndex(), True)
            for block in section.blocks:
                self.view.setFirstColumnSpanned( block.row(), section.index(), True)
        
        
        self.edit.setEnabled( True )
        self.saveBtn.setEnabled( True )
        
        self.actionUnfold()
        
    def saveFile( self, filename ):
        self.currentDir = "/".join( filename.split( "/" )[:-1] )
        self.model.saveFile( filename )

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
        val = str(self.edit.text())
        val = val.upper()
        val = re.sub(r'[^0-9A-F]', '', val)

        if len(val) % 2 != 0:
            QMessageBox.warning( self, "Bad string data", "Please enter a correct hexa string" )
            return
        if len(val)/2 != len(item.data.binData):
            QMessageBox.warning( self, "Bad string data", "Please keep same data length" )
            return
        newHexa = "".join( [chr(int(val[2*i:2*(i+1)],16)) for i in range( int( len(val) / 2 ) )] )
        
        item.data.setNewData( newHexa )

    def readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup("Objdump")
        self.commandBuilder.isATTSyntax = settings.value("isATTSyntax", True )
        settings.endGroup()

        
        
