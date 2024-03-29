import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent
from dao.dbOpUser import  User
from ui.Login import Ui_MainWindow
import service.GlobalValue as GlobalValue
from PyQt5 import Qt
from dao.dbConfig import localSourceConfig as localConfig
import pymysql


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self._startPos = None
        self._endPos = None
        self._tracking = False
        self.setWindowFlags( Qt.Qt.FramelessWindowHint)

        self.setupUi(self)
        self.setFixedSize(1300, 800)

        self.pushButton.clicked.connect(self.display)

    # self.forgetPasswd.clicked.connect(self.forgetPwd)
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def display(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        user = User(localConfig)
        role = user.userLogin(username, password)


        # # 登录成功，返回权限，1为学生,2为老师
        if role:

            u = {"username": username, "password": password,"role":role}
            GlobalValue._initUser(u)
            from service.HomeOp import MainWindow
            self.MyWindow = MainWindow()
            self.close()
            self.MyWindow.show()
        else:
            #QMessageBox().information(None, "提示", "账号或密码错误！", QMessageBox.Yes)

            msgBox = QMessageBox()
            msgBox.setWindowTitle('提示')
            msgBox.setText('账号或密码错误！')
            msgBox.setWindowFlags(msgBox.windowFlags() or Qt.WindowsStaysOnTopHint())
            msgBox.exec_()




    # def forgetPwd(self):
    #     from service.forgetPwd import fpWindow
    #     self.fpWindow = fpWindow()
    #     self.close()
    #     self.fpWindow.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = MyWindow()
#     widget.show()
# sys.exit(app.exec_())
