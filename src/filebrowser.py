from PyQt4.QtGui import QVBoxLayout, QFileSystemModel, QTreeView,\
                        QApplication, QWidget, QListWidget
                        
from PyQt4.QtCore import QDir

class FileBrowser(QWidget):
    def __init__(self, *args):
        super(FileBrowser, self).__init__(*args)

        layout = QVBoxLayout()
        model = QFileSystemModel()

        self.directoryTree = QTreeView()
	self.directoryTree.setModel(model)
        self.directoryTree.currentChanged = self.currentChanged

        self.fileList = QListWidget()

        layout.addWidget(self.directoryTree)
        layout.addWidget(self.fileList)
        self.setLayout(layout)
        
        dir = QDir('/home/emre')
        root = model.setRootPath(dir.path())
        files = filter( lambda filename: str(filename[-4:]).lower() in (".jpg", ".png"), dir.entryList() )
        self.fileList.addItems(files)
        self.directoryTree.setRootIndex(root)

    def currentChanged(self, current, previous):
        #print current.data().toString(), previous.data().toString()
        print self.directoryTree.selectionModel().selectedRows()[0].data(0).toString()
        QTreeView.currentChanged(self.directoryTree, current, previous)
            
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = FileBrowser()
    widget.show()
    sys.exit(app.exec_())
