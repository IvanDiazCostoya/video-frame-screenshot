# Opens the window with the video in it

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QRubberBand, QSlider
from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
from PyQt5.QtCore import QRect, QSize, Qt

import sys
import cv2

from PyQt5 import uic

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 7000
        # self.tmp = ()

        # Load ui file from PyQt5 designer
        uic.loadUi('window2.ui', self)

        self.frame_number = 0

        self.cam = cv2.VideoCapture("1.mp4")
        # self.cam.set(cv2.CAP_PROP_POS_FRAMES, 600)
        _, self.frame = self.cam.read()
        height, width, channel = self.frame.shape
        bytesPerLine = 3 * width

        # How many frames in the video
        # length_frames = 126006
        length_frames = int(self.cam.get(cv2.CAP_PROP_FRAME_COUNT))

        # Frames per second
        # fps = 60.0
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)

        # total seconds in the video
        # total_seconds = 2100.1
        total_seconds = length_frames * (1 / self.fps)

        hours = (total_seconds / (60 * 60))
        hours = int(hours)

        minutes = (total_seconds / (60))
        minutes = int(minutes)

        seconds = round(total_seconds - hours * 3600 - minutes * 60)

        self.qImg = QImage(self.frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.qImg2 = self.qImg

        self.rubberBand = False
        self.im = QPixmap(self.qImg)

        # Make main window 100 pixels higher than the image so there's space for the slider
        self.resize(self.im.width(), self.im.height() + 100)

        # self.lab = QLabel(self)
        self.label.resize(self.im.width(), self.im.height())
        self.label.move(0, 0)
        self.label.setPixmap(self.im)

        self.currentQRect = self.label.geometry()

        self.horizontalSlider.setGeometry(QRect(150, self.im.height() + 40, self.im.width() - 350, 22))
        self.horizontalSlider.setRange(1, length_frames)
        self.horizontalSlider.valueChanged.connect(self.slider_move)
        self.horizontalSlider.sliderReleased.connect(self.slider_release)

        self.label2 = QLabel(self)
        self.label2.move(40, self.im.height() + 35)
        self.label2.setAlignment(Qt.AlignLeft)
        # self.label2.setText(str(self.horizontalSlider.value()))
        self.label2.setText('frame: 0' + '\n' + 'time: 00:00:00')

        self.label3 = QLabel(self)
        self.label3.move(self.im.width() - 170, self.im.height() + 35)
        self.label3.setAlignment(Qt.AlignLeft)

        t = f"{hours:02d} {minutes:02d} {seconds:02d}"

        self.label3.setText('frame: ' + str(length_frames) + '\n' + 'time: ' + t)
        self.label3.adjustSize()

    def slider_release(self):
        self.frame_number = self.horizontalSlider.value()

        self.cam.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number - 1)
        _, self.frame = self.cam.read()
        height, width, channel = self.frame.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.qImg2 = self.qImg

        self.rubberBand = False
        self.im = QPixmap(self.qImg)
        self.label.setPixmap(self.im)

    def slider_move(self):
        self.label2.setText(str(self.horizontalSlider.value()))

        frames = self.horizontalSlider.value()

        total_seconds = frames * (1 / self.fps)

        hours = (total_seconds / (60 * 60))
        hours = int(hours)

        minutes = (total_seconds / (60))
        minutes = int(minutes)

        seconds = round(total_seconds - hours * 3600 - minutes * 60)

        tt = f"{hours:02d} {minutes:02d} {seconds:02d}"

        # self.label2.setText('frame: 0' + '\n' + 'time: 00:00:00')
        self.label2.setText('frame: ' + str(frames) + '\n' + 'time: ' + tt)

        if frames % 5 == 0:
            self.frame_number = self.horizontalSlider.value()

            self.cam.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number - 1)
            _, self.frame = self.cam.read()
            height, width, channel = self.frame.shape
            bytesPerLine = 3 * width
            self.qImg = QImage(self.frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.qImg2 = self.qImg

            # self.rubberBand = False
            self.im = QPixmap(self.qImg)
            self.label.setPixmap(self.im)


    def mousePressEvent(self, event):
        self.origin = event.pos()

        if self.origin.y() > self.label.height() - 1:
            self.origin.setY(self.label.height() - 1)

        if self.origin.y() < 0:
            self.origin.setY(0)

        if self.origin.x() > self.label.width() - 1:
            self.origin.setX(self.label.width() - 1)

        if self.origin.x() < 0:
            self.origin.setX(0)

        if not self.rubberBand:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self.label)
        self.rubberBand.hide()
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):

        moving = event.pos()

        if moving.y() > self.label.height() - 1:
            moving.setY(self.label.height() - 1)

        if moving.y() < 0:
            moving.setY(0)

        if moving.x() > self.label.width() - 1:
            moving.setX(self.label.width() - 1)

        if moving.x() < 0:
            moving.setX(0)

        self.rubberBand.setGeometry(QRect(self.origin, moving).normalized())

    def mouseReleaseEvent(self, event):
        # print(self.rubberBand.geometry())
        # print(self.rubberBand.x())
        # print(self.rubberBand.y())
        # print(self.rubberBand.width())
        # print(self.rubberBand.height())
        # # self.rubberBand.hide()
        # # determine selection, for example using QRect.intersects()
        # # and QRect.contains().
        #
        # x = self.rubberBand.x()
        # y = self.rubberBand.y()
        # w = self.rubberBand.width()
        # h = self.rubberBand.height()
        # self.frame2 = self.frame[x:x+w,:,:]
        # self.frame2 = self.frame[:,y:y+h,:]
        # print(self.frame2.shape)
        # height2, width2, channel2 = self.frame2.shape
        # bytesPerLine2 = 3 * width2

        # self.currentQRubberBand.hide()
        self.currentQRect = self.rubberBand.geometry().normalized()

        if self.currentQRect.y() > self.label.height() - 1:
            self.currentQRect.setY(self.label.height() - 1)

        if self.currentQRect.y() < 0:
            self.currentQRect.setY(0)

        if self.currentQRect.x() > self.label.width() - 1:
            self.currentQRect.setX(self.label.width() - 1)

        if self.currentQRect.x() < 0:
            self.currentQRect.setX(0)

        if self.currentQRect.y() + self.currentQRect.height() > self.label.height() - 1:
            self.currentQRect.setHeight(self.label.height() - self.currentQRect.y() - 1)

        if self.currentQRect.x() + self.currentQRect.width() > self.label.width() - 1:
            self.currentQRect.setWidth(self.label.width() - self.currentQRect.x() - 1)


        # self.rubberBand.deleteLater()
        # self.cropQPixmap = self.label.pixmap().copy(currentQRect)
        # self.cropQPixmap.save('output.png')
        # self.label.pixmap().save('output2.png')

        # self.tmp = currentQRect.getRect()




        # self.qImg2 = QImage(self.frame2.data, width2, height2, bytesPerLine2, QImage.Format_RGB888)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent and event.key() == Qt.Key_1:
            self.count += 100
            self.cam.set(1, self.count)
            _, self.frame = self.cam.read()
            height, width, channel = self.frame.shape
            bytesPerLine = 3 * width
            self.qImg = QImage(self.frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.im = QPixmap(self.qImg)
            self.label.setPixmap(self.im)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    test = MyApp()
    test.show()

    sys.exit(app.exec())
