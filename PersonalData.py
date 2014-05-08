# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject
from MAT import mat
from MAT import strippers
from PdataMatch import PdataMatch
import logging
import cv2
from math import sqrt
import copy
import string
import os
import shutil
import popplerqt4
import pdfrw
import re

class PdfPersonalData():
	"""
		Represents all visible, non-metadata
		identity revealing text in a pdf
	"""
	def __init__(self, filePath):
		self.path = filePath
		self.pdata = Strings(filePath, 'Pdf')

	def clearMarks(self):
		"""
			Clears red marks from rendered pages
		"""
		self.pdata.renderPages(markRed=False)

	def isClean(self):
		"""
			Checks if there are any personal 
			data issues
		"""
		for i in range(len(self.pdata.badRects)):
			for j in range(len(self.pdata.badRects[i])):
				if not self.pdata.badRects[i][j].marked:
					return False
		return True


class ImgPersonalData():
	"""
		Represents all visible, non-metadata
		identity revealing information in an image
	"""
	def __init__(self, filePath):
		self.path = filePath
		self.pdata = Faces(filePath)

	def clearMarks(self):
		"""
			Clears red marks from faces
		"""
		self.pdata.detectFaces(markRed=False)

	def isClean(self):
		"""
			Checks if there are any personal 
			data issues
		"""
		for br in self.pdata.badRects:
			if not br.marked:
				return False
		return True




class Faces:
	"""
		Represents an image file with faces detected
	"""
	def __init__(self, filePath):
		self.path = filePath
		self.trainingData = "Resources/haarcascade_frontalface_alt.xml"
		self.image = None
		self.cvImage = None
		self.badRects = []
		self.facesBackup = []
		self.detectFaces()

	def doBackup(self):
		for br in self.badRects:
			x, y, w, h = [ v for v in br.obj ]
			self.facesBackup.append((br.obj, copy.deepcopy(self.cvImage[y:y+h, x:x+w])))

	def loadBackup(self):
		self.reloadFaces(self.facesBackup)

	def doCommit(self):
		self.facesBackup = []
		self.refreshImage()


	def detectFaces(self, markRed=True):
		"""
			Detect faces, show them in red
		"""

		# Read the file
		image = cv2.imread(str(self.path))
		self.cvImage = image

		# load the training data
		cascade = cv2.CascadeClassifier(self.trainingData)

		# Run the classifiers
		faces = cascade.detectMultiScale(image, 1.3, 3, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
		for f in faces:
			x, y, w, h = [ v for v in f ]
			faceRect = QtCore.QRectF(x, y, w, h)
			br = BadRect(faceRect, 1, obj=f)
			self.badRects.append(br)

		qimage = QtGui.QImageReader(self.path).read()
		self.image = qimage

		if markRed:
			self.renderImage()

	def renderImage(self):

		# Store face locations as bad rectangles,
		# draw them on the image
		painter = QtGui.QPainter(self.image)
		painter.setPen(QtCore.Qt.red)
		painter.begin(self.image)
		for br in self.badRects:
			logging.debug(br.obj)
			x, y, w, h = [v for v in br.obj]
			rect = QtCore.QRect(x, y, w, h)
			painter.drawRect(rect)
		painter.end()

	def blurOne(self, x, y):
		found = False
		for br in self.badRects:
			if br.contains(QtCore.QPoint(x, y), 0):
				self.blurFace(br)
				found = True
		if found:
			self.refreshImage()
		return found

	def blurFace(self, br):
		x, y, w, h = [ v for v in br.obj ]
		face = self.cvImage[y:y+h, x:x+w]
		face = cv2.GaussianBlur(face,(33, 33), 30)
		self.cvImage[y:y+h, x:x+w] = face
		br.marked = True

	def reloadFaces(self, backup):
		for f in backup:
			x, y, w, h = [ v for v in f[0] ]
			self.cvImage[y:y+h, x:x+w] = f[1]
		self.refreshImage()


	def blurAll(self):
		for br in self.badRects:
			self.blurFace(br)
		self.refreshImage()
		return True
		

	def refreshImage(self):
		cv2.imwrite(str(self.path), self.cvImage)
		self.image = QtGui.QImageReader(self.path).read()


	def getDocSize(self):
		return QtCore.QSize(self.image.width(), self.image.height())

	# def fix(self, faceind):

	# 	facepos = faces[faceind]

	# 	if len(self.faces) != 0 and facepos in self.faces:
	# 		image = cv2.imread(str(self.filePath))
	# 		x, y, w, h = [ v for v in facepos ]

	#         sub_face = image[y:y+h, x:x+w]
	#         sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
	#         image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face

	# 	cv2.imwrite(str(self.filePath), image)
	# 	logging.debug("Done blurring " + str(self.filePath))
	# 	return True


class Strings():
	"""
		Detect personal data from text redeable file
	"""
	def __init__(self, filePath, fileType):
		self.path = filePath
		self.pdfDoc = None
		self.strings = []
		self.pdfImgs = []
		self.badRects = []
		self.badRectsCp = []
		self.pageOffset = []
		self.pdataMatch = PdataMatch()
		self.maxDocHeight = 0
		self.maxDocWidth = 0

		if fileType == 'Text':
			self.processTxt()
		elif fileType == 'Pdf':
			self.processPdf()

	def doBackup(self):
		self.badRectsCp = []
		logging.debug("Backing up...")
		for i in range(len(self.badRects)):
			self.badRectsCp.append([])
			for bc in self.badRects[i]:
				self.badRectsCp[i].append(BadRect(None, None, bc))
		logging.debug("Done backing up")


	def loadBackup(self):
		for i in range(len(self.badRects)):
			for j in range(len(self.badRects[i])):
				print self.badRects[i][j], self.badRectsCp[i][j]
		self.badRects = self.badRectsCp

	def doCommit(self):
		doc = QtGui.QTextDocument()
		cursor = QtGui.QTextCursor(doc)
		logging.debug("Commiting changes to file...")
		for i in range(0, len(self.pdfImgs)):
			logging.debug("Inserting page " + str(self.pdfImgs[i].width()))
			doc.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(str(i)), QtCore.QVariant(self.pdfImgs[i]))
			imageFormat = QtGui.QTextImageFormat()
			imageFormat.setWidth(self.pdfImgs[i].width())
			imageFormat.setHeight(self.pdfImgs[i].height())
			imageFormat.setName(QtCore.QString(str(i)))
			cursor.insertImage(imageFormat)

		PdataUtils.printToPdf(doc, QtCore.QSizeF(self.maxDocWidth, self.maxDocHeight), self.path)

		self.badRectsCp = self.badRects


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
			PDF file, then renders pages
		"""
		self.pdfDoc = popplerqt4.Poppler.Document.load(self.path)
		for i in range(0, self.pdfDoc.numPages()):
			# Store all bad areas in badRects
			self.badRects.append([])
			self.badRects[i] += self.processPdfString(self.pdfDoc.page(i), i)

		self.renderPages()
			

	def renderPages(self, page=-1, cover=False, clear=False, markRed=True):
		"""
			Renders pages into images
		"""
		# Clear the pages unless rendering one page
		if page == -1:
			self.pdfImgs = []

		for i in range(0, self.pdfDoc.numPages()):

			# Skip page that is not 'page' unless page is -1
			if page != -1:
				if i != page:
					continue

			# Render image
			pageImg = self.pdfDoc.page(i).renderToImage(360, 360, -1, -1, -1, -1)
			if pageImg.height() > self.maxDocHeight:
				self.maxDocHeight = pageImg.height()
			if pageImg.width() > self.maxDocWidth:
				self.maxDocWidth = pageImg.width()
			
			self.pageOffset.append(0)
			self.pageOffset[i] = pageImg.height()
		   
			# Draw bad rects in red on the page
			painter = QtGui.QPainter(pageImg)
			painter.setPen(QtCore.Qt.red)
			painter.begin(pageImg)
			for r in self.badRects[i]:
				if cover:
					r.mark()
				if clear:
					r.unmark()
				if r.marked:
					painter.fillRect(r.rect, QtGui.QBrush(QtCore.Qt.SolidPattern))
				elif markRed:
					painter.drawRect(r.rect)
			painter.end()

		    # Store the processed images
			if page == -1:
				self.pdfImgs.append(pageImg)
			else:
				try:
					self.pdfImgs[i] = pageImg
				except Exception:
					logging.error("No page at index " + str(i))



	def processString(self, string, page):
		"""
			Given a string chunk form a file
			runs Reg Exp to detect private info and append
			a marker to the list 'strings'
		"""

		# Regex for proper names
		regex = '[A-Z][a-zA-Z|.]+'
		patt = re.compile(regex)
		matches  = re.findAll(patt, string)
		# for w in allWords:
		# 	if self.matches(w):
		# 		sr = SingleString(w, string.index(w), page)
		# 		self.strings.append(sr)

	def processPdfString(self, pdfPage, pageNum):
		"""
			Similar to processString but for pdfs, appends
			a set of rectangles where suspicious words are found
		"""
		string = unicode(pdfPage.text(QtCore.QRectF())).encode('utf-8')
		allBadRects = []
		logging.debug("PdataMatch " + str(self.pdataMatch.allRegExps))
		for regex in self.pdataMatch.allRegExps:
			if len(regex) != 0:
				logging.debug("Matching " + regex)
				patt = re.compile(regex)
				matches  = re.findall(patt, string)
				for w in matches:
					# if self.matches(w):
					# logging.debug('Searching ' + w)
					location = QtCore.QRectF()
					pdfPage.search(QtCore.QString(w), location, pdfPage.SearchDirection(0), pdfPage.SearchMode(0), pdfPage.Rotation(0))
					newBadRect = BadRect(location, pageNum, scale=5.0)
					allBadRects.append(newBadRect)
		return allBadRects


	def coverAll(self):
		self.renderPages(cover=True)
		return True

	def coverOne(self, x, y):
		p = QtCore.QPointF(float(x), float(y))
		found = False
		for i in range(0, len(self.badRects)):
			for rec in self.badRects[i]:
				# logging.debug("Checking " + str(rec) + " against " + str(p))
				if rec.contains(p, self.pageOffset[rec.page]):
					logging.debug("Found rectangle " + str(rec))
					rec.mark()
					self.renderPages(page=i, cover=False)
					found = True
					break
		return found

	def getDocSize(self):
		return QtCore.QSize(self.maxDocWidth, self.maxDocHeight)
				

class BadRect:
	def __init__(self, rect, page, badrect=None, obj=None, scale=-1):
		if badrect != None:
			self.rect = badrect.rect
			self.marked = badrect.marked
			self.page = badrect.page
		else:
			self.scaleFactor = 1
			if scale != -1:
				self.scaleFactor = scale
			if obj != None:
				self.obj = obj
			self.rect = self.scale(rect)
			self.marked = False
			self.page = page
		
	
	def mark(self):
		self.marked = True

	def unmark(self):
		self.marked = False

	def contains(self, point, offset):
		if self.page != 0:
			point = QtCore.QPointF(point.x(), point.y() - offset)
			logging.debug("New point " + str(point) + " vs " + str(self.rect))

		return self.rect.contains(point)

	def scale(self, rect):
		xpos = rect.x() * self.scaleFactor
		ypos = rect.y() * self.scaleFactor
		width = rect.width() * self.scaleFactor
		height = rect.height() * self.scaleFactor
		return QtCore.QRectF(xpos, ypos, width, height)

	def __str__(self):
		return str(self.rect) + " Marked? " + str(self.marked)



class PdataUtils:

	@staticmethod
	def printToPdf(doc, papersize, outfile):
		printer = QtGui.QPrinter()  
		printer.setPageSize(QtGui.QPrinter.Letter)
		printer.setResolution(96)
		printer.setPaperSize(papersize, QtGui.QPrinter.Point)
		printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
		printer.setOutputFileName(outfile)
		printer.setFullPage(True)
		doc.print_(printer)
