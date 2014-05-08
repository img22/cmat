from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject
from MAT import mat
from MAT import strippers
import tempfile
import logging
import cv2
from math import sqrt
import string
import os
import shutil
import copy
from PersonalData import ImgPersonalData, PdfPersonalData
"""
	A class to represent a file dragged into the 
	workspace of cmat
"""

class AddedFile(QObject):

	#signal to emit when file is clean
	fileCleaned = QtCore.pyqtSignal(QtCore.QString)

	def __init__(self, name, path, outputPath, isfile, sz, parent):
		"""
			Initialize an AddedFile instance, this represents
			a new file dragged in. It contains all metadata and 
			prsonal info in the file.
		"""
		super(AddedFile, self).__init__()

		#check the file exists
		if not QtCore.QFileInfo(path).exists():
			raise Exception("No such file or directory!" + path)

		# create a new file to work with, new file has -cmat tag
		if isfile:
			self.fileName = AddedFile.newName(str(name), "-cmat")
			self.filePath = AddedFile.tempName(self.fileName)
			logging.debug('Out Path is ' + path)
		else:
			self.fileName = name
			self.filePath = path

		# basic file infor
		self.origPath = path
		self.origName = name
		self.outputPath = outputPath
		self.isFile = isfile
		self.fileSize = sz
		self.parent = parent
		self.type = ""
		self.supported = True
		self.matObject = None

		# all metadata in the file
		self.allMetadata = []
		self.hasMetadata = True

		# has it been cleaned
		self.autoPersonalCleaned = False
		self.autoMetaCleaned = False
		self.reconMetaCleaned = False
		
		# all personal info in the file
		self.personalData = None

		#Copy the given file to the -cmat file
		if self.isFile:
			self.makeCopy(self.origPath, self.filePath)
		
	def initAllMetadata(self):
		"""
			Gets all metadata of the file using the MAT
			library.
		"""
		if self.isFile:

			self.allMetadata = []

			self.matObject = mat.create_class_file(str(self.filePath), str(self.filePath), add2archive=True,
                low_pdf_quality=True)

			classType = self.matObject.__class__.__name__
			self.type = classType.replace("Stripper", "")

			if self.matObject is None:
				logging.debug(self.filePath + " is unsupported!")
				self.supported = False
				self.checkState()
				return self.allMetadata
			
			metaDict = self.matObject.get_meta()

			if metaDict is None or len(metaDict.keys()) == 0:
				self.hasMetadata = False
			else:
				for key in metaDict.keys():
					logging.debug("Found metadata header: " + key)
					self.allMetadata.append([key, metaDict[key]])
		else:
			self.hasMetadata = False


		logging.debug("Checking state")
		self.checkState()

		if self.type in ["JpegStripper", "PngStripper"]:
			self.detectFaces()

		logging.debug("Finished Extracting metadata")
		return self.allMetadata

	def hasMetadata(self):
		"""
			Any metadata detected?
		"""
		return self.hasMetadata

	def initAllPersonalData(self):
		"""
			Initialize/get personal data
		"""
		if self.type == 'Pdf':
			self.personalData = PdfPersonalData(self.filePath)
		elif self.type in ['Jpeg', 'Png']:
			self.personalData = ImgPersonalData(self.filePath)

	def cleanPersonalDataMarks(self):
		"""
			Renders personal data without red marks
		"""
		self.personalData.clearMarks()
		

	def refreshMetadata(self):
		self.allMetadata = []
		self.matObject = mat.create_class_file(str(self.filePath), str(self.filePath), add2archive=True,
                low_pdf_quality=True)
		logging.debug("Refreshing metadata..")
		
		metaDict = self.matObject.get_meta()
		if metaDict is not None:
			for key in metaDict.keys():
				logging.debug("Found metadata header: " + key)
				self.allMetadata.append([key, metaDict[key]])
		
		if len(self.allMetadata) == 0:
			self.hasMetadata = False
		logging.debug("Done refreshing metadata..")
		self.checkState()
		return self.allMetadata

	def refreshPdata(self):
		"""
			Reloads personal data from file
		"""
		self.initAllPersonalData()

	def renderPdata(self):
		"""
			Renders pesonal data without relaoding file
		"""
		if self.type == 'Pdf':
			self.personalData.pdata.renderPages()
		elif self.type in ['Jpg', 'Jpeg', 'Png']:
			logging.debug('Rendering Image..')
			self.personalData.pdata.renderImage()

	def cleanMeta(self, mname):
		cleanError = mname + " could not be removed! This means the metadata can not be removed separately! Try Auto Removing metadata from the file."
		if not self.matObject.remove_meta(str(mname)):
			raise Exception(cleanError)
		self.checkState()


	def checkState(self):
		if ((not self.hasMetadata) and (self.personalData is not None) and self.personalData.isClean()):
			logging.debug("File is clean! Emitting clean signal...")
			self.fileCleaned.emit(self.filePath)
			logging.debug("Writing to output...")

			# write the file to output, now that it is clean
			self.makeCopy(self.filePath, AddedFile.changeBase(self.origPath, self.outputPath))

	def removeAllMeta(self):
		if not self.matObject.remove_all():
			raise Exception("Error removing metadata")
		self.autoMetaCleaned = True
		self.checkState()

	def makeCopy(self, pathOrig, pathNew):
		logging.debug("Copying file from " + pathOrig + " to " + pathNew)
		shutil.copyfile(str(pathOrig), str(pathNew))

	def selfCopy(self):
		self.makeCopy(self.filePath, self.outputPath + '/' + self.origName)

	def selfRemove(self):
		logging.debug("Removing " + self.filePath)
		os.remove(self.filePath)


	def autoClean(self):
		logging.debug("Auto cleaning file...")
		success = False
		if self.type == "Pdf":
			success = self.personalData.pdata.coverAll()
			if success:
				self.autoPersonalCleaned = True
		elif self.type in ["Jpeg", "Png"]:
			success = self.personalData.pdata.blurAll()

		if self.personalData is not None:
			self.personalData.pdata.doCommit()

		self.refreshMetadata()
		self.removeAllMeta()
		self.refreshMetadata()
		
		logging.debug("Done auto cleaning!")

	@staticmethod
	def newName(origName, ext):
		origName = str(origName)
		lastDot = string.rfind(origName, ".")
		if lastDot == -1:
			lastDot = len(origName)
		return QtCore.QString(origName[:lastDot] + ext + origName[lastDot:])

	@staticmethod
	def tempName(fileName):
		tempDir = tempfile.mkdtemp()
		return QtCore.QString(tempDir + '/' + fileName)


	@staticmethod
	def changeExt(fname, newExt):
		fname = str(fname)
		ind = fname.rindex('.')
		fname = fname[:ind+1] + newExt
		return QtCore.QString(fname)

	@staticmethod
	def check_path(inputF, outputF):
		infoI = QtCore.QFileInfo(inputF)
		infoO = QtCore.QFileInfo(outputF)

		pathI = infoI.canonicalFilePath()
		pathO = infoO.canonicalFilePath()

		if pathI in pathO:
			return False
		return True

	@staticmethod
	def changeBase(path, newbase):
		fname = path.split('/')[-1]
		return newbase + '/' + fname

		        
