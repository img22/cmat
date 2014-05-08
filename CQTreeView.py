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
	filesStartedLoading = QtCore.pyqtSignal(bool)
	filesFinishedLoading = QtCore.pyqtSignal(bool)
	pdfFileClicked    = QtCore.pyqtSignal(AddedFile)
	otherFileClicked = QtCore.pyqtSignal(AddedFile)
	operationFailed   = QtCore.pyqtSignal(QtCore.QString)
	allMetadataClear  = QtCore.pyqtSignal(QtCore.QString)
	oneMetadataClear  = QtCore.pyqtSignal(int)

	def __init__(self, obj, container, mode):
		self.allFiles = {}
		self.allItems = {}
		super(CQTreeView, self).__init__(obj)
		self.container = container
		self.automode = mode
		QtCore.QObject.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.itemClicked)

	def dragEnterEvent(self, event):
		self.setStyleSheet("QTreeWidget { background-color: #A9BCF5; }")
		event.acceptProposedAction()

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

	def dragLeaveEvent(self, event):
		self.setStyleSheet("QTreeWidget { background-color: #FFFFFF; }")


	def dropEvent(self, event):
		self.setStyleSheet("QTreeWidget { background-color: #FFFFFF; }")
		event.acceptProposedAction()
		
		mimeData = event.mimeData()
		droppedFile = None
		if mimeData.hasUrls():
			self.filesStartedLoading.emit(False)
			for url in mimeData.urls():				
				self.registerFile(None, url.toLocalFile())
			self.filesFinishedLoading.emit(True)

		else:
			logging.debug("Dropped file has no urls!")

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
		droppedFile  = AddedFile(fileName, filePath, self.container.outputPath, isFile, fileSize, parent)
		logging.debug("Dropped file has path " + droppedFile.filePath)
		self.connectSignals(droppedFile)
		if self.addFileToTable(droppedFile):
			if isFile:
				droppedFile.initAllMetadata()
				droppedFile.initAllPersonalData()
				if self.automode:
					droppedFile.autoClean()

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
		dropped.fileCleaned.connect(self.handleCleaned)

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
			return True
		else:
			logging.error("File already added!")
			return False
			

	def itemClicked(self, item, column):
		"""
			Called every time a file in the widget is clicked
		"""
		clickedFile = item.text(2)
		fileObj = self.allFiles[clickedFile]

		# If the clicked file is an image
		logging.debug("Clicked file type " + fileObj.type)
		imgTypes = ["Jpg", "Jpeg", "Png"]
		pdfType = "Pdf"
		if fileObj.type in imgTypes:
			self.imageFileClicked.emit(fileObj)
		elif fileObj.type == pdfType:
			self.pdfFileClicked.emit(fileObj)
		else:
			self.otherFileClicked.emit(fileObj)



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
			fileObj = self.allFiles[filePath]
			logging.debug(fileObj.type)
			if not (fileObj.type in ['Jpeg', 'Jpg', 'Png']):
				raise Exception()
			else:
				fileObj.cleanMeta(meta)
				fileObj.refreshMetadata()
				self.itemClicked(self.allItems[filePath], 0)
		except Exception as inst:
			logging.error(str(inst))
			self.operationFailed.emit("Could not remove this field. Try remove all!")



	def hidePersonalData(self, filePath, onePdata=False, x=0, y=0):
		item = self.allFiles[filePath]
		success = False
		if item.type == "Pdf":
			if not onePdata:
				success = item.personalData.pdata.coverAll()
				if success:
					item.autoPersonalCleaned = True
			else:
				success = item.personalData.pdata.coverOne(x, y)
			if success:
				self.pdfFileClicked.emit(item)
		elif item.type in ["Jpeg", "Png"]:
			if not onePdata:
				success = item.personalData.pdata.blurAll()
				if success:
					item.autoPersonalCleaned = True
			else:
				success = item.personalData.pdata.blurOne(x, y)
			if success:
				self.imageFileClicked.emit(item)
		item.checkState()


	def handleCleaned(self, filePath):
		"""
			Changes background color or item to green
			and signals cleaned metadata
		"""
		item = self.allItems[filePath]
		self.changeColor(item, "green")
		self.allMetadataClear.emit(filePath)

	def changeColor(self, item, color):
		"""
			Changes the background color of an item
		"""
		col = QtGui.QColor(color)
		item.setBackgroundColor(0, col)
		item.setBackgroundColor(1, col)

	def refreshPdata(self, filePath):
		"""
			Refreshes personal data of file by reloading file
		"""
		item = self.allFiles[filePath]
		item.refreshPdata()
		self.itemClicked(self.allItems[filePath], 0)

	def renderPdata(self, filePath):
		"""
			Renders personal data without reloading file
		"""
		item = self.allFiles[filePath]
		item.renderPdata()
		self.itemClicked(self.allItems[filePath], 0)

	def cleanPdataMarks(self, filePath):
		"""
			Cleans the personal data area of red marks
		"""
		item = self.allFiles[filePath]
		item.cleanPersonalDataMarks()
		self.itemClicked(self.allItems[filePath], 0)

	def getFileObj(self, filePath):
		"""
			Exposes the AddedFile obj stored under filePath
		"""
		return self.allFiles[filePath]

	def loadBackup(self, filePath):
		"""
			Loads the last state of personal data
		"""
		fobj = self.allFiles[filePath]
		fobj.personalData.pdata.loadBackup()
		self.renderPdata(filePath)

	def doCommit(self, filePath):
		"""
			Commits the last state as the current state
		"""
		fobj = self.allFiles[filePath]
		fobj.personalData.pdata.doCommit()

	def doBackup(self, filePath):
		"""
			Stores the current state for later restoration
		"""
		fobj = self.allFiles[filePath]
		fobj.personalData.pdata.doBackup()

	def getPdataDocSize(self, filePath):
		"""
			Returns the document size
		"""
		fobj = self.allFiles[filePath]
		return fobj.personalData.pdata.getDocSize()

	def getOrigPath(self, filepath):
		"""
			Returns the original path of
			dropped file`
		"""
		# Prod - don't want to change test files
		#return self.allFiles[filePath].origPath
		return AddedFile.newName(filepath, '-dev')


	def removeAllMeta(self, path):
		try:
			res = self.allFiles[path].removeAllMeta()
		except Exception as inst:
			self.operationFailed.emit(QtCore.QString(str(inst)))
			return
		self.allFiles[path].refreshMetadata()
		self.itemClicked(self.allItems[path], 0)
		# self.allMetadataClear.emit(path)

	def changeMode(self, mode):
		self.automode = mode

	def saveFile(self, path):
		"""
			Saves the file to output dir specified
			in command line
		"""
		fobj = self.allFiles[path]
		self.allFiles[path].selfCopy()

	def cleanUp(self):
		for key in self.allFiles.keys():
			af = self.allFiles[key]
			af.selfRemove()