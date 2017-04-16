#! /usr/bin/env python3

import sys
import mainWindow
import PyQt4.QtGui as QtGui

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwindow = mainWindow.MainWindow()
    if len(sys.argv) > 1:
        mainwindow.loadFile( sys.argv[1] )
    sys.exit(app.exec_())
