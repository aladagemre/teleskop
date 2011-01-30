#from PyQt4.QtCore import QSize
#from PyQt4.QtGui import QLabel, QPixmap, QGroupBox, QGridLayout
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os
from PIL import Image

class ImageViewer(QLabel):
    def __init__(self):
        QLabel.__init__(self)

    def loadImage(self, image_path):
        self.image_path = image_path
        size = self.size()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(size)
        self.setPixmap(pixmap)
        
        
        # emit signal

    def resize(self, newSize, output=None):
        """Resizes the image to newsize, saves to output path if specified.
        If no path specified, overwrites the original file."""
        try:
            size = ( newSize.width(), newSize.height() )
        except:
            size = newSize
        
        if not output:
            output = self.image_path

        im = Image.open(self.image_path)
        resizedImage = im.resize(size, Image.BICUBIC)
        resizedImage.save(output, "JPEG")



class ImageInfoPanel(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self, "Image Information")

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        label_image_name = QLabel("Name:")
        label_image_directory = QLabel("Directory:")
        label_image_dimensions = QLabel("Dimensions:")
        label_image_size = QLabel("Size:")

        self.value_image_name = QLabel("-")
        self.value_image_directory = QLabel("-")
        self.value_image_dimensions = QLabel("-")
        self.value_image_size = QLabel("-")

        self.layout.addWidget(label_image_name, 0, 0)
        self.layout.addWidget(label_image_directory, 1, 0)
        self.layout.addWidget(label_image_dimensions, 2, 0)
        self.layout.addWidget(label_image_size, 3, 0)

        self.layout.addWidget(self.value_image_name, 0, 1)
        self.layout.addWidget(self.value_image_directory, 1, 1)
        self.layout.addWidget(self.value_image_dimensions, 2, 1)
        self.layout.addWidget(self.value_image_size, 3, 1)
        
        

    def loadImage(self, image_path):
        im = Image.open(image_path)
        self.value_image_name.setText( os.path.basename(image_path) )
        self.value_image_directory.setText( os.path.dirname(image_path) )
        self.value_image_dimensions.setText( "%sx%s" % (im.size) )
        self.value_image_size.setText("%.2f MB" %  ( os.path.getsize(image_path)/(1024.0**2) ) )
        
        

class ImagePanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ===========( NAVIGATION )=================
        self.button_left = QPushButton("<")
        self.button_right= QPushButton(">")
        self.button_left.clicked.connect(self.previousImage)
        self.button_right.clicked.connect(self.nextImage)

        layout_nav_button = QHBoxLayout()
        
        
        layout_nav_button.addWidget(self.button_left)
        layout_nav_button.addStretch()
        layout_nav_button.addWidget(self.button_right)

        self.button_left.setShortcut(QKeySequence("Left"))
        self.button_right.setShortcut(QKeySequence("Right"))
        
        # ===========( IMAGE VIEWER )=================
        self.image_viewer = ImageViewer()

        # ===========( INFORMATION PANEL )=================
        self.image_info = ImageInfoPanel()

        # =========== ( RESIZE BUTTONS ) =================
        # Define buttons and shortcuts
        self.button_resize800 = QPushButton("&800x600")
        self.button_resize1024 = QPushButton("&1024x768")
        self.button_delete = QPushButton("Delete")
        self.button_delete.setShortcut(QKeySequence("Del"))

        # Connect the slots
        self.button_resize800.clicked.connect(self.resize800)
        self.button_resize1024.clicked.connect(self.resize1024)
        self.button_delete.clicked.connect(self.deleteImage)

        # Add them to horizontal layout
        layout_resize_button = QHBoxLayout()
        layout_resize_button.addWidget(self.button_resize800)
        layout_resize_button.addWidget(self.button_resize1024)
        layout_resize_button.addWidget(self.button_delete)

        # ===========( LAYOUT PLACEMENT )=================
        self.layout.addLayout(layout_nav_button)
        self.layout.addWidget(self.image_viewer)
        self.layout.addWidget(self.image_info)
        self.layout.addLayout(layout_resize_button)
        
        self.loadDirectory("/home/emre/git/teleskop/src/images")
        
    def loadImage(self, image_path):
        if isinstance(image_path, int):
            # if we want x th image, then convert it to real path.
            self.current_index = image_path
            print image_path
            image_path = os.path.join( self.directory_path, self.file_list[ image_path ] )

        self.image_info.loadImage(image_path)
        self.image_viewer.loadImage(image_path)

    def loadDirectory(self, directory_path):
        self.directory_path = directory_path
        self.file_list = sorted( os.listdir(directory_path) )
        self.num_files = len(self.file_list)
        
        if self.file_list:
            self.loadImage(0)
        else:
            QMessageBox(self, None, "No images found", "This directory does not contain any image files.")

    def nextImage(self):
        if self.file_list:
            if self.current_index < self.num_files - 1:
                self.loadImage(self.current_index + 1)
            else:
                self.loadImage(0)

    def previousImage(self):
        if self.file_list:
            if self.current_index == 0:
                self.loadImage(self.num_files - 1)
            else:
                self.loadImage(self.current_index - 1)
    def deleteImage(self):
        rejected = QMessageBox.warning(
		self, "Are you sure?",
		"Are you sure want to delete this image? This is unrecoverable. Continue?",
		"&Yes", "&No")
        
        
        if not rejected:
            print "Removing", self.image_viewer.image_path
            os.remove(self.image_viewer.image_path)
            self.file_list.remove(os.path.basename( self.image_viewer.image_path))
            self.num_files -= 1
            self.loadImage(self.current_index)
            
    def resize800(self):
        self.image_viewer.resize((800, 600))
        self.nextImage()
    def resize1024(self):
        self.image_viewer.resize((1024, 768))
        self.nextImage()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = ImagePanel()
    p.show()
    sys.exit(app.exec_())