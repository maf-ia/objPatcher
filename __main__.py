#! /usr/bin/env python3

import sys
import mainWindow
import myWindow
import PyQt4.QtGui as QtGui
from PyQt4 import QtCore, QtGui, uic

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #mainWindow = myWindow.MyWindow()
    mainwindow = mainWindow.MainWindow()
    sys.exit(app.exec_())