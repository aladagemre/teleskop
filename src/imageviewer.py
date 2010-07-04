#from PyQt4.QtCore import QSize
from PyQt4.QtGui import QLabel, QPixmap
from PIL import Image

class ImageViewer(QLabel):
    def __init__(self):
        QLabel.__init__(self)

    def loadImage(self, path):
        self.path = path
        size = self.size()
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(size)
        self.setPixmap(pixmap)
        
        
        # emit signal

    def resize(self, newSize, output=None):
        """Resizes the image to newsize, saves to output path if specified.
        If no path specified, overwrites the original file."""

        size = ( newSize.width(), newSize.height() )
        if not output:
            output = self.path

        im = Image.open(self.path)
        resizedImage = im.resize(size, Image.BICUBIC)
        resizedImage.save(output, "JPEG")



        