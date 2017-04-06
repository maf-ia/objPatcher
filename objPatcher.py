#! /usr/bin/env python3

import sys
import mainWindow
import PyQt4.QtGui as QtGui

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwindow = mainWindow.MainWindow()
    sys.exit(app.exec_())