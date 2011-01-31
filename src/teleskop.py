# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from imageviewer import ImagePanel
from filebrowser import FileBrowser

import sys,os

class TeleskopWindow(QMainWindow):
    def __init__(self, scene=None):
        QMainWindow.__init__(self)
        self.setupGUI()

    def setupGUI(self):
        """self.imageViewer = ImageViewer()
        filename = "IMG_2163.JPG"
        file, ext = os.path.splitext(filename)
        self.imageViewer.loadImage(filename)
        self.imageViewer.resize(QSize(800,600), "%s_new%s" % (file, ext ) )

        self.fileBrowser = FileBrowser()
        
        layout = QHBoxLayout()
        layout.addWidget(self.imageViewer)
        layout.addWidget(self.fileBrowser)"""

        layout = QHBoxLayout()

        self.image_panel = ImagePanel()
        self.file_browser = FileBrowser()

        layout.addWidget(self.image_panel)
        layout.addWidget(self.file_browser)
        
        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Teleskop")

        self.createActions()
        self.statusBar()
        self.connectSlots()
        
    def connectSlots(self):
        #self.connect(self.scene, SIGNAL('sceneMouseMove'), self.displayCoordinate)
        pass

    def displayCoordinate(self, point):
        self.statusBar().showMessage("(%s, %s)" % (point.x(), point.y()))

    def createActions(self):
        exit = QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exit)

    
    """def resizeEvent(self, event):
        pass"""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = TeleskopWindow()
    mainWindow.showMaximized()
    #mainWindow.showFullScreen()
    sys.exit(app.exec_())

