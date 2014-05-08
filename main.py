import sys
from PyQt4.QtGui import QApplication, QMainWindow
from AddedFile import AddedFile
from mainwindow import Ui_MainWindow

app = QApplication(sys.argv)
if len(app.arguments()) != 3:
	print "Missing or unknown parameters"
	sys.exit(1)
inFile = app.arguments()[1]
outFile = app.arguments()[2]

if not AddedFile.check_path(inFile, outFile):
	print "Output cannot live in input. Please correct!"
	sys.exit(1)

window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window, inFile, outFile)

# clean up before exit
app.aboutToQuit.connect(ui.cleanUp)

window.show()
sys.exit(app.exec_())