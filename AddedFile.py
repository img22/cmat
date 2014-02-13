from PyQt4 import QtCore
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

	def getAllMetadata(self):
		self.allMetadata = [["Metadata1", "Value1"]]
		return self.allMetadata

	def removeMetadata(mname):
		pass