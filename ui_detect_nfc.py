import sys
from PyQt5.QtWidgets import QApplication, QWidget
from uibase import UiBase

class UiDetectNfc(UiBase):
    nextEvt=None
    resetEvt = None
    def __init__(self, nextEvt, resetEvt):
        self.nextCommnad= nextEvt
        self.resetEvt = resetEvt
    def OnStart(self):
        pass
    def OnFinish(self):
        pass