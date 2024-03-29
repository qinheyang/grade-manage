import sys
from PyQt5 import QtWidgets, uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, \
    QFormLayout
from PyQt5.QtCore import Qt
from ui.Home import Ui_Form
from dao.dbOpUser import User
from dao.dbOpGrade import Grade
from dao.dbOpCourse import Course
from dao.dbOpShowgrade import ShowGrade
import service.GlobalValue as GlobalValue
from dao.dbConfig import localSourceConfig as localConfig
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent
from functools import partial
import pymysql
import matplotlib


matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
import matplotlib.pyplot as plt
import sys
import pandas as pd
import time


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._startPos = None
        self._endPos = None
        self._tracking = False
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(1300, 800)
        self.setupUi(self)

        self.tabWidget.tabBar().hide()

        self.initLeft()

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块
        self.figure = None
        self.ax = None
        self.canvas = None

        self.figure_z = None
        self.ax_z = None
        self.canvas_z = None
        self.msgBox = None
        self.map_exec_grade={}
        self.map_exec_course={}


    def initLeft(self):
        self.pushButton_quit.clicked.connect(self.quit)
        if GlobalValue.get_user()["role"] == "0":
            self.left_end_grade.removeWidget(self.icon_cjxs)
            self.left_end_grade.removeWidget(self.pushButton_cjxs)
            self.icon_cjxs.deleteLater()
            self.pushButton_cjxs.deleteLater()
            self.pushButton_xs.clicked.connect(self.clickButton1)
            self.pushButton_cj.clicked.connect(self.clickButton2)
            self.pushButton_kc.clicked.connect(self.clickButton4)
            self.pushButton_fx.clicked.connect(self.clickButton5)
            self.pushButton_kcfx.clicked.connect(self.clickButton6)
            self.btnUserAdd.clicked.connect(self.clickUserSave)
            self.btnCourseAdd.clicked.connect(self.clickCourseSave)
            self.btnGradeAdd.clicked.connect(self.clickGradeSave)
            self.btn_search_grade.clicked.connect(self.clickSearch)
            self.btn_search_user.clicked.connect(self.clickSearch_user)
            self.btn_search_course.clicked.connect(self.clickSearch_course)
            self.btn_output_grade.clicked.connect(self.outputGrade)
            self.btn_output_course.clicked.connect(self.outputCourse)
            self.initHomeData()
            self.initHomeData_role()
            self.clickButton1()

        else:
            self.left_user.removeWidget(self.icon_xs)
            self.left_user.removeWidget(self.pushButton_xs)
            self.icon_xs.deleteLater()
            self.pushButton_xs.deleteLater()
            self.left_grade.removeWidget(self.icon_cj)
            self.left_grade.removeWidget(self.pushButton_cj)
            self.icon_cj.deleteLater()
            self.pushButton_cj.deleteLater()
            self.left_course.removeWidget(self.icon_kc)
            self.left_end_grade.removeWidget(self.pushButton_kc)
            self.icon_kc.deleteLater()
            self.pushButton_kc.deleteLater()
            self.left_analyz_grade.removeWidget(self.icon_fx)
            self.left_analyz_grade.removeWidget(self.pushButton_fx)
            self.icon_fx.deleteLater()
            self.pushButton_fx.deleteLater()
            self.left_analyz_course.removeWidget(self.icon_kcfx)
            self.left_analyz_course.removeWidget(self.pushButton_kcfx)
            self.icon_kcfx.deleteLater()
            self.pushButton_kcfx.deleteLater()
            self.pushButton_cjxs.clicked.connect(self.clickButton3)
            self.combobox_search_grade_xscj.activated.connect(self.activateSearch_grade)
            self.initHomeData_course()
            self.clickButton3()

    def quit(self):
        from service.LoginOp import MyWindow
        self.MyWindow = MyWindow()
        self.close()
        self.MyWindow.show()

    def initHomeData(self):

        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = Course(localConfig)
        class_data = db.courseList()
        self.combobox_search_grade.addItem("全部", "")
        for i, c in enumerate(class_data):
            self.combobox_search_grade.addItem(c["class_name"], c["class_id"])

    def initHomeData_course(self):
        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = Course(localConfig)
        class_data = db.courseList()
        self.combobox_search_grade_xscj.addItem("全部", "")
        for i, c in enumerate(class_data):
            self.combobox_search_grade_xscj.addItem(c["class_name"], c["class_id"])

    def initHomeData_role(self):
        self.combobox_search_role.addItem("全部", "")
        self.combobox_search_role.addItem('教师', '0')
        self.combobox_search_role.addItem('学生', "1")

    def clickSearch(self):
        self.showGradeList(class_id=self.combobox_search_grade.currentData(), user_name=self.input_search_grade.text())

    def clickSearch_user(self):
        self.showUserList(role=self.combobox_search_role.currentData(), user_name=self.input_search_name.text())

    def clickSearch_course(self):
        self.showCourseList(class_name=self.input_search_kc.text())

    def activateSearch_grade(self):
        self.showGradeList_xs(class_id=self.combobox_search_grade_xscj.currentData())

    def showGradeList_xs(self, **params):
        localConfig["cursorclass"] = None
        user = ShowGrade(localConfig)
        data = user.showGradeListByUserId(class_id=params.get("class_id"),user_code=GlobalValue.get_user()["username"])
        self.tableWidget_5.setRowCount(0)
        for i in range(len(data)):
            row_count = self.tableWidget_5.rowCount()  # 返回当前行数(尾部)
            self.tableWidget_5.insertRow(row_count)  # 尾部插入一行
            for j in range(0, len(data[i])):
                content = str(data[i][j])
                item = QTableWidgetItem(content)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_5.setItem(i, j, item)
        self.tabWidget.setCurrentIndex(2)
        self.tableWidget_5.verticalHeader().hide()
        user.cursor.close()
        user.db.close()
        self.combobox_search_grade_xscj.setCurrentIndex(0)

    def showGradeList(self, **params):
        localConfig["cursorclass"] = None
        user = Grade(localConfig)
        data = user.gradeList(class_id=params.get("class_id"), user_name=params.get("user_name"))
        self.tableGrade.setRowCount(0)
        for i in range(len(data)):
            row_count = self.tableGrade.rowCount()  # 返回当前行数(尾部)
            print(data[i])
            self.tableGrade.insertRow(row_count)  # 尾部插入一行
            for j in range(0, len(data[i])):
                if j == 5:
                    tmp_widget = QWidget()
                    tmp_layout = QHBoxLayout(tmp_widget)
                    btn1 = QPushButton()
                    btn1.setText("修改")
                    btn1.setObjectName(f"updateBtn{i}{j}")
                    btn1.clicked.connect(partial(self.clickGradeSave, data[i][j]))
                    btn2 = QPushButton()
                    btn2.setText("删除")
                    btn1.setObjectName(f"deleteBtn{i}{j}")
                    btn2.clicked.connect(partial(self.clickGradeDelete, data[i][j]))
                    tmp_layout.addWidget(btn1)
                    tmp_layout.addWidget(btn2)
                    self.tableGrade.setCellWidget(i, j, tmp_widget)
                else:
                    content = str(data[i][j])

                    item = QTableWidgetItem(content)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableGrade.setItem(i, j, item)
        self.tabWidget.setCurrentIndex(1)
        self.tableGrade.verticalHeader().hide()
        user.cursor.close()
        user.db.close()
        self.combobox_search_grade.setCurrentIndex(0)
        self.input_search_grade.setText("")

    def showCourseList(self, **params):
        localConfig["cursorclass"] = None
        user = Course(localConfig)
        data = user.getcourseList(class_name=params.get("class_name"))
        self.tableWidget_kc.setRowCount(0)
        for i in range(len(data)):
            row_count = self.tableWidget_kc.rowCount()  # 返回当前行数(尾部)
            self.tableWidget_kc.insertRow(row_count)  # 尾部插入一行
            for j in range(0, len(data[i])):
                if j == 2:
                    tmp_widget = QWidget()
                    tmp_layout = QHBoxLayout(tmp_widget)
                    btn1 = QPushButton()
                    btn1.setText("修改")
                    btn1.setObjectName(f"updateBtn{i}{j}")
                    btn1.clicked.connect(partial(self.clickCourseSave, data[i][j]))
                    btn2 = QPushButton()
                    btn2.setText("删除")
                    btn1.setObjectName(f"deleteBtn{i}{j}")
                    btn2.clicked.connect(partial(self.clickCourseDelete, data[i][j]))
                    tmp_layout.addWidget(btn1)
                    tmp_layout.addWidget(btn2)
                    self.tableWidget_kc.setCellWidget(i, j, tmp_widget)
                else:
                    content = str(data[i][j])
                    item = QTableWidgetItem(content)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_kc.setItem(i, j, item)
        self.tabWidget.setCurrentIndex(3)
        self.tableWidget_kc.verticalHeader().hide()
        user.cursor.close()
        user.db.close()
        self.input_search_kc.setText('')

    def showUserList(self, **params):
        localConfig["cursorclass"] = None
        user = User(localConfig)
        data = user.userList(role=params.get("role"), user_name=params.get("user_name"))
        self.tableUser.setRowCount(0)
        for i in range(len(data)):
            row_count = self.tableUser.rowCount()  # 返回当前行数(尾部)
            print(data[i])
            self.tableUser.insertRow(row_count)  # 尾部插入一行
            for j in range(0, len(data[i])):
                if j == 5:
                    tmp_widget = QWidget()
                    tmp_layout = QHBoxLayout(tmp_widget)
                    btn1 = QPushButton()
                    btn1.setText("修改")
                    btn1.setObjectName(f"updateBtn{i}{j}")
                    btn1.clicked.connect(partial(self.clickUserSave, data[i][j]))
                    btn2 = QPushButton()
                    btn2.setText("删除")
                    btn1.setObjectName(f"deleteBtn{i}{j}")
                    btn2.clicked.connect(partial(self.clickUserDelete, data[i][j]))
                    tmp_layout.addWidget(btn1)
                    tmp_layout.addWidget(btn2)
                    self.tableUser.setCellWidget(i, j, tmp_widget)
                else:
                    content = ""
                    if j == 4:
                        if data[i][j] == '0':
                            content = "教师"
                        else:
                            content = "学生"

                    else:
                        content = str(data[i][j])
                    item = QTableWidgetItem(content)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableUser.setItem(i, j, item)
        self.tabWidget.setCurrentIndex(0)
        self.tableUser.verticalHeader().hide()
        user.cursor.close()
        user.db.close()
        self.combobox_search_role.setCurrentIndex(0)
        self.input_search_name.setText('')

    def clickButton1(self):

        self.showUserList()

    def clickButton2(self):
        self.showGradeList()

    def clickButton3(self):
        self.showGradeList_xs()

    def clickButton4(self):
        self.showCourseList()

    def clickCourseSave(self, courseId):
        GlobalValue.set_save_course_id(courseId)
        from service.CourseSaveOp import MyWindow as CourseWindow
        self.userWindow = CourseWindow(pWindow=self)
        self.userWindow.show()

    def clickGradeSave(self, gradeId):
        GlobalValue.set_save_grade_id(gradeId)
        from service.GradeSaveOp import MyWindow as GradeWindow
        self.userWindow = GradeWindow(pWindow=self)
        self.userWindow.show()

    def clickUserSave(self, userId):
        GlobalValue.set_save_user_id(userId)
        from service.UserSaveOp import MyWindow as UserWindow
        self.userWindow = UserWindow(pWindow=self)
        self.userWindow.show()

    def clickUserDelete(self, userId):
        db = User()
        db.userDetele(userId)
        db.db.close()
        db.cursor.close()
        self.clickButton1()

    def clickGradeDelete(self, gradeId):
        db = Grade()
        db.gradeDetele(gradeId)
        db.db.close()
        db.cursor.close()
        self.clickButton2()

    def clickCourseDelete(self, classId):
        db = Course()
        db.courseDetele(classId)
        db.db.close()
        db.cursor.close()
        self.clickButton4()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def clickButton5(self):
        self.tabWidget.setCurrentIndex(4)
        # self.analyze_grade
        # self.menu_action.triggered.connect(self.plot_)
        # self.setCentralWidget(QtWidgets.QWidget())
        self.show_pie_chart()

    def clickButton6(self):
        self.tabWidget.setCurrentIndex(5)
        self.show_zhu_chart()

    def show_pie_chart(self):

        if not self.canvas:
            self.graphics_user.addWidget(self.canvas)
            self.figure, self.ax = plt.subplots()
           # plt.subplots_adjust(left=-0.5)

            self.canvas = FigureCanvas(self.figure)

            self.graphics_user.addWidget(self.canvas)
        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = Grade(localConfig)
        list = db.getGradeCount()
        db.cursor.close()
        db.db.close()
        data = []  # 示例数据
        labels = []
        for l in list:
            data.append(l["num"])
            labels.append(l["region"])
            if self.map_exec_grade.get("分数范围"):
                self.map_exec_grade.get("分数范围").append(l["region"])
                self.map_exec_grade.get("人数").append(l["num"])
            else:
                self.map_exec_grade["分数范围"] = []
                self.map_exec_grade.get("分数范围").append(l["region"])
                self.map_exec_grade["人数"] = []
                self.map_exec_grade.get("人数").append(l["num"])

        self.ax.clear()
        self.ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("学生分数范围示例饼状图")
        plt.legend(labels,loc='upper left', bbox_to_anchor=(1, 1))


        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.canvas.draw()
        self.canvas.flush_events()

    def show_zhu_chart(self):

        if not self.canvas_z:
            self.graphics_course.addWidget(self.canvas_z)
            self.figure_z, self.ax_z = plt.subplots()
            self.canvas_z = FigureCanvas(self.figure_z)
            self.graphics_course.addWidget(self.canvas_z)
        localConfig["cursorclass"] = pymysql.cursors.DictCursor
        db = Grade(localConfig)
        list = db.getGradeuUserCount()
        db.cursor.close()
        db.db.close()
        data = []  # 示例数据
        labels = []

        for l in list:
            data.append(l["num"])
            labels.append(l["label"])
            if self.map_exec_course.get("课程"):
                self.map_exec_course.get("课程").append(l["label"])
                self.map_exec_course.get("人数").append(l["num"])
            else:
                self.map_exec_course["课程"]=[]
                self.map_exec_course.get("课程").append(l["label"])
                self.map_exec_course["人数"] = []
                self.map_exec_course.get("人数").append(l["num"])

        self.ax_z.clear()
        self.ax_z.set(title = '选修课程人数示例柱状图',
        xlabel="选修课程" ,
        ylabel = '选修人数')

        self.ax_z.bar(labels, data,color="#40E0D0")


        self.canvas_z.draw()
        self.canvas_z.flush_events()

    def outputGrade(self):


        df = pd.DataFrame(self.map_exec_grade)
        fn = time.strftime('%Y%m%d%H%M%S', time.localtime()) + "grade.xlsx"
        df.to_excel("D:\\output\\" + fn ,index=False)
        self.msgBox = QMessageBox()
        self.msgBox.setText('导出成功！')
        self.msgBox.setWindowTitle("提示")
        self.msgBox.setWindowFlags(self.msgBox.windowFlags() | Qt.WindowStaysOnTopHint)
        self.msgBox.show()


    def outputCourse(self):
        df = pd.DataFrame(self.map_exec_course)
        fn = time.strftime('%Y%m%d%H%M%S', time.localtime()) + "course.xlsx"
        df.to_excel("D:\\output\\" + fn, index=False)
        self.msgBox = QMessageBox()
        self.msgBox.setText('导出成功！')
        self.msgBox.setWindowTitle("提示")
        self.msgBox.setWindowFlags(self.msgBox.windowFlags() | Qt.WindowStaysOnTopHint)
        self.msgBox.show()
