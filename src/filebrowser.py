from PyQt4.QtGui import QVBoxLayout, QFileSystemModel, QTreeView,\
                        QApplication, QWidget, QListWidget
                        
from PyQt4.QtCore import QDir, Qt, pyqtSignal, QString
import os


class FileBrowser(QWidget):

    fileSelectedSignal = pyqtSignal(QString)
    directorySelectedSignal = pyqtSignal(QString)

    def __init__(self, *args):
        super(FileBrowser, self).__init__(*args)

        layout = QVBoxLayout()
        model = QFileSystemModel()

        filters = ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG","*.png","*.PNG"]
        model.setNameFilters(filters)
        
        self.directoryTree = QTreeView()
	self.directoryTree.setModel(model)
        self.directoryTree.currentChanged = self.currentChanged
        self.directoryTree.setSortingEnabled(True)
        self.directoryTree.sortByColumn(0, Qt.AscendingOrder)

        self.fileList = QListWidget()

        layout.addWidget(self.directoryTree)
        self.setLayout(layout)
        
        dir = QDir('/home/emre/multimedia/resim')
        root = model.setRootPath(dir.path())
        self.directoryTree.setRootIndex(root)

    def currentChanged(self, current, previous):
        QTreeView.currentChanged(self.directoryTree, current, previous)
        currentIndex = self.directoryTree.selectionModel().currentIndex()
        path = str ( self.directoryTree.model().filePath(currentIndex) )
        
        if self.directoryTree.model().isDir(currentIndex):
            #self.directory_path = path
            self.directorySelectedSignal.emit(path)
        else:
            self.fileSelectedSignal.emit(path)            
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = FileBrowser()
    widget.show()
    sys.exit(app.exec_())
