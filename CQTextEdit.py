from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from AddedFile import AddedFile
import logging
import numpy

class CQTextEdit(QtGui.QTextEdit):
	areaClicked = QtCore.pyqtSignal(int, int)
	sx = 0
	sy = 0
	def mousePressEvent(self, event):
		sx = self.horizontalScrollBar().value()
		sy = self.verticalScrollBar().value()
		px = event.posF().x() + sx
		py = event.posF().y() + sy

		logging.debug(str(px) + "," + str(py) + " clicked")
		self.sx = sx
		self.sy = sy
		self.areaClicked.emit(px, py)

