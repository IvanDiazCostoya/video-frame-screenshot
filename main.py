# Write an app in PyQt5 that fills a label with an image and the label and window must have the original size of the image

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

import sys
import rubberband_on_label


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.resize(1325, 780)
        self.move(10, 10)

        # Frame of Open image / select box
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 10, 171, 91))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(1)

        # Open image button
        self.button = QPushButton(self.frame)
        self.button.setGeometry(QtCore.QRect(10, 10, 151, 31))
        self.button.setText('Open image')
        self.button.clicked.connect(self.show_new_window)

        # Select image button
        self.button2 = QPushButton(self.frame)
        self.button2.setGeometry(QtCore.QRect(10, 50, 151, 31))
        self.button2.setText('Select')
        self.button2.clicked.connect(self.func)

        # Outer big frame
        self.frame_2 = QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(10, 110, 1301, 651))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(1)

        self.pushButton_3 = QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 10, 93, 31))
        self.pushButton_3.setText("↑")
        self.pushButton_3.clicked.connect(self.but_up_up)

        self.pushButton_4 = QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(600, 50, 93, 31))
        self.pushButton_4.setText("↓")
        self.pushButton_4.clicked.connect(self.but_up_down)

        self.pushButton_5 = QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(QtCore.QRect(600, 560, 93, 31))
        self.pushButton_5.setText("↑")
        self.pushButton_5.clicked.connect(self.but_down_up)

        self.pushButton_6 = QPushButton(self.frame_2)
        self.pushButton_6.setGeometry(QtCore.QRect(600, 600, 93, 31))
        self.pushButton_6.setText("↓")
        self.pushButton_6.clicked.connect(self.but_down_down)

        self.pushButton_7 = QPushButton(self.frame_2)
        self.pushButton_7.setGeometry(QtCore.QRect(22, 250, 31, 91))
        self.pushButton_7.setText("←")
        self.pushButton_7.clicked.connect(self.but_left_left)

        self.pushButton_8 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_8.setGeometry(QtCore.QRect(60, 250, 31, 91))
        self.pushButton_8.setText("→")
        self.pushButton_8.clicked.connect(self.but_left_right)

        self.pushButton_9 = QPushButton(self.frame_2)
        self.pushButton_9.setGeometry(QtCore.QRect(1248, 260, 31, 91))
        self.pushButton_9.setText("→")
        self.pushButton_9.clicked.connect(self.but_right_right)

        self.pushButton_10 = QPushButton(self.frame_2)
        self.pushButton_10.setGeometry(QtCore.QRect(1210, 260, 31, 91))
        self.pushButton_10.setText("←")
        self.pushButton_10.clicked.connect(self.but_right_left)

        # Inner big frame
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(100, 90, 1101, 461))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.frame_3.setMidLineWidth(1)

        self.label2 = QLabel(self.frame_3)
        self.label2.setAlignment(Qt.AlignLeft)
        self.label2.setAlignment(Qt.AlignTop)
        self.label2.setGeometry(QtCore.QRect(4, 5, 1091, 451))

    def show_new_window(self, checked):
        self.w = rubberband_on_label.MyApp()
        self.w.show()

    def func(self):

        # self.im = self.label.pixmap().copy(currentQRect)
        self.im = self.w.im.copy(self.w.currentQRect)

        self.im = self.im.scaled(self.label2.size(), Qt.KeepAspectRatio)
        # self.label2.setScaledContents(True)
        # self.im = self.im.scaledToWidth(self.label2.width())
        # self.im = self.im.scaledToHeight(self.label2.height())
        # self.label2.setScaledContents(True)
        # self.resize(self.im.width() + 500, self.im.height() + 500)

        self.label2.setPixmap(self.im)
        self.w.close()

    def but_up_up(self):
        tmp = self.w.currentQRect.y() - 1

        if tmp < 0:
            tmp = 0

        self.w.currentQRect.setY(tmp)
        self.func()

    def but_up_down(self):
        tmp = self.w.currentQRect.y() + 1

        if self.w.currentQRect.height() < 2:
            tmp = tmp - 1

        self.w.currentQRect.setY(tmp)
        self.func()

    def but_down_up(self):
        tmp = self.w.currentQRect.height() - 1

        if self.w.currentQRect.height() < 2:
            tmp = tmp + 1

        self.w.currentQRect.setHeight(tmp)
        self.func()

    def but_down_down(self):
        tmp = self.w.currentQRect.height() + 1

        if tmp + self.w.currentQRect.y() > self.w.label.height() - 1:
            tmp = tmp - 1

        self.w.currentQRect.setHeight(tmp)
        self.func()

    def but_left_left(self):
        tmp = self.w.currentQRect.x() - 1

        if tmp < 0:
            tmp = 0

        self.w.currentQRect.setX(tmp)
        self.func()

    def but_left_right(self):
        tmp = self.w.currentQRect.x() + 1

        self.w.currentQRect.setX(tmp)
        self.func()

    def but_right_right(self):
        tmp = self.w.currentQRect.width() + 1

        self.w.currentQRect.setWidth(tmp)
        self.func()

    def but_right_left(self):
        tmp = self.w.currentQRect.width() - 1

        self.w.currentQRect.setWidth(tmp)
        self.func()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
