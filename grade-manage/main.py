import sys
from PyQt5.QtWidgets import QApplication
from service.LoginOp import MyWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWindow()
    widget.show()
    sys.exit(app.exec_())