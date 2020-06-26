from Ui_title import Ui_Title
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from mgrhelper import MgrHelper
import os

class Title(QtWidgets.QWidget, Ui_Title):
    sigCloseBtnClicked = pyqtSignal()
    sigMinBtnClicked = pyqtSignal()
    sigMaxBtnClicked = pyqtSignal()
    sigDoubleClicked = pyqtSignal()
    sigFullScreenBtnClicked = pyqtSignal()
    sigOpenFile = pyqtSignal(str)
    sigShowMenu = pyqtSignal()
    self = 0
    def __init__(self, parent=None):
        super(Title, self).__init__(parent=parent)
        self.setupUi(self)
        self.initUI()


    def initUI(self):
        #连接信号
        self.CloseBtn.clicked.connect(self.sigCloseBtnClicked)
        self.MinBtn.clicked.connect(self.sigMinBtnClicked)
        self.MaxBtn.clicked.connect(self.sigMaxBtnClicked)
        self.FullScreenBtn.clicked.connect(self.sigFullScreenBtnClicked)
        self.MenuBtn.clicked.connect(self.sigShowMenu)

        self.cwd = os.getcwd()
        self.stMenu = QMenu()

        self.stMenu.addAction("最大化",self.sigMaxBtnClicked)
        self.stMenu.addAction("最小化", self.sigMinBtnClicked)
        self.stMenu.addAction("退出", self.sigCloseBtnClicked)
        self.menu = self.stMenu.addMenu("打开")
        self.menu.addAction("打开文件",self.openFile)

        self.MenuBtn.setToolTip("显示主菜单")
        self.MinBtn.setToolTip("最小化")
        self.MaxBtn.setToolTip("最大化")
        self.CloseBtn.setToolTip("关闭")
        self.FullScreenBtn.setToolTip("全屏")
        MgrHelper.Instance().setIcon(self.MinBtn, 15, 0x2576)
        MgrHelper.Instance().setIcon(self.MaxBtn, 15, 0x2750)
        MgrHelper.Instance().setIcon(self.CloseBtn, 9, 0x2715)
        MgrHelper.Instance().setIcon(self.FullScreenBtn, 15, 0x2681)

    def openFile(self):
        files, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    self.cwd, # 起始路径
                                    "视频文件(*.mkv *.rmvb *.mp4 *.avi *.flv *.wmv *.3gp)")
        #emit(files)
        self.sigOpenFile.emit(files)
        #print(files)
    def onChangeMaxBtnStyle(self, bIfMax):
        if(bIfMax):
            self.MaxBtn.setFont(QFont("SimSun", 9, QFont.Bold))
            MgrHelper.Instance().setIcon(self.MaxBtn, 15, 0x2750)
        else:
            self.MaxBtn.setFont(QFont("SimSun", 9, QFont.Bold))
            MgrHelper.Instance().setIcon(self.MaxBtn, 15, 0x2750)

    def onPlay(self, movieName):
        m = QFileInfo(movieName)
        self.MovieNameLab.setText(m.fileName())

    def onStopFinished(self):
        self.MovieNameLab.clear()
    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.sigDoubleClicked.emit()




