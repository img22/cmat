from PyQt4 import QtGui, QtCore


class CQLabel(QtGui.QLabel):
	labelClicked = QtCore.pyqtSignal(int, int)	
	def __init__(self, row, column, parent=None):
		self.row = row
 		self.column = column
		QtGui.QLabel.__init__(self, parent)

	def mouseReleaseEvent(self, event):
		self.labelClicked.emit(self.row, self.column)