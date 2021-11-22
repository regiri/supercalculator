import dateutil.utils
from PyQt5.QtWidgets import QApplication, QLineEdit,  QLabel, QMessageBox, QMainWindow, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from supercalculator import Ui_MainWindow
from error import NewDialogWindow
from os import stat, rename, remove
import sys
import numpy
import copy
import os.path
import sqlite3
import datetime

MAX_MATRIX_SIZE = 100
MIN_MATRIX_SIZE = 1

LEFT_NUM_OFFSET = 10
UP_NUM_OFFSET = 35
BETWEEN_CELLS_OFFSET = 10
LEFT_CELL_OFFSET = 22
UP_CELL_OFFSET = 25

CELL_SIZE = 35

ROUND_NUMBER_COUNT = 2

ERROR_WRONG_USER = "Неправильное имя пользователя или пароль."
ERROR_USER_EXISTS = "Такой пользователь уже существует."
ERROR_USER_NOT_EXISTS = "Такого пользователя не существует."
ERROR_WRONG_PASSWORD = "Неправильный пароль."
ERROR_USER_NOT_LOGIN = "Вход в учетную запись не выполнен."


def log_uncouth_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls._name_, ex)
    import traceback
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncouth_exceptions


class NewWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.matrix = numpy.zeros([MIN_MATRIX_SIZE, MIN_MATRIX_SIZE], dtype=float)
        self.line_matrix = []
        self.a = MIN_MATRIX_SIZE
        self.b = MIN_MATRIX_SIZE
        self.user = ""
        self.con = sqlite3.connect("user_logs.db")
        self.cur = self.con.cursor()
        self.get_matrix_btn_3.clicked.connect(self.get_matrix)
        self.plus_number_btn.clicked.connect(self.plus_number)
        self.mult_number_btn.clicked.connect(self.mult_number)
        self.transpose_btn.clicked.connect(self.transpose)
        self.invert_btn.clicked.connect(self.invert)
        self.clear_matrix_btn.clicked.connect(self.clear_matrix)
        self.power_number_btn.clicked.connect(self.power_number)
        style = open("Darkeum.qss", 'r')
        self.setStyleSheet(style.read())
        self.register_btn.clicked.connect(self.register)
        self.save_session_btn.clicked.connect(self.save_session)
        self.load_session_btn.clicked.connect(self.load_session)
        self.user_login_btn.clicked.connect(self.user_login)
        self.user_logout_btn.clicked.connect(self.user_logout)
        self.error_dialog = NewDialogWindow()
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon("calculator_icon-icons.com_72046.ico"))

    def get_matrix(self):  # отображение матрицы
        try:
            # удаление старой матрицы
            self.line_matrix.clear()
            for child in self.matrix_container.children():
                child.deleteLater()

            # считывание и обработка количества строк матрицы
            a = int(self.row_count_line.text())
            if MIN_MATRIX_SIZE <= a <= MAX_MATRIX_SIZE:
                self.a = a
            elif a > MAX_MATRIX_SIZE:
                self.a = MAX_MATRIX_SIZE
                self.row_count_line.setText(str(MAX_MATRIX_SIZE))
            else:
                self.a = MIN_MATRIX_SIZE
                self.row_count_line.setText((str(MIN_MATRIX_SIZE)))

            # считывание и обработка количества строк матрицы
            b = int(self.col_count_line.text())
            if MIN_MATRIX_SIZE <= b <= MAX_MATRIX_SIZE:
                self.b = b
            elif b > MAX_MATRIX_SIZE:
                self.b = MAX_MATRIX_SIZE
                self.col_count_line.setText(str(MAX_MATRIX_SIZE))
            else:
                self.b = MIN_MATRIX_SIZE
                self.col_count_line.setText((str(MIN_MATRIX_SIZE)))

            # генерациы матрицы нужного размера
            self.matrix = numpy.zeros([a, b], dtype=float)
            x = UP_NUM_OFFSET
            y = LEFT_NUM_OFFSET
            for i in range(b):
                self.text = QLabel(str(i + 1), self.matrix_container)
                self.text.move(x, y)
                self.text.show()
                x += BETWEEN_CELLS_OFFSET + CELL_SIZE
            y = UP_NUM_OFFSET
            x = LEFT_NUM_OFFSET
            for i in range(a):
                self.text = QLabel(str(i + 1), self.matrix_container)
                self.text.move(x, y)
                self.text.show()
                y += BETWEEN_CELLS_OFFSET + CELL_SIZE
            x = LEFT_CELL_OFFSET
            y = UP_CELL_OFFSET
            size = max(x, y)
            for i in range(a):
                liline = []
                for j in range(b):
                    self.line = QLineEdit("0.0", self.matrix_container)
                    self.line.move(x, y)
                    self.line.resize(CELL_SIZE, CELL_SIZE)
                    self.line.textEdited.connect(self.update_np)
                    self.line.setAlignment(Qt.AlignHCenter)
                    self.line.show()
                    liline.append(self.line)
                    x += CELL_SIZE + BETWEEN_CELLS_OFFSET
                y += CELL_SIZE + BETWEEN_CELLS_OFFSET
                size = max(x + CELL_SIZE, y + CELL_SIZE, size)
                x = LEFT_CELL_OFFSET
                self.line_matrix.append(liline)
            self.matrix_container.resize(size, size)
            self.update_np()
            self.enable_all()
        except Exception as e:
            print(e)

    def enable_all(self):  # включение выключенных элементов интерфейса
        self.det_text.setEnabled(True)
        self.power_number_btn.setEnabled(True)
        self.invert_btn.setEnabled(True)
        self.clear_matrix_btn.setEnabled(True)
        self.transpose_btn.setEnabled(True)
        self.plus_number_btn.setEnabled(True)
        self.mult_number_btn.setEnabled(True)
        self.plus_number_line.setEnabled(True)
        self.mult_number_line.setEnabled(True)
        self.minus_matrix_btn.setEnabled(True)
        self.power_number_line.setEnabled(True)
        self.plus_matrix_btn.setEnabled(True)
        self.row_col_line.setEnabled(True)
        self.mult_matrix_btn.setEnabled(True)
        self.label.setEnabled(True)
        self.label_2.setEnabled(True)
        self.label_3.setEnabled(True)
        self.label_4.setEnabled(True)
        self.layoutWidget.setEnabled(True)
        self.layoutWidget_2.setEnabled(True)
        self.layoutWidget_3.setEnabled(True)

    def get_det(self):  # вычисление детерминанта матрицы
        if self.a == self.b:
            self.det_text.setText("det(A) = " + str(round(numpy.linalg.det(self.matrix))))
        else:
            self.det_text.setText("det(A) = ---")

    def update_np(self):  # обновление системной матрицы
        try:
            matrix = []
            for liline in self.line_matrix:
                matrix.append(list(map(lambda x: float(x.text()), liline)))
            self.matrix = numpy.array(matrix)
            self.get_det()
        except Exception as e:
            print(e)

    def update_matrix(self):  # обновление отображаемой матрицы
        try:
            for i in range(len(self.line_matrix)):
                for j in range(len(self.line_matrix[i])):
                    self.line_matrix[i][j].setText(str(round(self.matrix[i][j], ROUND_NUMBER_COUNT)))
            self.get_det()
        except Exception as e:
            print(e)

    def plus_number(self):  # сложение матрицы с числом
        old = copy.deepcopy(self.matrix)
        num = float(self.plus_number_line.text())
        for i in range(len(self.matrix)):
            self.matrix[i][i] += num
        self.update_matrix()
        self.log(str(old).replace('\n', ''), "plus_number", str(self.matrix).replace('\n', ''))

    def mult_number(self):  # умножение матрицы на число
        old = copy.deepcopy(self.matrix)
        t = self.mult_number_line.text()
        if '/' in t:
            a, b = map(float, t.split('/'))
            num = a / b
        else:
            num = float(t)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = float(self.matrix[i][j]) * num
        self.update_matrix()
        self.log(str(old).replace('\n', ''), "mult_number", str(self.matrix).replace('\n', ''))

    def transpose(self):  # транспонирование матрицы
        # TODO обработка случая неквадратной матрицы
        old = copy.deepcopy(self.matrix)
        self.matrix = self.matrix.transpose()
        self.update_matrix()
        self.log(str(old).replace('\n', ''), "transpose", str(self.matrix).replace('\n', ''))

    def invert(self):  # инвертирование матрицы
        old = copy.deepcopy(self.matrix)
        self.matrix = numpy.linalg.inv(self.matrix)
        self.update_matrix()
        self.log(str(old).replace('\n', ''), "invert", str(self.matrix).replace('\n', ''))

    def clear_matrix(self):  # очистка матрицы
        old = copy.deepcopy(self.matrix)
        self.matrix = numpy.zeros([self.a, self.b], dtype=float)
        self.update_matrix()
        self.log(str(old).replace('\n', ''), "clear_matrix", str(self.matrix).replace('\n', ''))

    def power_number(self):  # возведение матрицы в степень
        old = copy.deepcopy(self.matrix)
        self.matrix = numpy.linalg.matrix_power(self.matrix, int(self.power_number_line.text()))
        self.update_matrix()
        self.log(str(old).replace('\n', ''), "power_number", str(self.matrix).replace('\n', ''))

    def log(self, *action):  # метод логгирования
        with open("logs/log.txt", 'a') as log_file:
            log_file.write(';'.join(action) + '\n')

    def register(self):  # метод регистрации пользователя
        user_name = self.user_name_line.text()
        user_password = self.user_password_line.text()
        res = self.cur.execute(f"select user_password from user where user_name = '{user_name}'").fetchall()
        if not user_name or not user_password:
            self.error_dialog.dialog_error_line.setText(ERROR_WRONG_USER)
            self.error_dialog.show()
        elif res:
            self.error_dialog.dialog_error_line.setText(ERROR_USER_EXISTS)
            self.error_dialog.show()
        else:
            self.cur.execute(f"insert into user(user_name, user_password) values('{user_name}', '{user_password}')")
            self.con.commit()
            self.user_login()

    def fill_table(self):  # заполнение списка сохранений
        self.saves_list.clear()
        res = self.cur.execute(f"select * from user_log").fetchall()
        res = list(map(lambda x: (x[0][5:], x[1]), res))
        res = list(map(lambda x: ': '.join(x[::-1]), res))
        self.saves_list.addItems(res)

    def save_session(self):  # сохранение сессии
        if self.user and stat("logs/log.txt").st_size != 0:
            if not self.log_file_line.text():
                file_name = "logs/" + str(datetime.datetime.now()).replace(' ', '_').replace(':', '_') +\
                            '_' + self.user + '.txt'
            else:
                file_name = "logs/" + self.log_file_line.text() + ".txt"
            try:
                rename("logs/log.txt", file_name)
            except FileExistsError:
                remove(file_name)
                rename("logs/log.txt", file_name)
            self.cur.execute(f"insert into log(logname, logfile) values('{file_name[:-4]}', '{file_name}')")
            self.cur.execute(f"insert into user_log(user, log) values('{self.user}', '{file_name[:-4]}')")
            self.con.commit()
            self.fill_table()
        else:
            self.error_dialog.dialog_error_line.setText(ERROR_USER_NOT_LOGIN)
            self.error_dialog.show()

    def load_session(self):  # загрузка сессии
        pass

    def user_login(self):  # вход в учетную запись
        user_name = self.user_name_line.text()
        user_password = self.user_password_line.text()
        res = self.cur.execute(f"select user_id, user_password from user where user_name = '{user_name}'").fetchall()
        try:
            if user_password == res[0][1]:
                self.user = user_name
                self.cur_user_display_label.setText("Пользователь: " + user_name)
                res = self.cur.execute(f"select * from user_log where user = '{res[0][0]}'")
                self.saves_list.addItems(map(lambda x: x[0], res))
            elif res:
                self.error_dialog.dialog_error_line.setText(ERROR_WRONG_PASSWORD)
                self.error_dialog.show()
            self.fill_table()
        except IndexError:
            self.error_dialog.dialog_error_line.setText(ERROR_USER_NOT_EXISTS)
            self.error_dialog.show()

    def user_logout(self):  # выход из учетной записи
        if self.user:
            self.user = ""
            self.cur_user_display_label.setText("Пользователь:")
            self.saves_list.clear()
        else:
            self.error_dialog.dialog_error_line.setText(ERROR_USER_NOT_LOGIN)
            self.error_dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NewWindow()
    ex.show()
    e = app.exec()
    file_path = "log.txt"
    if os.path.isfile(file_path):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path)
        os.remove(path)
    sys.exit(e)


