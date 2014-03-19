from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject
from MAT import mat
from MAT import strippers
import logging
import cv2
from math import sqrt
import string
import os
import shutil
from PersonalData import PersonalData
"""
	A class to represent a file dragged into the 
	workspace of cmat
"""

class AddedFile(QObject):

	#signal to emit when file is clean
	fileCleaned = QtCore.pyqtSignal(QtCore.QString)

	def __init__(self, name, path, isfile, sz, parent):
		"""
			Initialize an AddedFile instance, this represents
			a new file dragged in. It contains all metadata and 
			prsonal info in the file.
		"""
		super(AddedFile, self).__init__()

		#check the file exists
		if not QtCore.QFileInfo(path).exists():
			raise Exception("No such file or directory!" + path)

		# create a new file to work with, new file has -clean tag
		if isfile:
			self.fileName = self.newName(str(name))
			self.filePath = self.newName(str(path))
		else:
			self.fileName = name
			self.filePath = path

		# basic file infor
		self.origPath = path
		self.isFile = isfile
		self.fileSize = sz
		self.parent = parent
		self.type = ""
		self.supported = True
		self.matObject = None

		# all metadata in the file
		self.allMetadata = []
		self.hasMetadata = True
		
		# all personal info in the file
		self.personalData = None

		#Copy the given file to the -clean file
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

			if len(metaDict.keys()) == 0:
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
		self.personalData = PersonalData(self.filePath, self.type)
		

	def refreshMetadata(self):
		self.matObject = mat.create_class_file(str(self.filePath), str(self.filePath), add2archive=True,
                low_pdf_quality=True)
		if len(self.allMetadata) != 0 or self.allMetadata[0] != -1:
			metaDict = self.matObject.get_meta()
			for key in metaDict.keys():
				logging.debug("Found metadata header: " + key)
				self.allMetadata.append([key, metaDict[key]])
		return self.allMetadata

	def cleanMeta(self, mname):
		cleanError = mname + " could not be removed! This means the metadata can not be removed separately! Try Auto Removing metadata from the file."
		if not self.matObject.remove_meta(str(mname)):
			raise Exception(cleanError)
		self.checkState()


	def blurAll(self):
		for f in self.faces:
			self.blurFace(f)


	def checkState(self):
		if (self.allMetadata is None 
			or len(self.allMetadata) == 0 
			or self.allMetadata[0] == -1) and (self.faces is None 
			or len(self.faces) == 0):

			logging.debug("File is clean! Emitting clean signal...")
			self.fileCleaned.emit(self.filePath)

	def removeAllMeta(self):
		if not self.matObject.remove_all():
			raise Exception("Error removing metadata")
		self.checkState()

	def makeCopy(self, pathOrig, pathNew):
		shutil.copyfile(str(pathOrig), str(pathNew))

	def newName(self, origName):
		lastDot = string.rfind(origName, ".")
		if lastDot == -1:
			lastDot = origName.length
		return QtCore.QString(origName[:lastDot] + "-clean" + origName[lastDot:])

		        