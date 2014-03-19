from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from AddedFile import AddedFile
import logging
import numpy

class CQTextEdit(QtGui.QTextEdit):
	def paintEvent(self, event):
		painter = QtGui.QPainter(self.viewport())
        rect = QtCore.QRectF(10.0, 20.0, 80.0, 60.0)
        painter.drawRect(rect)
