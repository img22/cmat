from PyQt4 import QtGui, QtCore

class CQTableWidget(QtGui.QTableWidget):
    cellExited = QtCore.pyqtSignal(int, int)
    itemExited = QtCore.pyqtSignal(QtGui.QTableWidgetItem)

    def __init__(self, rows, columns, parent=None):
        QtGui.QTableWidget.__init__(self, rows, columns, parent)
        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()

            if event.type() == QtCore.QEvent.Wheel:
                self.cellExited.emit(index.row(), index.column())
                return
            row = self._last_index.row()
            column = self._last_index.column()
            item = self.item(row, column)
            if index != self._last_index:
                if item is not None:
                    self.itemExited.emit(item)
                self.cellExited.emit(row, column)
                self._last_index = QtCore.QPersistentModelIndex(index)
        return QtGui.QTableWidget.eventFilter(self, widget, event)