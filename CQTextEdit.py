from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from AddedFile import AddedFile
import logging
import numpy

class CQTextEdit(QtGui.QWidget):
	def __init__(self):
		self.recToDraw = None
		self.drawn = False
		super(CQTextEdit, self).__init__()

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawRect(self.recToDraw)
		print "Drawing", self.recToDraw
		#super(CQTextEdit, self).paintEvent(event)
	def setRect(self, rec):
		self.recToDraw = rec