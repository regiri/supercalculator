# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mes_dialog(object):
    def setupUi(self, mes_dialog):
        mes_dialog.setObjectName("mes_dialog")
        mes_dialog.resize(263, 138)
        self.widget = QtWidgets.QWidget(mes_dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 261, 131))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dialog_error_line = QtWidgets.QLabel(self.widget)
        self.dialog_error_line.setText("")
        self.dialog_error_line.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_error_line.setObjectName("dialog_error_line")
        self.verticalLayout.addWidget(self.dialog_error_line)
        self.dialog_ok_button = QtWidgets.QPushButton(self.widget)
        self.dialog_ok_button.setObjectName("dialog_ok_button")
        self.verticalLayout.addWidget(self.dialog_ok_button)

        self.retranslateUi(mes_dialog)
        QtCore.QMetaObject.connectSlotsByName(mes_dialog)

    def retranslateUi(self, mes_dialog):
        _translate = QtCore.QCoreApplication.translate
        mes_dialog.setWindowTitle(_translate("mes_dialog", "Ошибка!"))
        self.dialog_ok_button.setText(_translate("mes_dialog", "ok"))