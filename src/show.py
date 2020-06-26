from Ui_show import Ui_Show
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import av
from av import open
from mgrhelper import MgrHelper
from videoplay import VideoPlay
import time

class Show(QtWidgets.QWidget, Ui_Show):

    # sigPlay = pyqtSignal(str)
    sigOpenFile = pyqtSignal(str)
    # sigGetOneFrame = pyqtSignal(QPixmap)
    sigStop = pyqtSignal(bool)
    sigIsPlayTrue = pyqtSignal()
    def __init__(self, parent=None):
        super(Show,self).__init__(parent=parent)
        self.setupUi(self)
        self.nLastFrameWidth = 0
        self.nLastFrameHeight = 0
        self.stMenu = QMenu()
        self.g_show_rect_mutex = QMutex()
        self.img = QImage()
        # self.stActionGroup = QActionGroup(self)
        #         # self.timerShowCursor = QTimer()
        # self.initUi()

        self.videoplay = VideoPlay()
        self.connectSignalSlots()
        self.bStop = False

    def initUi(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.label.setUpdatesEnabled(False)
        self.setMouseTracking(True)
        # self.stActionGroup.addAction("全屏")
        # self.stActionGroup.addAction("暂停")
        # self.stActionGroup.addAction("停止")
        # self.stMenu.addActions(self.stActionGroup.actions())

    def connectSignalSlots(self):
        self.sigStop.connect(self.isStop)
        # self.sigPlay.connect(self.onPlay)
        # self.videoplay.sigGetOneFrame.connect(self.onGetOneFrame)
        return

    # def onPlay(self, filename):
    #     self.videoplay.start()


    def onGetOneFrame(self,img):
        self.img = img
        # print("get OneFrame")
        self.paintLabel()

    # def paintEvent(self, QPaintEvent):
    #     print("shaw paint here")
    #
    #     painter = QPainter(self)
    #     painter.setBrush(QtCore.Qt.black);
    #     painter.drawRect(0, 0, self.width, self.height)
    #     if (self.img.size().width() <= 0):
    #         return
    #     img = self.img.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
    #     painter.drawImage(QPoint(0, 0), img)
    #     # self.g_show_rect_mutex.unlock()
    def isStop(self, bStop):
        self.bStop = bStop

    def paintLabel(self):
        # self.g_show_rect_mutex.lock()
        if (self.img.size().width() <= 0):
            return
        img = self.img.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        pix = QtGui.QPixmap(img)
        self.label.setPixmap(pix)
        # QApplication.processEvents()
        self.sigIsPlayTrue.emit()
        # self.g_show_rect_mutex.unlock()



    def resizeEvent(self, event):
        # event.accept()
        # print(event.type() == QEvent.Resize)
        self.changeShow()
        event.accept()

    def OnFrameDimensionsChanged(self):
        return

    def changeShow(self):
        self.g_show_rect_mutex.lock()
        if((self.nLastFrameHeight == 0) and (self.nLastFrameWidth == 0)):
            self.label.setGeometry(0, 0, self.width(), self.height())
        else:
            aspect_ratio = float(self.nLastFrameWidth) / float(self.nLastFrameHeight)
            heigt = self.height()
            width = (aspect_ratio * heigt)& ~1
            if(width > self.width()):
                width = self.width()
                heigt = (width * aspect_ratio)& ~1
            x = (self.width() - width) / 2
            y = (self.height() - heigt) / 2
            self.label.setGeometry(x, y, width, heigt)
        # self.paintLabel()
        if self.bStop == True:
            if (self.img.size().width() <= 0):
                return
            img = self.img.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
            pix = QtGui.QPixmap(img)
            self.label.setPixmap(pix)

        self.g_show_rect_mutex.unlock()


    def dropEvent(self, event):
        urls = event.mimeData().urls()





