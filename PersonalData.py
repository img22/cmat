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
import popplerqt4
import pdfrw

class PersonalData:
	"""
		Represents all visible, non-metadata
		identity revealing information in a file
	"""
	def __init__(self, fileName, fileType):

		# If file is an image, detect all faces
		if fileType in ["Jpeg", "Png"]:
			self.dataType = 'Faces'
			self.data = Faces(fileName)

		# All Text based files
		else:
			self.dataType = 'Strings'
			self.data = Strings(fileName, fileType)

		# TODO support wav, audio video files

	def getIssues(self):
		return self.data

	def fixData(self, index):
		"""
			Given some index, fixes the personal
			data at that index
		"""
		return self.data.fix(index)




class Faces:
	"""
		Detect Faces from image files
	"""
	def __init__(self, filePath):
		self.path = filePath
		self.trainingData = "Resources/haarcascade_frontalface_alt.xml"
		self.faces = self.detectFaces()

	def detectFaces(self):

		# Read the file
		image = cv2.imread(str(self.path))

		# Specify the trained cascade classifier
		face_cascade_name = self.trainingData

		# Create a cascade classifier
		face_cascade = cv2.CascadeClassifier()

		# Load the specified classifier
		face_cascade.load(face_cascade_name)

		#Preprocess the image
		grayimg = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
		grayimg = cv2.equalizeHist(grayimg)

		#Run the classifiers
		return face_cascade.detectMultiScale(grayimg, 1.1, 2, 0|cv2.cv.CV_HAAR_SCALE_IMAGE, (30, 30))

	def fix(self, faceind):

		facepos = faces[faceind]

		if len(self.faces) != 0 and facepos in self.faces:
			image = cv2.imread(str(self.filePath))
			x, y, w, h = [ v for v in facepos ]

	        sub_face = image[y:y+h, x:x+w]
	        sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
	        image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face

		cv2.imwrite(str(self.filePath), image)
		logging.debug("Done blurring " + str(self.filePath))
		return True


class Strings(QObject):
	"""
		Detect personal data from text redeable file
	"""
	def __init__(self, filePath, fileType):
		self.path = filePath
		self.strings = []

		if fileType == 'Text':
			self.processTxt()
		elif fileType == 'PDF':
			self.processPdf()

	def processTxt(self):
		"""
			Opens and searches for private info in a
			text file
		"""
		try:
			txtFile = open(self.path, 'r')
			line = txtFile.readline()
			while line != "":
				line = txtFile.readline()
				self.processString(line, 0)
			txtFile.close()
		except Exception:
			logging.debug("Exception in processTxt")

	def processPdf(self):
		"""
			Opens and searches for private info in a
			PDF file
		"""
		pdfDoc = popplerqt4.Poppler.Document.load(filePath)
		for i in range(0, pdfDoc.numPages()):
			self.processPdfString(pdfDoc.page(i), i)


	def matches(self, string):
		"""
			Does string match the personal info
			regex
		"""
		# TODO implement an actual reg ex for names,
		# places, etc
		return True;


	def processString(self, string, page):
		"""
			Given a string chunk form a file
			runs Reg Exp to detect private info and append
			a marker to the list 'strings'
		"""
		allWords = string.split(' ')
		for w in allWords:
			if self.matches(w):
				sr = SingleString(w, string.index(w), page)
				self.strings.append(sr)

	def processPdfString(self, pdfPage, pageNum):
		"""
			Similar to processString but for pdfs, appends
			a set of rectangles where suspicious words are found
		"""
		string = str(pdfPage.text(None))
		allWords = string.split(' ')
		for w in allWords:
			if self.matches(w):
				for rec in pdfPage.search():
					self.strings.append(rec)


	def fixTxt(self, ind):
		"""
			Replaces each occurance of strings in 
			self.strings with XXXX in the given text file
		"""
		try:
			with open(self.path, 'wr') as txtFile:
				pos = self.strings[ind].location
				oldStr = self.strings[ind].string

				txtFile.seek(ind, 0)
				for i in range(0, len(oldStr)):
					txtFile.write('X')
		except Exception:
			logging.error("Exception in fixTxt")

	def fixPdf(self, ind):
		"""
			Replaces each occurance of strings in 
			self.strings with a dark rectangles
		"""
		pass




	def fix(self, ind):
		if fileType == 'Text':
			self.fixTxt(ind)
		elif fileType == 'PDF':
			self.fixPdf(ind)




class SingleString:
	"""
		Represents a single string that has been
		found in a file as identity revealing
	"""
	def __init__(self, string, location, page):
		self.string = string
		self.location = location
		self.page = page

	def __init__(self, page, obj):
		self.page = page
		self.object = obj
