from PyQt5 import QtWidgets
from Ui_about import Ui_About

class About(QtWidgets.QWidget, Ui_About):
    def __init__(self, parent=None):
        super(About,self).__init__(parent=parent)
        self.setupUi(self)
