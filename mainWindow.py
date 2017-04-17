import sys
#, os, pprint, time

from PyQt4.QtGui import *
from PyQt4 import QtCore
from treedump import *
import parse

  


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("objPatcher")
        
        self.buildInterface()
        self.buildActions() 
        #self.statusBar()

        self.show()
        
        
    def buildInterface(self):
        self.setCentralWidget(QWidget(self))
        
        self.view = TreedumpView(self)
        self.model = QStandardItemModel()
        self.view.setModel(self.model)
        
        #self.view.connect(self.view, QtCore.SIGNAL(clicked(QModelIndex)),self, SLOT(clicked(QModelIndex)))
        self.view.clicked.connect(self.clickItem)
               
        self.edit = QLineEdit(self)
        self.edit.setEnabled( False )
        self.saveBtn = QPushButton("Save", self)
        self.saveBtn.setEnabled( False )
        
        hlay = QHBoxLayout()
        hlay.addWidget( self.edit, 1 )
        hlay.addWidget( self.saveBtn )
        
        mainLayout=QVBoxLayout(self.centralWidget())
        mainLayout.addWidget(self.view)
        mainLayout.addLayout( hlay )
        
    def clickItem(self,idx):
        item = self.model.itemFromIndex(idx)
        
        if item.line:
            self.edit.setText( item.line.hexa )
            #print(item.line.hexa)

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
        tree = parse.TreeDump()
        tree.loadFile( filename )
        
        
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Address', 'Hexa', 'Code', 'Comment'])
        
        for section in tree.sections:
            sectionItem = QStandardItem( section.title )
            for block in section.blocks:
                blockItem = QStandardItem( block.title )
                for line in block.lines:
                    addrItem = QStandardItem(line.addr)
                    addrItem.line = line
                    hexaItem = QStandardItem(line.hexa)
                    hexaItem.line = line
                    codeItem = QStandardItem(line.code)
                    codeItem.line = line
                    commentItem = QStandardItem(line.comment)
                    commentItem.line = line
                    blockItem.appendRow( [addrItem, hexaItem, codeItem, commentItem] )
                    
                sectionItem.appendRow( blockItem )
                #sectionItem.setFirstColumnSpanned(True)
            self.model.appendRow( sectionItem )
            self.view.setFirstColumnSpanned( self.model.rowCount()-1, self.view.rootIndex(), True)
        
        self.edit.setEnabled( True )
        self.saveBtn.setEnabled( True )
        
        #self.model.connect( self.manageClick )
        #self.view.selectionChanged = self.manageClick
        #self.view.connect(self.view, SIGNAL('selectionChanged()'), self.manageClick)
        self.actionUnfold()
