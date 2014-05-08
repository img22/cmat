# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from CQTreeView import CQTreeView
from CQTableWidget import CQTableWidget
from CQLabel import CQLabel
from CQFileDialog import CQFileDialog
from CQTextEdit import CQTextEdit
from PdataMatch import PdataMatch
from AddedFile import AddedFile
import logging
import popplerqt4
from MAT import mat
from monitor import DirMonitor
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
    def setupUi(self, MainWindow, inPath, outPath):
        MainWindow.setObjectName(_fromUtf8("CMAT (Manual Mode)"))
        MainWindow.resize(800, 500)

        self.mainWindow = MainWindow
        self.inputPath  = [inPath]
        self.outputPath = outPath

        self.autoMode = False

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
        self.filesBox.setMaximumWidth(400)
        self.filesBox.setObjectName(_fromUtf8("filesBox"))
        self.vLayoutFilesBox = QtGui.QVBoxLayout(self.filesBox)
        self.vLayoutFilesBox.setObjectName(_fromUtf8("verticalLayout"))
        self.vLayoutFilesBox.setContentsMargins(5, 5, 5, 5)

        #Tree widget with dirs and files in the filebox
        self.filesList = CQTreeView(self.filesBox, self, self.autoMode)
        self.filesList.setObjectName(_fromUtf8("filesList"))
        self.filesList.setAcceptDrops(True)
        self.filesList.setColumnCount(2)
        self.filesList.setHeaderLabels(["File Name", "Size"])
        #vlayout for the files and dirs
        self.vLayoutFilesBox.addWidget(self.filesList)
        self.gridLayoutForAll.addWidget(self.filesBox, 0, 0, 1, 1)

        # Monitor inPath
        self.dirMonitor = DirMonitor(str(self.inputPath[0]), self.filesList)
        self.dirMonitor.start()
        
        #The tab area containing the metadata and content tabs
        self.tabArea = QtGui.QTabWidget(self.centralWidget)
        self.tabArea.setEnabled(False)
        self.tabArea.setMinimumSize(QtCore.QSize(300, 300))
        self.tabArea.setObjectName(_fromUtf8("tabArea"))

        # The first tab
        self.allMetadata = QtGui.QWidget()
        self.allMetadata.setObjectName(_fromUtf8("All Metadata"))
        self.vLayoutTab1 = QtGui.QVBoxLayout(self.allMetadata)
        self.vLayoutTab1.setObjectName(_fromUtf8("vLayoutTabArea"))
        self.vLayoutTab1.setContentsMargins(5, 5, 5, 5)

        #Table of metadata on the first tab
        self.metadataList = CQTableWidget(0, 2, self.allMetadata)
        self.metadataList.setColumnCount(2)
        header = self.metadataList.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)
        self.metadataList.setHorizontalHeaderLabels(["Metadata Header", "Value"])
        self.metadataList.setObjectName(_fromUtf8("metadataList"))
        self.metadataList.setMouseTracking(True)

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
        self.personalDataList = CQTextEdit(self.allPersonalData)
        self.personalDataList.setReadOnly(True)
        self.personalDataList.setObjectName(_fromUtf8("personalDataList"))

        self.vLayoutTab2.addWidget(self.personalDataList)
        self.tabArea.addTab(self.allPersonalData, _fromUtf8(""))

        # Set the focus of the tab area on the first tab
        self.tabArea.setCurrentIndex(0)

        # Buttons on the second tab
        self.pDataCancelButton = QtGui.QPushButton('Cancel')
        self.pDataCommitButton = QtGui.QPushButton('Commit')
        self.pDataCancelButton.hide()
        self.pDataCommitButton.hide()
        self.pDataButtonsHLayout = QtGui.QHBoxLayout()
        self.pDataButtonsHLayout.addWidget(self.pDataCancelButton)
        self.pDataButtonsHLayout.addWidget(self.pDataCommitButton)
        self.vLayoutTab2.addLayout(self.pDataButtonsHLayout)
        

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
        self.detailsDisplay.setTabStopWidth(2)
        self.detailsDisplay.setFontFamily("\"Courier New\", Courier, monospace")
        self.detailsDisplay.setFontPointSize(8)
        
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
        # self.toolBar = QtGui.QToolBar(MainWindow)
        # self.toolBar.setObjectName(_fromUtf8("toolBar"))
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        # self.menuBar = QtGui.QMenuBar(MainWindow)

        self.fileMenu = self.mainWindow.menuBar().addMenu("File")
        self.metaMenu = self.mainWindow.menuBar().addMenu("Metadata")
        self.contentMenu = self.mainWindow.menuBar().addMenu("Content")
        self.settingsMenu = self.mainWindow.menuBar().addMenu("Settings")

        # self.menuBar.addMenu(self.fileMenu)
        # self.menuBar.addMenu(self.metaMenu)
        # self.menuBar.addMenu(self.contentMenu)

        self.actionAdd = QtGui.QAction(self.fileMenu)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))

        self.actionRemove = QtGui.QAction(self.fileMenu)
        self.actionRemove.setEnabled(False)
        self.actionRemove.setObjectName(_fromUtf8("actionRemove"))

        self.actionSave = QtGui.QAction(self.fileMenu)
        self.actionSave.setEnabled(False)
        self.actionRemove.setObjectName(_fromUtf8("actionSave"))

        self.fileMenu.addAction(self.actionAdd)
        self.fileMenu.addAction(self.actionRemove)
        self.fileMenu.addAction(self.actionSave)

        self.actionCheck_Content = QtGui.QMenu("Remove All", self.contentMenu)
        self.actionCheck_Content.setEnabled(False)
        self.actionCheck_Content.setObjectName(_fromUtf8("actionCheck_Content"))

        self.actionCheck_Content_auto = QtGui.QAction("Automatic", self.actionCheck_Content)
        self.actionCheck_Content_onebyone = QtGui.QAction("One-by-one", self.actionCheck_Content)
        self.actionCheck_Content_useblur = QtGui.QAction("Use blur tool", self.actionCheck_Content)
        self.actionCheck_Content_settings = QtGui.QAction("Settings...", self.actionCheck_Content)

        self.actionCheck_Content.addAction(self.actionCheck_Content_auto)
        self.actionCheck_Content.addAction(self.actionCheck_Content_onebyone)
        self.actionCheck_Content.addAction(self.actionCheck_Content_settings)

        self.contentMenu.addMenu(self.actionCheck_Content)

        self.actionCheck_Metadata = QtGui.QMenu("Remove All", self.metaMenu)
        self.actionCheck_Metadata.setEnabled(False)
        self.actionCheck_Metadata.setObjectName(_fromUtf8("actionCheck_Metadata"))

        self.actionCheck_Metadata_keep = QtGui.QAction("Keep File", self.actionCheck_Metadata)
        self.actionCheck_Metadata_recon = QtGui.QAction("Remake as PDF", self.actionCheck_Metadata)

        self.actionCheck_Metadata.addAction(self.actionCheck_Metadata_keep)
        self.actionCheck_Metadata.addAction(self.actionCheck_Metadata_recon)

        self.metaMenu.addMenu(self.actionCheck_Metadata)

        self.monitorMenu = QtGui.QAction("Monitor", self.settingsMenu)
        self.monitorPopUp = QtGui.QWidget(self.mainWindow)
        self.monitorPopUp.setWindowFlags(QtCore.Qt.Popup)
        self.monitorPopUpLabel1 = QtGui.QLabel("Change input and output directories.")
        self.monitorPopUpError = QtGui.QLabel("Invalid directory detected! Please correct!")
        self.monitorPopUpError.hide()

        self.monitorPopUpLabel2 = QtGui.QLabel("\nMonitored directories:")
        self.monitorPopUpInputDefault = QtGui.QLabel(self.inputPath[0])

        self.monitorPopUpLabel3 = QtGui.QLabel("Change monitored directories, comma separated:")
        self.monitorPopUpInput = QtGui.QLineEdit(self.monitorPopUp)
        self.monitorPopUpInputAdd = QtGui.QPushButton("Add", self.monitorPopUp)
        self.monitorPopUpInputAdd.setFixedWidth(100)

        self.monitorPopUpLabel4 = QtGui.QLabel("\nOutput directory:")
        self.monitorPopUpOutputDefault = QtGui.QLabel(self.outputPath)
        self.monitorPopUpLabel5 = QtGui.QLabel("Change output directory.\nDirectory must not be a subdirectory of any of the monitored directories.")
        self.monitorPopUpOutput = QtGui.QLineEdit(self.monitorPopUp)
        self.monitorPopUpOutputSet = QtGui.QPushButton("Set", self.monitorPopUp)
        self.monitorPopUpOutputSet.setFixedWidth(100)

        self.monitorPopUpLayout = QtGui.QVBoxLayout()
        self.monitorPopUpLabelLayout = QtGui.QVBoxLayout()
        self.monitorPopUpLayout.addWidget(self.monitorPopUpLabel1)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpError)
        self.monitorPopUpLabelLayout.addWidget(self.monitorPopUpLabel2)
        self.monitorPopUpLabelLayout.addWidget(self.monitorPopUpInputDefault)
        self.monitorPopUpLayout.addLayout(self.monitorPopUpLabelLayout)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpLabel3)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpInput)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpInputAdd)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpLabel4)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpOutputDefault)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpLabel5)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpOutput)
        self.monitorPopUpLayout.addWidget(self.monitorPopUpOutputSet)
        self.monitorPopUp.setLayout(self.monitorPopUpLayout)
        self.monitorPopUpLables = []
        self.monitorPopUpLables.append(self.monitorPopUpInputDefault)
        self.monitorPopUp.hide()

        self.settingsMenu.addAction(self.monitorMenu)

        # Mode of operation (default Manual)
        self.modeToggle = QtGui.QAction("Auto Mode", self.settingsMenu)
        self.settingsMenu.addAction(self.modeToggle)

        # self.toolBar.addAction(self.actionAdd)
        # self.toolBar.addAction(self.actionRemove)
        # self.toolBar.addAction(self.actionCheck_Content.menuAction())
        # self.toolBar.addAction(self.actionCheck_Metadata.menuAction())

        #file dialog to appear when add is clicked
        self.fDialog = CQFileDialog(self.centralWidget)

        # Settings pop up window
        self.pdataMatch = PdataMatch()
        self.settingsPopup = QtGui.QWidget(self.mainWindow)
        self.settingsPopup.setWindowFlags(QtCore.Qt.Popup)
        self.spLabelErr = QtGui.QLabel("Please correct your regular expression", self.settingsPopup)
        self.spLabelErr.hide()
        self.spLabel1 = QtGui.QLabel("Mark these strings or regular expressions (comma separated) in file:", self.settingsPopup)
        self.spLineEdit = QtGui.QLineEdit(self.settingsPopup)
        self.spLabel2 = QtGui.QLabel("Also mark the following:", self.settingsPopup)
        self.spProperNouns = QtGui.QCheckBox("Proper Nouns", self.settingsPopup)
        self.spProperNouns.setCheckState(True)
        self.spDates = QtGui.QCheckBox("Dates", self.settingsPopup)
        self.spPnums = QtGui.QCheckBox("Phone numbers", self.settingsPopup)
        self.spSSNs = QtGui.QCheckBox("Social security numbers", self.settingsPopup)
        self.spAdds = QtGui.QCheckBox("Addresses", self.settingsPopup)
        self.spPushBtn = QtGui.QPushButton("Set", self.settingsPopup)
        self.spPushBtn.setFixedWidth(100)
        self.settingsPopupLayout = QtGui.QVBoxLayout()
        self.settingsPopupLayout.addWidget(self.spLabelErr)
        self.settingsPopupLayout.addWidget(self.spLabel1)
        self.settingsPopupLayout.addWidget(self.spLineEdit)
        self.settingsPopupLayout.addWidget(self.spLabel2)
        self.settingsPopupLayout.addWidget(self.spProperNouns)
        self.settingsPopupLayout.addWidget(self.spDates)
        self.settingsPopupLayout.addWidget(self.spPnums)
        self.settingsPopupLayout.addWidget(self.spSSNs)
        self.settingsPopupLayout.addWidget(self.spAdds)
        self.settingsPopupLayout.addWidget(self.spPushBtn)
        self.settingsPopup.setLayout(self.settingsPopupLayout)
        self.settingsPopup.hide()

        self.retranslateUi(MainWindow)
        self.tabArea.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connectSignals()



    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("CMAT (Manual Mode)", "CMAT (Manual Mode)", None))
        self.filesBox.setTitle(_translate("Files", "Files", None))
        self.tabArea.setTabText(self.tabArea.indexOf(self.allMetadata), _translate("MainWindow", "All Metadata", None))
        self.tabArea.setTabText(self.tabArea.indexOf(self.allPersonalData), _translate("MainWindow", "Personal Data", None))
        self.detailsBox.setTitle(_translate("MainWindow", "Details", None))
        # self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionAdd.setText(_translate("MainWindow", "Add", None))
        self.actionRemove.setText(_translate("MainWindow", "Remove", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        # self.actionCheck_Content.setText(_translate("MainWindow", "Auto Fix Content", None))
        # self.actionCheck_Metadata.setText(_translate("MainWindow", "Auto Remove Metadata", None))


    def connectSignals(self):
        self.actionAdd.triggered.connect(self.handleActionAdd)
        self.actionRemove.triggered.connect(self.handleRemoveFile)
        self.actionSave.triggered.connect(self.handleActionSave)

        self.fDialog.filesSelected.connect(self.receiveFileFromDialog)
        #QtCore.QObject.connect(self.filesList, QtCore.SIGNAL('fileClicked'), self.displayMetadata)
        #self.filesList.fileClicked.connect(self.displayMetadata)
        self.filesList.imageFileClicked.connect(self.displayImageData)
        self.filesList.pdfFileClicked.connect(self.displayPdfData)
        self.filesList.otherFileClicked.connect(self.displayOtherData)
        #self.filesList.oneMetadataClear.connect(self.handleOneMetaClear)
        self.filesList.allMetadataClear.connect(self.handleAllMetaClear)
        self.filesList.operationFailed.connect(self.displayError)
        self.filesList.filesStartedLoading.connect(self.changeEnabled)
        self.filesList.filesFinishedLoading.connect(self.changeEnabled)

        self.metadataList.itemEntered.connect(self.metaCellEntered)
        self.metadataList.itemExited.connect(self.metaCellExited)

        self.actionCheck_Content_onebyone.triggered.connect(self.changeCursor)
        self.actionCheck_Content_auto.triggered.connect(self.hideAllPersonalData)

        self.actionCheck_Metadata_keep.triggered.connect(self.handleCleanMetadataKeep)
        self.actionCheck_Metadata_recon.triggered.connect(self.handleCleanMetadataRecon)
        self.actionCheck_Content_settings.triggered.connect(self.showPDataSettings)
        self.monitorMenu.triggered.connect(self.handleMonitorSettings)
        self.modeToggle.triggered.connect(self.handleModeToggle)

        self.spPushBtn.clicked.connect(self.setPdataSettings)
        self.pDataCommitButton.clicked.connect(self.handleCommit)
        self.pDataCancelButton.clicked.connect(self.handleCancel)
        self.monitorPopUpInputAdd.clicked.connect(self.handleMonitorInputAdd)
        self.monitorPopUpOutputSet.clicked.connect(self.handleMonitorOutputSet)

        #self.actionCheck_Content_keep.triggered.connect(self.handleCleanContentKeep)
        #self.actionCheck_Content_recon.triggered.connect(self.handleCleanContentRecon)

        #self.filesList.newFile.connect(self.acceptNewFile)
    
    def writeDetails(self, message):
		self.detailsDisplay.append(message)



    ############################################# 
    ###   Adding and removing files
    #############################################
    def handleActionAdd(self):
        """
            Shows add file dialog
        """
        self.fDialog.show()

    def receiveFileFromDialog(self, paths):
        """
            Receives file from file dialog
        """
        self.filesList.filesStartedLoading.emit(False)
        for p in paths:
           self.filesList.registerFile(None, QtCore.QString(p))
        self.filesList.filesFinishedLoading.emit(True)

    def handleRemoveFile(self):
        """
            Removes file from list
        """
        for w in self.filesList.selectedItems():
            self.filesList.removeFile(w.text(2))
        self.metadataList.clear()
        self.metadataList.setRowCount(0)
        self.metadataList.setHorizontalHeaderLabels(["Metadata Header", "Value"])
        self.personalDataList.clear()

    def handleActionSave(self):
        """
            Saves the selected file as it is
        """
        for w in self.filesList.selectedItems():
            self.filesList.saveFile(w.text(2))




    ############################################# 
    ###   Metadata operations
    #############################################

    def metaCellEntered(self, item):
        """
            Hover event over metadata table
        """
        # Add X button to the cell
        logging.debug("inserting X in " + str(item.row()) + ", " + str(item.column()))
        button = CQLabel(item.row(), item.column())
        deleteImg = QtGui.QImage()
        deleteImg.load("Resources/deleteIcon.png")
        button.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        button.setPixmap(QtGui.QPixmap.fromImage(deleteImg))
        self.metadataList.setCellWidget(item.row(), 1, button)

        # Connect the button to slot
        button.labelClicked.connect(self.removeMeta)

        # Highlight the cell
        item.setBackground(QtGui.QColor('lightGray'))

    def metaCellExited(self, item):
        """
            Fired when mose exits metadata region
        """
        self.metadataList.removeCellWidget(item.row(), 1)
        item.setBackground(QtGui.QTableWidgetItem().background())

    def removeMeta(self, row, column):
        """
            Remove metadata by clicking X
        """
        filePath = self.filesList.selectedItems()[0].text(2)
        metaHeader = (self.metadataList.item(row, 0)).text()
        logging.debug("Removing metadata " + metaHeader + " from " + str(filePath))
        self.filesList.removeMeta(filePath, metaHeader, row)
        

    def displayMetadata(self, metadata):
        """
            Displays metadata or not supported image
        """
        #Unsupported types return -1 as metadata
        self.writeDetails("Listing metadata...")
        if metadata is not None and len(metadata) == 0:
            self.writeDetails("\tNo metadata found!")
            self.metadataList.show()
            self.metadataList.clear()
            self.metadataList.setRowCount(0)
            self.metadataList.setHorizontalHeaderLabels(["Metadata Header", "Value"])
        elif metadata[0] == -1:
                self.metadataList.hide()
                self.fileNotSupported.show()
                self.writeDetails("\tFile type not supported")
                logging.debug("No metadata, file not supported")

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
                self.writeDetails("\t" + row[0] + ": " + row[1])


    def handleCleanMetadataKeep(self):
        """
            Clean metadata but keep orig file
        """
        logging.debug("Removing all metadata found...")
        filePath = self.filesList.selectedItems()[0].text(2)
        self.filesList.removeAllMeta(filePath)

    def handleCleanMetadataRecon(self):
        """
            Make a new clean file
        """
        logging.debug("Removing compromising personal info and remaking the file...")
        filePath = self.filesList.selectedItems()[0].text(2)
        fileType = self.filesList.getFileObj(filePath).type
        self.printPdfPersonalData(filePath, 
            fileType,
            AddedFile.changeBase(filePath, self.outputPath))
        self.tabArea.setCurrentIndex(1)
        self.changeCursor()
        self.filesList.getFileObj(filePath).reconMetaCleaned = True


    def handleAllMetaClear(self, path):
        """
            When all metadata has been cleared
        """
        logging.debug("All Metadata removed, clearing the table...")
        self.metadataList.clear()
        self.metadataList.setRowCount(0)
        self.metadataList.setHorizontalHeaderLabels(["Metadata Header", "Value"])
        self.fileNotSupported.hide()
        self.changeEnableMenus(self.filesList.getFileObj(path))

    # def handleOneMetaClear(self, row):
    #     """
    #         When just one metadata has been cleared
    #     """
    #     self.metadataList.removeCellWidget(row, 1)
    #     self.metadataList.takeItem(row, 0)
    #     self.metadataList.takeItem(row, 1)


    ############################################# 
    ###   Personal Data operations
    #############################################

    def loadImageToPersonalData(self, url, image):
        """
            Loads image of file as personal data
        """
        url = QtCore.QUrl(url)
        # if image.height() > 842 or image.width() > 595:
            # self.personalDataList.zoomOut(4)
        doc = self.personalDataList.document()
        doc.addResource(QtGui.QTextDocument.ImageResource, url, QtCore.QVariant(image))
        self.personalDataList.setDocument(doc)


        cursor = self.personalDataList.textCursor()
        imageFormat = QtGui.QTextImageFormat()
        imageFormat.setWidth(image.width())
        imageFormat.setHeight(image.height())
        imageFormat.setName(url.toString())
        cursor.insertImage(imageFormat)

        if self.personalDataList.sx is not None:
            self.personalDataList.horizontalScrollBar().setValue(self.personalDataList.sx)
            self.personalDataList.verticalScrollBar().setValue(self.personalDataList.sy)


    def displayImageData(self, fileObj):
        """
            Load image into second tab
        """
        # Enable the menus
        self.changeEnableMenus(fileObj)

        # Display metadata
        self.displayMetadata(fileObj.allMetadata)

        # Clear the text field
        self.personalDataList.clear()

        # Load image
        url = QtCore.QUrl(QtCore.QString("file://%1").arg(fileObj.filePath))
        fileImg = fileObj.personalData.pdata.image
        self.loadImageToPersonalData(url, fileImg)


    def displayPdfData(self, fileObj):
        """
            Load pdf into second tab
        """
        # Enable the menus
        self.changeEnableMenus(fileObj)

        # Display the metadata
        self.displayMetadata(fileObj.allMetadata)

        # Clear the text field
        self.personalDataList.clear()

        # load all pages
        logging.debug("Loading " + str(len(fileObj.personalData.pdata.pdfImgs)) + " pages") 
        i = 1
        for pageImg in fileObj.personalData.pdata.pdfImgs:
            self.loadImageToPersonalData(fileObj.filePath + QtCore.QString(i), pageImg)
            i += 1

    def displayOtherData(self, fileObj):
        """
            Load only Metadata for these files
        """
        self.changeEnableMenus(fileObj)
        self.displayMetadata(fileObj.allMetadata)
        self.personalDataList.clear()
        

    def printPdfPersonalData(self, fileName, fileType, outFile):
        """
            Print whatever is displayed in second tab as pdf to a file
        """
        self.filesList.doBackup(fileName)
        self.filesList.cleanPdataMarks(fileName)

        if fileType != 'Pdf':
            outFile = AddedFile.changeExt(outFile, "pdf")
        #try:
        
        printer = QtGui.QPrinter()  
        printer.setPageSize(QtGui.QPrinter.Letter)
        printer.setResolution(96)
        print "Page size ", str(self.filesList.getPdataDocSize(fileName).height())
        printer.setPaperSize(QtCore.QSizeF(self.filesList.getPdataDocSize(fileName)), QtGui.QPrinter.Point)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(outFile)
        printer.setFullPage(True)
        self.personalDataList.document().print_(printer)
        self.writeDetails("Writing PDF to " + outFile)
        self.filesList.loadBackup(fileName)

        #Finally clean the new pdf
        self.cleanPrintedPdf(outFile);

        # self.filesList.refreshPdata(fileName)
        #except Exception:
        #    self.writeDetails("Failed to write to " + fileName)

    def cleanPrintedPdf(self, outFile):
        mobj = mat.create_class_file(str(outFile), str(outFile), add2archive=True,
                low_pdf_quality=True)
        mobj.remove_all()


    def hideAllPersonalData(self):
        """
            Blur or cover personal data
        """
        filePath = self.filesList.selectedItems()[0].text(2)
        self.filesList.doBackup(filePath)
        self.filesList.hidePersonalData(filePath)
        self.pDataCancelButton.show()
        self.pDataCommitButton.show()

    def hideOnePersonalData(self, x, y):
        """
            Blur or cover a single block
        """
        filePath = self.filesList.selectedItems()[0].text(2)
        self.filesList.hidePersonalData(filePath, True, x, y)


    def displayError(self, error):
        """
            Error dialog
        """
        msgBox = QtGui.QMessageBox(self.mainWindow)
        msgBox.setText(error)
        msgBox.exec_()

    def handleCleanContentKeep(self):
        """
            ?
        """
        logging.debug("Removing compromising personal info...")   



    def handleCommit(self):
        """
            Whenever a commit is made
        """
        filePath = self.filesList.selectedItems()[0].text(2)
        self.filesList.doCommit(filePath)
        logging.debug("Committing to " + filePath)
        # Special case for PDFs
        # obj = self.filesList.getFileObj(filePath)
        # if obj.type == 'Pdf':
        #     self.printPdfPersonalData(filePath, 'Pdf', 
        #         self.filesList.getOrigPath(filePath))
        self.pDataCancelButton.hide()
        self.pDataCommitButton.hide()
        self.resetCursor()

    def handleCancel(self):
        """
            Whenever a cancel is made
        """
        self.filesList.loadBackup(self.filesList.selectedItems()[0].text(2))
        self.pDataCancelButton.hide()
        self.pDataCommitButton.hide()
        self.resetCursor()
        

    def showPDataSettings(self):
        """
            Show settings options for pdata filtering
        """
        winPos = self.mainWindow.pos()
        popPos = QtCore.QPoint(winPos.x() + (self.mainWindow.width() - self.settingsPopup.width()) / 2, 
            winPos.y() + self.mainWindow.height() / 2)
        self.settingsPopup.move(popPos)
        self.settingsPopup.show()

    def setPdataSettings(self):
        """
            Set pdata filtering settings
        """
        if self.spAdds.checkState():
            self.pdataMatch.addAddress()
        else:
            self.pdataMatch.removeRegex('Address')
        if self.spSSNs.checkState():
            self.pdataMatch.addSSN()
        else:
            self.pdataMatch.removeRegex('SSN')
        if self.spDates.checkState():
            self.pdataMatch.addDate()
        else:
            self.pdataMatch.removeRegex('Date')
        if self.spPnums.checkState():
            self.pdataMatch.addPhone()
        else:
            self.pdataMatch.removeRegex('Phone')
        if not self.spProperNouns.checkState():
            self.pdataMatch.removeRegex('Pnoun')

        newRegex = self.spLineEdit.text()
        if newRegex != '':
            valid = self.pdataMatch.addRegExp(newRegex)
            if not valid:
                self.spLabelErr.show()
        else:
            self.spLabelErr.hide()

        if len(self.filesList.selectedItems()) != 0:
            self.filesList.renderPdata(self.filesList.selectedItems()[0].text(2))
        self.settingsPopup.hide()




    ############################################# 
    ###   Utils
    #############################################
    def changeEnableMenus(self, fileObj):
        """
            Disable or enable some menus
        """
        logging.debug("Changing menus..." + str(fileObj.autoPersonalCleaned))
        self.actionCheck_Content.setEnabled(True)
        self.actionCheck_Content_auto.setEnabled(not fileObj.autoPersonalCleaned)
        self.actionCheck_Content_onebyone.setEnabled(not fileObj.autoPersonalCleaned)
        self.actionCheck_Content_useblur.setEnabled(not fileObj.autoPersonalCleaned)

        self.actionCheck_Metadata.setEnabled(True)
        self.actionCheck_Metadata_keep.setEnabled(not fileObj.autoMetaCleaned)
        self.actionCheck_Metadata_recon.setEnabled(not fileObj.reconMetaCleaned)

    def changeEnabled(self, val):
        """
            Enables some gui components
        """
        logging.debug("Changing enabled to " + str(val))
        self.filesList.setEnabled(val)
        self.tabArea.setEnabled(val)
        self.actionRemove.setEnabled(val)
        self.actionSave.setEnabled(val)


    def changeCursor(self):
        """
            Change cursor from pointer to cross, prepare
            for click operations
        """
        filePath = self.filesList.selectedItems()[0].text(2)
        self.filesList.doBackup(filePath)
        self.personalDataList.viewport().setCursor(QtCore.Qt.CrossCursor)
        self.personalDataList.areaClicked.connect(self.hideOnePersonalData)
        self.pDataCancelButton.show()
        self.pDataCommitButton.show()


    def resetCursor(self):
        """
            Change cursor from cross to pointer
        """
        self.personalDataList.viewport().setCursor(QtCore.Qt.ArrowCursor)
        self.personalDataList.areaClicked.disconnect()

    def checkIfDir(self, path):
        """
            Checks if path is a valid dir
        """
        finfo = QtCore.QFileInfo(path)
        logging.debug("Checking if " + path + "is a dir: " + str(finfo.isDir()))
        return finfo.isDir()



    ############################################
    ### Other
    ###########################################
    def handleMonitorSettings(self):
        """
            Fired to change monitor settings
        """
        winPos = self.mainWindow.pos()
        popPos = QtCore.QPoint(winPos.x() + (self.mainWindow.width() - self.settingsPopup.width()) / 2, 
            winPos.y() + self.mainWindow.height() / 2)
        self.monitorPopUp.move(popPos)
        self.monitorPopUp.show()


    def handleMonitorInputAdd(self):
        """
            Set new set of directories to monitor
        """
        newIn = self.monitorPopUpInput.text()
        # try:
        if newIn != '':
            newIns = newIn.split(',')
            for ni in newIns:
                ni = ni.trimmed()
                if not self.checkIfDir(ni):
                    self.monitorPopUpError.show()
                    return
                if not AddedFile.check_path(ni, self.outputPath):
                    logging.debug("Input in output!")
                    self.monitorPopUpError.show()
                    return
            for oldLable in self.monitorPopUpLables:
                oldLable.hide()
                self.monitorPopUpLabelLayout.removeWidget(oldLable)
            self.monitorPopUpLables = []
            self.dirMonitor.resetWatched()
            self.monitorPopUpError.hide()
            self.inputPath = []
            for ni in newIns:
                ni = ni.trimmed()
                logging.debug("Adding new label" + ni)
                newLabel = QtGui.QLabel(ni)
                self.dirMonitor.addWatched(str(ni))
                self.monitorPopUpLabelLayout.addWidget(newLabel)
                newLabel.show()
                self.monitorPopUpLables.append(newLabel)
                self.inputPath.append(ni)

            print self.monitorPopUpLables
        # except Exception as e:
        #     logging.error(str(e))



    def handleMonitorOutputSet(self):
        """
            Set new output directory
        """
        newOut = self.monitorPopUpOutput.text()
        if newOut != '':
            if not self.checkIfDir(newOut):
                self.monitorPopUpError.show()
                return
            for inp in self.inputPath:
                if not AddedFile.check_path(inp, newOut):
                    logging.debug("Input in output!")
                    self.monitorPopUpError.show()
                    return
        
            logging.debug("Changing output to " + newOut)
            self.outputPath = newOut
            self.monitorPopUpOutputDefault.setText(newOut)


    def handleModeToggle(self):
        """
            Change operation mode to auto or manual
        """
        self.filesList.changeMode(not self.autoMode)
        if self.autoMode:
            self.modeToggle.setText("Auto Mode")
            self.mainWindow.setWindowTitle("CMAT (Manual Mode)")
        else:
            self.modeToggle.setText("Manual Mode")
            self.mainWindow.setWindowTitle("CMAT (Auto Mode)")
        self.autoMode = not self.autoMode


    def cleanUp(self):
        """
            Cleans up/ stops directory listening
        """
        self.dirMonitor.stop()
        self.filesList.cleanUp()

