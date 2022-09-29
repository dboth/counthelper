import sys, os
from ClickImage import ClickImage
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pathlib import Path
import natsort
import json

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'de.dboth.counter.100'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass  


class CountHelper(QMainWindow):
    def __init__(self, parent = None):
        super(CountHelper, self).__init__(parent)
        self.setAcceptDrops(True)
        self.currentFile = False
        self.toplayout = QStackedWidget()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.log = {}
        layout.addStretch()
        
        self.text = QLabel()
        self.text.setText("Drop picture here")
        self.text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text)

        self.orText = QLabel()
        self.orText.setText("or")
        self.orText.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.orText)
        
        self.button = QPushButton()
        self.button.setText("Select picture")
        self.button.clicked.connect(self.selectImage)
        layout.addWidget(self.button)

        layout.addStretch()

        widget = QWidget()

        widget.setLayout(layout)


       
        widget2 = QWidget()
        layout2 = QVBoxLayout()
        widget2.setLayout(layout2)
 
        self.clickImage = ClickImage()

        layout2.addWidget(self.clickImage)

        self.toplayout.addWidget(widget)
        self.toplayout.addWidget(widget2)

        self.toplayout.setCurrentIndex(0)
        
        self.setCentralWidget(self.toplayout)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icon.ico')))
        self.setWindowTitle("CountHelper v0.1")

        self.filelabel = QLabel()
        self.filelabel.setText("...")

        toolbar = QToolBar("Toolbar")
        toolbar2 = QToolBar("Toolbar")
        toolbar2.setFixedWidth(50);
        toolbar3 = QToolBar("Toolbar")
        toolbar3.setFixedWidth(50);
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        self.addToolBar(Qt.LeftToolBarArea, toolbar2)
        self.addToolBar(Qt.RightToolBarArea, toolbar3)
        pixmapi3 = getattr(QStyle, "SP_FileDialogContentsView")
        button_action3 = QAction("Count", self)
        button_action3.setIcon(self.style().standardIcon(pixmapi3))
        button_action3.setStatusTip("Count")
        button_action3.triggered.connect(self.countAction)
        toolbar.addAction(button_action3)
        self.filelabel = QAction("...", self)
        self.filelabel.triggered.connect(self.selectImage)
        toolbar.addAction(self.filelabel)
        pixmapi1 = getattr(QStyle, "SP_ArrowBack")
        pixmapi2 = getattr(QStyle, "SP_ArrowForward")

        button_action = QPushButton()
        button_action.setFixedWidth(45)
        button_action.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
        button_action.setIcon(self.style().standardIcon(pixmapi1))
        button_action.setIconSize(QSize(45,45))
        button_action.clicked.connect(self.previousFile)
        toolbar2.addWidget(button_action)
        
        button_action2 = QPushButton()
        button_action2.setFixedWidth(45)
        button_action2.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding);
        button_action2.setIcon(self.style().standardIcon(pixmapi2))
        button_action2.setIconSize(QSize(45,45))
        button_action2.clicked.connect(self.nextFile)
        toolbar3.addWidget(button_action2)

    def countAction(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec():
            filenames = dlg.selectedFiles()[0]
            with open(os.path.join(filenames,"count.tsv"),"w") as tsv:
                for x in Path(filenames).rglob('*.json'):
                    jfilename = str(x)
                    with open(jfilename,"r") as jfile:
                        count = len(json.load(jfile))
                        tsv.write((jfilename.replace("\\","\t").replace("/","\t"))+"\t"+str(count)+"\n")
            msgBox = QMessageBox();
            msgBox.setText("Count was done. You find the count.tsv in the folder. Import it with Excel.")
            msgBox.exec()
                    


    def selectImage(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec():
            filenames = dlg.selectedFiles()
            self.fileSelection(filenames)

    def previousFile(self):
        if not self.currentFile:
            return
        directory, filename = os.path.split(self.currentFile)
        current = self.currentFile.replace('/', os.sep)
        lookup = directory
        nextPath = None
        level = 0
        while nextPath is None:
            if level > 4:
                return
            level += 1
            print("Lookup",lookup)
            fileList = natsort.natsorted([str(x) for x in Path(lookup).rglob('*.tif')], reverse=False)
            nextIndex = fileList.index(current) - 1
            if nextIndex < 0:
                lookup = Path(lookup).parent.absolute()
            else:
                nextPath = fileList[nextIndex]
        self.fileSelection([nextPath])

    def nextFile(self):
        if not self.currentFile:
            return

        directory, filename = os.path.split(self.currentFile)
        current = self.currentFile.replace('/', os.sep)
        lookup = directory
        nextPath = None
        level = 0
        while nextPath is None:
            if level > 4:
                return
            level += 1
            print("Lookup",lookup)
            images = ["*.tiff","*.tif","*.png","*.jpg","*.jpeg"]
            fileListx = []
            for image in images:
                fileListx += [str(x) for x in Path(lookup).rglob(image)]
            fileList = natsort.natsorted(fileListx, reverse=False)
            nextIndex = fileList.index(current) + 1
            if nextIndex == 0 or nextIndex == len(fileList):
                lookup = Path(lookup).parent.absolute()
            else:
                nextPath = fileList[nextIndex]
        self.fileSelection([nextPath])
    
    def reset(self):
        self.button.show()
        self.orText.show()
        self.setAcceptDrops(True)
    
    def fileSelection(self,files):
        self.setAcceptDrops(True)
        self.filelabel.setText(files[0])
        self.clickImage.setImage(files[0])
        self.currentFile = files[0]
        self.toplayout.setCurrentIndex(1)

    def dragLeaveEvent(self, event):
        self.reset()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.button.hide()
            self.orText.hide()
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.fileSelection(files)

    
    def sizeHint(self):
      return QSize(600,400)



def main():
   app = QApplication(sys.argv)
   ex = CountHelper()
   ex.show()
   sys.exit(app.exec())
	
if __name__ == '__main__':
   main()