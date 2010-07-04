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

        self.fileList = QListWidget()

        layout.addWidget(self.directoryTree)
        layout.addWidget(self.fileList)
        self.setLayout(layout)

        dir = QDir('/home/emre')
        root = model.setRootPath(dir.path())
        files = dir.entryList()
        self.directoryTree.setRootIndex(root)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = FileBrowser()
    widget.show()
    sys.exit(app.exec_())
