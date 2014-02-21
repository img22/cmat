from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject
from MAT import mat
from MAT import strippers
import logging
import cv2
from math import sqrt
"""
	A class to represent a file dragged into the 
	workspace of cmat
"""

class AddedFile(QObject):

	#signal to emit when file is clean
	fileCleaned = QtCore.pyqtSignal(QtCore.QString)

	def __init__(self, name, path, isfile, sz, parent):

		super(AddedFile, self).__init__()

		#check the file exists
		if not QtCore.QFileInfo(path).exists():
			raise Exception("No such file or directory!" + path)

		self.fileName = name
		self.filePath = path
		self.isFile = isfile
		self.fileSize = sz
		self.allMetadata = []
		self.parent = parent
		self.type = ""
		self.supported = True
		self.matObject = None

		#Face region if the file is image, and contains faces
		self.faces = None
		
	def getAllMetadata(self):
		if self.isFile:
			#TODO make sure filePath + -old does not exist
			self.allMetadata = []
			logging.debug("Extracting metadata for " + self.filePath)
			self.matObject = mat.create_class_file(str(self.filePath), str(self.filePath + "-old"), add2archive=True,
                low_pdf_quality=True)
			self.type = self.matObject.__class__.__name__
			if self.matObject is None:
				logging.debug(self.filePath + " is unsupported!")
				self.allMetadata.append(-1)
				self.supported = False
				self.checkState()
				return self.allMetadata
				
			metaDict = self.matObject.get_meta()
			for key in metaDict.keys():
				logging.debug("Found metadata header: " + key)
				self.allMetadata.append([key, metaDict[key]])
		else:
			self.allMetadata.append(-1)

		self.checkState()

		if self.type in ["JpegStripper", "PngStripper"]:
			self.detectFaces()
		return self.allMetadata

	def refreshMetadata(self):
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

	def detectFaces(self):
		image = cv2.imread(str(self.filePath))

		# Specify the trained cascade classifier
		face_cascade_name = "/home/accts/img22/Desktop/haarcascade_frontalface_alt.xml"

		# Create a cascade classifier
		face_cascade = cv2.CascadeClassifier()

		# Load the specified classifier
		face_cascade.load(face_cascade_name)

		#Preprocess the image
		grayimg = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
		grayimg = cv2.equalizeHist(grayimg)

		#Run the classifiers
		faces = face_cascade.detectMultiScale(grayimg, 1.1, 2, 0|cv2.cv.CV_HAAR_SCALE_IMAGE, (30, 30))
		self.faces = faces

	def blurFace(self, facepos):

		if len(self.faces) != 0 and facepos in self.faces:
			image = cv2.imread(str(self.filePath))
			x, y, w, h = [ v for v in facepos ]

			# get the rectangle img around all the faces
	        # cv2.rectangle(image, (x,y), (x+w,y+h), (255,255,0), 1)
	        sub_face = image[y:y+h, x:x+w]
	        # apply a gaussian blur on this new recangle image
	        sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
	        # merge this blurry rectangle to our final image
	        image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face

		# cv2.imshow("Detected face", result_image)
		#self.faces.remove(facepos)
		cv2.imwrite(str(self.filePath), image)
		logging.debug("Done blurring " + str(self.filePath))
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

		        