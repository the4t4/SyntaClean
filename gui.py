import sys, os

import SyntaClean
from clean_parser.abstraction import AbstractionLevel

from PySide2.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, QFile, QDir, QRegularExpression
from PySide2.QtGui import QFont, QPainter, QColor, QTextCursor, QTextCharFormat, QIcon
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QTableWidget, QTableWidgetItem, QPushButton, QSlider, QLabel, QPlainTextEdit, 
    QGroupBox, QButtonGroup, QRadioButton, QStackedLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QHeaderView, 
    QAbstractItemView, QScrollArea, QFrame, QToolButton, QSizePolicy
)

if getattr(sys, 'frozen', False):
    iconFile = os.path.join(sys._MEIPASS, "gui" + os.sep + "resources" + os.sep + "icon.ico")
    qssFile = os.path.join(sys._MEIPASS, "gui" + os.sep + "resources" + os.sep + "MaterialDark.qss")
else:
    iconFile = "." + os.sep + "gui" + os.sep + "resources" + os.sep + "icon.ico"
    qssFile = "." + os.sep + "gui" + os.sep + "resources" + os.sep + "MaterialDark.qss"

class ComparisonWindow(QWidget):
    def __init__(self, file1, file2, parent=None):
        super().__init__()

        self.setWindowTitle("SyntaClean")
        self.setWindowIcon(QIcon(iconFile))
        self.resize(1200,600)
        self.setMinimumSize(400,200)
        self.move(parent.mapToGlobal(parent.pos()))
        
        self.qfile1 = QFile(file1)
        self.qfile1.open(QFile.ReadOnly)
        text1 = str(self.qfile1.readAll(), 'cp1252')

        self.qfile2 = QFile(file2)
        self.qfile2.open(QFile.ReadOnly)
        text2 = str(self.qfile2.readAll(), 'cp1252')
        
        self.left = QGroupBox(file1)
        self.left.setFont(QFont("Helvetica [Cronyx]", 12))
        self.leftfile = QPlainTextEdit(text1)
        self.leftfile.setFont(QFont("Helvetica [Cronyx]", 10))
        self.leftfile.setReadOnly(True)
        
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.leftfile)
        self.left.setLayout(leftLayout)

        self.right = QGroupBox(file2)
        self.right.setFont(QFont("Helvetica [Cronyx]", 12))
        self.rightfile = QPlainTextEdit(text2)
        self.rightfile.setFont(QFont("Helvetica [Cronyx]", 10))
        self.rightfile.setReadOnly(True)

        self.highlightSimilarities()
        self.restoreCommentFormat() 

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.rightfile)
        self.right.setLayout(rightLayout)
        
        horizontalLayout = QHBoxLayout()    
        horizontalLayout.addWidget(self.left)
        horizontalLayout.addWidget(self.right)
        self.setLayout(horizontalLayout)

    def highlightSimilarities(self):
        file1 = QDir.toNativeSeparators(self.qfile1.fileName())
        file2 = QDir.toNativeSeparators(self.qfile2.fileName())
        collisions1, collisions2 = SyntaClean.checker.getCollisionsOfTwo(file1, file2)

        if len(collisions1) == 0:
            return

        textCursorLeft = self.leftfile.textCursor()
        textCursorRight = self.rightfile.textCursor()

        similarFormat = QTextCharFormat()
        similarFormat.setForeground(Qt.red)

        for collision1, collision2 in zip(collisions1, collisions2):
            leftMeta = collision1.meta
            leftStartLine = leftMeta.line - 1
            leftStartCol = leftMeta.column - 1
            leftEndLine = leftMeta.end_line - leftStartLine - 1
            leftEndCol = leftMeta.end_column - leftStartCol - 1

            textCursorLeft.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, leftStartLine)
            textCursorLeft.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, leftStartCol)

            textCursorLeft.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, leftEndLine)
            textCursorLeft.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, leftEndCol)

            textCursorLeft.setCharFormat(similarFormat)
            textCursorLeft.setPosition(0)

            rightMeta = collision2.meta
            rightStartLine = rightMeta.line - 1
            rightStartCol = rightMeta.column - 1
            rightEndLine = rightMeta.end_line - rightStartLine - 1
            rightEndCol = rightMeta.end_column - rightStartCol - 1

            textCursorRight.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, rightStartLine)
            textCursorRight.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, rightStartCol)

            textCursorRight.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, rightEndLine)
            textCursorRight.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, rightEndCol)

            textCursorRight.setCharFormat(similarFormat)
            textCursorRight.setPosition(0)
    
    def restoreCommentFormat(self):
        textCursorLeft = self.leftfile.textCursor()
        textCursorRight = self.rightfile.textCursor()

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor('#a9b7c6'))
        
        singleLineCommentRegex = QRegularExpression("//[^\n]*")
        multiLineCommentRegex = QRegularExpression("/\\*([^*]|(\\*+[^/]))*\\*+/")

        crsrs = [textCursorLeft, textCursorRight]
        texts = [self.leftfile.toPlainText(), self.rightfile.toPlainText()]
        exprs = [singleLineCommentRegex, multiLineCommentRegex]

        for crsr, text in zip(crsrs, texts):
            for expr in exprs:
                iter = expr.globalMatch(text)
                while iter.hasNext():
                    match = iter.next()
                    crsr.setPosition(match.capturedStart(), QTextCursor.MoveAnchor)
                    crsr.setPosition(match.capturedStart() + match.capturedLength(), QTextCursor.KeepAnchor)
                    crsr.setCharFormat(commentFormat)        

class ListWidget(QListWidget):
    def __init__(self, placeholderText='', additive=True, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)
        self.__placeholderText = placeholderText
        self.additive = additive

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
        if not self.additive:
            self.clear()
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            files = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    files.append(QDir.toNativeSeparators(str(url.toLocalFile())))
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

        self.contentArea.setStyleSheet("QScrollArea { background-color: #1e1d23; border: none; }")
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
    
    def setFont(self, font):
            super().setFont(font)
            self.toggleButton.setFont(font)

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

        self.dropSpace = ListWidget("Drop base file here", False, self)

        baseFileLayout = QVBoxLayout()
        baseFileLayout.addWidget(self.dropSpace)
        self.baseFile.setLayout(baseFileLayout)

        self.threshold = QGroupBox("Similarity Threshold")
        self.threshold.setFont(QFont("Helvetica [Cronyx]", 12))
        self.threshold.setMaximumHeight(100)

        self.thresholdSliderValue = QLabel(alignment=Qt.AlignCenter)
        self.thresholdSliderValue.setFont(QFont("Helvetica [Cronyx]", 12))
        self.thresholdSliderValue.setText("30%")
        self.thresholdSlider = QSlider(Qt.Horizontal)
        self.thresholdSlider.setMaximum(100)
        self.thresholdSlider.setValue(30)
        self.thresholdSlider.valueChanged.connect(self.onThresholdSliderValueChange)

        thresholdLayout = QVBoxLayout()
        thresholdLayout.addWidget(self.thresholdSliderValue)
        thresholdLayout.addWidget(self.thresholdSlider)
        thresholdLayout.addStretch()

        self.threshold.setLayout(thresholdLayout)

        self.granularity = QGroupBox("Match Granularity")
        self.granularity.setFont(QFont("Helvetica [Cronyx]", 12))
        self.granularity.setMaximumHeight(100)

        self.granularitySliderValue = QLabel(alignment=Qt.AlignCenter)
        self.granularitySliderValue.setFont(QFont("Helvetica [Cronyx]", 12))
        self.granularitySliderValue.setNum(1)
        self.granularitySlider = QSlider(Qt.Horizontal)
        self.granularitySlider.setMinimum(1)
        self.granularitySlider.setMaximum(10)
        self.granularitySlider.setValue(1)
        self.granularitySlider.valueChanged.connect(self.onGranularitySliderValueChange)

        granularityLayout = QVBoxLayout()
        granularityLayout.addWidget(self.granularitySliderValue)
        granularityLayout.addWidget(self.granularitySlider)
        granularityLayout.addStretch()

        self.granularity.setLayout(granularityLayout)

        self.abstraction = QGroupBox("Abstraction Level")
        self.abstraction.setFont(QFont("Helvetica [Cronyx]", 12))

        self.radioNone = QRadioButton("None")
        self.radioSimple = QRadioButton("Simple")
        self.radioComplete = QRadioButton("Complete")

        self.radioNone.setFont(QFont("Helvetica [Cronyx]", 12))
        self.radioSimple.setFont(QFont("Helvetica [Cronyx]", 12)) 
        self.radioComplete.setFont(QFont("Helvetica [Cronyx]", 12)) 

        self.radioButtons = QButtonGroup()
        self.radioButtons.addButton(self.radioNone, 0)
        self.radioButtons.addButton(self.radioSimple, 1)
        self.radioButtons.addButton(self.radioComplete, 2)
        self.radioButtons.buttonClicked.connect(self.onRadioValueChange)

        self.radioNone.setChecked(True)
        
        abstractionLayout = QHBoxLayout()   
        abstractionLayout.addWidget(self.radioNone)
        abstractionLayout.addStretch()
        abstractionLayout.addWidget(self.radioSimple)
        abstractionLayout.addStretch()
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
        verticalLayout.addWidget(self.granularity)
        verticalLayout.addWidget(self.abstraction)
        verticalLayout.addWidget(self.buttons)
        self.setLayout(verticalLayout)
    
    def onThresholdSliderValueChange(self, num):
        SyntaClean.checker.setThreshold(num/100)
        self.thresholdSliderValue.setText(str(num) + "%")

    def onGranularitySliderValueChange(self, num):
        SyntaClean.checker.setGranularity(num)
        self.granularitySliderValue.setNum(num)
    
    def onRadioValueChange(self):
        levelNum = self.radioButtons.checkedId()
        abstractionLevel = AbstractionLevel(levelNum)
        SyntaClean.parser.setAbstractionLevel(abstractionLevel)

    def onClearButtonClick(self):
        SyntaClean.checker.reset()
        startingPage = self.parent()
        startingPage.listWidget.clear()
        self.dropSpace.clear()
    
    def onCheckButtonClick(self):
        startingPage = self.parent()
        mainWindow = self.parent().parent()
        
        SyntaClean.checker.reset()
        files = [startingPage.listWidget.item(i).text() for i in range(startingPage.listWidget.count())]
        baseFile = startingPage.settingsWidget.dropSpace.item(0)
        if baseFile is not None:
            SyntaClean.setBaseFile(baseFile.text())
        result, similarities, fingerprints = SyntaClean.main(files)

        mainWindow.resultPageWidget.setData(result, similarities, fingerprints)
        mainWindow.stackedLayout.setCurrentIndex(1)

class StartingPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listWidget = ListWidget("Drop files here", True, self)
        self.settingsWidget = SettingsWidget(self)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.listWidget)
        horizontalLayout.addWidget(self.settingsWidget)
        self.setLayout(horizontalLayout)

class ResultPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.widget = QWidget()
        self.moreInfoToggled = False

        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("QScrollArea { background-color: white; border: none; }")

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
        self.listWidget.setFont(QFont("Helvetica [Cronyx]", 10))
        self.listWidget.hide()

        self.back = QPushButton('Back', self)
        self.back.setFont(QFont("Helvetica [Cronyx]", 12))
        self.back.clicked.connect(self.onBackClick)

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.results)
        verticalLayout.addWidget(self.moreInfo)
        verticalLayout.addStretch()
        verticalLayout.addWidget(self.back)
        self.widget.setLayout(verticalLayout)
        self.widget.setMinimumSize(0,0)

        self.scrollArea.setWidget(self.widget)

        scrollLayout = QVBoxLayout()
        scrollLayout.addWidget(self.scrollArea)
        self.setLayout(scrollLayout)

        self.comparisonWindow = None

    def setData(self, results, similarities, fingerprints):
        self.createResultsContent(results)
        size = len(similarities)
        self.tableWidget.setColumnCount(size)
        self.tableWidget.setRowCount(size)

        for row in range(size):
            for column in range(size):
                similarity = similarities[row][column]
                cell = QTableWidgetItem(str(round(similarity * 100)) + "%")
                cell.setTextAlignment(Qt.AlignCenter)
                color = QColor(min(255, 2*255*(similarity)), min(255, 2*255*(1-similarity)), 0)
                cell.setBackgroundColor(color)
                self.tableWidget.setItem(row, column, cell)

        tableHeight = sum([ self.tableWidget.verticalHeader().sectionSize(i) for i in range(min(size,15)) ]) + self.tableWidget.horizontalHeader().height() + 2 * self.tableWidget.frameWidth()
        self.tableWidget.setMinimumHeight(tableHeight)

        self.listWidget.clear()
        for fingerprint in fingerprints:
            self.listWidget.addItem(str(fingerprint.id + 1) + " = " + fingerprint.file)
        
        listHeight = self.listWidget.sizeHintForRow(0) * min(self.listWidget.count(),15) + 2 * self.listWidget.frameWidth()
        self.listWidget.setMinimumHeight(listHeight)   

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
                spoiler.setFont(QFont("Helvetica [Cronyx]", 10))
                resultLayout = QVBoxLayout()

                for i in range(len(matches)):
                    matchedFile = matches[i][0]
                    similarity = round(matches[i][1] * 100)
                    text = matchedFile + " (" + str(similarity) + "%)"
                    resultButton = QPushButton(text, self)
                    resultButton.setFont(QFont("Helvetica [Cronyx]", 10))
                    resultButton.clicked.connect(lambda file1=file, file2=matchedFile: onResultButtonClick(file1, file2))
                    resultLayout.addWidget(resultButton)

                spoiler.setContentLayout(resultLayout)
                layout.addWidget(spoiler)
        
        def onResultButtonClick(file1, file2):
            self.comparisonWindow = ComparisonWindow(file1, file2, self)
            self.comparisonWindow.show()

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
        self.moreInfoToggled = True
        layout = self.widget.layout()
        
        self.moreInfo.hide()
        layout.takeAt(1)
        
        self.tableWidget.show()
        self.listWidget.show()        
        self.lessInfo.show()

        layout.insertWidget(1, self.tableWidget)
        layout.insertWidget(2, self.listWidget)
        layout.insertWidget(3, self.lessInfo)

    def onLessInfoClick(self):
        self.moreInfoToggled = False
        layout = self.widget.layout()

        self.moreInfo.show()

        self.tableWidget.hide()
        self.listWidget.hide()        
        self.lessInfo.hide()

        layout.takeAt(3)
        layout.takeAt(2)
        layout.takeAt(1)

        layout.insertWidget(1, self.moreInfo)
    
    def onBackClick(self):
        parent = self.parent()

        if self.moreInfoToggled:
            self.onLessInfoClick()

        parent.stackedLayout.setCurrentIndex(0)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.stackedLayout = QStackedLayout()

        self.startingPageWidget = StartingPageWidget(self)
        self.resultPageWidget = ResultPageWidget(self)

        self.stackedLayout.addWidget(self.startingPageWidget)
        self.stackedLayout.addWidget(self.resultPageWidget)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.stackedLayout)
        self.setLayout(self.mainLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SyntaClean")
        self.setWindowIcon(QIcon(iconFile))
        self.resize(1200,600)
        self.setMinimumSize(400,200)
        widget = MainWidget()
        self.setCentralWidget(widget)

def getStyleSheet():
    stream = QFile(qssFile)
    if stream.open(QFile.ReadOnly):
        st = str(stream.readAll(), 'ASCII')
        stream.close()
    else:
        print(stream.errorString())
    return st

def main(argv):
    app = QApplication(argv)
    app.setStyle("plastique")
    styleSheet = getStyleSheet()

    app.setStyleSheet(styleSheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
