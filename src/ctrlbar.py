from Ui_ctrlbar import Ui_CtrlBar
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from mgrhelper import MgrHelper

class CtrlBar(QtWidgets.QWidget, Ui_CtrlBar):
    sigShowOrHidePlaylist = pyqtSignal()
    sigPlaySeek = pyqtSignal()
    sigPlayVolume = pyqtSignal(int)
    sigPlayOrPause = pyqtSignal()
    sigStop = pyqtSignal(bool)
    sigForwardPlay = pyqtSignal()
    sigBackwardPlay = pyqtSignal()
    sigShowMenu = pyqtSignal()
    sigShowSetting = pyqtSignal()

    def __init__(self, parent=None):
        super(CtrlBar,self).__init__(parent=parent)
        self.setupUi(self)
        self.initUi()
        self.nTotalPlaySeconds = 0
        self.bStop = False
        # self.onVideoTotalSeconds(1000)

    def initUi(self):

        MgrHelper.Instance().setIcon(self.PlaylistCtrlBtn, 10, 0xf04b)
        MgrHelper.Instance().setIcon(self.SettingBtn, 10, 0xf04d)
        MgrHelper.Instance().setIcon(self.VolumeBtn, 10, 0xf028)
        MgrHelper.Instance().setIcon(self.ForwardBtn, 10, 0x23E9)
        MgrHelper.Instance().setIcon(self.BackwardBtn, 10, 0x23EA)
        MgrHelper.Instance().setIcon(self.StopBtn, 9, 0x25A0)
        MgrHelper.Instance().setIcon(self.PlayOrPauseBtn, 9, 0x2210)

        self.PlaylistCtrlBtn.setToolTip("播放列表")
        self.SettingBtn.setToolTip("设置")
        self.VolumeBtn.setToolTip("静音")
        self.ForwardBtn.setToolTip("下一个")
        self.BackwardBtn.setToolTip("上一个")
        self.StopBtn.setToolTip("停止")
        self.PlayOrPauseBtn.setToolTip("播放")
        self.connectSignalSlots()

    def connectSignalSlots(self):
        self.PlaylistCtrlBtn.clicked.connect(self.sigShowOrHidePlaylist)
        # self.PlaySlider.
        # self.PlaySlider.SigCustomSliderValueChanged.connect(self.onPlaySliderValueChanged)
        # self.VolumeSlider.SigCustomSliderValueChanged.connect(self.onVolumeSliderValueChanged)
        self.BackwardBtn.clicked.connect(self.sigBackwardPlay)
        self.ForwardBtn.clicked.connect(self.sigForwardPlay)
        self.PlayOrPauseBtn.clicked.connect(self.onPlayOrPauseBtnclicked)
        self.VolumeBtn.clicked.connect(self.onVolumeBtnclicked)
        self.StopBtn.clicked.connect(self.onStopBtnclicked)

    def onPlaySliderValueChanged(self):
        return
    def onVolumeSliderValueChanged(self):
        return

    def onPlayOrPauseBtnclicked(self):
        self.sigPlayOrPause.emit()

    def onVolumeBtnclicked(self):
        if self.VolumeBtn.text() == chr(0xf028):
            # MgrHelper.SetIcon(ui->VolumeBtn, 12, QChar(0xf026));
            self.VolumeSlider.setValue(0)
            self.sigPlayVolume.emit(0)
        else:
            elf.VolumeSlider.setValue(0)
            # GlobalHelper:: SetIcon(ui->VolumeBtn, 12, QChar(0xf028));
            # self.VolumeSlider.setValue(m_dLastVolumePercent * MAX_SLIDER_VALUE)
            self.sigPlayVolume.emit(1)
    def onPauseStat(self, bPaused):
        qDebug("CtrlBar::OnPauseStat")
        if (bPaused):
            MgrHelper.Instance().setIcon(self.PlayOrPauseBtn, 10, 0x25A0)
            self.PlayOrPauseBtn.setToolTip("播放")
        else:
            MgrHelper.Instance().setIcon(self.PlayOrPauseBtn, 10, 0x25BA)
            self.PlayOrPauseBtn.setToolTip("暂停");


    def onStopBtnclicked(self):
        if(self.bStop == False):
            self.bStop = True
        else:
            self.bStop = False
        self.sigStop.emit(self.bStop)

    def on_SettingBtn_clicked(self):
        return


    def onVideoTotalSeconds(self, nSeconds):
        self.nTotalPlaySeconds = nSeconds
        thh = nSeconds / 3600
        tmm = (nSeconds % 3600) / 60
        tss = (nSeconds % 60)
        TotalTime = QTime(thh, tmm, tss)
        self.VideoTotalTimeTimeEdit.setTime(TotalTime)
    def onVideoPlaySeconds(self, nSeconds):
        nSeconds  = nSeconds / 1000
        thh = nSeconds / 3600
        tmm = (nSeconds % 3600) / 60
        tss = (nSeconds % 60)
        Time = QTime(thh, tmm, tss)
        self.VideoPlayTimeTimeEdit.setTime(Time)
