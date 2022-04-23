import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QWidget, QListWidget, QTableWidget, QTableWidgetItem, QPushButton, QStackedLayout, QVBoxLayout, QHBoxLayout, QHeaderView, QAbstractItemView

import SyntaClean

class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            files = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    files.append(str(url.toLocalFile()))
            self.addItems(files)
        else:
            event.ignore()

class StartingPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listWidget = ListWidget(self)

        self.btn = QPushButton('Check', self)
        self.btn.setFont(QFont("Helvetica [Cronyx]", 12))
        self.btn.clicked.connect(lambda: self.buttonPress())

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.listWidget)
        horizontalLayout.addWidget(self.btn)
        self.setLayout(horizontalLayout)

    def buttonPress(self):
        items = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        self.listWidget.clear()
        results, fingerprints = SyntaClean.main(items)
        self.parent().resultPageWidget.setData(results, fingerprints)
        self.parent().stackedLayout.setCurrentIndex(1)

class ResultPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.listWidget = QListWidget(self)

        self.btn = QPushButton('Back', self)
        self.btn.setFont(QFont("Helvetica [Cronyx]", 12))
        self.btn.clicked.connect(lambda: parent.stackedLayout.setCurrentIndex(0))

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.tableWidget)
        verticalLayout.addWidget(self.listWidget)
        verticalLayout.addWidget(self.btn)
        self.setLayout(verticalLayout)
    
    def setData(self, data, fingerprints):
        size = len(data)
        self.tableWidget.setColumnCount(size)
        self.tableWidget.setRowCount(size)

        for row in range(size):
            for column in range(size):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

        self.listWidget.clear()
        for fingerprint in fingerprints:
            self.listWidget.addItem(str(fingerprint.id + 1) + " = " + fingerprint.file)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("SyntaClean")
        self.resize(1200,600)
        self.setMinimumSize(400,200)
        
        self.startingPageWidget = StartingPageWidget(self)
        self.resultPageWidget = ResultPageWidget(self)

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.addWidget(self.startingPageWidget)
        self.stackedLayout.addWidget(self.resultPageWidget)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.stackedLayout)
        self.setLayout(self.mainLayout)

def main(argv):
    app = QApplication(argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
