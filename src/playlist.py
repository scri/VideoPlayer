from Ui_playlist import Ui_Playlist
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from mgrhelper import MgrHelper


class PlayList(QtWidgets.QWidget, Ui_Playlist):
    sigPlay = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PlayList, self).__init__(parent=parent)
        self.setupUi(self)
        self.nCurrentPlayListIndex = 0
        self.initUi()
    def initUi(self):
        self.List.clear()

    def onAddFileAndPlay(self, filename):

        fileInfo = QFileInfo(filename)
        listItem = self.List.findItems(fileInfo.fileName(), QtCore.Qt.MatchExactly)
        if(len(listItem) == 0):
            pItem = QListWidgetItem(self.List)
            pItem.setData(QtCore.Qt.UserRole, QVariant(fileInfo.filePath()))
            pItem.setText(fileInfo.fileName())
            pItem.setToolTip(fileInfo.filePath());
            self.List.addItem(pItem);
        else:
            pItem = listItem.at(0)
        self.on_List_itemDoubleClicked(pItem)

    def on_List_itemDoubleClicked(self, item):
        # print(item.data(QtCore.Qt.UserRole))
        self.sigPlay.emit(item.data(Qt.UserRole))
        self.nCurrentPlayListIndex = self.List.row(item)
        self.List.setCurrentRow(self.nCurrentPlayListIndex)

    # def mouseDoubleClickEvent(self, event):
    #     print("hello")
    #     event.accept()
    def getPlaylistStatus(self):
        if(self.isHidden()):
            return False
        else:
            return True