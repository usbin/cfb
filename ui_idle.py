import sys
from PyQt5.QtWidgets import QApplication, QWidget
from uibase import UiBase

class UiIdle(UiBase):
    nextEvt=None
    resetEvt = None
    def __init__(self, nextEvt, resetEvt):
        self.nextCommnad= nextEvt
        self.resetEvt = resetEvt
    def OnStart(self):
        self.setWindowTitle('Start')
        lb1 = QLabel('커피박 투입을 시작하려면 클릭하세요', self)
        self.vbox = QVboxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(lb1)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)
    def OnFinish(self):
        pass