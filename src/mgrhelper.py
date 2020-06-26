from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MgrHelper(QObject):
    self = 0
    def  __init__(self):
        super(MgrHelper, self).__init__()
        self.iconFont = QFont("FontAwesome", 9, QFont.Bold)
    def Instance():
        if not MgrHelper.self:
            MgrHelper.self = MgrHelper()
        return MgrHelper.self

    def setIcon(self, btn, iconSize, icon):

        self.iconFont.setFamily("FontAwesome")
        self.iconFont.setPointSize(iconSize)
        btn.setFont(self.iconFont)
        btn.setText(chr(icon))


