import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.UserSave import Ui_Form
from PyQt5.QtCore import Qt, QRect
from dao.dbOpUser import User
from service.GlobalValue import get_save_user_id
from dao.dbConfig import localSourceConfig as localConfig
import pymysql

class MyWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None, pWindow=None):
        super(MyWindow, self).__init__(parent)

        # 新建的窗口始终位于当前屏幕的最前面
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg_box = None
        # 阻塞父类窗口不能点击
        self.setWindowModality(Qt.ApplicationModal)

        self.setupUi(self)
        self.pWindow = pWindow

        self.buttonSave.clicked.connect(self.saveUser)
        if get_save_user_id():
              self.initUser()

    def initUser(self):
        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = User(localConfig)
        obj =  db.userDetail(get_save_user_id())
        self.inputUserCode.setText(obj["user_code"])
        self.inputUserName.setText(obj["user_name"])
        self.inputProfession.setText(obj["profession"])
        self.inputTeam.setText(obj["team"])
        self.inputPassword.setText(obj["password"])
        if obj['role'] == "0":
            self.radioRole.setChecked(True)
        else:
            self.radioRole2.setChecked(True)


    def getRole(self):
        if self.radioRole.isChecked():
            return '0'
        elif self.radioRole2.isChecked():
            return '1'
        return None


    def saveUser(self):
        userCode = self.inputUserCode.toPlainText()
        userName = self.inputUserName.toPlainText()
        profession = self.inputProfession.toPlainText()
        team = self.inputTeam.toPlainText()
        password = self.inputPassword.text()
        role = self.getRole()
        str = ""
        if userCode == "":
            str = "请输入学号/工号！"
        elif self.getRole() == None:
            str = "请选择身份！"
        elif userName == "":
            str = "请输入姓名！"
        elif role == "1" and profession == "":
            str = "请输入专业！"
        elif role == "1" and team == "":
            str = "请输入班级！"
        elif password == "":
            str = "请输入密码！"
        if str != "":
            self.msg_box = QMessageBox()
            self.msg_box.setText(str)
            self.msg_box.setWindowTitle("提示")
            self.msg_box.setWindowFlags(self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            self.msg_box.show()
            return
        db = User()
        if role == "0":
            profession = ""
            team = ""
        res = db.userSave(user_id=get_save_user_id(), user_code=userCode, user_name=userName, role=role,
                          password=password,
                          profession=profession, team=team)
        db.cursor.close()
        db.db.close()
        if res == "工号/学号已存在!":
            self.msg_box = QMessageBox()
            self.msg_box.setText(res)
            self.msg_box.setWindowTitle("提示")
            self.msg_box.setWindowFlags(self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            self.msg_box.show()

        else:
            self.pWindow.clickButton1()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWindow()
    widget.show()
    sys.exit(app.exec_())
