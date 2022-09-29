
from PySide6.QtCore import *
import uuid, os, json

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Crosshair import Crosshair

class ClickImage(QWidget):
    pixmap = False
    _sizeHint = QSize()
    ratio = Qt.KeepAspectRatio
    transformation = Qt.SmoothTransformation

    def __init__(self, pixmap=None):
        super().__init__()
        self.lastImage = ""
        self.counters = {}
        pal = self.palette()
        pal.setColor(QPalette.Window,Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.setStyleSheet("border: 1px solid #aaa; background-color: black")
        self.setPixmap(pixmap)

    def getPoints(self):
        return [self.c0.getPoint(),self.c1.getPoint(),self.c2.getPoint(),self.c3.getPoint()]

    def setImage(self,image):
        pixmap = QPixmap(image)
        self.imagepath = image
        if self.lastImage != image:
            self.resetCounters()
        self.setPixmap(pixmap)
        if self.lastImage != image:
            self.load()
        self.lastImage = image


    def resetCounters(self):
        for counter in self.counters:
            self.counters[counter].delete()
        self.counters = {}

    def setPixmap(self, pixmap):
        if self.pixmap != pixmap:
            self.pixmap = pixmap
            if isinstance(pixmap, QPixmap):
                self._sizeHint = pixmap.size()
            else:
                self._sizeHint = QSize()
            self.updateGeometry()
            self.updateScaled()

    def setAspectRatio(self, ratio):
        if self.ratio != ratio:
            self.ratio = ratio
            self.updateScaled()

    def setTransformation(self, transformation):
        if self.transformation != transformation:
            self.transformation = transformation
            self.updateScaled()

    def updateScaled(self):
        if self.pixmap:
            self.scaled = self.pixmap.scaled(self.size(), self.ratio, self.transformation)
        self.update()

    def sizeHint(self):
        return self._sizeHint

    def resizeEvent(self, event):
        self.updateScaled()

    def paintEvent(self, event):
        if not self.pixmap:
            return
        qp = QPainter(self)
        r = self.scaled.rect()
        r.moveCenter(self.rect().center())
        qp.drawPixmap(r, self.scaled)
        for counter in self.counters:
            self.counters[counter].refreshPosition()

    def mousePressEvent(self, event):
        pos = event.pos()
        name = uuid.uuid4()
        self.counters[name] = Crosshair(self,name,pos)
        self.save()

    def load(self):
        folder, file = os.path.split(self.imagepath)
        print(folder,file)
        self.json = os.path.join(folder,file+".json")
        if os.path.exists(self.json):
            with open(self.json,"r") as file:
                savedata = json.load(file)
                for point in savedata:
                    name = uuid.uuid4()
                    self.counters[name] = Crosshair(self,name,point,True)

    def deleteMe(self,name):
        self.counters[name].delete()
        del self.counters[name]
        self.save()

    def save(self):
        out = [self.counters[x].position for x in self.counters]
        with open(self.json,"w") as file:
            json.dump(out,file)