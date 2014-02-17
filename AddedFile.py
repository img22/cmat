from PyQt4 import QtCore
from MAT import mat
from MAT import strippers
import logging
"""
	A class to represent a file dragged into the 
	workspace of cmat
"""

class AddedFile:
	def __init__(self, name, path, isfile, sz, parent):

		#check the file exists
		if not QtCore.QFileInfo(path).exists():
			raise Exception("No such file or directory!" + path)

		self.fileName = name
		self.filePath = path
		self.isFile = isfile
		self.fileSize = sz
		self.allMetadata = []
		self.parent = parent
		self.supported = True
		self.matObject = None
		
	def getAllMetadata(self):
		if self.isFile:
			#TODO make sure filePath + -old does not exist
			logging.debug("Extracting metadata for " + self.filePath)
			self.matObject = mat.create_class_file(str(self.filePath), str(self.filePath + "-old"), add2archive=True,
                low_pdf_quality=True)
			if self.matObject is None:
				logging.debug(self.filePath + " is unsupported!")
				self.allMetadata.append(-1)
				self.supported = False
				return self.allMetadata
				
			metaDict = self.matObject.get_meta()
			for key in metaDict.keys():
				logging.debug("Found metadata header: " + key)
				self.allMetadata.append([key, metaDict[key]])
		else:
			self.allMetadata.append(-1)
		return self.allMetadata

	def removeMetadata(mname):
		pass
