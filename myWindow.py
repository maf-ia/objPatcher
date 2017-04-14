import sys
from PyQt4 import QtGui, uic
import parse
from PyQt4.QtGui import *
from PyQt4 import QtCore

import os
dir = os.path.dirname(__file__)

from objreader import ObjReader
from parser import Parser
class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi(os.path.join(dir, "objPatcher.ui"), self)
        self.show()
        self.loadFile()

    def loadFile( self ):
        objReader = ObjReader()
        parser = Parser()
        code = objReader.read('intel', os.path.join(dir, 'sample/step1.bin'))
        tree = parser.parse(code)
        model = QStandardItemModel()
        self.treeView.setModel(model)
        model.clear()
        model.setHorizontalHeaderLabels(['Address', 'Hexa', 'Code', 'Comment'])
        
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
            self.treeView.setFirstColumnSpanned( model.rowCount()-1, self.treeView.rootIndex(), True)
       # self.edit.setEnabled( True )
       # self.saveBtn.setEnabled( True )