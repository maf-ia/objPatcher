#! /usr/bin/env python3

import sys
#, os, pprint, time

from PyQt4.QtGui import *
from PyQt4 import QtCore
import parse

app = QApplication(sys.argv)

view = QTreeView()
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
    
view.show()
sys.exit(app.exec_())
