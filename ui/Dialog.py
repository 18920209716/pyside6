# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(368, 247)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(152, 60, 181, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 60, 91, 31))
        self.label.setObjectName("label")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(80, 160, 93, 28))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(220, 160, 93, 28))
        self.pushButton_cancel.setObjectName("pushButton_cancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "请输入密码："))
        self.pushButton_ok.setText(_translate("Dialog", "确定"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))

import image_rc
