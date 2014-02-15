from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from AddedFile import AddedFile
import logging

class CQTreeView(QtGui.QTreeWidget):

	fileClicked = QtCore.pyqtSignal(list)
	def __init__(self, obj):
		self.allFiles = {}
		self.allItems = {}
		super(CQTreeView, self).__init__(obj)
		QtCore.QObject.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.itemClicked)

	def dropEvent(self, event):
		#print "Something got dropped"
		pass

	def dragEnterEvent(self, event):
		#print "Drag enter event"
		#self.setBackgroundRole(QtGui.QPalette.Highlight)
		self.setStyleSheet("QTreeWidget { background-color: #A9BCF5; }")
		event.acceptProposedAction()

	def dragMoveEvent(self, event):
		#print "Drag move event"
		event.acceptProposedAction()

	def dragLeaveEvent(self, event):
		#print "Drag Leave Event"
		self.setStyleSheet("QTreeWidget { background-color: #FFFFFF; }")


	def dropEvent(self, event):
		#print "Drop Event"
		self.setStyleSheet("QTreeWidget { background-color: #FFFFFF; }")
		event.acceptProposedAction()
		
		mimeData = event.mimeData()
		droppedFile = None
		if mimeData.hasUrls():
			for url in mimeData.urls():				
				self.registerFile(None, url.toLocalFile())

		else:
			print "Has no urls :("

		#emit signal to notify drop

	def registerFile(self, parent, filePath):
		fileInfo = QtCore.QFileInfo(filePath)
		isFile   = fileInfo.isFile()
		fileName = ""
		tSlash   = True
		if not filePath[-1] == '/':
			tSlash   = False
			fileName = filePath.section('/', -1)
		else:
			fileName = filePath.split('/')[-2]
		fileSize     = fileInfo.size()
		droppedFile  = AddedFile(fileName, filePath, isFile, fileSize, parent)
		if isFile:
			droppedFile.getAllMetadata()
		self.addFileToTable(droppedFile)

		# #print "Received", filePath
		# if isFile:
		# 	#print "Processing file", filePath
		# 	fileName = filePath.section('/', -1)
		# 	fileInfo = QtCore.QFileInfo(filePath)
		# 	isFile = fileInfo.isFile()
		# 	fileSize = fileInfo.size()
		# 	droppedFile = AddedFile(fileName, filePath, isFile, fileSize, parent)
		# 	droppedFile.getAllMetadata()
		# 	self.addFileToTable(droppedFile)
		if not isFile:
			#print "Processing dir", filePath
			directory = QtCore.QDir(filePath)
			for fname in directory.entryList():
				if fname == "." or fname == "..":
					continue
				else:
					if tSlash:
						self.registerFile(filePath, filePath + fname)
					else:
						self.registerFile(filePath, filePath + "/" + fname)

	def addFileToTable(self, fileObj):
		if not fileObj.filePath in self.allFiles.keys():
			logging.debug("Adding " + str(fileObj.fileName) + " with parent " + str(fileObj.parent))
			newItem = None
			size = "-"
			if fileObj.isFile:
				size = str(fileObj.fileSize)

			# if file has not parent, add with self as parent
			if fileObj.parent == None:
				newItem = QtGui.QTreeWidgetItem(self, [fileObj.fileName, size, fileObj.filePath])

			# if file has parent, find the parent and add that as parent
			else:
				parent = None
				parentName = ""
				if not (fileObj.parent in self.allItems.keys()):
					parentName = fileObj.parent.split('/')[-2]
					parent = QtGui.QTreeWidgetItem(self, [parentName, "-", fileObj.filePath])
					self.allItems[fileObj.parent] = parent
					self.insertTopLevelItem(0, parent)
					print "Added parent", fileObj.parent
				parent = self.allItems[fileObj.parent]
				newItem = QtGui.QTreeWidgetItem(parent, [fileObj.fileName, size, fileObj.filePath])
			self.allFiles[fileObj.filePath] = fileObj
			self.allItems[fileObj.filePath] = newItem
			self.insertTopLevelItem(0, newItem)
		else:
			print "File already added!"
			

	def itemClicked(self, item, column):
		print "Item Clicked"
		clickedFile = item.text(2)
		self.fileClicked.emit(self.allFiles[clickedFile].allMetadata)

	def removeFile(self, filePath):
		root = self.invisibleRootItem()
		item = self.allItems[filePath]
		if item.parent() is not None:
			(item.parent()).removeChild(item)
		else:
			root.removeChild(item)
		
		#remove all children from the dictionary
		for ind in self.allItems.keys():
			if filePath in ind or filePath == ind:
				loggint.debug("Removing " + ind + " from file list.")
				try:
					del self.allItems[ind]
					del self.allFiles[ind]
				except KeyError:
					print "No such file", str(filePath)

