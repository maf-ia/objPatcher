#! /usr/bin/env python3

import sys
import mainWindow
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

if __name__ == '__main__':
    QtCore.QCoreApplication.organizationName = "maf-ia"
    QtCore.QCoreApplication.organizationDomain = "maf-ia"
    QtCore.QCoreApplication.applicationName = "objPatcher"
    
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = mainWindow.MainWindow()
    if len(sys.argv) > 1:
        mainwindow.loadFile( sys.argv[1] )
    sys.exit(app.exec_())
