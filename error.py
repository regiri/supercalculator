from PyQt5.QtWidgets import QDialog
from error_dialog import Ui_mes_dialog


class NewDialogWindow(QDialog, Ui_mes_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dialog_ok_button.clicked.connect(self.dialog_ok)
        style = open("Darkeum.qss", 'r')
        self.setStyleSheet(style.read())

    def dialog_ok(self):
        self.close()
