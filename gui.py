import sys

from PySide2.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation
from PySide2.QtGui import QFont, QPainter
from PySide2.QtWidgets import QApplication, QWidget, QListWidget, QTableWidget, QTableWidgetItem, QPushButton, QSlider, QLabel, QGroupBox, QButtonGroup, QRadioButton, QStackedLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QHeaderView, QAbstractItemView, QScrollArea, QFrame, QToolButton, QSizePolicy

import SyntaClean

class ListWidget(QListWidget):
    def __init__(self, placeholderText='', parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)
        self.__placeholderText = placeholderText

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
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.setFont(QFont("Helvetica [Cronyx]", 12))
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                self.__placeholderText, Qt.ElideRight, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
            painter.restore()

class Spoiler(QWidget):
    def __init__(self, title='', animationDuration=300, parent=None):
        """
        References:
            Adapted from
            https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt/37927256#37927256
        """
        super(Spoiler, self).__init__(parent=parent)

        self.animationDuration = animationDuration
        self.toggleAnimation = QParallelAnimationGroup()
        self.contentArea = QScrollArea()
        self.headerLine = QFrame()
        self.toggleButton = QToolButton()
        self.mainLayout = QGridLayout()

        toggleButton = self.toggleButton
        toggleButton.setStyleSheet("QToolButton { border: none; }")
        toggleButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toggleButton.setArrowType(Qt.RightArrow)
        toggleButton.setText(str(title))
        toggleButton.setCheckable(True)
        toggleButton.setChecked(False)

        headerLine = self.headerLine
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.contentArea.setStyleSheet("QScrollArea { background-color: white; border: none; }")
        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        row = 0
        mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        row += 1
        mainLayout.addWidget(self.contentArea, row, 0, 1, 3)
        self.setLayout(self.mainLayout)

        def start_animation(checked):
            arrow_type = Qt.DownArrow if checked else Qt.RightArrow
            direction = QAbstractAnimation.Forward if checked else QAbstractAnimation.Backward
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.clicked.connect(start_animation)

    def setContentLayout(self, contentLayout):
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = self.toggleAnimation.animationAt(i)
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.baseFile = QGroupBox("Base File")
        self.baseFile.setFont(QFont("Helvetica [Cronyx]", 12))

        self.dropSpace = ListWidget("Drop base file here", self)

        baseFileLayout = QVBoxLayout()
        baseFileLayout.addWidget(self.dropSpace)
        self.baseFile.setLayout(baseFileLayout)

        self.threshold = QGroupBox("Similarity Threshold")
        self.threshold.setFont(QFont("Helvetica [Cronyx]", 12))
        self.threshold.setMaximumHeight(100)

        self.sliderValueLabel = QLabel(alignment=Qt.AlignCenter)
        self.sliderValueLabel.setText("30%")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(100)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.onSliderValueChange)

        thresholdLayout = QVBoxLayout()
        thresholdLayout.addWidget(self.sliderValueLabel)
        thresholdLayout.addWidget(self.slider)
        thresholdLayout.addStretch()

        self.threshold.setLayout(thresholdLayout)

        self.abstraction = QGroupBox("Abstraction Level")
        self.abstraction.setFont(QFont("Helvetica [Cronyx]", 12))

        self.radioNone = QRadioButton("None")
        self.radioSimple = QRadioButton("Simple")
        self.radioComplete = QRadioButton("Complete")

        self.radioButtons = QButtonGroup()
        self.radioButtons.addButton(self.radioNone, 0)
        self.radioButtons.addButton(self.radioSimple, 1)
        self.radioButtons.addButton(self.radioComplete, 2)
        self.radioButtons.buttonClicked.connect(self.onRadioValueChange)

        self.radioNone.setChecked(True)
        
        abstractionLayout = QHBoxLayout()   
        abstractionLayout.addWidget(self.radioNone)
        abstractionLayout.addWidget(self.radioSimple)
        abstractionLayout.addWidget(self.radioComplete)    
        self.abstraction.setLayout(abstractionLayout)

        self.buttons = QGroupBox()
        self.buttons.setObjectName("ButtonsGroupBox")
        self.buttons.setStyleSheet("#ButtonsGroupBox{border:0}")

        self.clearButton = QPushButton('Clear', self)
        self.clearButton.setFont(QFont("Helvetica [Cronyx]", 12))
        self.clearButton.clicked.connect(self.onClearButtonClick)

        self.checkButton = QPushButton('Check', self)
        self.checkButton.setFont(QFont("Helvetica [Cronyx]", 12))
        self.checkButton.clicked.connect(self.onCheckButtonClick)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.clearButton)
        buttonsLayout.addWidget(self.checkButton)
        self.buttons.setLayout(buttonsLayout)

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.baseFile)
        verticalLayout.addWidget(self.threshold)
        verticalLayout.addWidget(self.abstraction)
        verticalLayout.addWidget(self.buttons)
        self.setLayout(verticalLayout)
    
    def onSliderValueChange(self, num):
        SyntaClean.checker.setThreshold(num/100)
        self.sliderValueLabel.setText(str(num) + "%")
    
    def onRadioValueChange(self):
        level = self.radioButtons.checkedId()
        SyntaClean.parser.setAbstractionLevel(level)

    def onClearButtonClick(self):
        SyntaClean.checker.reset()
        startingPage = self.parent()
        startingPage.listWidget.clear()
        self.dropSpace.clear()
    
    def onCheckButtonClick(self):
        startingPage = self.parent()
        mainWindow = self.parent().parent()
        SyntaClean.checker.reset()
        items = [startingPage.listWidget.item(i).text() for i in range(startingPage.listWidget.count())]
        result, similarities, fingerprints = SyntaClean.main(items)
        mainWindow.resultPageWidget.setData(result, similarities, fingerprints)
        mainWindow.stackedLayout.setCurrentIndex(1)

class StartingPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listWidget = ListWidget("Drop files here", self)
        self.settingsWidget = SettingsWidget(self)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.listWidget)
        horizontalLayout.addWidget(self.settingsWidget)
        self.setLayout(horizontalLayout)

class ResultPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.results = QGroupBox("Results")
        self.results.setFont(QFont("Helvetica [Cronyx]", 12))
        resultsLayout = QVBoxLayout()
        self.results.setLayout(resultsLayout)

        self.moreInfo = QPushButton('More Info', self)
        self.moreInfo.setFont(QFont("Helvetica [Cronyx]", 12))
        self.moreInfo.clicked.connect(self.onMoreInfoClick)

        self.lessInfo = QPushButton('Less Info', self)
        self.lessInfo.setFont(QFont("Helvetica [Cronyx]", 12))
        self.lessInfo.clicked.connect(self.onLessInfoClick)
        self.lessInfo.hide()

        self.tableWidget = QTableWidget(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.hide()

        self.listWidget = QListWidget(self)
        self.listWidget.hide()

        self.back = QPushButton('Back', self)
        self.back.setFont(QFont("Helvetica [Cronyx]", 12))
        self.back.clicked.connect(lambda: parent.stackedLayout.setCurrentIndex(0))

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.results)
        verticalLayout.addWidget(self.moreInfo)
        verticalLayout.addWidget(self.back)
        self.setLayout(verticalLayout)
    
    def setData(self, results, similarities, fingerprints):
        self.createResultsContent(results)
        size = len(similarities)
        self.tableWidget.setColumnCount(size)
        self.tableWidget.setRowCount(size)

        for row in range(size):
            for column in range(size):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(similarities[row][column])))

        self.listWidget.clear()
        for fingerprint in fingerprints:
            self.listWidget.addItem(str(fingerprint.id + 1) + " = " + fingerprint.file)

    def createResultsContent(self, results):
        layout = self.results.layout()
        self.clearLayout(layout)

        if len(results) == 0:
            label = QLabel(alignment=Qt.AlignCenter)
            label.setFont(QFont("Helvetica [Cronyx]", 12))
            label.setText("No files match the criteria, press More Info for a detailed report.")
            layout.addWidget(label)
        else:
            for file, matches in results.items():
                spoiler = Spoiler(file)
                resultLayout = QVBoxLayout()

                for i in range(len(matches)):
                    matchedFile = matches[i][0]
                    similarity = round(matches[i][1] * 100)
                    text = matchedFile + " (" + str(similarity) + "%)"
                    resultButton = QPushButton(text, self)
                    resultLayout.addWidget(resultButton)

                spoiler.setContentLayout(resultLayout)
                layout.addWidget(spoiler)
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def onMoreInfoClick(self):
        layout = self.layout()
        
        self.moreInfo.hide()
        
        layout.takeAt(1)
        
        self.tableWidget.show()
        self.listWidget.show()        
        self.lessInfo.show()

        layout.insertWidget(1, self.tableWidget)
        layout.insertWidget(2, self.listWidget)
        layout.insertWidget(3, self.lessInfo)

    def onLessInfoClick(self):
        layout = self.layout()

        self.moreInfo.show()

        self.tableWidget.hide()
        self.listWidget.hide()        
        self.lessInfo.hide()

        layout.takeAt(1)
        layout.takeAt(2)
        layout.takeAt(3)

        layout.insertWidget(1, self.moreInfo)


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
