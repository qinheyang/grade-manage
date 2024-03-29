import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.CourseSave  import Ui_Form
from PyQt5.QtCore import Qt,QRect
from dao.dbOpCourse import Course
from service.GlobalValue import get_save_course_id
from dao.dbConfig import localSourceConfig as localConfig
import pymysql


class MyWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None,pWindow=None):
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
        self.pushButton.clicked.connect(self.saveCourse)

        if get_save_course_id():
              self.initCourse()

    def initCourse(self):
        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = Course(localConfig)
        obj = db.courseDetail(get_save_course_id())
        self.textEdit_courseCode.setText(obj["class_code"])
        self.textEdit_courseName.setText(obj["class_name"])




    def saveCourse(self):
        course_code = self.textEdit_courseCode.toPlainText()
        course_name = self.textEdit_courseName.toPlainText()
        str=''
        if course_code=='':
            str='请输入课程号'
        elif course_name=='':
            str='请输入课程名'


        if str!='':
            self.msg_box = QMessageBox()
            self.msg_box.setText(str)
            self.msg_box.setWindowTitle("提示")
            self.msg_box.setWindowFlags(self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            self.msg_box.show()
            return

        db=Course()

        res = db.courseSave(class_id=get_save_course_id(), class_code=course_code, class_name=course_name)
        db.cursor.close()
        db.db.close()
        if res == "课程号已存在!":
            self.msg_box = QMessageBox()
            self.msg_box.setText(res)
            self.msg_box.setWindowTitle("提示")
            self.msg_box.setWindowFlags(self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            self.msg_box.show()

        else:
            self.pWindow.clickButton4()
            self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWindow()
    widget.show()
    sys.exit(app.exec_())
