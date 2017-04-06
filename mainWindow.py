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
        
        view = QTreeView(self)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Address', 'Hexa', 'Code', 'Comment'])
        view.setModel(model)
        view.setUniformRowHeights(True)

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
            model.appendRow( sectionItem )
            view.setFirstColumnSpanned( model.rowCount()-1, view.rootIndex(), True)

        mainLayout=QVBoxLayout(self.centralWidget())
        mainLayout.addWidget(view)

    def buildAction( self, label, shortcut, tip, method ):
        action = QAction(label, self)
        action.setShortcut(shortcut)
        action.setStatusTip(tip)
        action.triggered.connect(method)
        
        return action

    def buildActions(self):
        openAction = self.buildAction( "&Open", "Ctrl+O", "Open", self.actionQuit )
        quitAction = self.buildAction( "&Quit", "Ctrl+Q", "Quit", self.actionQuit )
                
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(quitAction)
        

    def actionQuit(self):
        #print("Exit")
        sys.exit()



    
