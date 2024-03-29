import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.GradeSave import Ui_Form
from PyQt5.QtCore import Qt, QRect
from dao.dbOpGrade import Grade
from service.GlobalValue import get_save_grade_id
from dao.dbOpUser import User
from dao.dbOpCourse import Course
from dao.dbConfig import localSourceConfig as localConfig
import pymysql
from service.GlobalValue import get_save_grade_id


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
        # self.xy_size = self.parent.geometry()  # 获取主界面 初始坐标
        # self.move(self.xy_size.x()-100, self.xy_size.y()-70 )  # 子界面移动到 居中
        self.pushButton.clicked.connect(self.saveGrade)
        self.initGrade()

    def initGrade(self):
        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = User(localConfig)
        user_data = db.userListByRole("1")
        db.cursor.close()
        db.db.close()
        db = Course(localConfig)
        class_data = db.courseList()
        db.cursor.close()
        db.db.close()
        grade = None
        if get_save_grade_id():
            db = Grade(localConfig)
            grade = db.gradeDetail(get_save_grade_id())
            self.textEdit_score.setText(str(grade["score"]))
        else:
            self.comboBox_name.addItem("请选择学生", "")
            self.comboBox_course.addItem("请选择课程", "")

        for i,u in enumerate(user_data):
            self.comboBox_name.addItem(u["user_name"], u["user_id"])
            if grade and u["user_id"] ==grade["user_id"]:
                self.comboBox_name.setCurrentIndex(i)

        for i,c in enumerate(class_data):
            self.comboBox_course.addItem(c["class_name"], c["class_id"])
            if grade and c["class_id"] == grade["class_id"]:
                self.comboBox_course.setCurrentIndex(i)


    def saveGrade(self):
        user_id = self.comboBox_name.currentData()
        class_id = self.comboBox_course.currentData()
        score = self.textEdit_score.toPlainText()
        str = ''
        if user_id == '':
            str = "请选择学生"
        elif class_id == "":
            str = "请选择课程"
        elif score == '':
            str = '请输入分数'

        if str != '':
            self.msg_box = QMessageBox()
            self.msg_box.setText(str)
            self.msg_box.setWindowTitle("提示")
            self.msg_box.setWindowFlags(self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            self.msg_box.show()
            return

        db = Grade()
        db.gradeSave(grade_id=get_save_grade_id(), user_id=user_id, class_id=class_id, score=score)
        db.cursor.close()
        db.db.close()

        self.pWindow.clickButton2()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWindow()
    widget.show()
    sys.exit(app.exec_())
