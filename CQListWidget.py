from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from AddedFile import AddedFile

class CQTreeView(QtGui.QTreeView):
	def dropEvent(self, event):
		print "Something got dropped"

	def dragEnterEvent(self, event):
		print "Drag enter event"
		#self.setBackgroundRole(QtGui.QPalette.Highlight)
		self.setStyleSheet("QListWidget { background-color: #A9BCF5; }")
		event.acceptProposedAction()

	def dragMoveEvent(self, event):
		print "Drag move event"
		event.acceptProposedAction()

	def dragLeaveEvent(self, event):
		print "Drag Leave Event"
		self.setStyleSheet("QListWidget { background-color: #FFFFFF; }")


	def dropEvent(self, event):
		print "Drop Event"
		self.setStyleSheet("QListWidget { background-color: #FFFFFF; }");
		
		mimeData = event.mimeData()
		droppedFile = None
		if mimeData.hasUrls():
			for url in mimeData.urls():
				# Create a new file info
				ifilePath = url.toLocalFile()
				ifileName = ifilePath.section('/', -1)
				isfile = QtCore.QFileInfo(ifilePath).isFile()
				droppedFile = AddedFile(ifileName, ifilePath, isfile)
				addFileToTable(droppedFile)

				# Emit new file signal
				#self.newFile = pyqtSignal()
				#self.emit(QtCore.SIGNAL('newFile'), droppedFile)

		else:
			print "Has no urls :("

		#emit signal to notify drop


	def addFileToTable(self, fileObj):
		if fileObj.isFile:
		    self.filesList.addItem(fileObj.fileName)
		else:
		    model = QtGui.QFileSystemModel()
		    model.setRootPath(fileObj.filePath)
		    tree = QtGui.QTreeView(self.filesList)
		    tree.setModel(model)
		    tree.show()
