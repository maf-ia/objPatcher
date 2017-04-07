import sys
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
        #self.statusBar()

        self.show()
        
        
    def buildInterface(self):
        self.setCentralWidget(QWidget(self))
        
        self.view = QTreeView(self)
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Address', 'Hexa', 'Code', 'Comment'])
        self.view.setModel(self.model)
        self.view.setUniformRowHeights(True)      

        mainLayout=QVBoxLayout(self.centralWidget())
        mainLayout.addWidget(self.view)
        
        hlay = QHBoxLayout()
        edit = QLineEdit(self)
        hlay.addWidget( edit )
        mainLayout.addLayout( hlay )

    def buildAction( self, label, shortcut, tip, method ):
        action = QAction(label, self)
        action.setShortcut(shortcut)
        action.setStatusTip(tip)
        action.triggered.connect(method)
        
        return action

    def buildActions(self):
        openAction = self.buildAction( "&Open", "Ctrl+O", "Open", self.actionOpen )
        quitAction = self.buildAction( "&Quit", "Ctrl+Q", "Quit", self.actionQuit )
        
        unfoldAction = self.buildAction( "&Unfold ", "Ctrl+U", "Unfold tree", self.actionQuit )
        foldAction = self.buildAction( "&Fold ", "", "Fold tree", self.actionQuit )
        findAction = self.buildAction( "&Find ", "Ctrl+F", "Find", self.actionQuit )
                
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
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

    def loadFile( self, filename ):
        tree = parse.readDump()

        for section in tree.sections:
            sectionItem = QStandardItem( section.title )
            for block in section.blocks:
                blockItem = QStandardItem( block.title )
                for line in block.lines:
                    addrItem = QStandardItem(line.addr)
                    hexaItem = QStandardItem(line.hexa)
                    codeItem = QStandardItem(line.code)
                    commentItem = QStandardItem(line.comment)
                    blockItem.appendRow( [addrItem, hexaItem, codeItem, commentItem] )
                    
                sectionItem.appendRow( blockItem )
                #sectionItem.setFirstColumnSpanned(True)
            self.model.appendRow( sectionItem )
            self.view.setFirstColumnSpanned( self.model.rowCount()-1, self.view.rootIndex(), True)

    
