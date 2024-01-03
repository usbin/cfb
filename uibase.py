import sys
from PyQt5.QtWidgets import QApplication, QWidget
from abc import ABC, abstractmethod



class UiBase(QWidget):
    @abstractmethod
    def __init__(self, nextCommand, resetCommand):
        pass
    @abstractmethod
    def OnStart(self):
        pass
    @abstractmethod
    def OnFinish(self):
        pass