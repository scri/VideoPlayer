# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_show.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Show(object):
    def setupUi(self, Show):
        Show.setObjectName("Show")
        Show.resize(724, 455)
        self.label = QtWidgets.QLabel(Show)
        self.label.setGeometry(QtCore.QRect(0, 0, 721, 461))
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Show)
        QtCore.QMetaObject.connectSlotsByName(Show)

    def retranslateUi(self, Show):
        _translate = QtCore.QCoreApplication.translate
        Show.setWindowTitle(_translate("Show", "Form"))
