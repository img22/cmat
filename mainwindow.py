# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from CQTreeView import CQTreeView
import logging

#Debug
logging.basicConfig(filename="cmatlog.txt", level=logging.DEBUG)
#Prod
#logging.basicConfig(filename="cmatlog.txt", level=logging.CRITICAL)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(700, 500)

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.centralWidgetGridLayout = QtGui.QGridLayout(self.centralWidget)
        self.centralWidgetGridLayout.setObjectName(_fromUtf8("centralWidgetGridLayout"))

        self.gridLayoutForAll = QtGui.QGridLayout()
        self.gridLayoutForAll.setObjectName(_fromUtf8("gridLayoutForAll"))

        #Files box containing all the files
        self.filesBox = QtGui.QGroupBox(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filesBox.sizePolicy().hasHeightForWidth())
        self.filesBox.setSizePolicy(sizePolicy)
        self.filesBox.setMinimumSize(QtCore.QSize(300, 300))
        self.filesBox.setObjectName(_fromUtf8("filesBox"))
        self.vLayoutFilesBox = QtGui.QVBoxLayout(self.filesBox)
        self.vLayoutFilesBox.setObjectName(_fromUtf8("verticalLayout"))
        self.vLayoutFilesBox.setContentsMargins(5, 5, 5, 5)

        #Tree widget with dirs and files in the filebox
        self.filesList = CQTreeView(self.filesBox)
        self.filesList.setObjectName(_fromUtf8("filesList"))
        self.filesList.setAcceptDrops(True)
        self.filesList.setColumnCount(2)
        self.filesList.setHeaderLabels(["File Name", "Size"])
        #vlayout for the files and dirs
        self.vLayoutFilesBox.addWidget(self.filesList)
        self.gridLayoutForAll.addWidget(self.filesBox, 0, 0, 1, 1)
        
        #The tab area containing the metadata and content tabs
        self.tabArea = QtGui.QTabWidget(self.centralWidget)
        self.tabArea.setMinimumSize(QtCore.QSize(300, 300))
        self.tabArea.setObjectName(_fromUtf8("tabArea"))

        # The first tab
        self.allMetadata = QtGui.QWidget()
        self.allMetadata.setObjectName(_fromUtf8("All Metadata"))
        self.vLayoutTab1 = QtGui.QVBoxLayout(self.allMetadata)
        self.vLayoutTab1.setObjectName(_fromUtf8("vLayoutTabArea"))
        self.vLayoutTab1.setContentsMargins(5, 5, 5, 5)

        #Table of metadata on the first tab
        self.metadataList = QtGui.QTableWidget(self.allMetadata)
        self.metadataList.setColumnCount(2)
        header = self.metadataList.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)
        self.metadataList.setHorizontalHeaderLabels(["Metadata Header", "Value"])
        self.metadataList.setObjectName(_fromUtf8("metadataList"))

        #File not found label for unsupported file types
        self.fileNotSupported = QtGui.QLabel(self.allMetadata)
        fNotSupportedImage = QtGui.QImage()
        fNotSupportedImage.load("Resources/fileNotFound-2.png")
        self.fileNotSupported.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.fileNotSupported.setPixmap(QtGui.QPixmap.fromImage(fNotSupportedImage))
        self.fileNotSupported.hide()


        # self.splitter = QtGui.QSplitter(self.centralWidget)
        # self.splitter.addWidget(self.filesBox)
        # self.splitter.addWidget(self.allMetadata)

        self.vLayoutTab1.addWidget(self.metadataList)
        self.vLayoutTab1.addWidget(self.fileNotSupported)
        self.tabArea.addTab(self.allMetadata, _fromUtf8(""))

        # The second tab
        self.allPersonalData = QtGui.QWidget()
        self.allPersonalData.setObjectName(_fromUtf8("All Personal Data"))
        self.vLayoutTab2 = QtGui.QVBoxLayout(self.allPersonalData)
        self.vLayoutTab2.setObjectName(_fromUtf8("vLayoutTab2"))
        self.vLayoutTab2.setContentsMargins(5, 5, 5, 5)

        # Text area on the second tab
        self.personalDataList = QtGui.QTextEdit(self.allPersonalData)
        self.personalDataList.setReadOnly(True)
        self.personalDataList.setObjectName(_fromUtf8("personalDataList"))

        self.vLayoutTab2.addWidget(self.personalDataList)
        self.tabArea.addTab(self.allPersonalData, _fromUtf8(""))

        # Set the focus of the tab area on the first tab
        self.tabArea.setCurrentIndex(0)

        # Add the tab area to the grid
        self.gridLayoutForAll.addWidget(self.tabArea, 0, 2, 1, 1)

        # The details section at the bottom
        self.detailsBox = QtGui.QGroupBox(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailsBox.sizePolicy().hasHeightForWidth())
        self.detailsBox.setSizePolicy(sizePolicy)
        self.detailsBox.setMaximumHeight(160)
        self.detailsBox.setObjectName(_fromUtf8("DetailsBox"))
        self.vLayoutDetailsBox = QtGui.QVBoxLayout(self.detailsBox)
        self.vLayoutDetailsBox.setContentsMargins(5, 5, 5, 5)
        self.vLayoutDetailsBox.setObjectName(_fromUtf8("vLayoutDetailsBox"))

        # Add test area to the details box
        self.detailsDisplay = QtGui.QTextEdit(self.detailsBox)
        self.detailsDisplay.setReadOnly(True)
        
        # Add it to the layout
        self.vLayoutDetailsBox.addWidget(self.detailsDisplay)
        self.gridLayoutForAll.addWidget(self.detailsBox, 1, 0, 1, 3)

        # Add layouts in the cetral widget
        self.centralWidgetGridLayout.addLayout(self.gridLayoutForAll, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        # The status bar and menu bars
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAdd = QtGui.QAction(MainWindow)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.actionRemove = QtGui.QAction(MainWindow)
        self.actionRemove.setObjectName(_fromUtf8("actionRemove"))
        self.actionCheck_Content = QtGui.QAction(MainWindow)
        self.actionCheck_Content.setObjectName(_fromUtf8("actionCheck_Content"))
        self.actionCheck_Metadata = QtGui.QAction(MainWindow)
        self.actionCheck_Metadata.setObjectName(_fromUtf8("actionCheck_Metadata"))
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionRemove)
        self.toolBar.addAction(self.actionCheck_Content)
        self.toolBar.addAction(self.actionCheck_Metadata)

        #file dialog to appear when add is clicked
        self.fDialog = QtGui.QFileDialog(self.centralWidget, caption="Pick a file or directory")

        self.retranslateUi(MainWindow)
        self.tabArea.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connectSignals()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.filesBox.setTitle(_translate("MainWindow", "Files", None))
        self.tabArea.setTabText(self.tabArea.indexOf(self.allMetadata), _translate("MainWindow", "All Metadata", None))
        self.tabArea.setTabText(self.tabArea.indexOf(self.allPersonalData), _translate("MainWindow", "Personal Data", None))
        self.detailsBox.setTitle(_translate("MainWindow", "Details", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionAdd.setText(_translate("MainWindow", "Add", None))
        self.actionRemove.setText(_translate("MainWindow", "Remove", None))
        self.actionCheck_Content.setText(_translate("MainWindow", "Auto Fix Content", None))
        self.actionCheck_Metadata.setText(_translate("MainWindow", "Auto Remove Metadata", None))


    def connectSignals(self):
        self.actionAdd.triggered.connect(self.handleActionAdd)
        #self.fDialog.fileSelected.connect(self.addFileToTable)
        #QtCore.QObject.connect(self.filesList, QtCore.SIGNAL('fileClicked'), self.displayMetadata)
        self.filesList.fileClicked.connect(self.displayMetadata)
        self.actionRemove.triggered.connect(self.handleRemoveFile)
        #self.filesList.newFile.connect(self.acceptNewFile)
    
    def writeDetails(self, message):
		self.detailsDisplay.append(message)


    def handleActionAdd(self):
        self.fDialog.show()

    def handleRemoveFile(self):
        for w in self.filesList.selectedItems():
            self.filesList.removeFile(w.text(2))
        

    def receiveFileFromDialog(self, path):
        #self.filesList.addItem(fileName.section('/', -1))
        pass

    def displayMetadata(self, metadata):
        #Unsupported types return -1 as metadata
        self.writeDetails("Listing metadata...")
        if metadata[0] == -1:
            self.metadataList.hide()
            self.fileNotSupported.show()
            self.writeDetails("\tFile type not supported")

        #Supported types have list of metadata
        else:
            self.fileNotSupported.hide()
            self.metadataList.show()
            self.metadataList.clear()
            self.metadataList.setRowCount(0)
            self.metadataList.setHorizontalHeaderLabels(["Metadata Header", "Value"])
            i = self.metadataList.rowCount()
            for row in metadata:
                metaName = QtGui.QTableWidgetItem(row[0])
                metaValue = QtGui.QTableWidgetItem(row[1])
                metaName.setFlags(metaName.flags() & (~QtCore.Qt.ItemIsEditable))
                metaValue.setFlags(metaValue.flags() & (~QtCore.Qt.ItemIsEditable))
                self.metadataList.insertRow(i)
                self.metadataList.setItem(i, 0, metaName)
                self.metadataList.setItem(i, 1, metaValue)
                i += 1
                self.writeDetails(metaName + ": " + mtaValue)

    def acceptNewFile(self):
        pass
