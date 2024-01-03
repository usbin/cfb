import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget
from ui_idle import UiIdle
from ui_detect_nfc import UiDetectNfc

class UiManager:
    uiList = None
    curUiIdx = -1
    nextEvt = None
    resetEvt = None

    def __init__(self, uiList=None, curUiIdx=-1, nextEvt=None, resetEvt=None):
        self.curUiIdx = 0
        self.nextEvt = pyqtSignal()
        self.resetEvt = pyqtSignal()
        self.nextEvt.connect(self.Next)
        self.resetEvt.connect(self.Reset)
        self.uiList.add(UiIdle(self.nextEvt, self.resetEvt))
        self.uiList.add(UiDetectNfc(self.nextEvt, self.resetEvt))

        self.setWindowTitle('Start')
        self.resize(1000, 625)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft)
        self.show()

        self.Start()

    def Start(self):
        self.uiList[self.curUiIdx].Start()
    def Next(self):
        pass
    def Reset(self):
        pass