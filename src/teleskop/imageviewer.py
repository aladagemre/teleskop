from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os
import exifread

from PIL import Image

BEST_CANDIDATE_SET = set()
TRASH_CANDIDATE_SET = set()

class ImageViewer(QLabel):
    def __init__(self):
        QLabel.__init__(self)

    def reset(self):
        self.image_path = None
        self.pixmap = QPixmap("questionmark.png")
        self.setPixmap(self.pixmap)

    def loadImage(self, image_path):
        self.image_path = image_path
        self.pixmap = pixmap = QPixmap(image_path)

        # TODO: Scaling problems exist. Need to work here.

        # Find label width/height
        lwidth, lheight = self.size().width(), self.size().height()
        # Find image width/height
        width, height = pixmap.width(), pixmap.height()

        windowSize = self.window().size()
        newWidth = windowSize.width()*0.75
        newHeight = windowSize.height()*0.65


        # According to image width/height,
        # scale up to label width/height
        if pixmap:
            pixmap = pixmap.scaledToHeight(newHeight)
        """if width > height:
            pixmap = pixmap.scaledToWidth(newWidth)
        else:
            pixmap = pixmap.scaledToHeight(newHeight)"""

        """print "Label:", lwidth, lheight
        print "Image:", width, height

        if height > lheight:
            pixmap = pixmap.scaledToHeight(lheight)
        elif width > lwidth:
            pixmap = pixmap.scaledToWidth(newWidth)"""

        self.setPixmap(pixmap)
        #self.setWindowFlags(Qt.Window)
        #self.setScaledContents(True)
        #self.showFullScreen()


    def resize(self, newSize, output=None):
        """Resizes the image to newsize, saves to output path if specified.
        If no path specified, overwrites the original file."""
        try:
            size = ( newSize.width(), newSize.height() )
        except:
            size = newSize

        # find photo's size
        width, height = self.pixmap.width(), self.pixmap.height()

        # if this is a portrait, not landscape, then switch the dimensions.
        if height > width:
            size = ( size[1], size[0] )

        if not output:
            output = self.image_path

        """im = Image.open(self.image_path)
        resizedImage = im.resize(size, Image.ANTIALIAS)
        resizedImage.save(output, "JPEG",quality=100)"""
        command = "mogrify -resize %dx%d %s &" % (size[0], size[1], self.image_path)
        os.system(command)


class ImageInfoPanel(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self, "Image Information")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        label_image_name = QLabel("Name:")
        label_image_directory = QLabel("Directory:")
        label_image_dimensions = QLabel("Dimensions:")
        label_image_size = QLabel("Size:")
        label_image_set = QLabel("Set:")

        self.value_image_name = QLabel("-")
        self.value_image_directory = QLabel("-")
        self.value_image_dimensions = QLabel("-")
        self.value_image_size = QLabel("-")
        self.value_image_set = QLabel("-")

        self.layout.addWidget(label_image_name, 0, 0)
        self.layout.addWidget(label_image_directory, 1, 0)
        self.layout.addWidget(label_image_dimensions, 2, 0)
        self.layout.addWidget(label_image_size, 3, 0)
        self.layout.addWidget(label_image_set, 4, 0)

        self.layout.addWidget(self.value_image_name, 0, 1)
        self.layout.addWidget(self.value_image_directory, 1, 1)
        self.layout.addWidget(self.value_image_dimensions, 2, 1)
        self.layout.addWidget(self.value_image_size, 3, 1)
        self.layout.addWidget(self.value_image_set, 4, 1)


    def reset(self):
        self.value_image_name.setText("-")
        self.value_image_directory.setText("-")
        self.value_image_dimensions.setText("-")
        self.value_image_size.setText("-")
        self.value_image_set.setText("-")

    def loadImage(self, image_path):
        image_path = str(image_path)
        redPalette = QPalette()
        redPalette.setColor(QPalette.Foreground, Qt.red)
        greenPalette = QPalette()
        greenPalette.setColor(QPalette.Foreground, Qt.green)
        blackPalette = QPalette()
        blackPalette.setColor(QPalette.Foreground, Qt.black)
        try:
            im = Image.open(image_path)

            self.value_image_name.setText( os.path.basename(image_path) )
            self.value_image_directory.setText( os.path.dirname(image_path) )
            self.value_image_dimensions.setText( "%sx%s" % (im.size) )
            self.value_image_size.setText("%.2f MB" %  ( os.path.getsize(image_path)/(1024.0**2) ) )
            if image_path in BEST_CANDIDATE_SET:
                self.value_image_set.setText("Best Candidate")
                self.value_image_set.setPalette(greenPalette)
            elif image_path in TRASH_CANDIDATE_SET:
                self.value_image_set.setText("Trash Candidate")
                self.value_image_set.setPalette(redPalette)

            else:
                self.value_image_set.setText("-")
                self.value_image_set.setPalette(blackPalette)


        except IOError:
            print "I/O Error for file:", image_path


class ImagePanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        global BEST_CANDIDATE_SET
        global TRASH_CANDIDATE_SET

        BEST_CANDIDATE_SET = self.best_candidate_set = set()
        TRASH_CANDIDATE_SET = self.trash_candidate_set = set()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ===========( NAVIGATION )=================
        self.button_left = QPushButton("<")
        self.button_right= QPushButton(">")
        self.button_left.clicked.connect(self.previousImage)
        self.button_right.clicked.connect(self.nextImage)

        self.label_progress = QLabel("N/A")

        layout_nav_button = QHBoxLayout()

        layout_nav_button.addWidget(self.button_left)
        layout_nav_button.addStretch()
        layout_nav_button.addWidget(self.label_progress)
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
        self.button_resize800 = QPushButton("[&Z] 800x600")
        self.button_resize1024 = QPushButton("[&X] 1024x768")
        self.button_delete = QPushButton("Delete")
        self.button_delete.setShortcut(QKeySequence("Del"))

        self.button_best_candidate = QPushButton("Best Candidate")
        self.button_trash = QPushButton("Trash It!")

        self.button_split_best_candidates = QPushButton("Split Best Candidates")
        self.button_split_trash = QPushButton("Split Trashes")

        self.button_best_candidate.setShortcut(QKeySequence("B"))
        self.button_trash.setShortcut(QKeySequence("T"))

        # Connect the slots
        self.button_resize800.clicked.connect(self.resize800)
        self.button_resize1024.clicked.connect(self.resize1024)
        self.button_delete.clicked.connect(self.deleteImage)

        self.button_best_candidate.clicked.connect(self.best_candidate)
        self.button_trash.clicked.connect(self.trash)

        self.button_split_best_candidates.clicked.connect(self.split_best_candidates)
        self.button_split_trash.clicked.connect(self.split_trashes)

        # Add them to horizontal layout
        layout_election_buttons = QHBoxLayout()
        layout_election_buttons.addWidget(self.button_best_candidate)
        layout_election_buttons.addWidget(self.button_trash)
        layout_election_buttons.addWidget(self.button_split_best_candidates)
        layout_election_buttons.addWidget(self.button_split_trash)

        layout_resize_button = QHBoxLayout()
        layout_resize_button.addWidget(self.button_resize800)
        layout_resize_button.addWidget(self.button_resize1024)
        layout_resize_button.addWidget(self.button_delete)

        # ===========( LAYOUT PLACEMENT )=================
        self.layout.addLayout(layout_nav_button)
        self.layout.addWidget(self.image_viewer)
        self.layout.setAlignment(self.image_viewer, Qt.AlignHCenter)
        self.layout.addWidget(self.image_info)
        self.layout.addLayout(layout_election_buttons)
        self.layout.addLayout(layout_resize_button)

        self.loadDirectory(QDir.homePath())

    def loadImage(self, image_path):
        if isinstance(image_path, int):
            # if we want x th image, then convert it to real path.
            if image_path >= self.num_files:
                image_path = 0
            self.current_index = image_path
            image_path = os.path.join( self.directory_path, self.file_list[ image_path ] )
        else:
            # find the current index then
            self.current_index = self.file_list.index( os.path.basename(str ( image_path ) ) )

        self.image_info.loadImage(image_path)
        self.image_viewer.loadImage(image_path)
        self.refreshProgress()

    def loadDirectory(self, directory_path):
        self.directory_path = str( directory_path )
        files = filter( lambda filename: str(filename[-4:]).lower() in (".jpg", ".png"), os.listdir(directory_path) )
        self.file_list = sorted(files)
        self.num_files = len(self.file_list)

        if self.file_list:
            self.loadImage(0)
        else:
            # QMessageBox.information(self, "No images found", "This directory does not contain any image files.")
            self.image_viewer.reset()
            self.image_info.reset()
            self.refreshProgress()

    def refreshProgress(self):
        if self.num_files:
            self.label_progress.setText("%d out of %d" % ( self.current_index + 1, self.num_files) )
        else:
            self.label_progress.setText("No images in this folder.")


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
            self.file_list.remove(os.path.basename( self.image_viewer.image_path ) )
            self.num_files -= 1
            self.loadImage(self.current_index)

    def resize800(self):
        self.image_viewer.resize((800, 600))
        self.nextImage()

    def resize1024(self):
        self.image_viewer.resize((1024, 768))
        self.nextImage()

    def trash(self):
        path = self.image_viewer.image_path
        if path not in self.trash_candidate_set:
            print "Trashing "  + path
            self.trash_candidate_set.add(path)
            try:
                self.best_candidate_set.remove(path)
            except KeyError,e:
                pass
        else:
            print "Removing from Trash "  + path
            self.trash_candidate_set.remove(path)

        self.nextImage()

    def best_candidate(self):
        path = self.image_viewer.image_path

        if path not in self.best_candidate_set:
            print "Chosen as the best candidate: " + path
            self.best_candidate_set.add(path)
            try:
                self.trash_candidate_set.remove(path)
            except KeyError,e:
                pass
        else:
            print "Removimg from best candidates: " + path
            self.best_candidate_set.remove(path)

        self.nextImage()


    def split_best_candidates(self):
        if self.best_candidate_set:
            fullpath = self.directory_path
            curdir = fullpath.split("/")[-1]
            if curdir != "best-candidates":
                if not os.path.exists("%s/best-candidates" % fullpath):
                    os.mkdir("%s/best-candidates" % fullpath)
                else:
                    print "best-candidates folder already exists."

                for filename in self.best_candidate_set:

                    to_path = "%s/best-candidates/%s" % (fullpath, filename.split("/")[-1])
                    os.rename(filename, to_path)
                self.best_candidate_set.clear()

            else:
                if not os.path.exists("%s/best" % fullpath):
                    os.mkdir("%s/best" % fullpath)
                else:
                    print "best folder already exists."

                for filename in self.best_candidate_set:
                    to_path = "%s/best/%s" % (fullpath, filename.split("/")[-1])
                    os.rename(filename, to_path)
                self.best_candidate_set.clear()
        else:
            print "No best candidate selected."

    def split_trashes(self):
        if self.trash_candidate_set:
            fullpath = self.directory_path
            curdir = fullpath.split("/")[-1]

            if curdir != "trash-candidates":
                if not os.path.exists("%s/trash-candidates" % fullpath):
                    os.mkdir("%s/trash-candidates" % fullpath)
                else:
                    print "trash-candidates folder already exists."

                for filename in self.trash_candidate_set:
                    to_path = "%s/trash-candidates/%s" % (fullpath, filename.split("/")[-1])
                    os.rename(filename, to_path)
                self.trash_candidate_set.clear()
            else:
                if not os.path.exists("%s/trash" % fullpath):
                    os.mkdir("%s/trash" % fullpath)
                else:
                    print "trash folder already exists."

                for filename in self.trash_candidate_set:
                    to_path = "%s/trash/%s" % (fullpath, filename.split("/")[-1])
                    os.rename(filename, to_path)
                self.trash_candidate_set.clear()
        else:
            print "No trash candidate selected."

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = ImagePanel()
    p.show()
    sys.exit(app.exec_())
