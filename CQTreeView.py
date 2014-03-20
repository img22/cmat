from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from AddedFile import AddedFile
import logging
import numpy

class CQTreeView(QtGui.QTreeWidget):
	"""
		Custom QTreeWidget which also contains objects
		of addfiles. 
	"""

	#fileClicked       = QtCore.pyqtSignal(list)
	imageFileClicked  = QtCore.pyqtSignal(AddedFile)
	pdfFileClicked    = QtCore.pyqtSignal(AddedFile)
	operationFailed   = QtCore.pyqtSignal(QtCore.QString)
	allMetadataClear  = QtCore.pyqtSignal(QtCore.QString)
	oneMetadataClear  = QtCore.pyqtSignal(int)

	def __init__(self, obj):
		self.allFiles = {}
		self.allItems = {}
		super(CQTreeView, self).__init__(obj)
		QtCore.QObject.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.itemClicked)

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
		"""
			Register new file into the widget
		"""
		fileInfo = QtCore.QFileInfo(filePath)
		isFile   = fileInfo.isFile()
		fileName = ""
		tSlash   = True

		# If path is not a directory
		if not filePath[-1] == '/':
			tSlash   = False
			fileName = filePath.section('/', -1)
		else:
			fileName = filePath.split('/')[-2]

		fileSize     = fileInfo.size()
		droppedFile  = AddedFile(fileName, filePath, isFile, fileSize, parent)

		if isFile:
			droppedFile.initAllMetadata()
			droppedFile.initAllPersonalData()

		self.addFileToTable(droppedFile)
		self.connectSignals(droppedFile)

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

	def connectSignals(self, dropped):
		"""
			Connect dropped file object signals to
			methods in this class
		"""
		dropped.fileCleaned.connect(self.changeToGreen)

	def addFileToTable(self, fileObj):
		"""
			Adds trees of file to the tree widget
		"""
		if not fileObj.filePath in self.allFiles.keys():
			logging.debug("Adding " + str(fileObj.filePath) + " with parent " + str(fileObj.parent))
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
				parent = self.allItems[fileObj.parent]
				newItem = QtGui.QTreeWidgetItem(parent, [fileObj.fileName, size, fileObj.filePath])

			#Store the objects for later
			self.allFiles[fileObj.filePath] = fileObj
			self.allItems[fileObj.filePath] = newItem

			# Change the color of the file to red initially
			self.changeColor(newItem, "#F78181")
			self.insertTopLevelItem(0, newItem)
		else:
			logging.error("File already added!")
			

	def itemClicked(self, item, column):
		"""
			Called every time a file in the widget is clicked
		"""
		clickedFile = item.text(2)
		fileObj = self.allFiles[clickedFile]

		# If the clicked file is an image
		logging.debug("Clicked file type " + fileObj.type)
		imgTypes = ["Jpeg", "Png"]
		pdfType = "Pdf"
		if fileObj.type in imgTypes:
			self.imageFileClicked.emit(fileObj)
		if fileObj.type == pdfType:
			self.pdfFileClicked.emit(fileObj)



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
				logging.debug("Removing " + ind + " from file list.")
				try:
					del self.allItems[ind]
					del self.allFiles[ind]
				except KeyError:
					self.operationFailed.emit(filePath + " could not be found!")

	def removeMeta(self, filePath, meta, row):
		try:
			self.allFiles[filePath].cleanMeta(meta)
		except Exception as inst:
			self.operationFailed.emit(QtCore.QString(str(inst)))
			return
		self.oneMetadataClear.emit(row)


	def blurAllFaces(self, filePath):
		self.allFiles[filePath].blurAll()
		item = self.allItems[filePath]
		self.imageItemClicked(filePath)

	def changeToGreen(self, filePath):
		#TODO try catch
		item = self.allItems[filePath]
		self.changeColor(item, "green")

	def changeColor(self, item, color):
		col = QtGui.QColor(color)
		item.setBackgroundColor(0, col)
		item.setBackgroundColor(1, col)

	def removeAllMeta(self, path):
		try:
			res = self.allFiles[path].removeAllMeta()
		except Exception as inst:
			self.operationFailed.emit(QtCore.QString(str(inst)))
			return
		self.allFiles[path].refreshMetadata()
		self.allMetadataClear.emit(path)

