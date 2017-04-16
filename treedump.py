from PyQt4.QtGui import *
from PyQt4 import QtCore

class TreedumpView(QTreeView):
    def __init__(self, parent):
        super(QTreeView, self).__init__(parent)
        
    def selectionChanged(self, *args, **kwds):
        print ('selection changed')
        #self.emit( QtCore.SIGNAL('selectionChanged()'))
        super(QTreeView, self).selectionChanged(*args, **kwds)  
