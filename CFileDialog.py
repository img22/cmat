from PyQt4 import QtCore, QtGui, QDropEvent

class CFileDialog(QtGui.QListWidget):
	def dropEvent(self, event):
		print "Something got dropped"