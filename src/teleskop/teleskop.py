# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from imageviewer import ImagePanel
from filebrowser import FileBrowser

import sys

class TeleskopWindow(QMainWindow):
    def __init__(self, scene=None):
        QMainWindow.__init__(self)
        self.setupGUI()

    def resizeEvent(self, event):
        size = self.size()
        self.image_panel.setMaximumWidth(size.width()*0.75)
        self.file_browser.setMaximumWidth(size.width()*0.25)
        self.image_panel.setMaximumHeight(size.height()*0.9)
        self.file_browser.setMaximumHeight(size.height())
        
    def setupGUI(self):
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
        self.file_browser.fileSelectedSignal.connect(self.image_panel.loadImage)
        self.file_browser.directorySelectedSignal.connect(self.image_panel.loadDirectory)
        

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = TeleskopWindow()
    mainWindow.showMaximized()
    #mainWindow.showFullScreen()
    sys.exit(app.exec_())

