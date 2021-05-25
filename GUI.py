# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(987, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Browse = QtWidgets.QPushButton(self.centralwidget)
        self.Browse.setObjectName("Browse")
        self.gridLayout.addWidget(self.Browse, 0, 0, 1, 1)
        self.Clear = QtWidgets.QPushButton(self.centralwidget)
        self.Clear.setObjectName("Clear")
        self.gridLayout.addWidget(self.Clear, 0, 1, 1, 1)
        self.SVM = QtWidgets.QPushButton(self.centralwidget)
        self.SVM.setObjectName("SVM")
        self.gridLayout.addWidget(self.SVM, 0, 2, 1, 1)
        self.NN = QtWidgets.QPushButton(self.centralwidget)
        self.NN.setObjectName("NN")
        self.gridLayout.addWidget(self.NN, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 3, 1, 1)
        self.Input = PlotWidget(self.centralwidget)
        self.Input.setObjectName("Input")
        self.gridLayout.addWidget(self.Input, 2, 0, 1, 2)
        self.Output = PlotWidget(self.centralwidget)
        self.Output.setObjectName("Output")
        self.gridLayout.addWidget(self.Output, 2, 2, 1, 2)
        self.KValue = QtWidgets.QTextEdit(self.centralwidget)
        self.KValue.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.KValue.sizePolicy().hasHeightForWidth())
        self.KValue.setSizePolicy(sizePolicy)
        self.KValue.setObjectName("KValue")
        self.gridLayout.addWidget(self.KValue, 3, 0, 1, 1)
        self.Segment = QtWidgets.QPushButton(self.centralwidget)
        self.Segment.setObjectName("Segment")
        self.gridLayout.addWidget(self.Segment, 3, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Browse.setText(_translate("MainWindow", "Browse"))
        self.Clear.setText(_translate("MainWindow", "Clear"))
        self.SVM.setText(_translate("MainWindow", "SVM"))
        self.NN.setText(_translate("MainWindow", "NN"))
        self.Segment.setText(_translate("MainWindow", "Enter Cluster"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

