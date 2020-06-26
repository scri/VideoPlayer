
import sys
import os
import queue
from PyQt5 import QtWidgets
from PyQt5 import *
from Ui_mainwid import Ui_MainWid
from title import Title
from playlist import PlayList
from mgrhelper import MgrHelper
from about import About
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from videoplay import VideoPlay
from audioplay import AudioPlay
from video import Video


class MainWid(QtWidgets.QMainWindow,Ui_MainWid):
    #定义信号
    sigShowMax = pyqtSignal(bool)
    sigOpenFile = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWid,self).__init__(parent=parent)
        # self.setDa
        self.setupUi(self)

        self.stMenu = QMenu()
        self.cwd = os.getcwd()
        self.stActExit = QAction()
        self.stActAbout = QAction()
        self.stActOpen = QAction()
        self.stActFullscreen = QAction()
        self.stAbout = About()
        self.bFullScreenPlay = False  # 全屏播放标识
        self.bFullscreenCtrlBarShow = False
        self.m_drag = False
        self.bMoveDrag = False
        self.img = QImage()
        self.pixmap = QPixmap()
        self.g_show_rect_mutex = QMutex()

        self.stCtrlbarAnimationShow = QPropertyAnimation(self.CtrlBarWid,b"geometry")
        self.stCtrlbarAnimationHide = QPropertyAnimation(self.CtrlBarWid,b"geometry")
        self.stCtrlBarAnimationShow = QRect()
        self.stCtrlBarAnimationHide = QRect()
        self.stCtrlBarAnimationTimer = QTimer()
        self.stFullscreenMouseDetectTimer = QTimer()
        self.stCtrlBarHideTimer = QTimer()

        self.title = Title()
        self.playlist = PlayList()
        self.video = None
        self.videoPlay = VideoPlay()
        self.audioPlay = AudioPlay()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setMouseTracking(True)
        self.setProperty('canMove', True)

        em = QtWidgets.QWidget()
        self.TitleWid.setTitleBarWidget(em)
        em = QtWidgets.QWidget()
        self.PlayList.setTitleBarWidget(em)

        self.TitleWid.setWidget(self.title)
        self.PlayList.setWidget(self.playlist)

        self.stActFullscreen.setText("全屏")
        self.stActFullscreen.setCheckable(True)
        self.stMenu.addAction(self.stActFullscreen)
        self.stActOpen.setText("打开")
        self.stMenu.addAction(self.stActOpen)
        self.stActAbout.setText("关于");
        self.stMenu.addAction(self.stActAbout)
        self.stActExit.setText("退出");
        self.stMenu.addAction(self.stActExit)

        self.connectSignalSlots()

    def connectSignalSlots(self):
        self.title.sigCloseBtnClicked.connect(self.onCloseBtnClicked)
        self.title.sigMaxBtnClicked.connect(self.onMaxBtnClicked)
        self.title.sigMinBtnClicked.connect(self.onMinBtnClicked)
        self.title.sigFullScreenBtnClicked.connect(self.onFullScreenPlay)
        self.title.sigOpenFile.connect(self.playlist.onAddFileAndPlay)
        self.title.sigShowMenu.connect(self.onShowMenu)

        self.playlist.sigPlay.connect(self.onPlay)

        self.ShowWid.sigOpenFile.connect(self.playlist.onAddFileAndPlay)
        self.ShowWid.sigIsPlayTrue.connect(self.videoPlay.sigIsPlayTrue)
        self.ShowWid.sigIsPlayTrue.connect(self.audioPlay.sigIsPlayTrue)

        self.CtrlBarWid.sigStop.connect(self.videoPlay.sigStop)
        self.CtrlBarWid.sigStop.connect(self.audioPlay.sigStop)

        self.CtrlBarWid.sigStop.connect(self.ShowWid.sigStop)

        self.videoPlay.sigGetOneFrame.connect(self.ShowWid.onGetOneFrame)

        self.sigOpenFile.connect(self.playlist.onAddFileAndPlay)
        self.stMenu.triggered[QAction].connect(self.stMenuAct)

    def stMenuAct(self, q):
        #print(q.text())
        if(q.text() == "打开"):
            self.openFile()
        elif(q.text() == "全屏"):
            self.onFullScreenPlay()
        elif(q.text() == "关于"):
            self.onShowAbout()
        else:
            self.onCloseBtnClicked()

    def onShowAbout(self):
        # self.stAbout.move(self.cursor().pos().x() - self.stAbout.width()/2,
        #                   self.cursor().pos().x()- self.stAbout.height()/2)
        self.stAbout.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.stAbout.show()
        # return
    def openFile(self):
        files, filetype = QFileDialog.getOpenFileName(self,
                                                      "选取文件",
                                                      self.cwd,  # 起始路径
                                                      "视频文件(*.mkv *.rmvb *.mp4 *.avi *.flv *.wmv *.3gp)")
        self.sigOpenFile.emit(files)


    def onPlay(self, filename):
        # self.video.connectFile(filename)
        #self.videoplay.start()

        # self.video.run()
        video_queue = queue.Queue()
        audio_queue = queue.Queue()
        self.videoPlay.setQueue(video_queue)
        self.audioPlay.setQueue(audio_queue)
        self.video = Video(filename, video_queue, audio_queue)
        self.video.sigSeconds.connect(self.CtrlBarWid.onVideoTotalSeconds)
        self.videoPlay.sigSeconds.connect(self.CtrlBarWid.onVideoPlaySeconds)
        if self.audioPlay.isRunning() or self.videoPlay.isRunning():
            print("stall run!")
            self.audioPlay.terminate()
            self.videoPlay.terminate()
            self.video.terminate()
            video_queue.queue.clear()
            audio_queue.queue.clear()

        else:
            print("complete")
        self.audioPlay.start()
        self.videoPlay.start()
        self.video.start()


    def onShowSettingWid(self):
        return

    def onFullScreenPlay(self):
        if(self.bFullScreenPlay == False):
            self.bFullScreenPlay = True
            self.stActFullscreen.setCheckable(True)
            self.ShowWid.setWindowFlags(QtCore.Qt.Window)

            self.ShowWid.showFullScreen()
            self.stCtrlBarAnimationShow = QRect(self.ShowWid.x(),
                                                self.ShowWid.height()-self.CtrlBarWid.height(),
                                                self.ShowWid.width(),
                                                self.CtrlBarWid.height())
            self.stCtrlBarAnimationHide = QRect(self.ShowWid.x(),
                                                self.ShowWid.height(),
                                                self.ShowWid.width(),
                                                self.CtrlBarWid.height())
            self.stCtrlbarAnimationShow.setStartValue(self.stCtrlBarAnimationHide)
            self.stCtrlbarAnimationShow.setEndValue(self.stCtrlBarAnimationShow)
            self.stCtrlbarAnimationShow.setDuration(1000)

            self.stCtrlbarAnimationHide.setStartValue(self.stCtrlBarAnimationShow)
            self.stCtrlbarAnimationHide.setEndValue(self.stCtrlBarAnimationHide)
            self.stCtrlbarAnimationHide.setDuration(1000)

            self.CtrlBarWid.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
            self.CtrlBarWid.windowHandle()
            # self.CtrlBarWid.raise()
            self.CtrlBarWid.setWindowOpacity(0.5)
            self.CtrlBarWid.showNormal()
            self.stCtrlbarAnimationShow.start()
            self.bFullscreenCtrlBarShow = True
            self.stFullscreenMouseDetectTimer.start()
            self.setFocus()
        else:
            self.bFullScreenPlay = False
            self.stActFullscreen.setChecked(False)
            self.stCtrlbarAnimationShow.stop()
            self.stCtrlbarAnimationHide.stop()
            self.CtrlBarWid.setWindowOpacity(1)
            self.CtrlBarWid.setWindowFlags(QtCore.Qt.SubWindow)
            self.ShowWid.setWindowFlags(QtCore.Qt.SubWindow)
            self.CtrlBarWid.showNormal()
            self.ShowWid.showNormal()
            self.stFullscreenMouseDetectTimer.stop()
            self.setFocus()

    def onCloseBtnClicked(self):
        self.close()
    def onShowMenu(self):
        self.stMenu.exec(self.cursor().pos())

    def onMinBtnClicked(self):
        self.showMinimized()

    def onMaxBtnClicked(self):
        if self.isMaximized():
            self.showNormal()
            self.sigShowMax.emit(False)
        else:
            self.showMaximized()
            self.sigShowMax.emit(True)

    def onShowOrHidePlaylist(self):
        if(self.PlayList.isHidden()):
            self.PlayList.show()
        else:
            self.PlayList.hide()

    def keyPressEvent(self, event):
        print(event.key())
        qDebug("MainWid::keyPressEvent:")
        if(event.key() == 16777216):
            print("hello")
        elif (event.key() == 1):
            print("0")
        event.accept()


    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.TitleWid.geometry().contains(event.pos()):
                self.m_drag = True
                self.m_DragPosition = event.globalPos() - self.pos()
        event.accept()
        # self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
        event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        #self.setCursor(QCursor(Qt.ArrowCursor))
        QMouseEvent.accept()

    def contextMenuEvent(self, event):
        self.m_stMenu.exec(event.globalPos())
        event.accept()

    def dropEvent(self, QDropEvent):
        urls = QDropEvent.mimeData().urls()
        QDropEvent.acept()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MainWid()
    my_pyqt_form.show()
    sys.exit(app.exec_())