'''
*********************************************************************************************
  *File: GUI_test.py
  *Project: servodogVersion2.0
  *Filepath: /home/guoyucan/ServoDogVersion1.0/servodogVersion2.0/GUI_test.py 
  *File Created: Wednesday, 1st December 2021 9:06:07 pm
  *Author: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Last Modified: Wednesday, 1st December 2021 9:06:10 pm
  *Modified By: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Copyright @ 2021 , BionicDL LAB, SUSTECH, Shenzhen, China 
*********************************************************************************************
'''

import sys, random
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QFrame, QGridLayout, QVBoxLayout, QToolButton, QStatusBar, QLabel
from PyQt5.QtCore import Qt, QEvent, QMimeData
from PyQt5.QtGui import QDrag, QFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time 
## import packages I write persnally
from Xbox_value import XBOX_class



class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Multiple Graphs in a single window')
        self.setMinimumSize(1500, 800)
        self.setAcceptDrops(True)

        # Resize and Scroll the graph
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Graph window container
        self.graphContainer = QWidget()
        self.gridLayout = QGridLayout(self.graphContainer)

        self.scrollArea.setWidget(self.graphContainer)
        self.layout.addWidget(self.scrollArea)

        self.createGraph()

    # manage event to drag the graph
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    # manage event to drop the graph
    def dropEvent(self, event):
        if not event.source().geometry().contains(event.pos()):
            targetWindowIndex = self.getWindowIndex(event.pos())
            if targetWindowIndex is None:
                return
            i, j = max(self.targetIndex, targetWindowIndex), min(self.targetIndex, targetWindowIndex)
            p1, p2 = self.gridLayout.getItemPosition(i), self.gridLayout.getItemPosition(j)
            self.gridLayout.addItem(self.gridLayout.takeAt(i), *p2)
            self.gridLayout.addItem(self.gridLayout.takeAt(j), *p1)

    # mouse event filter
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self.mouseMoveEvent(event)
        return super().eventFilter(obj, event)

    # mouse press event manager
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            coord = event.windowPos().toPoint()  # QPoint object
            self.targetIndex = self.getWindowIndex(coord)
        else:
            self.targetIndex = None

    # mouse move event manager
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.targetIndex is not None:
            windowItem = self.gridLayout.itemAt(self.targetIndex)

            drag = QDrag(windowItem)

            pix = windowItem.itemAt(0).widget().grab()

            mimeData = QMimeData()
            mimeData.setImageData(pix)

            drag.setMimeData(mimeData)
            drag.setPixmap(pix)
            drag.setHotSpot(event.pos())
            drag.exec_()

    # get the graph index in the window
    def getWindowIndex(self, pos):
        for i in range(self.gridLayout.count()):
            if self.gridLayout.itemAt(i).geometry().contains(pos):
                return i

    # create graphs in a single window
    def createGraph(self):
        tracker = 0

        for r in range(3):
            for c in range(1):
                frame = QFrame()
                frame.setStyleSheet('background-color: white')
                frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

                frameContrainer = QVBoxLayout(frame)

                chartData = [0.0 for i in range(100)]
                tracker += 1

                # create matplotlib graph
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)  # pyqt5 widget
                ax = self.figure.add_subplot()
                ax.plot(chartData, 'r-')
                self.figure.suptitle('Chart #{0}'.format(tracker))
                self.canvas.draw()

                # TODO: Drag and drop feature

                frameContrainer.addWidget(self.canvas)

                self.gridLayout.addLayout(frameContrainer, r, c)

                box = QVBoxLayout()
                box.addWidget(frame)
                self.gridLayout.addLayout(box, r, c)

                # resize the graphs to fit the size of the window
                self.gridLayout.setColumnStretch(r % 2, 1)
                self.gridLayout.setRowStretch(r, 1)

        # status bar use to show the system status
        self.statusBar = QStatusBar(self)
        self.statusBar.move(1380, 750)
        self.statusBar.showMessage('Ready')
        self.statusBar.setFont(QFont('Arial', 15))

        # Label for servo information button
        self.lbl1 = QLabel("Servo 1 Angle Command", self)
        self.lbl1.resize(180, 30)
        self.lbl1.move(875, 30)

        self.lbl2 = QLabel("servo 2 Angle Command", self)
        self.lbl2.resize(180, 30)
        self.lbl2.move(1125, 30)

        # servo angle command panel
        self.btn1 = QToolButton(self)
        self.btn1.setText("0.0")
        self.btn1.move(900, 60)
        self.btn1.resize(200, 30)

        self.btn2 = QToolButton(self)
        self.btn2.setText("0.0")
        self.btn2.move(1150, 60)
        self.btn2.resize(200, 30)

        self.show()
        self.setUpdatesEnabled(True)



    # TODO: update subplots in a single window
    # def updateGraph(self,data ):
    #     return None

    # TODO: Update GUI information based on servo angle command we sent to servo
    def updateStatus(self, axis_0, axis_1):
        # print(axis_0,axis_1)
        self.lbl1.setNum(((axis_0)))
        self.lbl1.repaint()
        print("Repaint")
        self.lbl2.setNum(((axis_1)))
        self.lbl1.repaint()

        # self.update()
        # self.repaint()

        # time.sleep(0.1)

        return None

if __name__ == '__main__':

    # create a Application object
    app = QApplication(sys.argv)
    myapp = MyApp()
    
    
    xbox = XBOX_class()
    xbox.initialize_xbox()


    while True:
        axis_0, axis_1 = xbox.get_xbox_status()
        myapp.updateStatus(axis_0,axis_1)
        # myapp.hide()
        # time.sleep(0.1)
        # myapp.show()

        # time.sleep(0.5)
        # myapp.updateStatus(xbox.axis_0, xbox.axis_1)
    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('This window will be closed soon!')
